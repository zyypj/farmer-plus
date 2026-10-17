from pathlib import Path
from PIL import Image
from io import BytesIO
import base64
import hashlib
import itertools
import json
import math
import re
from strawberries import transform, BUDGETS

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'common/src/main/resources/assets/farmerplus'


def bounds(model):
    points = []
    for element in model['elements']:
        rotation = element.get('rotation', {})
        origin = rotation.get('origin', [0, 0, 0])
        angles = [rotation.get(axis, 0) for axis in ('x', 'y', 'z')]
        if 'axis' in rotation:
            angles[['x', 'y', 'z'].index(rotation['axis'])] = rotation['angle']
        for point in itertools.product(*zip(element['from'], element['to'])):
            rotated = transform([point[i] - origin[i] for i in range(3)], angles)
            points.append([rotated[i] + origin[i] for i in range(3)])
    return {'min': [min(p[i] for p in points) for i in range(3)], 'max': [max(p[i] for p in points) for i in range(3)]}


def box(element):
    rot = element.get('rotation', {})
    origin = rot.get('origin', [0, 0, 0])
    angles = [rot.get(axis, 0) for axis in ('x', 'y', 'z')]
    if 'axis' in rot:
        angles[['x', 'y', 'z'].index(rot['axis'])] = rot['angle']
    centre = [(a + b) / 2 for a, b in zip(element['from'], element['to'])]
    offset = transform([centre[i] - origin[i] for i in range(3)], angles)
    return {'centre': [origin[i] + offset[i] for i in range(3)], 'axes': [transform(v, angles) for v in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]], 'half': [(b - a) / 2 for a, b in zip(element['from'], element['to'])]}


def intersects(a, b):
    dot = lambda u, v: sum(x * y for x, y in zip(u, v))
    cross = lambda u, v: [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
    delta = [b['centre'][i] - a['centre'][i] for i in range(3)]
    for axis in a['axes'] + b['axes'] + [cross(u, v) for u in a['axes'] for v in b['axes']]:
        radius = lambda value: sum(abs(dot(axis, direction)) * half for direction, half in zip(value['axes'], value['half']))
        if abs(dot(axis, delta)) > radius(a) + radius(b) + 1e-6:
            return False
    return True


def validate(quiet=False):
    report = {'models': [], 'errors': [], 'hashes': {}, 'shapes': {}}
    def check(condition, message):
        if not condition:
            report['errors'].append(message)
    for wild in (False, True):
        prefix = 'wild_strawberries' if wild else 'strawberry_plant'
        variants = json.loads((ASSET / 'blockstates' / f'{prefix}.json').read_text())['variants']
        state = {key.removesuffix(',flattening=0'): value for key, value in variants.items() if key.endswith(',flattening=0')}
        check(set(state) == {f'age={age}' for age in range(5)}, prefix + ': five ages')
        shapes = []
        for age in range(5):
            signatures = []
            bounds_for_age = []
            entries = state[f'age={age}']
            count = 2 if wild else 4
            check(len(entries) == count * 4 and all(e.get('weight', 1) == 1 for e in entries), f'{prefix} {age}: equally weighted models and rotations')
            for variant in range(count):
                name = f'{prefix}_stage{age}' + (f'_variant{variant}' if variant else '')
                path = ASSET / 'models/block' / f'{name}.json'
                model = json.loads(path.read_text())
                source_path = ROOT / 'art/blockbench' / f'{name}.bbmodel'
                source = json.loads(source_path.read_text())
                check({e['y'] for e in entries if e['model'] == f'farmerplus:block/{name}'} == {0, 90, 180, 270}, name + ': four rotations')
                check(len(model['elements']) <= (12 if wild else BUDGETS[age]), name + ': budget')
                check(model.get('ambientocclusion') is False and bool(model['textures']['particle']), name + ': lighting and particles')
                check(source['resolution'] == {'width': 16, 'height': 16}, name + ': native 16 grid')
                check(len(source['elements']) == len(model['elements']), name + ': native geometry preserved')
                crown = next(e for e in model['elements'] if e['name'] == 'soil_crown')
                check(crown['from'][1] == -1, name + ': soil contact')
                signatures.append(json.dumps([{k: e.get(k) for k in ('name', 'from', 'to', 'rotation')} for e in model['elements']], sort_keys=True))
                fruit = [e for e in model['elements'] if e['name'].endswith(('ripe_body', 'unripe_body'))]
                expected = (2 if wild else 3 if age == 3 else 4) if age >= 3 else 0
                check(len(fruit) == expected, name + ': fruit count')
                for element in model['elements']:
                    if element['name'].startswith('leaf_'):
                        check(element.get('shade_direction_override') == 'up' and 'up' in element['faces'] and 'down' in element['faces'], name + ': double-sided leaf shading')
                    if element['name'].startswith('fruit_') and not 'stalk' in element['name']:
                        check(all(b > a for a, b in zip(element['from'], element['to'])) and len(element['faces']) == 6, name + ': solid berry volume')
                for body in fruit:
                    index = body['name'].split('_')[1]
                    parts = [e for e in model['elements'] if e['name'].startswith(f'fruit_{index}_') and not 'stalk' in e['name']]
                    check(len(parts) == 3 and any('tapered_tip' in e['name'] for e in parts), name + ': three-piece tapered berry')
                    cap = next(e for e in parts if 'calyx' in e['name'])
                    tip = next(e for e in parts if 'tapered_tip' in e['name'])
                    check(sum(abs(v) > .1 for k, v in tip['rotation'].items() if k in ('x', 'y', 'z')) >= 2, name + ': genuinely three-dimensional tapered tip')
                    check(cap['rotation'] != body['rotation'], name + ': independently tilted heart-shaped shoulders')
                    check(intersects(box(cap), box(body)) and intersects(box(tip), box(body)), name + ': three solid berry sections touch')
                    stalks = [e for e in model['elements'] if 'arching_stalk' in e['name']]
                    target = cap['rotation']['origin']
                    endpoints = []
                    for stalk in stalks:
                        r = stalk.get('rotation', {})
                        origin = r.get('origin', [0, 0, 0])
                        angles = [r.get(a, 0) for a in ('x', 'y', 'z')]
                        if 'axis' in r:
                            angles[['x', 'y', 'z'].index(r['axis'])] = r['angle']
                        for x in [stalk['from'][0], stalk['to'][0]]:
                            v_start = min(next(iter(stalk['faces'].values()))['uv'][1::2]) * 2
                            fraction = 15 / (32 - v_start)
                            local = [x, stalk['from'][1] + (stalk['to'][1] - stalk['from'][1]) * fraction, stalk['from'][2]]
                            offset = transform([local[i] - origin[i] for i in range(3)], angles)
                            endpoints.append([origin[i] + offset[i] for i in range(3)])
                    check(min(math.dist(point, target) for point in endpoints) < .001, name + ': stalk reaches berry calyx')
                    if age == 4:
                        fruit_bounds = bounds({'elements': parts})
                        check(fruit_bounds['min'][1] >= .25, name + ': ripe berry clears both farmland and adjacent full-height soil')
                for texture in source['textures']:
                    pixels = Image.open(BytesIO(base64.b64decode(texture['source'].split(',')[1]))).convert('RGBA')
                    final = ASSET / 'textures/block' / texture['name']
                    check(pixels.size == (16, 16) and pixels.tobytes() == Image.open(final).convert('RGBA').tobytes(), name + ': embedded ' + texture['name'])
                extent = bounds(model)
                check(extent['min'][1] >= -1.001 and all(extent['min'][i] >= -2.001 and extent['max'][i] <= 18.001 for i in (0, 2)), name + ': model bounds')
                bounds_for_age.append(extent)
                fruit_parts = [e for e in model['elements'] if e['name'].startswith('fruit_') and 'stalk' not in e['name']]
                fruit_lowest = bounds({'elements': fruit_parts})['min'][1] if fruit_parts else None
                report['models'].append({'name': name, 'elements': len(model['elements']), 'faces': sum(len(e['faces']) for e in model['elements']), 'bounds': extent, 'berries': len(fruit), 'fruitLowestY': fruit_lowest})
                for file in [path, source_path]:
                    report['hashes'][file.relative_to(ROOT).as_posix()] = hashlib.sha256(file.read_bytes()).hexdigest()
            check(len(set(signatures)) == count, prefix + f' age {age}: distinct arrangements')
            radius = max(abs(b[edge][axis] - 8) for b in bounds_for_age for edge in ('min', 'max') for axis in (0, 2))
            shapes.append({'width': math.ceil(radius * 4) / 2, 'bottom': -1, 'top': math.ceil(max(b['max'][1] for b in bounds_for_age) * 4) / 4})
        report['shapes'][prefix] = shapes
        java_name = 'WildStrawberriesBlock' if wild else 'StrawberryPlantBlock'
        java = (ROOT / 'common/src/main/java/com/zyypj/farmerplus/content/strawberry' / f'{java_name}.java').read_text()
        shape_array = re.search(r'VoxelShape\[\] SHAPES = \{(.*?)\n    \};', java, re.S).group(1)
        declared = [tuple(float(v) for v in match) for match in re.findall(r'Block.column\(([\d.]+), (-?[\d.]+), ([\d.]+)\)', shape_array)]
        check(declared == [(s['width'], s['bottom'], s['top']) for s in shapes], java_name + ': static selection shapes match exported geometry')
    for path in list((ASSET / 'textures/block').glob('strawberry_*.png')) + [ASSET / 'textures/item/strawberry.png']:
        im = Image.open(path)
        alpha_valid = path.name == 'strawberry_jam_glass.png' or set(im.getchannel('A').get_flattened_data()) <= {0, 255}
        check(im.size == (16, 16) and im.mode == 'RGBA' and alpha_valid, str(path) + ': hard 16 pixel art')
        report['hashes'][path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    target = ROOT / 'build/art/validation/strawberries.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    if not quiet:
        print(json.dumps({'models': len(report['models']), 'errors': report['errors'], 'shapes': report['shapes']}, indent=2))
    return report


if __name__ == '__main__':
    raise SystemExit(bool(validate()['errors']))
