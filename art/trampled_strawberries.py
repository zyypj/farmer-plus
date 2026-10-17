from pathlib import Path
import copy
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets/farmerplus'
MODELS = ASSETS / 'models/block'
BLOCKSTATES = ASSETS / 'blockstates'

PLANTS = {'strawberry_plant': 4, 'wild_strawberries': 2}
AGES = range(5)
LEVELS = {1: 0.5, 2: 0.85, 3: 1.0}
RESTING_ELEVATION = [2.0, 3.5, 2.5, 4.0, 3.0, 1.5]
GROUND = -0.9
CRUSHED_TEXTURES = {'leaf': 'farmerplus:block/strawberry_leaf_aged', 'particle': 'farmerplus:block/strawberry_leaf_aged'}
STALKS = ('_petiole', '_stalk', '_stalks', '_whole')
FRUIT_DROP = {1: 0.6, 2: 1.0, 3: 1.0}
UPRIGHT_LEAN = 0.3
SMASHED_HALF_WIDTH = 1.1
SMASHED_HEIGHT = 0.3
FRUIT_GROUND = -0.95
ATTACHMENTS = {'_petiole': '_trifoliate', '_stalk': '_five_petals'}
UP = np.array([0.0, 1.0, 0.0])


def euler_matrix(rotation):
    if rotation is None:
        return np.eye(3)
    if 'axis' in rotation:
        angle = math.radians(rotation['angle'])
        axis = {'x': np.array([1.0, 0, 0]), 'y': np.array([0, 1.0, 0]), 'z': np.array([0, 0, 1.0])}[rotation['axis']]
        return axis_matrix(axis, angle)
    x, y, z = (math.radians(rotation.get(key, 0)) for key in ('x', 'y', 'z'))
    return axis_matrix(np.array([0, 0, 1.0]), z) @ axis_matrix(np.array([0, 1.0, 0]), y) @ axis_matrix(np.array([1.0, 0, 0]), x)


def axis_matrix(axis, angle):
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c, s = math.cos(angle), math.sin(angle)
    t = 1 - c
    return np.array([
        [t * x * x + c, t * x * y - s * z, t * x * z + s * y],
        [t * x * y + s * z, t * y * y + c, t * y * z - s * x],
        [t * x * z - s * y, t * y * z + s * x, t * z * z + c],
    ])


def to_euler(matrix):
    y = math.asin(max(-1.0, min(1.0, -matrix[2][0])))
    x = math.atan2(matrix[2][1], matrix[2][2])
    z = math.atan2(matrix[1][0], matrix[0][0])
    return {key: round(math.degrees(value), 4) for key, value in (('x', x), ('y', y), ('z', z))}


def corners(element):
    (x0, y0, z0), (x1, y1, z1) = element['from'], element['to']
    return [np.array([x, y, z], dtype=float) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]


def world_corners(element, matrix, origin):
    return [matrix @ (corner - origin) + origin for corner in corners(element)]


def origin_of(element):
    rotation = element.get('rotation')
    return np.array(rotation['origin'], dtype=float) if rotation else np.array([8.0, GROUND, 8.0])


def tip_direction(element, matrix, origin):
    centre = (np.array(element['from'], dtype=float) + np.array(element['to'], dtype=float)) / 2
    direction = matrix @ (centre - origin)
    length = np.linalg.norm(direction)
    return direction / length if length > 1e-6 else UP


def press_rotation(direction, fallback_azimuth, target_elevation):
    elevation = math.asin(max(-1.0, min(1.0, direction[1])))
    horizontal = np.array([direction[0], 0.0, direction[2]])
    if np.linalg.norm(horizontal) < 1e-3:
        horizontal = np.array([math.cos(fallback_azimuth), 0.0, math.sin(fallback_azimuth)])
    horizontal /= np.linalg.norm(horizontal)
    delta = elevation - target_elevation
    if delta <= 0:
        return np.eye(3)
    return axis_matrix(np.cross(UP, horizontal), delta)


def is_horizontal_plane(element):
    return abs(element['from'][1] - element['to'][1]) < 1e-6


def flatten_rotation(element, matrix, origin, factor, index):
    rest = RESTING_ELEVATION[index % len(RESTING_ELEVATION)] if factor >= 0.85 else 0.0
    if is_horizontal_plane(element):
        normal = matrix @ UP
        target = UP if normal[1] >= 0 else -UP
        angle = math.degrees(math.acos(max(-1.0, min(1.0, float(normal @ target)))))
        axis = np.cross(normal, target)
        remaining = max(angle * (1 - factor), min(rest, angle))
        if np.linalg.norm(axis) < 1e-6 or angle - remaining <= 0:
            return np.eye(3)
        return axis_matrix(axis, math.radians(angle - remaining))
    direction = tip_direction(element, matrix, origin)
    elevation = math.degrees(math.asin(max(-1.0, min(1.0, direction[1]))))
    if np.linalg.norm(direction[[0, 2]]) < UPRIGHT_LEAN:
        direction = upright_fall_direction(element, matrix, index)
    return press_rotation(direction, index * 1.3, math.radians(max(elevation * (1 - factor), rest)))


def upright_fall_direction(element, matrix, index):
    size = np.abs(np.array(element['to'], dtype=float) - np.array(element['from'], dtype=float))
    local_normal = np.eye(3)[int(np.argmin(size))]
    normal = matrix @ local_normal
    sign = 1 if index % 2 == 0 else -1
    lean = normal * sign * UPRIGHT_LEAN
    return (UP + np.array([lean[0], 0.0, lean[2]])) / np.linalg.norm(UP + np.array([lean[0], 0.0, lean[2]]))


def place(element, matrix, origin, translation):
    moved = copy.deepcopy(element)
    moved['from'] = [round(v, 4) for v in np.array(element['from']) + translation]
    moved['to'] = [round(v, 4) for v in np.array(element['to']) + translation]
    moved['rotation'] = {'origin': [round(v, 4) for v in origin + translation], **to_euler(matrix)}
    return moved


def lift_above_ground(element):
    matrix, origin = euler_matrix(element['rotation']), np.array(element['rotation']['origin'])
    lowest = min(point[1] for point in world_corners(element, matrix, origin))
    if lowest >= GROUND:
        return element
    lift = np.array([0.0, GROUND - lowest, 0.0])
    return place(element, matrix, origin, lift)


def pressed(element, rigid, pivot, factor, index):
    matrix, origin = euler_matrix(element.get('rotation')), origin_of(element)
    rigid_matrix = rigid @ matrix
    rigid_origin = rigid @ (origin - pivot) + pivot
    own = flatten_rotation(element, rigid_matrix, rigid_origin, factor, index)
    final = place(element, own @ rigid_matrix, origin, rigid_origin - origin)
    return lift_above_ground(final)


def fruit_groups(model):
    groups = {}
    for element in model['elements']:
        name = element['name']
        if name.startswith('fruit_') and not name.endswith(('_stalk', '_stalks')):
            groups.setdefault(name.split('_')[1], []).append(element)
    return groups


def dropped_fruit(group, level):
    placed = [(element, euler_matrix(element.get('rotation')), origin_of(element)) for element in group]
    points = [point for element, matrix, origin in placed for point in world_corners(element, matrix, origin)]
    lowest = min(point[1] for point in points)
    if level == 3:
        centre = np.mean(points, axis=0)
        body = next(element for element in group if element['name'].endswith('_body'))
        texture = body['faces']['north']['texture']
        face = {'uv': [0, 0, 8, 6], 'texture': texture}
        return [{
            'name': group[0]['name'].rsplit('_', 2)[0] + '_smashed',
            'from': [round(centre[0] - SMASHED_HALF_WIDTH, 4), FRUIT_GROUND, round(centre[2] - SMASHED_HALF_WIDTH, 4)],
            'to': [round(centre[0] + SMASHED_HALF_WIDTH, 4), round(FRUIT_GROUND + SMASHED_HEIGHT, 4), round(centre[2] + SMASHED_HALF_WIDTH, 4)],
            'faces': {direction: dict(face) for direction in ('north', 'east', 'south', 'west', 'up')},
        }]
    drop = np.array([0.0, -(lowest - FRUIT_GROUND) * FRUIT_DROP[level], 0.0])
    return [place(element, matrix, origin, drop) for element, matrix, origin in placed]


def trample_model(model, level):
    factor = LEVELS[level]
    elements = {element['name']: element for element in model['elements']}
    result = []
    handled = set()
    for index, element in enumerate(model['elements']):
        name = element['name']
        if name in handled:
            continue
        if name.startswith('fruit_') and not name.endswith(('_stalk', '_stalks')):
            continue
        if level == 3 and name.startswith('flower'):
            continue
        stalk_suffix = next((suffix for suffix in STALKS if name.endswith(suffix)), None)
        if stalk_suffix is None:
            result.append(copy.deepcopy(element))
            continue
        matrix, origin = euler_matrix(element.get('rotation')), origin_of(element)
        rigid = flatten_rotation(element, matrix, origin, factor, index)
        result.append(place(element, rigid @ matrix, origin, np.zeros(3)))
        attached_name = name[: -len(stalk_suffix)] + ATTACHMENTS.get(stalk_suffix, '')
        if stalk_suffix in ATTACHMENTS and attached_name in elements:
            result.append(pressed(elements[attached_name], rigid, origin, factor, index))
            handled.add(attached_name)
    for group in fruit_groups(model).values():
        result.extend(dropped_fruit(group, level))
    trampled = {key: value for key, value in model.items() if key != 'elements'}
    trampled['textures'] = dict(model['textures'])
    if level == 3:
        trampled['textures'].update(CRUSHED_TEXTURES)
    trampled['elements'] = result
    return trampled


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def model_name(block, age, variant):
    return f'{block}_stage{age}' + (f'_variant{variant}' if variant else '')


def trampled_name(block, age, level, variant):
    return f'{block}_trampled_stage{age}_{level}' + (f'_variant{variant}' if variant else '')


def build():
    written = 0
    for block, variants in PLANTS.items():
        for age in AGES:
            for variant in range(variants):
                source = json.loads((MODELS / f'{model_name(block, age, variant)}.json').read_text(encoding='utf-8'))
                for level in LEVELS:
                    save_json(MODELS / f'{trampled_name(block, age, level, variant)}.json', trample_model(source, level))
                    written += 1
        path = BLOCKSTATES / f'{block}.json'
        states = json.loads(path.read_text(encoding='utf-8'))['variants']
        states = {(key if 'flattening' in key else key + ',flattening=0'): value
                  for key, value in states.items() if 'flattening' not in key or key.endswith(',flattening=0')}
        for age in AGES:
            model_age = age
            for level in LEVELS:
                states[f'age={age},flattening={level}'] = [
                    {'model': f'farmerplus:block/{trampled_name(block, model_age, level, variant)}', 'y': turn, 'weight': 1}
                    for variant in range(variants) for turn in (0, 90, 180, 270)
                ]
        save_json(path, {'variants': states})
    print(json.dumps({'trampled_models': written}))


if __name__ == '__main__':
    build()
