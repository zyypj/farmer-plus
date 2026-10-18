import json
import math
import random
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets/farmerplus'
NS = 'farmerplus:block/'
CARDINAL = {'north': 0, 'east': 90, 'south': 180, 'west': 270}
DIAGONAL = {'north_east': 0, 'south_east': 90, 'south_west': 180, 'north_west': 270}
LEAF_SEGMENTS = ('base', 'blade', 'tip')


def rgb(value):
    value = value.lstrip('#')
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def save(image, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8', newline='\n')


def canvas():
    return Image.new('RGBA', (16, 16), (0, 0, 0, 0))


def leaf_texture(tip):
    rng = random.Random(41 if tip else 17)
    image = canvas()
    blade, vein, dark, rib, rib_edge, dry = (rgb(c) for c in ('#4b8a2b', '#6aa83d', '#3c7323', '#b9cc6c', '#79a243', '#9a8f45'))
    tears = {(4, 'l'), (11, 'l'), (7, 'r'), (13, 'r')} if not tip else {(9, 'l'), (12, 'r')}
    for y in range(16):
        half = 7.5 if not tip else min(7.5, 0.6 + y * 0.52)
        for x in range(16):
            offset = abs(x - 7.5)
            if offset > half:
                continue
            if offset <= 0.5:
                color = rib
            elif offset <= 1.5:
                color = rib_edge
            else:
                color = vein if (y + int(offset * 0.35)) % 3 == 0 else blade
                if offset > half - 1 and rng.random() < 0.35:
                    color = dry
                elif rng.random() < 0.08:
                    color = dark
            image.putpixel((x, y), color)
    for row, side in tears:
        xs = range(0, 4) if side == 'l' else range(12, 16)
        for x in xs:
            image.putpixel((x, row), (0, 0, 0, 0))
    return image


def dry_leaf_texture():
    rng = random.Random(23)
    image = canvas()
    browns = [rgb(c) for c in ('#8b6b3a', '#a3834a', '#6e5230', '#7d5e33')]
    rib_color = rgb('#c2a46a')
    for y in range(16):
        half = max(0.6, 7.5 - y * 0.42)
        for x in range(16):
            offset = abs(x - 7.5)
            if offset > half:
                continue
            if offset <= 0.5:
                color = rib_color
            elif rng.random() < 0.18:
                continue
            else:
                color = browns[(x * 3 + y + rng.randrange(2)) % len(browns)]
            image.putpixel((x, y), color)
    for row in (3, 6, 10):
        for x in list(range(0, 5)) + list(range(11, 16)):
            image.putpixel((x, row), (0, 0, 0, 0))
    return image


def stem_texture():
    rng = random.Random(5)
    image = canvas()
    base, light, edge, blotch, blotch_dark, dried = (rgb(c) for c in ('#7aa046', '#9cc062', '#557a32', '#6e4733', '#4d3125', '#8f7044'))
    for y in range(16):
        for x in range(16):
            color = base
            if x in (3, 9, 14):
                color = edge
            elif x in (4, 10, 15):
                color = light
            image.putpixel((x, y), color)
    for _ in range(7):
        cx, cy = rng.randrange(16), rng.randrange(16)
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (0, -1)):
            if rng.random() < 0.8:
                image.putpixel(((cx + dx) % 16, (cy + dy) % 16), blotch if rng.random() < 0.6 else blotch_dark)
    for y in range(0, 16):
        if rng.random() < 0.7:
            image.putpixel((0, y), dried)
    return image


def stem_top_texture():
    image = canvas()
    rings = [(1.2, '#e7e2bf'), (2.2, '#cdd79a'), (3.1, '#8fb352'), (5.0, '#6f9a3f'), (99, '#557a32')]
    for y in range(16):
        for x in range(16):
            distance = math.hypot(x - 7.5, y - 7.5)
            image.putpixel((x, y), next(rgb(c) for r, c in rings if distance <= r))
    return image


def heart_texture():
    image = canvas()
    base, dark, light, bloom = (rgb(c) for c in ('#6b1f3d', '#4a142b', '#93385a', '#a8687f'))
    for y in range(16):
        for x in range(16):
            row = (y + (x // 4) * 2) % 5
            color = dark if row == 0 else light if row == 1 else base
            if (x * 7 + y * 3) % 11 == 0:
                color = bloom
            image.putpixel((x, y), color)
    return image


def fingers_texture(ripe):
    image = canvas()
    if ripe:
        body, high, edge, gap, tip = (rgb(c) for c in ('#e6c235', '#f7e06a', '#c9a226', '#7d5f1c', '#4a3a1a'))
    else:
        body, high, edge, gap, tip = (rgb(c) for c in ('#76ad3c', '#98c958', '#5e8f30', '#3f6420', '#3a4222'))
    spot = rgb('#7a5520')
    for y in range(16):
        for x in range(16):
            column = x % 4
            color = gap if column == 3 else high if column == 1 else edge if column == 0 else body
            if y % 8 == 0 and column != 3:
                color = tip
            if ripe and (x * 5 + y * 3) % 17 == 0 and column != 3:
                color = spot
            image.putpixel((x, y), color)
    return image


def sapling_texture():
    image = canvas()
    stem, stem_dark, leaf, rib, blotch = (rgb(c) for c in ('#7aa046', '#557a32', '#5a9a30', '#a6c45e', '#7a3f2a'))
    for y in range(9, 16):
        image.putpixel((7, y), stem_dark)
        image.putpixel((8, y), stem)
    image.putpixel((8, 12), blotch)
    blades = [[(7, 8), (7, 7), (8, 6), (8, 5), (8, 4), (7, 3), (7, 2), (8, 1)],
              [(6, 9), (5, 8), (4, 7), (3, 6), (2, 5), (2, 4), (1, 3)],
              [(9, 9), (10, 8), (11, 7), (12, 6), (13, 5), (13, 4), (14, 3)]]
    for blade in blades:
        for i, (x, y) in enumerate(blade):
            image.putpixel((x, y), rib)
            for side in (-1, 1):
                nx = x + side
                if 0 <= nx < 16 and image.getpixel((nx, y))[3] == 0 and i > 0:
                    image.putpixel((nx, y), leaf)
    image.putpixel((3, 6), blotch)
    image.putpixel((12, 6), blotch)
    return image


def banana_item_texture():
    rows = [
        '............gb..',
        '...........ogo..',
        '...........oso..',
        '..........osyo..',
        '.........osyho..',
        '........osyyho..',
        '.......osyyho...',
        '......osyyhho...',
        '.....osyyyho....',
        '...oosyyyhoo....',
        '.boosyyyhho.....',
        '.bssyyyhhoo.....',
        '..ossyyhoo......',
        '...oooooo.......',
        '................',
        '................',
    ]
    palette = {'o': '#8a6414', 'y': '#e8c63a', 'h': '#f8e27a', 's': '#c99f25', 'b': '#4a3416', 'g': '#7a8a3a'}
    image = canvas()
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char in palette:
                image.putpixel((x, y), rgb(palette[char]))
    return image


def leaf_item_texture():
    image = canvas()
    blade, vein, rib, petiole = (rgb(c) for c in ('#4b8a2b', '#6aa83d', '#c3d278', '#7aa046'))
    start, end = (2.0, 13.5), (14.0, 1.5)
    length = math.hypot(end[0] - start[0], end[1] - start[1])
    ux, uy = (end[0] - start[0]) / length, (end[1] - start[1]) / length
    for y in range(16):
        for x in range(16):
            px, py = x + 0.5 - start[0], y + 0.5 - start[1]
            t = (px * ux + py * uy) / length
            d = px * -uy + py * ux
            if t < 0 or t > 1:
                continue
            if t < 0.18:
                if abs(d) < 0.6:
                    image.putpixel((x, y), petiole)
                continue
            width = 3.4 * math.sin(math.pi * min(1.0, (t - 0.12) / 0.88)) ** 0.7
            if abs(d) < 0.55:
                image.putpixel((x, y), rib)
            elif abs(d) < width:
                image.putpixel((x, y), vein if (x + y) % 3 == 0 else blade)
    return image


def face(uv, texture, rotation=None):
    data = {'uv': uv, 'texture': texture}
    if rotation:
        data['rotation'] = rotation
    return data


def box(name, start, end, faces, rotation=None):
    element = {'name': name, 'from': start, 'to': end, 'faces': faces}
    if rotation:
        element['rotation'] = rotation
    return element


def flat(name, start, end, uv, texture, rotation):
    return box(name, start, end, {'up': face(uv, texture), 'down': face(uv, texture)}, rotation)


def sides(uv, texture, end_uv=None, end_texture=None):
    faces = {side: face(uv, texture) for side in ('north', 'east', 'south', 'west')}
    if end_uv:
        faces['up'] = face(end_uv, end_texture or texture)
        faces['down'] = face(end_uv, end_texture or texture)
    return faces


def euler(origin, x=0, y=0, z=0):
    return {'origin': origin, 'x': x, 'y': y, 'z': z}


def model(textures, elements, ambient_occlusion=False):
    return {'ambientocclusion': ambient_occlusion, 'textures': dict(textures, particle=textures[next(iter(textures))]), 'elements': elements}


HALF_WIDTH = 6.5
AGES = {
    'young': {'petiole': 30, 'blade': 4, 'tip': -22},
    'mature': {'petiole': 14, 'blade': -7, 'tip': -42},
}


def leaf_halves(prefix, z0, z1, y, uv_left, uv_right, texture, origin, x=0, spread=10, yaw=0):
    fold = spread if yaw == 0 else 0
    return [
        flat(prefix + '_left', [origin[0] - HALF_WIDTH, y, z0], [origin[0], y, z1], uv_left, texture, euler(origin, x, yaw, fold)),
        flat(prefix + '_right', [origin[0], y, z0], [origin[0] + HALF_WIDTH, y, z1], uv_right, texture, euler(origin, x, yaw, -fold)),
    ]


def rib(name, z0, z1, y, origin, x=0, yaw=0):
    return box(name, [origin[0] - 0.75, y - 0.6, z0], [origin[0] + 0.75, y, z1],
               sides([7, 0, 9, 16], '#leaf', [7, 0, 9, 16]), euler(origin, x, yaw))


def petiole(center_x, z0, z1, pivot, tilt, yaw=0):
    return box('petiole', [center_x - 0.75, 9, z0], [center_x + 0.75, 10.5, z1],
               sides([6, 0, 7, 16], '#leaf', [6, 0, 7, 2]), euler(pivot, x=tilt, y=yaw))


def lift(length, degrees):
    return length * math.sin(math.radians(degrees))


def leaf_models():
    textures = {'leaf': NS + 'banana_leaf', 'tip': NS + 'banana_leaf_tip'}
    models = {}
    for age, pose in AGES.items():
        blade_y = round(9.75 + lift(13, pose['petiole']), 2)
        tip_y = round(blade_y + lift(16, pose['blade']), 2)
        models['banana_leaf_%s_base' % age] = model(textures, [petiole(8, 8, 21, [8, 9.75, 21], pose['petiole'])]
                                                    + leaf_halves('blade_base', 0, 10, blade_y, [0, 16, 8, 5], [8, 16, 16, 5], '#tip', [8, blade_y, 10]))
        models['banana_leaf_%s_blade' % age] = model(textures, leaf_halves('blade', 0, 16, blade_y, [0, 0, 8, 16], [8, 0, 16, 16], '#leaf', [8, blade_y, 16], x=pose['blade'])
                                                     + [rib('midrib', 0, 16, blade_y + 0.4, [8, blade_y, 16], x=pose['blade'])])
        models['banana_leaf_%s_tip' % age] = model(textures, leaf_halves('tip', 0, 16, tip_y, [0, 0, 8, 16], [8, 0, 16, 16], '#tip', [8, tip_y, 16], x=pose['tip'])
                                                   + [rib('midrib', 0, 16, tip_y + 0.4, [8, tip_y, 16], x=pose['tip'])])
        models['banana_leaf_%s_diagonal_base' % age] = model(textures, [petiole(-8, 7, 21, [-8, 9.75, 24], pose['petiole'], yaw=-45)]
                                                             + leaf_halves('blade', -9.9, 11, blade_y, [0, 16, 8, 3], [8, 16, 16, 3], '#tip', [-8, blade_y, 24], yaw=-45))
        models['banana_leaf_%s_diagonal_tip' % age] = model(textures, leaf_halves('tip', -6.6, 16, blade_y, [0, 0, 8, 16], [8, 0, 16, 16], '#tip', [0, blade_y, 16],
                                                                                  x=round((pose['blade'] + pose['tip']) * 0.75), yaw=-45))
    dry = {'leaf': NS + 'banana_leaf_dry'}
    hanging = lambda name, yaw: box(name, [8 - HALF_WIDTH * 0.7, -14, 14.5], [8 + HALF_WIDTH * 0.7, 10, 14.5],
                                    {'north': face([3, 0, 13, 16], '#leaf'), 'south': face([3, 0, 13, 16], '#leaf')}, euler([8, 10, 14.5], x=-6, y=yaw))
    models['banana_leaf_dry'] = model(dry, [
        box('petiole', [7.25, 9.5, 14.5], [8.75, 11, 21.5], sides([6, 0, 7, 7], '#leaf', [6, 0, 7, 2]), euler([8, 10, 21.5], x=-25)),
        hanging('blade_left', 10), hanging('blade_right', -10),
    ])
    return models


def stem_models():
    textures = {'side': NS + 'banana_stem', 'end': NS + 'banana_stem_top', 'leaf': NS + 'banana_leaf'}
    column = lambda top: box('pseudostem', [5, 0, 5], [11, top, 11], sides([5, 16 - top, 11, 16], '#side', [5, 5, 11, 11], '#end'))
    return {
        'banana_stem_base': model(textures, [
            column(16),
            box('corm', [4, 0, 4], [12, 2.5, 12], sides([4, 13.5, 12, 16], '#side', [4, 4, 12, 12], '#end')),
        ]),
        'banana_stem_middle': model(textures, [column(16)]),
        'banana_stem_crown': model(textures, [
            column(13),
            box('leaf_sheaths', [4.5, 10, 4.5], [11.5, 15, 11.5], sides([4, 1, 12, 6], '#side', [4, 4, 12, 12], '#end')),
            box('cigar_leaf', [7.25, 13, 7.25], [8.75, 28, 8.75], sides([7, 0, 9, 15], '#leaf', [7, 0, 9, 2]), euler([8, 13, 8], x=6)),
        ]),
    }


def bunch_models():
    stalk = [
        box('peduncle_arch', [7, 14, -5], [9, 16, 7], sides([7, 0, 9, 12], '#stalk', [7, 4, 9, 16])),
        box('peduncle_drop', [7, 14, 5], [9, 16, 7], sides([7, 0, 9, 2], '#stalk', [7, 5, 9, 7])),
    ]

    def hands(tiers, texture):
        result = []
        for i, (inset, top) in enumerate(tiers):
            size = 12 - inset * 2
            result.append(box('hand_%d' % i, [2 + inset, top - 3.5, 3 + inset], [14 - inset, top, 15 - inset],
                              sides([0, 4.5, size, 8], texture, [0, 0, size, size])))
        return result

    heart = lambda start, end: box('male_bud', start, end, sides([4, 2, 12, 14], '#heart', [5, 5, 11, 11]))
    rachis = lambda top, bottom: box('rachis', [7.6, bottom, 8.6], [8.4, top, 9.4], sides([7, 0, 9, 8], '#stalk', [7, 7, 9, 9]))
    base_textures = {'stalk': NS + 'banana_stem', 'heart': NS + 'banana_heart'}
    full_tiers = [(0, 14), (0.5, 10.5), (1, 7), (2, 3.5)]
    return {
        'banana_bunch_bud': model(base_textures, stalk + [heart([6, 3, 6.5], [10, 9.5, 10.5]), heart([7, 0, 7.5], [9, 3, 9.5])]),
        'banana_bunch_flowering': model(dict(base_textures, fingers=NS + 'banana_fingers_green'),
                                        stalk + hands([(2, 12), (2.5, 8.5)], '#fingers') + [rachis(3, 0), heart([6.5, -5, 7.5], [9.5, 0.5, 10.5])]),
        'banana_bunch_green': model(dict(base_textures, fingers=NS + 'banana_fingers_green'),
                                    stalk + hands(full_tiers, '#fingers') + [rachis(0.5, -3), heart([6.5, -8, 7.5], [9.5, -3, 10.5])]),
        'banana_bunch_ripe': model(dict(base_textures, fingers=NS + 'banana_fingers_ripe'),
                                   stalk + hands(full_tiers, '#fingers') + [rachis(0.5, -3), heart([6.5, -8, 7.5], [9.5, -3, 10.5])]),
    }


def blockstates():
    leaf = {}
    for direction, angle in {**CARDINAL, **DIAGONAL}.items():
        for age in ('young', 'mature', 'dry'):
            for segment in range(3):
                if age == 'dry':
                    name = 'banana_leaf_dry'
                    angle_used = CARDINAL.get(direction, DIAGONAL.get(direction))
                elif direction in CARDINAL:
                    name = 'banana_leaf_%s_%s' % (age, LEAF_SEGMENTS[segment])
                    angle_used = angle
                else:
                    name = 'banana_leaf_%s_diagonal_%s' % (age, 'base' if segment == 0 else 'tip')
                    angle_used = angle
                variant = {'model': 'farmerplus:block/' + name}
                if angle_used:
                    variant['y'] = angle_used
                leaf['age=%s,direction=%s,segment=%d' % (age, direction, segment)] = variant
    stem = {'fruited=%s,segment=%s' % (fruited, segment): {'model': 'farmerplus:block/banana_stem_' + segment}
            for fruited in ('false', 'true') for segment in ('base', 'middle', 'crown')}
    bunch = {}
    for facing, angle in CARDINAL.items():
        for stage, name in enumerate(('bud', 'flowering', 'green', 'ripe')):
            variant = {'model': 'farmerplus:block/banana_bunch_' + name}
            if angle:
                variant['y'] = angle
            bunch['facing=%s,stage=%d' % (facing, stage)] = variant
    return {
        'banana_leaf': {'variants': leaf},
        'banana_stem': {'variants': stem},
        'banana_bunch': {'variants': bunch},
        'banana_sapling': {'variants': {'': {'model': 'farmerplus:block/banana_sapling'}}},
    }


def main():
    textures = {
        'block/banana_leaf': leaf_texture(False),
        'block/banana_leaf_tip': leaf_texture(True),
        'block/banana_leaf_dry': dry_leaf_texture(),
        'block/banana_stem': stem_texture(),
        'block/banana_stem_top': stem_top_texture(),
        'block/banana_heart': heart_texture(),
        'block/banana_fingers_green': fingers_texture(False),
        'block/banana_fingers_ripe': fingers_texture(True),
        'block/banana_sapling': sapling_texture(),
        'item/banana': banana_item_texture(),
        'item/banana_leaf': leaf_item_texture(),
    }
    for name, image in textures.items():
        target = ASSETS / 'textures' / (name + '.png')
        if not target.exists():
            save(image, target)
    for name, data in {**leaf_models(), **stem_models(), **bunch_models()}.items():
        write(ASSETS / 'models/block' / (name + '.json'), data)
    write(ASSETS / 'models/block/banana_sapling.json', {'parent': 'minecraft:block/cross', 'textures': {'cross': NS + 'banana_sapling'}})
    for name, data in blockstates().items():
        write(ASSETS / 'blockstates' / (name + '.json'), data)
    for item, layer in (('banana', 'farmerplus:item/banana'), ('banana_leaf', 'farmerplus:item/banana_leaf'), ('banana_sapling', NS + 'banana_sapling')):
        write(ASSETS / 'models/item' / (item + '.json'), {'parent': 'minecraft:item/generated', 'textures': {'layer0': layer}})
        write(ASSETS / 'items' / (item + '.json'), {'model': {'type': 'minecraft:model', 'model': 'farmerplus:item/' + item}})
    print('banana art written')


if __name__ == '__main__':
    main()
