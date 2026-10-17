from pathlib import Path
from PIL import Image, ImageDraw
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


def texture(name, image, item=False):
    path = ASSET / 'textures' / ('item' if item else 'block') / f'{name}.png'
    image.save(path)


def leaf_texture(kind):
    image = Image.new('RGBA', (32, 32))
    draw = ImageDraw.Draw(image)
    palettes = {
        'mature': ['254b2b', '356c37', '488644', '69a854', '91bf68', 'a9ce7a'],
        'young': ['396b36', '50863e', '6ba54d', '8dc364', 'b2d786', 'c7e39b'],
        'aged': ['465733', '617340', '7c8b46', '9da455', 'b9bc6e', 'd1ce88'],
        'under': ['476744', '5b8050', '73965c', '8caa70', 'a6bd87', 'b7ca98']
    }
    p = ['#' + c for c in palettes[kind]]
    draw.line([(16, 31), (16, 15)], fill=p[2], width=2)
    draw.line([(16, 25), (7, 18)], fill=p[2], width=1)
    draw.line([(16, 25), (25, 18)], fill=p[2], width=1)
    central = [(16, 1), (18, 3), (20, 3), (20, 5), (22, 6), (21, 8), (22, 10), (20, 11), (21, 13), (19, 14), (19, 16), (16, 19), (13, 17), (13, 15), (11, 14), (12, 12), (10, 11), (11, 9), (10, 7), (12, 6), (12, 4), (14, 4)]
    left = [(2, 10), (5, 10), (6, 9), (8, 11), (10, 11), (10, 13), (12, 14), (11, 16), (13, 18), (11, 20), (10, 23), (7, 23), (6, 25), (4, 23), (2, 23), (2, 21), (0, 20), (1, 18), (0, 16), (2, 15), (1, 13)]
    right = [(31 - x, y + 1) for x, y in left]
    for index, outline in enumerate([left, right, central]):
        draw.polygon(outline, fill=p[0])
        cx = sum(v[0] for v in outline) / len(outline)
        cy = sum(v[1] for v in outline) / len(outline)
        inner = [(round(cx + (x - cx) * .82), round(cy + (y - cy) * .86)) for x, y in outline]
        draw.polygon(inner, fill=p[2])
        if index == 2:
            draw.polygon([(16, 3), (13, 6), (12, 10), (14, 14), (16, 17)], fill=p[3])
            draw.line([(16, 4), (16, 17)], fill=p[4], width=1)
            for y in [7, 11, 14]:
                draw.line([(16, y + 2), (13, y)], fill=p[3], width=1)
                draw.line([(17, y + 2), (20, y)], fill=p[1], width=1)
        else:
            mirror = index == 1
            def point(x, y):
                return (31 - x, y + 1) if mirror else (x, y)
            draw.polygon([point(x, y) for x, y in [(3, 12), (7, 13), (9, 17), (8, 21), (5, 19), (3, 16)]], fill=p[3])
            draw.line([point(3, 12), point(10, 22)], fill=p[4], width=1)
            draw.line([point(6, 17), point(3, 18)], fill=p[4], width=1)
            draw.line([point(8, 20), point(9, 16)], fill=p[1], width=1)
    return image


def textures():
    for suffix, kind in [('', 'mature'), ('_young', 'young'), ('_aged', 'aged'), ('_under', 'under')]:
        texture('strawberry_leaf' + suffix, leaf_texture(kind))
    flower = Image.new('RGBA', (32, 32))
    d = ImageDraw.Draw(flower)
    for i in range(5):
        a = math.radians(-90 + 72 * i)
        def polar(radial, lateral):
            return (round(16 + math.cos(a) * radial - math.sin(a) * lateral), round(12 + math.sin(a) * radial + math.cos(a) * lateral))
        points = [polar(2, -2), polar(5, -4), polar(8, -3), polar(10, -1), polar(10, 1), polar(8, 3), polar(5, 4), polar(2, 2)]
        d.polygon(points, fill='#c7d0b9')
        d.polygon([polar(2, -1), polar(5, -3), polar(8, -2), polar(9, 0), polar(7, 2), polar(3, 2)], fill='#fff7e1')
        d.line([polar(3, -1), polar(7, -1)], fill='#ffffff', width=1)
    d.ellipse((12, 9, 19, 15), fill='#bea640')
    d.ellipse((13, 9, 18, 13), fill='#eed566')
    d.point((14, 10), fill='#fff1a1')
    d.line([(3, 31), (3, 28), (6, 26), (9, 28)], fill='#648444', width=1)
    d.polygon([(2, 27), (4, 25), (7, 26), (9, 25), (10, 28), (6, 29)], fill='#f5efd8')
    texture('strawberry_flower', flower)
    fruit = Image.new('RGBA', (32, 32))
    d = ImageDraw.Draw(fruit)
    for ox, green in [(0, False), (16, True)]:
        p = ['#6e252f', '#a72c38', '#ce3b42', '#ec5152', '#fa7870', '#ffc0a3'] if not green else ['#658244', '#91a35c', '#bdc382', '#dfd8ad', '#f1e6ca', '#fff1dc']
        d.rectangle((ox, 0, ox + 15, 15), fill=p[2])
        d.polygon([(ox, 0), (ox + 9, 0), (ox + 6, 10), (ox, 12)], fill=p[3])
        d.polygon([(ox + 12, 0), (ox + 15, 0), (ox + 15, 15), (ox + 6, 15), (ox + 11, 10)], fill=p[1])
        d.line([(ox + 14, 3), (ox + 14, 14), (ox + 8, 14)], fill=p[0], width=1)
        d.line([(ox + 3, 2), (ox + 6, 2)], fill=p[5], width=1)
        d.point((ox + 2, 3), fill=p[4])
        for x, y in [(3, 5), (9, 3), (12, 7), (6, 9), (2, 12), (10, 12)]:
            d.point((ox + x + 1, y + 1), fill=p[0])
            d.line([(ox + x, y), (ox + x, y + 1)], fill='#f5d67f' if not green else '#ddcf83', width=1)
        d.rectangle((ox, 16, ox + 15, 31), fill=p[2])
        d.polygon([(ox + 8, 17), (ox + 10, 21), (ox + 15, 21), (ox + 11, 25), (ox + 13, 30), (ox + 8, 27), (ox + 3, 30), (ox + 5, 25), (ox, 21), (ox + 6, 21)], fill='#355f32')
        d.line([(ox + 8, 19), (ox + 8, 26), (ox + 4, 28)], fill='#8eb454', width=1)
        d.line([(ox + 8, 23), (ox + 12, 22)], fill='#66963d', width=1)
        for corner in [(0, 0), (1, 0), (0, 1), (15, 0), (14, 0), (15, 1)]:
            d.point((ox + corner[0], corner[1]), fill=(0, 0, 0, 0))
        for x, y in [(0, 16), (1, 16), (0, 17), (15, 16), (14, 16), (15, 17), (0, 31), (15, 31)]:
            d.point((ox + x, y), fill=(0, 0, 0, 0))
    texture('strawberry_fruit', fruit)
    base_red = ['6e252f', 'a72c38', 'ce3b42', 'ec5152', 'fa7870', 'ffc0a3']
    base_green = ['658244', '91a35c', 'bdc382', 'dfd8ad', 'f1e6ca', 'fff1dc']
    for suffix, red, green in [
        ('rose', ['8b3039', 'bd3f45', 'e05257', 'f16d68', 'ff9483', 'ffd3ad'], ['8a945f', 'b0b78a', 'd1d1b0', 'e5dfc8', 'f5ebd7', 'fff5e4']),
        ('deep', ['59232f', '8e2939', 'b32e40', 'd9414f', 'ee6c6a', 'ffb0a1'], ['50723e', '7a9851', 'a6b771', 'c8ce96', 'e6dfb8', 'f3ebce'])
    ]:
        mapping = {tuple(bytes.fromhex(a)) + (255,): tuple(bytes.fromhex(b)) + (255,) for a, b in zip(base_red + base_green, red + green)}
        alternative = fruit.copy()
        alternative.putdata([mapping.get(pixel, pixel) for pixel in fruit.get_flattened_data()])
        texture('strawberry_fruit_' + suffix, alternative)
    stem = Image.new('RGBA', (32, 32))
    d = ImageDraw.Draw(stem)
    d.rectangle((0, 0, 1, 31), fill='#6d9749')
    d.line([(1, 0), (1, 31)], fill='#436a36', width=1)
    d.rectangle((16, 16, 31, 31), fill='#536d37')
    for x in range(17, 32, 3):
        d.line([(x, 17), (x, 30)], fill='#829047', width=1)
        d.point((x, 28), fill='#755b38')
    d.rectangle((16, 16, 31, 31), fill=(0, 0, 0, 0))
    d.polygon([(23, 17), (26, 20), (30, 20), (28, 24), (30, 27), (26, 28), (24, 31), (21, 28), (17, 28), (19, 24), (17, 21), (21, 20)], fill='#49703a')
    d.polygon([(23, 19), (26, 22), (27, 26), (24, 29), (21, 26), (20, 23)], fill='#78964b')
    d.rectangle((22, 23, 25, 25), fill='#826c41')
    texture('strawberry_stem', stem)
    peduncle = Image.new('RGBA', (32, 32))
    d = ImageDraw.Draw(peduncle)
    d.line([(0, 31), (6, 20), (15, 6), (24, 10), (31, 16)], fill='#416b35', width=2)
    d.line([(0, 31), (6, 20), (15, 6), (24, 10), (31, 16)], fill='#83a957', width=1)
    texture('strawberry_peduncle', peduncle)
    paired = Image.new('RGBA', (32, 32))
    d = ImageDraw.Draw(paired)
    for points in [[(16, 31), (11, 19), (7, 10), (3, 13), (0, 16)], [(16, 31), (20, 19), (25, 10), (29, 13), (31, 16)]]:
        d.line(points, fill='#608c45', width=1)
    texture('strawberry_peduncle_pair', paired)
    item = Image.new('RGBA', (32, 32))
    d = ImageDraw.Draw(item)
    outline = [(6, 8), (12, 6), (17, 8), (23, 7), (28, 11), (29, 16), (26, 22), (21, 27), (16, 30), (12, 28), (6, 21), (3, 15), (3, 11)]
    d.polygon(outline, fill='#7c2533')
    d.polygon([(6, 9), (12, 7), (17, 9), (23, 8), (27, 12), (27, 17), (24, 22), (16, 28), (12, 26), (7, 20), (4, 14)], fill='#cf3544')
    d.polygon([(7, 10), (12, 9), (17, 11), (20, 10), (23, 13), (20, 21), (14, 25), (9, 20), (6, 15)], fill='#ee5055')
    d.polygon([(8, 11), (12, 10), (15, 12), (13, 16), (8, 16), (6, 14)], fill='#fa7c76')
    d.line([(8, 12), (11, 11), (13, 12)], fill='#ffc1a5', width=1)
    for x, y in [(6, 17), (11, 19), (17, 14), (24, 13), (22, 19), (16, 22), (18, 26), (10, 24)]:
        d.line([(x + 1, y + 1), (x + 1, y + 2)], fill='#a82c37', width=1)
        d.line([(x, y), (x, y + 1)], fill='#f6d57b', width=1)
    d.polygon([(7, 7), (12, 7), (12, 3), (17, 6), (22, 3), (21, 7), (27, 8), (22, 10), (23, 13), (17, 11), (13, 14), (12, 10), (6, 11)], fill='#305d32')
    d.line([(10, 8), (15, 9), (20, 6)], fill='#88b953', width=2)
    d.line([(16, 8), (17, 4), (20, 2)], fill='#668b3c', width=2)
    texture('strawberry', item, item=True)


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
    elements.append({'name': f'fruit_{index}_tapered_tip', 'from': [v - half for v in centre], 'to': [v + half for v in centre], 'rotation': rotation(centre, tip_angles), 'faces': {face: {'uv': [u + 2, 2, u + 6, 6], 'texture': material} for face in ('north', 'south', 'east', 'west', 'up', 'down')}})


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
    return name, {'ambientocclusion': False, 'texture_size': [32, 32], 'textures': {key: 'farmerplus:block/' + value for key, value in [('particle', 'strawberry_leaf'), ('leaf', 'strawberry_leaf'), ('young', 'strawberry_leaf_young'), ('aged', 'strawberry_leaf_aged'), ('under', 'strawberry_leaf_under'), ('flower', 'strawberry_flower'), ('fruit', 'strawberry_fruit'), ('rose', 'strawberry_fruit_rose'), ('deep', 'strawberry_fruit_deep'), ('stem', 'strawberry_stem'), ('peduncle', 'strawberry_peduncle'), ('paired', 'strawberry_peduncle_pair')]}, 'elements': elements}


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
            states[f'age={age}'] = entries
        write_json(ASSET / 'blockstates' / f'{block}.json', {'variants': states})
    write_json(WORK / 'strawberry-models.json', manifest)
    print(json.dumps({'models': len(manifest), 'textures': 12, 'outputs': str(WORK)}))


if __name__ == '__main__':
    build()
