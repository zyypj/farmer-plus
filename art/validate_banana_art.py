import base64
import hashlib
import json
import math
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

from preview_world_models import apply, collect, rotation_matrix, variants_for
from preview_world_trees import DEFAULT_WORLD

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets/farmerplus'
errors = []
checks = 0
joins = []


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def world_point(element, point, offset, yaw):
    point = apply(rotation_matrix(element['rotation']), point, element['rotation']['origin'])
    point = apply(rotation_matrix({'y': -yaw}), point, [8, 8, 8])
    return [point[axis] + offset[axis] for axis in range(3)]


def rib_endpoint(element, outer, offset, yaw):
    return world_point(element, [element['rotation']['origin'][0], element['rotation']['origin'][1], element['from' if outer else 'to'][2]], offset, yaw)


def skin_endpoint(element, outer, offset, yaw, across):
    origin = element['rotation']['origin']
    return world_point(element, [origin[0] + across, origin[1], element['from'][2] + 0.65 if outer else element['to'][2] - 0.65], offset, yaw)


def skin_interval(element, point, offset, yaw):
    point = apply(rotation_matrix({'y': yaw}), [point[axis] - offset[axis] for axis in range(3)], [8, 8, 8])
    matrix = rotation_matrix(element['rotation'])
    inverse = list(map(list, zip(*matrix)))
    origin = element['rotation']['origin']
    point = apply(inverse, point, origin)
    direction = [inverse[axis][1] for axis in range(3)]
    low, high = -math.inf, math.inf
    for axis in range(3):
        if abs(direction[axis]) < 1e-9:
            if not element['from'][axis] - 0.002 <= point[axis] <= element['to'][axis] + 0.002:
                return None
        else:
            ends = [(element[bound][axis] - point[axis]) / direction[axis] for bound in ('from', 'to')]
            low, high = max(low, min(ends)), min(high, max(ends))
    return (low, high) if low <= high + 0.002 else None


def check_joint(left, right, left_model, right_model, left_offset, right_offset, yaw, label):
    gap = math.dist(rib_endpoint(left, True, left_offset, yaw), rib_endpoint(right, False, right_offset, yaw))
    joins.append({'label': label, 'yaw': yaw, 'midrib_gap': gap})
    check(gap < 0.002, label + ': connected midrib')
    left_name, right_name = left['name'].removesuffix('_midrib'), right['name'].removesuffix('_midrib')
    for across in (-7.1, -5, -3, -1, 1, 3, 5, 7.1):
        side = '_left' if across < 0 else '_right'
        previous = next(element for element in left_model['elements'] if element['name'] == left_name + side)
        following = next(element for element in right_model['elements'] if element['name'] == right_name + side)
        first = skin_endpoint(previous, True, left_offset, yaw, across)
        second = skin_endpoint(following, False, right_offset, yaw, across)
        point = [(first[axis] + second[axis]) / 2 for axis in range(3)]
        first_interval = skin_interval(previous, point, left_offset, yaw)
        second_interval = skin_interval(following, point, right_offset, yaw)
        connected = first_interval and second_interval and max(first_interval[0], second_interval[0]) <= min(first_interval[1], second_interval[1]) + 0.002
        check(bool(connected), label + ': folded blade overlaps at ' + str(across))


def main():
    names = load(ROOT / 'build/art/banana-models.json')
    resources = []
    for name in names:
        path = ASSETS / 'models/block' / (name + '.json')
        data = load(path)
        source = load(ROOT / 'art/blockbench' / (name + '.bbmodel'))
        resources.append(path)
        check(data.get('ambientocclusion') is False, name + ': ambient occlusion')
        check(len(data['elements']) <= 12, name + ': element budget')
        check(len(source['elements']) == len(data['elements']), name + ': source element count')
        check(source['meta']['model_format'] == 'java_block', name + ': editable Java project')
        for element in data['elements']:
            check(all(-16 <= value <= 32 for key in ('from', 'to') for value in element[key]), name + ': bounds')
            for info in element['faces'].values():
                check(all(0 <= value <= 16 for value in info['uv']), name + ': UV')
        for texture in source['textures']:
            image = Image.open(BytesIO(base64.b64decode(texture['source'].split(',')[1]))).convert('RGBA')
            actual = ASSETS / 'textures/block' / texture['name']
            check(image.tobytes() == Image.open(actual).convert('RGBA').tobytes(), name + ': embedded pixels ' + texture['name'])
    for path in (ASSETS / 'textures').glob('*/banana*.png'):
        image = Image.open(path)
        check(image.size == (16, 16) and image.mode == 'RGBA', path.name + ': 16x16 RGBA')
        check(set(image.getchannel('A').get_flattened_data()) <= {0, 255}, path.name + ': hard alpha')
        resources.append(path)
    leaf_state = load(ASSETS / 'blockstates/banana_leaf.json')
    for direction, delta_x, delta_z in [('north', 0, -1), ('north_east', 1, -1), ('east', 1, 0), ('south_east', 1, 1), ('south', 0, 1), ('south_west', -1, 1), ('west', -1, 0), ('north_west', -1, -1)]:
        variant = leaf_state['variants']['age=dry,direction=%s,segment=0' % direction]
        diagonal = delta_x != 0 and delta_z != 0
        root = [-8, 8, 24] if diagonal else [8, 8, 21]
        root = apply(rotation_matrix({'y': -variant.get('y', 0)}), root, [8, 8, 8])
        root[0] += delta_x * 16
        root[2] += delta_z * 16
        check(all(4.999 <= root[axis] <= 11.001 for axis in (0, 2)), direction + ': dry petiole reaches the stem')
        check(variant['model'].endswith('banana_leaf_dry_diagonal' if diagonal else 'banana_leaf_dry'), direction + ': correct dry model frame')
    shapes = load(ROOT / 'common/src/main/resources/farmerplus/shapes/banana_leaf.json')
    check(len(shapes['states']) == 72 and len(shapes['shapes']) == 48, 'Regenerated leaf hitboxes cover cardinal and diagonal dry leaves')
    for age in ('young', 'mature'):
        for diagonal in (False, True):
            suffixes = ['diagonal_base', 'diagonal_tip'] if diagonal else ['base', 'blade', 'tip']
            models = [load(ASSETS / 'models/block' / ('banana_leaf_%s_%s.json' % (age, suffix))) for suffix in suffixes]
            ribs = [[element for element in model['elements'] if element['name'].endswith('_midrib')] for model in models]
            for yaw in (0, 90, 180, 270):
                direction = apply(rotation_matrix({'y': -yaw}), [16 if diagonal else 0, 0, -16], [0, 0, 0])
                for index, (left, right) in enumerate(zip(ribs, ribs[1:])):
                    previous = [direction[axis] * (index + 1) for axis in range(3)]
                    following = [direction[axis] * (index + 2) for axis in range(3)]
                    check_joint(left[-1], right[0], models[index], models[index + 1], previous, following, yaw, age + '_' + suffixes[index] + '_block_seam')
                for index, sections in enumerate(ribs):
                    offset = [direction[axis] * (index + 1) for axis in range(3)]
                    for section, (left, right) in enumerate(zip(sections, sections[1:])):
                        check_joint(left, right, models[index], models[index], offset, offset, yaw, age + '_' + suffixes[index] + '_curve_' + str(section))
    state = load(ASSETS / 'blockstates/banana_bunch.json')
    resources.append(ASSETS / 'blockstates/banana_bunch.json')
    totals = {}
    for stage in range(4):
        for facing in ('north', 'east', 'south', 'west'):
            selected = variants_for(state, {'stage': str(stage), 'facing': facing})
            check(len(selected) == (1 if stage == 0 else 5 if stage == 1 else 9), 'Multipart stage/facing coverage')
            count = sum(len(load(ASSETS / 'models' / (part['model'].split(':')[1] + '.json'))['elements']) for part in selected)
            totals[str(stage)] = count
    world = collect(DEFAULT_WORLD, (95, 165, 95, 105, 199, 210))
    directions = sorted({properties['direction'] for name, properties in world.values() if name == 'farmerplus:banana_leaf' and properties.get('age') != 'dry'})
    check(len(directions) == 8, 'Generated world covers eight leaf directions: ' + str(directions))
    for loader in ('fabric', 'neoforge', 'forge'):
        jars = [path for path in (ROOT / loader / 'build/libs').glob('*.jar') if not any(token in path.name for token in ('sources', 'dev', 'javadoc'))]
        check(bool(jars), loader + ': distributable jar')
        for path in jars:
            with ZipFile(path) as archive:
                for resource in resources:
                    entry = resource.relative_to(ROOT / 'common/src/main/resources').as_posix()
                    check(archive.read(entry) == resource.read_bytes(), loader + ': matching ' + entry)
    report = {'checks': checks, 'errors': errors, 'joins': joins, 'world_leaf_directions': directions, 'bunch_total_elements_by_stage': totals,
              'sha256': {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in resources}}
    target = ROOT / 'build/art/validation/banana-art.json'
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'checks': checks, 'errors': errors, 'bunch_elements': totals, 'report': str(target)}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
