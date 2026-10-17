from pathlib import Path
from strawberry_pixels import textures
import json
import math

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art'
ASSET = ROOT / 'common/src/main/resources/assets/farmerplus'
WORK = ROOT / 'build/art'
BUDGETS = [8, 12, 16, 20, 20]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def transform(point, angles):
    x, y, z = point
    ax, ay, az = [math.radians(v) for v in angles]
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    return [x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az), z]


def rotation(origin, angles):
    return {'origin': origin, **dict(zip(('x', 'y', 'z'), [(angle + 180) % 360 - 180 for angle in angles]))}


def compose(first, second):
    axes = [transform(transform(axis, second), first) for axis in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
    return [math.degrees(math.atan2(axes[1][2], axes[2][2])), math.degrees(math.asin(-axes[0][2])), math.degrees(math.atan2(axes[0][1], axes[0][0]))]


def leaf(elements, index, root, yaw, length, width, pitch, roll, young=False, aged=False, arched=True):
    split = .55
    first = rotation(root, [pitch, yaw, roll])
    uv_joint = 16 * (1 - split)
    material = '#young' if young else '#aged' if aged else '#leaf'
    def card(name, origin, depth, angles, uv):
        x, y, z = origin
        elements.append({'name': name, 'from': [x - width / 2, y, z - depth], 'to': [x + width / 2, y, z], 'rotation': rotation(origin, angles), 'shade_direction_override': 'up', 'faces': {'up': {'uv': uv, 'texture': material}, 'down': {'uv': [uv[0], uv[3], uv[2], uv[1]], 'texture': '#under'}}})
    if not arched:
        card(f'leaf_{index}_whole', root, length, [25 + index % 3 * 6, yaw, roll], [0, 0, 16, 16])
        return
    card(f'leaf_{index}_petiole', root, length * split, [pitch, yaw, roll], [0, uv_joint, 16, 16])
    delta = transform([0, 0, -length * split], [pitch, yaw, roll])
    joint = [root[i] + delta[i] for i in range(3)]
    card(f'leaf_{index}_trifoliate', joint, length * (1 - split), [-13 + index % 3 * 3, yaw, roll], [0, 0, 16, uv_joint])


def straight_stalk(elements, name, root, end):
    delta = [end[i] - root[i] for i in range(3)]
    length = math.sqrt(sum(v * v for v in delta))
    angles = [math.degrees(math.asin(delta[2] / length)), 0, math.degrees(math.atan2(-delta[0], delta[1]))]
    x, y, z = root
    elements.append({'name': name, 'from': [x - .11, y, z], 'to': [x + .11, y + length, z], 'rotation': rotation(root, angles), 'faces': {face: {'uv': [0, 0, 1, 16], 'texture': '#stem'} for face in ('north', 'south')}})


def flower(elements, index, root, centre, yaw):
    straight_stalk(elements, f'flower_{index}_stalk', root, centre)
    x, y, z = centre
    elements.append({'name': f'flower_{index}_five_petals', 'from': [x - 1.25, y, z - 1], 'to': [x + 1.25, y, z + 1], 'rotation': rotation(centre, [8 + index * 3, yaw, -8]), 'shade_direction_override': 'up', 'faces': {'up': {'uv': [0, 0, 16, 12], 'texture': '#flower'}, 'down': {'uv': [0, 12, 16, 0], 'texture': '#flower'}}})


def berry(elements, index, root, angle, radius, ripe, wild, variant, shared_top=None):
    a = math.radians(angle)
    x, z = root[0] + radius * math.cos(a), root[2] + radius * math.sin(a)
    size = [.84, 1.04, .93, 1.1][(index + variant) % 4]
    height = (2.5 if ripe else 2) * (.72 if wild else 1) * size
    width = (2.2 if ripe else 1.6) * (.72 if wild else 1) * size
    top = root[1] + height + .9 + .12 * ((index + variant) % 3)
    if shared_top is not None:
        top = shared_top
    plane_height = (top - root[1]) * 32 / 15
    if shared_top is None:
        elements.append({'name': f'fruit_{index}_arching_stalk', 'from': list(root), 'to': [root[0] + radius, root[1] + plane_height, root[2]], 'rotation': rotation(root, [0, -angle, 0]), 'faces': {'north': {'uv': [16, 0, 0, 16], 'texture': '#peduncle'}, 'south': {'uv': [0, 0, 16, 16], 'texture': '#peduncle'}}})
    u = 0 if ripe else 8
    material = ['#fruit', '#rose', '#deep'][(index + variant) % 3]
    turn = rotation([x, top, z], [(-1 if index % 2 else 1) * 6, angle + variant * 11, -7 + index * 4])
    parent_angles = [turn[axis] for axis in ('x', 'y', 'z')]
    for side, left, right, lean, uv in [('body', -.45, .05, -12, [u, 8, u + 4.5, 16]), ('calyx_shoulders', -.05, .45, 12, [u + 3.5, 8, u + 8, 16])]:
        name = ('ripe_body' if ripe else 'unripe_body') if side == 'body' else side
        elements.append({'name': f'fruit_{index}_' + name, 'from': [x + width * left, top - height * .52, z - width * .4], 'to': [x + width * right, top, z + width * .4], 'rotation': rotation([x, top, z], compose(parent_angles, [0, 0, lean])), 'faces': {**{face: {'uv': [u, 0, u + 8, 6], 'texture': material} for face in ('north', 'south', 'east', 'west', 'down')}, 'up': {'uv': uv, 'texture': material}}})
    delta = transform([0, -height * .58, 0], parent_angles)
    centre = [x + delta[0], top + delta[1], z + delta[2]]
    base_angles = [45, 0, -math.degrees(math.atan(1 / math.sqrt(2)))]
    tip_angles = compose(parent_angles, base_angles)
    half = height * .42 / math.sqrt(3)
    elements.append({'name': f'fruit_{index}_tapered_tip', 'from': [v - half for v in centre], 'to': [v + half for v in centre], 'rotation': rotation(centre, tip_angles), 'faces': {face: {'uv': [u + 3, 4, u + 5, 6], 'texture': material} for face in ('north', 'south', 'east', 'west', 'up', 'down')}})


def model(age, variant, wild):
    prefix = 'wild_strawberries' if wild else 'strawberry_plant'
    name = f'{prefix}_stage{age}' + (f'_variant{variant}' if variant else '')
    scale = [.35, .68, .84, .96, 1][age] * (.69 if wild else 1)
    root = [8, -.65, 8]
    elements = [{'name': 'soil_crown', 'from': [7, -1, 7], 'to': [9, -.62, 9], 'faces': {face: {'uv': [8, 8, 16, 16], 'texture': '#stem'} for face in ('north', 'south', 'east', 'west', 'up', 'down')}}]
    count = 2 if wild and age in (0, 2, 3) else 3 if wild else 3 if age == 0 else 4 if age == 2 else 5
    offsets = [[0, 7, -10, 11, -6], [13, -5, 12, -8, 4], [-8, 15, -4, 8, -12], [9, -12, 3, 17, -5]][variant]
    for i in range(count):
        yaw = i * 360 / count + offsets[i] + variant * 17
        length = (7.4 + ((i * 3 + variant) % 5) * .18) * scale
        width = (8 + (i + variant) % 3 * .2) * scale
        arched = age < 3
        leaf(elements, i, root, yaw, length, width, 54 + (i + variant) % 4 * 3, -4 + (i * 5 + variant * 3) % 9, young=age == 0, aged=age >= 3 and i == 1 and variant == 2, arched=arched)
    if age == 2 or age == 3:
        flowers = (2 if wild else 3) if age == 2 else 1
        for i in range(flowers):
            a = math.radians(35 + i * 120 + variant * 47)
            radius = 3.3 * (.65 if wild else 1)
            centre = [8 + math.cos(a) * radius, (4.6 + .25 * ((i + variant) % 3)) * (.65 if wild else 1), 8 + math.sin(a) * radius]
            flower(elements, i, root, centre, variant * 23 + i * 40)
    if age >= 3:
        fruits = (2 if wild else 3) if age == 3 else (2 if wild else 4)
        angles = [12, 108, 201, 294] if not wild else [31, 203, 285]
        if age == 4 or wild:
            angles = [12, 192, 104, 284] if not wild else [31, 211]
            for pair in range(fruits // 2):
                angle = angles[pair * 2] + variant * 13
                radius = 8.2 * (.67 if wild else 1)
                top = (3.4 + pair * .15) * (.7 if wild else 1)
                depth = (top - root[1]) * 32 / 15
                elements.append({'name': f'fruit_pair_{pair}_arching_stalks', 'from': [root[0] - radius, root[1], root[2]], 'to': [root[0] + radius, root[1] + depth * 22 / 32, root[2]], 'rotation': rotation(root, [0, -angle, 0]), 'faces': {'north': {'uv': [16, 5, 0, 16], 'texture': '#paired'}, 'south': {'uv': [0, 5, 16, 16], 'texture': '#paired'}}})
        for i in range(fruits):
            shared = age == 4 or wild
            angle = angles[i] + variant * 13 if shared else angles[i] + [0, 16, -10, 9][variant] + (i % 2) * variant * 8
            radius = (8.2 if shared else 8.1 + .16 * ((i + variant) % 3)) * (.67 if wild else 1)
            top = (3.4 + (i // 2) * .15) * (.7 if wild else 1) if shared else None
            berry(elements, i, root, angle, radius, age == 4, wild, variant, top)
    budget = 12 if wild else BUDGETS[age]
    assert len(elements) <= budget, (name, len(elements), budget)
    return name, {'ambientocclusion': False, 'texture_size': [16, 16], 'textures': {key: 'farmerplus:block/' + value for key, value in [('particle', 'strawberry_leaf'), ('leaf', 'strawberry_leaf'), ('young', 'strawberry_leaf_young'), ('aged', 'strawberry_leaf_aged'), ('under', 'strawberry_leaf_under'), ('flower', 'strawberry_flower'), ('fruit', 'strawberry_fruit'), ('rose', 'strawberry_fruit_rose'), ('deep', 'strawberry_fruit_deep'), ('stem', 'strawberry_stem'), ('peduncle', 'strawberry_peduncle'), ('paired', 'strawberry_peduncle_pair')]}, 'elements': elements}


def build():
    textures()
    manifest = []
    for wild in [False, True]:
        block = 'wild_strawberries' if wild else 'strawberry_plant'
        states = {}
        for age in range(5):
            entries = []
            for variant in range(2 if wild else 4):
                name, value = model(age, variant, wild)
                write_json(ART / 'model-inputs' / f'{name}.json', value)
                manifest.append(name)
                entries += [{'model': f'farmerplus:block/{name}', 'y': turn, 'weight': 1} for turn in [0, 90, 180, 270]]
            states[f'age={age},flattening=0'] = entries
        write_json(ASSET / 'blockstates' / f'{block}.json', {'variants': states})
    write_json(WORK / 'strawberry-models.json', manifest)
    print(json.dumps({'models': len(manifest), 'textures': 12, 'outputs': str(WORK)}))


if __name__ == '__main__':
    build()
