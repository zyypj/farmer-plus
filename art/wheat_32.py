from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import math
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'common/src/main/resources'
ART = ROOT / 'art'
PREVIEWS = ROOT / 'build/art/previews'
FP = RES / 'assets/farmerplus'
MC = RES / 'assets/minecraft'
PALETTES = [
    ['283d2b', '3b5934', '547840', '739e50', 'a1bf6a', '486938', '7ea354', 'c3d989'],
    ['283d2b', '3b5934', '547840', '739e50', 'a1bf6a', '486938', '7ea354', 'c3d989'],
    ['30432c', '456135', '618440', '83a651', 'afc570', '55763b', '91ad58', 'cad892'],
    ['35472c', '4e6936', '6a8b42', '8eae55', 'b8cb77', '607d3d', '9cb65f', 'd2dc99'],
    ['3c4a2d', '576b37', '7c9046', 'a0b15b', 'c6cf80', '6e8240', 'aebb68', 'e0dfa0'],
    ['4b4e2d', '74733b', '9a9950', 'bcb566', 'dcd18a', '7d8540', 'b5b461', 'eee1a2'],
    ['594e2d', '89733c', 'b39650', 'd0b666', 'e9ce86', '7d803e', 'aaa257', 'f4e0a0'],
    ['65502d', '91703a', 'b9924a', 'd9b45f', 'eed18a', '7d7d40', 'ad9b50', 'f7e3a7']
]
CULM_PALETTES = [
    ['3b5930', '4d6f39', '67883f', '7d9a4e', '93ad61'],
    ['3b5930', '4d6f39', '67883f', '7d9a4e', '93ad61'],
    ['3b5930', '4d6f39', '67883f', '7d9a4e', '93ad61'],
    ['3b5930', '4d6f39', '67883f', '7d9a4e', '93ad61'],
    ['3b5930', '4d6f39', '67883f', '7d9a4e', '93ad61'],
    ['4c6034', '607b3e', '89944b', 'aebb68', 'c3ca83'],
    ['68683b', '7f8145', 'a39c55', 'c7ba73', 'dfd08e'],
    ['80683f', 'a3824f', 'c8aa69', 'e0c387', 'f0d59d']
]
FOLIAGE_PALETTES = {
    6: ['7a8147', 'a39e59', 'c7bc77'],
    7: ['967c4b', 'bba16a', 'ddc48d']
}


def colors(hexes):
    return [tuple(bytes.fromhex(c)) + (255,) for c in hexes]


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def save_texture(path, image):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert('RGBA').save(path)


def blank():
    return Image.new('RGBA', (32, 32))


def leaf(image, root, direction, length, p, dry=False, droop=0):
    x, y = root
    rise = max(3, round(length * 0.85))
    shoulder = (x + direction * (length - 2), y - rise)
    tip = (x + direction * length, y - rise + droop)
    draw = ImageDraw.Draw(image)
    draw.polygon([(x, y), shoulder, tip, (shoulder[0], shoulder[1] + 2), (x + direction, y)], fill=p[6 if dry else 2])
    draw.line([(x, y), shoulder, tip], fill=p[3 if dry else 4], width=1)
    if length >= 7:
        draw.line([(x + direction, y), (shoulder[0], shoulder[1] + 2)], fill=p[1 if dry else 5], width=1)


def grain_head(image, x, y, p, length=11, bend=1, full=True):
    draw = ImageDraw.Draw(image)
    for row in range(length + 1):
        offset = bend if row < 3 else 0
        draw.point((x + offset, y + row), fill=p[2])
    for side in (-1, 1):
        for row in range(2 if side < 0 else 3, length - 1, 3):
            axis = x + (bend if row < 3 else 0)
            reach = 3 if full and row < length - 3 else 2 if full else 1
            draw.polygon([(axis, y + row + 2), (axis + side * reach, y + row), (axis + side * (reach - 1), y + row - 1), (axis, y + row)], fill=p[3 if side < 0 else 2])
            draw.line([(axis + side * (reach - 1), y + row), (axis + side, y + row + 1)], fill=p[4 if side < 0 else 3], width=1)
            draw.point((axis, y + row + 2), fill=p[1])
    draw.point((x + bend, y), fill=p[7])
    if full:
        draw.line([(x + bend, y), (x + bend + (1 if bend > 0 else -1), y - 2)], fill=p[3], width=1)
        for dx, row in [(-3, 3), (3, 5)]:
            draw.line([(x + (2 if dx > 0 else -2), y + row), (x + dx, y + row - 2)], fill=p[3], width=1)


def full_grain_head(image, x, y, p, bend=1, drop=0):
    draw = ImageDraw.Draw(image)

    def q(dx, dy):
        return (x + dx + round(bend * (1 - dy / 14)), y + dy + round(drop * (1 - dy / 14)))

    draw.line([q(0, 1), q(0, 14)], fill=p[2], width=1)
    for index, row in enumerate((2, 4, 6, 8, 10, 12)):
        side = -1 if index % 2 == 0 else 1
        draw.polygon([q(0, row + 2), q(side * 2, row), q(side * 2, row - 1), q(side, row - 1), q(0, row)], fill=p[3 if side < 0 else 2])
        draw.line([q(side * 2, row - 1), q(side, row)], fill=p[4 if side < 0 else 3], width=1)
        draw.point(q(side, row + 1), fill=p[2 if side < 0 else 1])
    draw.line([q(0, 1), q(0, 0)], fill=p[4], width=1)
    draw.line([q(0, 0), q(bend, -2)], fill=p[3], width=1)
    draw.line([q(-2, 4), q(-3, 2)], fill=p[3], width=1)
    draw.line([q(2, 7), q(3, 5)], fill=p[2], width=1)


def broad_leaf(image, root, side, length, rise, palette):
    draw = ImageDraw.Draw(image)
    x, y = root
    length = max(3, min(length, 30 - x if side > 0 else x - 1))
    control = (x + side * (length * 0.65), y - rise - 2)
    end = (x + side * length, y - 1)
    points = []
    for step in range(13):
        t = step / 12
        points.append((round((1 - t) ** 2 * x + 2 * (1 - t) * t * control[0] + t ** 2 * end[0]), round((1 - t) ** 2 * y + 2 * (1 - t) * t * control[1] + t ** 2 * end[1])))
    draw.line(points[:-2], fill=palette[0], width=2)
    draw.line(points[1:-2], fill=palette[1], width=1)
    draw.line(points[-4:], fill=palette[1], width=1)
    draw.line(points[3:8], fill=palette[2], width=1)


def shaded_culm(image, points, palette, phase=0, width=2):
    draw = ImageDraw.Draw(image)
    samples = {}
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            t = (y - y0) / (y1 - y0) if y1 != y0 else 0
            samples[y] = round(x0 + (x1 - x0) * t)
    top = min(samples)
    for y, x in samples.items():
        if y < top + 3:
            draw.point((x, y), fill=palette[2])
        else:
            draw.point((x - 1, y), fill=palette[3] if top + 4 + phase % 3 <= y <= top + 7 + phase % 3 else palette[2])
            draw.point((x, y), fill=palette[1])
    node = 26 + phase % 3
    if node in samples:
        draw.point((samples[node] - 1, node), fill=palette[1])


def abundant_crop(age, variant):
    image = blank()
    draw = ImageDraw.Draw(image)
    p = colors(PALETTES[age])
    shifts = [(0, 0, 0), (-3, 1, -2), (4, 3, 0), (2, -2, -3)]
    p = [tuple(max(0, min(255, c + shifts[variant][i])) for i, c in enumerate(color[:3])) + (255,) for color in p]
    foliage = colors(FOLIAGE_PALETTES[age])
    layouts = [
        [(5, 4, -2), (12, 3, 1), (20, 4, -1), (27, 6, 2)],
        [(5, 6, -2), (12, 4, -1), (20, 3, 2), (27, 5, 2)],
        [(5, 4, -2), (12, 6, 1), (20, 3, -2), (27, 5, 2)],
        [(5, 6, -2), (12, 4, -1), (20, 3, 1), (27, 6, 2)]
    ]
    for index, (x, top, bend) in enumerate(layouts[variant]):
        top += 1 if age == 6 else 0
        neck_x = x + (-1 if index == 0 else 1 if index == 3 else 0)
        shoulder_x = x + (neck_x - x if index in (0, 3) else (-1 if (variant + index) % 2 else 1))
        shaded_culm(image, [(x, 31), (x, 24), (shoulder_x, 22), (neck_x, top + 14)], colors(CULM_PALETTES[age]), phase=index + variant)
        inward = 1 if x < 16 else -1
        if index == 1:
            broad_leaf(image, (x, [29, 28, 30, 27][variant]), inward if variant % 2 else -inward, 5, 3, foliage)
        full_grain_head(image, neck_x, top, p, bend=bend, drop=1 if index in (0, 3) and variant % 2 == 0 else 0)
    return image


def layered_foliage(age, variant):
    image = blank()
    draw = ImageDraw.Draw(image)
    palette = colors(FOLIAGE_PALETTES[age])
    centres = []
    left = []
    right = []
    for y in range(32):
        t = y / 31
        centre = round((1 - t) ** 2 * 16 + 2 * (1 - t) * t * (9 + variant) + t ** 2 * (18 - variant))
        width = max(0.5, 3 * math.sin(math.pi * t) ** 0.7)
        centres.append((centre, y))
        left.append((round(centre - width), y))
        right.append((round(centre + width), y))
    draw.polygon(left + right[::-1], fill=palette[0])
    draw.polygon(centres[2:29] + left[2:29][::-1], fill=palette[1])
    draw.line(centres[8:19], fill=palette[2], width=1)
    return image


def crop(age, variant=0):
    if age >= 6:
        return abundant_crop(age, variant)
    image = blank()
    draw = ImageDraw.Draw(image)
    p = colors(PALETTES[age])
    shifts = [(0, 0, 0), (-3, 1, -2), (4, 3, 0), (2, -2, -3)]
    p = [tuple(max(0, min(255, c + shifts[variant][i])) for i, c in enumerate(color[:3])) + (255,) for color in p]
    heights = [6, 10, 15, 20, 24, 27, 30, 32]
    stalks = [
        [(6, 3, -1), (16, 0, 1), (26, 5, -1)],
        [(5, 4, 1), (14, 1, -1), (25, 2, 1)],
        [(7, 1, -1), (17, 5, -1), (26, 0, 1)],
        [(5, 5, 1), (15, 2, 1), (25, 3, -1)]
    ][variant]
    for index, (root_x, stagger, bend) in enumerate(stalks):
        top = max(2, 32 - heights[age] + stagger)
        ear_size = 11 if age >= 6 else 9 if age == 5 else 4 if age == 4 else 0
        ear_x = root_x + (bend if age >= 3 else 0)
        stem_top = top + ear_size
        stem_points = [(root_x, 31), (root_x, max(stem_top + 4, 23 - age)), (ear_x, stem_top)]
        if age >= 3:
            shaded_culm(image, stem_points, colors(CULM_PALETTES[age]), phase=index + variant, width=2)
        else:
            draw.line(stem_points, fill=p[2], width=1)
        if age <= 1:
            leaf(image, (root_x, 30), -1 if index % 2 else 1, 4 + age * 2, p)
            leaf(image, (root_x, 31), 1 if index % 2 else -1, 3 + age * 2, p)
        else:
            lower_y = 29 - min(age, 4) - (1 if (variant + index) % 3 == 2 else 0)
            leaf(image, (root_x, lower_y + 2), -1, 6 + age // 2, p, dry=age >= 6, droop=2 if age >= 5 else 1)
            leaf(image, (root_x, lower_y), 1, 5 + age // 2, p, dry=age == 7, droop=1)
            if age >= 3:
                leaf(image, (root_x, lower_y - 4), bend, 6 + age // 3, p, dry=age >= 6)
            if age in (2, 3, 4):
                leaf(image, (root_x, lower_y - 1), -bend, 5 + age, p)
            if age in (2, 3):
                leaf(image, (ear_x, stem_top + 4), bend, 5 + age, p)
        if age >= 4:
            grain_head(image, ear_x, top, p, length=ear_size, bend=bend, full=age >= 5)
    return image


def plane(name, start, end, texture, axis='z', angle=0, uv=None):
    uv = uv or [0, 0, 16, 16]
    sides = ('north', 'south') if axis == 'z' else ('west', 'east')
    return {
        'name': name, 'from': start, 'to': end,
        'rotation': {'origin': [8, 0, 8], 'axis': 'y', 'angle': angle},
        'shade_direction_override': 'up',
        'faces': {
            sides[0]: {'uv': uv, 'texture': texture},
            sides[1]: {'uv': [uv[2], uv[1], uv[0], uv[3]], 'texture': texture}
        }
    }


def crop_height_variant(model, top):
    result = deepcopy(model)
    scale = (top + 1) / (model['elements'][0]['to'][1] + 1)
    for element in result['elements'][:4]:
        element['to'][1] = -1 + (element['to'][1] + 1) * scale
    shifts = {}
    for element in result['elements'][4:]:
        prefix = element['name'].rsplit('_', 1)[0]
        if element['name'].endswith('_base'):
            root_y = element['rotation']['origin'][1]
            shifts[prefix] = (-1 + (root_y + 1) * scale) - root_y
        shift = shifts[prefix]
        element['from'][1] += shift
        element['to'][1] += shift
        element['rotation']['origin'][1] += shift
    return result


def crops():
    suffixes = ['', '_alternate', '_variant2', '_variant3']
    for age in range(8):
        for variant, suffix in enumerate(suffixes):
            name = f'wheat_stage{age}{suffix}'
            save_texture(FP / f'textures/block/{name}.png', crop(age, variant))
            if age >= 6:
                save_texture(FP / f'textures/block/{name}_leaves.png', layered_foliage(age, variant))
        save_texture(MC / f'textures/block/wheat_stage{age}.png', crop(age))
        top = [15, 15, 15, 15, 17, 19, 21, 23][age]
        model = {
            'texture_size': [32, 32], 'ambientocclusion': False,
            'textures': {
                'particle': f'farmerplus:block/wheat_stage{age}',
                'crop': f'farmerplus:block/wheat_stage{age}',
                'alternate': f'farmerplus:block/wheat_stage{age}_alternate',
                'variant2': f'farmerplus:block/wheat_stage{age}_variant2',
                'variant3': f'farmerplus:block/wheat_stage{age}_variant3'
            },
            'elements': [
                plane('front_stalks', [0, -1, 4], [16, top, 4], '#crop', angle=-22.5),
                plane('back_stalks', [0, -1, 11.5], [16, top - (0.5 if age >= 5 else 0), 11.5], '#alternate', angle=22.5, uv=[16, 0, 0, 16]),
                plane('left_stalks', [4, -1, 0], [4, top, 16], '#alternate', axis='x', angle=45),
                plane('right_stalks', [12, -1, 0], [12, top - (1 if age >= 5 else 0), 16], '#crop', axis='x', angle=-45, uv=[16, 0, 0, 16])
            ]
        }
        if age >= 6:
            model['textures'].update({f'foliage{variant}' if variant else 'foliage': f'farmerplus:block/wheat_stage{age}{suffix}_leaves' for variant, suffix in enumerate(suffixes)})
            for name, card, pixel_x, height, direction, span_axis, length in [
                ('front_leaf', 0, 5, 5.4, -1, 'z', 2.75),
                ('rear_leaf', 1, 27, 4.75, 1, 'z', 3),
                ('left_leaf', 2, 12, 5.8, -1, 'x', 2),
                ('right_leaf', 3, 12, 3.9, 1, 'x', 3),
                ('front_lower_leaf', 0, 27, 3.75, -1, 'z', 1.6),
                ('rear_upper_leaf', 1, 5, 6.1, 1, 'z', 1.65)
            ]:
                plant = model['elements'][card]
                local_x = 16 - pixel_x / 2 if card == 0 else pixel_x / 2 if card == 1 else plant['from'][0]
                local_z = pixel_x / 2 if card == 2 else 16 - pixel_x / 2 if card == 3 else plant['from'][2]
                yaw = math.radians(plant['rotation']['angle'])
                root_x = 8 + (local_x - 8) * math.cos(yaw) + (local_z - 8) * math.sin(yaw)
                root_z = 8 - (local_x - 8) * math.sin(yaw) + (local_z - 8) * math.cos(yaw)
                root_y = height * (top + 1) / 24
                if span_axis == 'z':
                    root_z += direction * 0.04
                else:
                    root_x += direction * 0.04
                for part in range(2):
                    x, y, z = root_x, root_y, root_z
                    if part:
                        y += length * math.sin(math.pi / 8)
                        if span_axis == 'z':
                            z += direction * length * math.cos(math.pi / 8)
                        else:
                            x += direction * length * math.cos(math.pi / 8)
                    if span_axis == 'z':
                        start_z, end_z = sorted([z, z + direction * length])
                        start, end = [x - 3, y, start_z], [x + 3, y, end_z]
                    else:
                        start_x, end_x = sorted([x, x + direction * length])
                        start, end = [start_x, y, z - 3], [end_x, y, z + 3]
                    uv = [0, part * 8, 16, (part + 1) * 8] if direction > 0 else [0, (part + 1) * 8, 16, part * 8]
                    if span_axis == 'x':
                        uv = [uv[0], uv[3], uv[2], uv[1]]
                    model['elements'].append({
                        'name': f'{name}_{"tip" if part else "base"}',
                        'from': start, 'to': end,
                        'rotation': {'origin': [x, y, z], 'axis': 'x' if span_axis == 'z' else 'z', 'angle': direction * (1 if span_axis == 'z' else -1) * (22.5 if part else -22.5)},
                        'shade_direction_override': 'up',
                        'faces': {'up': {'uv': uv, 'texture': '#foliage', 'rotation': 0 if span_axis == 'z' else 90}, 'down': {'uv': [uv[0], uv[3], uv[2], uv[1]], 'texture': '#foliage', 'rotation': 0 if span_axis == 'z' else 270}}
                    })
        save_json(ART / f'model-inputs/wheat_stage{age}.json', model)
        save_json(MC / f'models/block/wheat_stage{age}.json', {
            'parent': f'farmerplus:block/wheat_stage{age}',
            'textures': {'crop': f'minecraft:block/wheat_stage{age}', 'particle': f'minecraft:block/wheat_stage{age}'}
        })
        for variant, (first, second) in enumerate([(1, 2), (3, 1), (2, 3)], start=1):
            variant_model = {
                'parent': f'farmerplus:block/wheat_stage{age}',
                'textures': {
                    'crop': f'farmerplus:block/wheat_stage{age}{suffixes[first]}',
                    'alternate': f'farmerplus:block/wheat_stage{age}{suffixes[second]}',
                    'particle': f'farmerplus:block/wheat_stage{age}{suffixes[first]}'
                }
            }
            if age >= 6:
                variant_model['textures']['foliage'] = f'farmerplus:block/wheat_stage{age}{suffixes[variant]}_leaves'
                heights = [21, 18, 24, 20] if age == 6 else [23, 19, 26, 21]
                geometry = crop_height_variant(model, heights[variant])
                geometry['textures'].update(variant_model['textures'])
                geometry['textures'] = {key: value for key, value in geometry['textures'].items() if key in ('particle', 'crop', 'alternate', 'foliage')}
                save_json(ART / f'model-inputs/wheat_stage{age}_variant{variant}.json', geometry)
                save_json(FP / f'models/block/wheat_stage{age}_variant{variant}.json', geometry)
            else:
                save_json(FP / f'models/block/wheat_stage{age}_variant{variant}.json', variant_model)
    save_json(MC / 'blockstates/wheat.json', {'variants': {
        f'age={age}': [
            {'model': f'minecraft:block/wheat_stage{age}' if variant == 0 else f'farmerplus:block/wheat_stage{age}_variant{variant}', 'y': angle}
            for variant in range(4) for angle in (0, 90, 180, 270)
        ] for age in range(8)
    }})


def items():
    flour = blank()
    d = ImageDraw.Draw(flour)
    p = colors(['85705a', 'ad9475', 'c9b99b', 'ded1b5', 'ede3cc', 'fff1da'])
    outline = [(2, 26), (6, 22), (10, 18), (13, 12), (16, 8), (18, 12), (20, 18), (24, 22), (28, 25), (27, 28), (7, 29)]
    d.polygon(outline, fill=p[2])
    d.polygon([(2, 26), (7, 22), (11, 17), (16, 8), (16, 13), (13, 19), (11, 25), (6, 27)], fill=p[5])
    d.polygon([(16, 10), (18, 14), (17, 18), (20, 22), (23, 25), (17, 25), (13, 27), (11, 25), (13, 20)], fill=p[4])
    d.polygon([(18, 13), (20, 18), (23, 22), (26, 25), (22, 26), (20, 22), (17, 20)], fill=p[3])
    d.line([(4, 27), (11, 28), (19, 28), (27, 27)], fill=p[1], width=1)
    for xy in [(3, 29), (28, 29), (1, 27), (24, 30), (9, 25), (10, 23), (15, 16), (17, 24), (21, 27)]:
        d.point(xy, fill=p[4])
    save_texture(FP / 'textures/item/flour.png', flour)

    dough = blank()
    d = ImageDraw.Draw(dough)
    p = colors(['906c45', 'ad8655', 'c3a06a', 'dab984', 'e9ce9c', 'f4dfb6', 'ffebc5'])
    d.polygon([(3, 18), (5, 13), (10, 9), (17, 8), (23, 10), (28, 14), (30, 20), (28, 25), (23, 28), (10, 29), (5, 26), (2, 22)], fill=p[1])
    d.polygon([(3, 18), (6, 13), (11, 10), (18, 9), (24, 12), (28, 16), (28, 22), (24, 26), (11, 27), (6, 24), (3, 21)], fill=p[3])
    d.polygon([(5, 16), (11, 11), (18, 10), (23, 13), (22, 18), (16, 22), (10, 24), (6, 22), (4, 19)], fill=p[5])
    d.polygon([(9, 13), (15, 11), (19, 12), (16, 15), (11, 17), (7, 19), (6, 17)], fill=p[6])
    d.line([(23, 12), (25, 16), (24, 19), (21, 20), (19, 24), (14, 26), (10, 26)], fill=p[2], width=1)
    d.line([(22, 12), (23, 16), (22, 18), (19, 20), (17, 23), (13, 24)], fill=p[4], width=1)
    d.line([(6, 24), (10, 27), (20, 27), (26, 24)], fill=p[2], width=1)
    for xy in [(11, 18), (12, 18), (16, 13), (20, 15), (8, 21), (26, 21), (15, 25)]:
        d.point(xy, fill=p[4])
    save_texture(FP / 'textures/item/dough.png', dough)

    porridge = blank()
    d = ImageDraw.Draw(porridge)
    wood = colors(['423026', '63432e', '815a38', 'a07549', 'c39a62'])
    cream = colors(['af8c55', 'ccad72', 'dfc48d', 'eed7a6', 'f8e7c3', 'fff0d2'])
    d.polygon([(2, 14), (29, 14), (28, 22), (25, 26), (21, 28), (11, 28), (6, 25), (3, 21)], fill=wood[1])
    d.polygon([(3, 16), (15, 18), (26, 16), (25, 22), (21, 25), (12, 25), (7, 23), (4, 20)], fill=wood[2])
    d.line([(5, 20), (10, 23), (20, 24), (25, 21)], fill=wood[3], width=1)
    d.line([(7, 25), (12, 27), (21, 27), (26, 24)], fill=wood[0], width=1)
    d.ellipse((1, 7, 30, 20), fill=wood[0])
    d.ellipse((2, 7, 29, 18), fill=wood[3])
    d.ellipse((4, 8, 27, 16), fill=cream[2])
    d.ellipse((5, 8, 26, 15), fill=cream[4])
    d.arc((2, 7, 29, 18), 180, 320, fill=wood[4], width=1)
    d.arc((4, 8, 27, 17), 10, 160, fill=cream[0], width=1)
    for x, y, shade in [(8, 11, 1), (13, 10, 2), (20, 10, 1), (23, 13, 2), (17, 13, 0), (11, 14, 1), (6, 13, 2)]:
        d.line([(x, y), (x + 2, y)], fill=cream[shade], width=1)
        d.point((x, y - 1), fill=cream[3])
    for xy in [(10, 9), (14, 12), (20, 14), (7, 12), (24, 11)]:
        d.point(xy, fill=cream[5])
    save_texture(FP / 'textures/item/wheat_porridge.png', porridge)

    wheat = blank()
    d = ImageDraw.Draw(wheat)
    p = colors(['806039', 'a47b3e', 'bd944d', 'd3ad5c', 'e5c577', 'f4dca0', 'a69b53'])
    for tip_x, tip_y, lean, base_x in [(7, 6, 0.22, 9), (27, 8, -0.35, 12), (18, 2, -0.18, 10)]:
        def point(u, v):
            return (round(tip_x + lean * v + u), tip_y + v)
        end = point(0, 13)
        d.line([(base_x + 1, 29), (15, 23), end], fill=p[1], width=2)
        d.line([(base_x, 29), (14, 23), (end[0] - 1, end[1])], fill=p[4], width=1)
        d.polygon([point(0, 0), point(-1, 2), point(-2, 5), point(-2, 9), point(0, 13), point(2, 9), point(2, 4)], fill=p[2])
        for v in (3, 6, 9):
            d.polygon([point(0, v + 3), point(-2, v + 1), point(-3, v - 1), point(-1, v), point(0, v + 1)], fill=p[4])
            d.line([point(-2, v - 1), point(-1, v)], fill=p[5], width=1)
            d.polygon([point(0, v + 3), point(2, v + 2), point(3, v), point(1, v + 1), point(0, v + 1)], fill=p[3])
            d.point(point(2, v + 2), fill=p[1])
        d.line([point(0, 1), point(0, -1)], fill=p[5], width=1)
        d.line([point(-2, 3), point(-3, 1)], fill=p[3], width=1)
        d.line([point(2, 7), point(3, 5)], fill=p[4], width=1)
    d.polygon([(12, 25), (8, 22), (6, 18), (9, 20), (11, 23)], fill=p[6])
    d.line([(12, 25), (8, 21)], fill=p[4], width=1)
    d.polygon([(13, 26), (17, 22), (22, 21), (19, 24)], fill=p[2])
    d.line([(14, 25), (19, 22)], fill=p[4], width=1)
    save_texture(MC / 'textures/item/wheat.png', wheat)

    seeds = blank()
    d = ImageDraw.Draw(seeds)
    p = colors(['806139', 'a18343', 'bb9f58', 'd2bb78', 'ead6a0', 'f7e8bb', '8e9651'])
    for x, y, angle in [(9, 7, -30), (23, 8, 35), (16, 16, -20), (7, 25, 25), (24, 25, -35)]:
        angle = math.radians(angle)
        def polygon(points, shade):
            d.polygon([(round(x + u * math.cos(angle) - v * math.sin(angle)), round(y + u * math.sin(angle) + v * math.cos(angle))) for u, v in points], fill=p[shade])
        polygon([(-5, 0), (-3, -2), (1, -2), (4, -1), (5, 0), (3, 2), (-1, 2), (-4, 1)], 1)
        polygon([(-5, 0), (-3, -2), (1, -2), (3, -1), (0, 0), (-3, 1)], 4)
        polygon([(-3, -1), (-1, -2), (1, -2), (2, -1), (-2, 0)], 5)
        polygon([(-3, 1), (0, 1), (3, 0), (4, 0), (2, 1), (-1, 2)], 3)
        crease = [(-3, 0), (-1, 0), (1, -1), (3, -1)]
        d.line([(round(x + u * math.cos(angle) - v * math.sin(angle)), round(y + u * math.sin(angle) + v * math.cos(angle))) for u, v in crease], fill=p[1], width=1)
        polygon([(-4, 0), (-3, 1), (-4, 1)], 6)
        polygon([(3, 0), (4, 1), (3, 2)], 2)
    save_texture(MC / 'textures/item/wheat_seeds.png', seeds)
    for name in ('wheat', 'wheat_seeds'):
        save_json(MC / f'items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'minecraft:item/{name}'}})
        save_json(MC / f'models/item/{name}.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'minecraft:item/{name}'}})


def sheaf():
    p = colors(['8f7446', 'aa8d52', 'c3a563', 'dabb78', 'ecd39a', 'f7e5b5'])
    side = blank()
    draw = ImageDraw.Draw(side)
    draw.rectangle((0, 0, 31, 31), fill=p[2])
    for index, x in enumerate((0, 2, 5, 7, 10, 13, 15, 18, 21, 24, 26, 29)):
        draw.line([(x, 0), (x, 31)], fill=p[1], width=1)
        draw.line([(x + 1, 0), (x + 1, 31)], fill=p[3], width=1)
        draw.line([(x + 1, 4 + index % 6), (x + 1, 10 + index % 6)], fill=p[4], width=1)
    draw.rectangle((0, 0, 11, 0), fill=(0, 0, 0, 0))
    draw.rectangle((20, 0, 31, 0), fill=(0, 0, 0, 0))
    draw.rectangle((0, 1, 5, 1), fill=(0, 0, 0, 0))
    draw.rectangle((26, 1, 31, 1), fill=(0, 0, 0, 0))
    save_texture(FP / 'textures/block/wheat_sheaf_side.png', side)
    top = blank()
    draw = ImageDraw.Draw(top)
    draw.rectangle((0, 0, 31, 31), fill=p[2])
    for y in range(0, 32, 4):
        for x in range(-1, 32, 4):
            offset = 2 if (y // 4) % 2 else 0
            draw.ellipse((x + offset, y, x + offset + 2, y + 2), fill=p[4])
            draw.point((x + offset + 1, y + 1), fill=p[1])
    save_texture(FP / 'textures/block/wheat_sheaf_top.png', top)
    twine = blank()
    draw = ImageDraw.Draw(twine)
    rope = colors(['67503a', '8e6f4b', 'ae8c5e', 'c7a778', 'dec494'])
    draw.rectangle((0, 0, 31, 31), fill=rope[2])
    for y in range(32):
        for x in range(32):
            thread = (x + y // 2) % 6
            draw.point((x, y), fill=rope[3 if thread < 2 else 1 if thread == 5 else 2])
    save_texture(FP / 'textures/block/wheat_sheaf_twine.png', twine)

    stalks = side.copy()
    mask = Image.new('L', (32, 32))
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.polygon([(10, 0), (22, 0), (30, 29), (29, 31), (2, 31), (1, 29)], fill=255)
    for x in range(32):
        end = 29 + (x * 7 // 2) % 3
        if end < 31:
            mask_draw.line([(x, end + 1), (x, 31)], fill=0, width=1)
    stalks.putalpha(mask)
    save_texture(FP / 'textures/block/wheat_sheaf_stalks.png', stalks)
    bound = stalks.copy()
    save_texture(FP / 'textures/block/wheat_sheaf_bound_stalks.png', bound)
    def harvest_ear(image, x, y, bend, length=14):
        draw = ImageDraw.Draw(image)
        def kernel(dx, dy):
            return (x + round(dx * (0.75 if length <= 11 else 1)) + round(bend * (1 - dy / 14)), y + round(dy * length / 14))
        draw.polygon([kernel(0, 1), kernel(-1, 2), kernel(-2, 5), kernel(-1, 11), kernel(0, 14), kernel(1, 11), kernel(2, 5), kernel(1, 2)], fill=p[2])
        for row in (3, 6, 9, 12):
            reach = 1 if row == 12 else 2
            draw.line([kernel(-reach, row), kernel(-1, row + 1), kernel(0, row + 2)], fill=p[4], width=1)
            draw.line([kernel(reach, row + 1), kernel(1, row + 2)], fill=p[1], width=1)
            draw.point(kernel(1, row), fill=p[3])
        draw.line([kernel(0, 1), kernel(bend, -1)], fill=p[4], width=1)
        draw.line([kernel(-2, 4), kernel(-3, 2)], fill=p[3], width=1)
        draw.line([kernel(2, 7), kernel(3, 5)], fill=p[3], width=1)
    ears = blank()
    draw = ImageDraw.Draw(ears)
    for index, (x, y, bend) in enumerate(((4, 5, -1), (10, 2, -1), (16, 1, 0), (22, 3, 1), (28, 6, 1))):
        draw.line([(11 + index * 2.5, 31), (x, y + 14)], fill=p[1], width=2)
        draw.line([(10 + index * 2.5, 31), (x - 1, y + 14)], fill=p[3], width=1)
        harvest_ear(ears, x, y, bend)
    save_texture(FP / 'textures/block/wheat_sheaf_ears.png', ears)
    icon = blank()
    draw = ImageDraw.Draw(icon)
    draw.polygon([(8, 29), (13, 20), (18, 20), (24, 29), (22, 30), (9, 30)], fill=p[1])
    for index, bottom_x in enumerate((8, 10, 12, 14, 17, 19, 21, 24)):
        draw.line([(bottom_x, 29 + index % 2), (13 + index * 0.7, 20)], fill=p[3 if index % 2 else 2], width=1)
    for index, (x, y, bend) in enumerate(((5, 6, -1), (11, 3, -1), (16, 1, 0), (22, 4, 1), (27, 7, 1))):
        draw.line([(13 + index, 21), (x, y + 10)], fill=p[1], width=2)
        draw.line([(12 + index, 20), (x - 1, y + 10)], fill=p[4], width=1)
        harvest_ear(icon, x, y, bend, length=10)
    draw.line([(12, 20), (18, 21)], fill=rope[0], width=3)
    draw.line([(12, 19), (18, 20)], fill=rope[3], width=1)
    draw.line([(16, 21), (12, 18), (9, 18), (10, 21), (13, 23), (16, 21), (20, 18), (23, 19), (22, 22), (19, 23), (16, 21)], fill=rope[0], width=2)
    draw.line([(15, 20), (12, 18), (10, 18)], fill=rope[3], width=1)
    draw.line([(18, 20), (20, 18), (22, 19)], fill=rope[4], width=1)
    draw.line([(16, 22), (13, 25), (13, 28)], fill=rope[1], width=2)
    draw.line([(18, 22), (20, 25), (23, 26)], fill=rope[2], width=2)
    draw.rectangle((15, 20, 18, 22), fill=rope[1])
    draw.point((16, 20), fill=rope[4])
    save_texture(FP / 'textures/item/wheat_sheaf.png', icon)
    save_json(FP / 'models/item/wheat_sheaf.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'farmerplus:item/wheat_sheaf'}})
    save_json(FP / 'items/wheat_sheaf.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:display_context', 'cases': [{'when': ['gui'], 'model': {'type': 'minecraft:model', 'model': 'farmerplus:item/wheat_sheaf'}}], 'fallback': {'type': 'minecraft:model', 'model': 'farmerplus:block/wheat_sheaf'}}})

    displays = {
        'gui': {'rotation': [12, 210, -8], 'translation': [0, 0, 0], 'scale': [0.78] * 3},
        'ground': {'rotation': [0, 0, 0], 'translation': [0, 3, 0], 'scale': [0.35] * 3},
        'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [0.5] * 3},
        'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [0.375] * 3},
        'thirdperson_lefthand': {'rotation': [75, 225, 0], 'translation': [0, 2.5, 0], 'scale': [0.375] * 3},
        'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 1, 0], 'scale': [0.4] * 3},
        'firstperson_lefthand': {'rotation': [0, 225, 0], 'translation': [0, 1, 0], 'scale': [0.4] * 3}
    }
    model = {
        'texture_size': [32, 32],
        'textures': {key: f'farmerplus:block/wheat_sheaf_{suffix}' for key, suffix in [('particle', 'side'), ('side', 'side'), ('top', 'top'), ('twine', 'twine'), ('ears', 'ears'), ('stalks', 'stalks'), ('bound', 'bound_stalks')]},
        'elements': [
            plane('front_stalk_ends', [4, 0, 6.2], [12, 7.1, 6.2], '#bound', angle=22.5),
            plane('back_stalk_ends', [4, 0, 9.8], [12, 7.1, 9.8], '#stalks', angle=-22.5, uv=[16, 0, 0, 16]),
            plane('left_stalk_ends', [6.2, 0, 4], [6.2, 7.1, 12], '#stalks', axis='x', angle=-22.5),
            plane('right_stalk_ends', [9.8, 0, 4], [9.8, 7.1, 12], '#stalks', axis='x', angle=22.5, uv=[16, 0, 0, 16]),
            plane('front_harvested_heads', [3, 6.6, 6.1], [13, 16, 6.1], '#ears', angle=22.5),
            plane('back_harvested_heads', [3, 6.6, 9.9], [13, 15.5, 9.9], '#ears', angle=-22.5, uv=[16, 0, 0, 16]),
            plane('left_harvested_heads', [6.1, 6.6, 2.5], [6.1, 15.8, 13.5], '#ears', axis='x', angle=-22.5),
            plane('right_harvested_heads', [9.9, 6.6, 2.5], [9.9, 15.4, 13.5], '#ears', axis='x', angle=22.5, uv=[16, 0, 0, 16])
        ],
        'display': displays
    }
    model['elements'].append({
        'name': 'compressed_stalk_waist', 'from': [6, 5.7, 6], 'to': [10, 7.7, 10],
        'faces': {**{direction: {'uv': [4, 5, 8, 7], 'texture': '#side'} for direction in ('north', 'south', 'east', 'west')}, **{direction: {'uv': [0, 0, 8, 8], 'texture': '#top'} for direction in ('up', 'down')}}
    })
    def cord_box(name, start, end, rotation=None, capped=True):
        width = min(16, max(end[i] - start[i] for i in range(3)))
        directions = ('north', 'south', 'east', 'west', 'up', 'down') if capped else ('north', 'south', 'up', 'down')
        element = {'name': name, 'from': start, 'to': end, 'faces': {direction: {'uv': [0, 2, width, 3], 'texture': '#twine'} for direction in directions}}
        if rotation:
            element['rotation'] = rotation
        model['elements'].append(element)
    cord_box('binding_front', [5.75, 6.9, 5.75], [10.25, 7.25, 6.1])
    cord_box('binding_right', [9.9, 6.9, 6.1], [10.25, 7.25, 9.9])
    cord_box('binding_back', [5.75, 6.9, 9.9], [10.25, 7.25, 10.25])
    cord_box('binding_left', [5.75, 6.9, 6.1], [6.1, 7.25, 9.9])
    for side, centre_x, reach, depth in [('left', 6.4, 1.5, 5.4), ('right', 9.7, 1.6, 5.3)]:
        rise = reach * math.tan(math.radians(22.5))
        vertices = [(centre_x - reach, 7.05), (centre_x, 7.05 + rise), (centre_x + reach, 7.05), (centre_x, 7.05 - rise)]
        for index, (a, b) in enumerate(zip(vertices, vertices[1:] + vertices[:1])):
            if b[0] < a[0]:
                a, b = b, a
            length = math.dist(a, b)
            angle = 22.5 if b[1] > a[1] else -22.5
            cord_box(f'bow_{side}_{index}', [a[0] - 0.06, a[1] - 0.14, depth - 0.14], [a[0] + length + 0.06, a[1] + 0.14, depth + 0.14], {'origin': [a[0], a[1], depth], 'axis': 'z', 'angle': angle}, capped=False)
    cord_box('binding_knot', [7.55, 6.65, 4.95], [8.45, 7.5, 5.9], {'origin': [8, 7.05, 5.4], 'axis': 'z', 'angle': 22.5})
    for name, root, length, angle in [('left', [7.85, 6.85, 5.35], 2.45, -22.5), ('right', [8.2, 6.85, 5.2], 2.05, 45)]:
        x, y, z = root
        cord_box(f'bow_tail_{name}', [x - 0.14, y - length, z - 0.14], [x + 0.14, y + 0.08, z + 0.14], {'origin': root, 'axis': 'z', 'angle': angle})
    save_json(ART / 'model-inputs/wheat_sheaf.json', model)


def contact():
    sheet = Image.new('RGB', (1440, 700), '#202b25')
    d = ImageDraw.Draw(sheet)
    font_path = Path('C:/Windows/Fonts/consola.ttf')
    font = ImageFont.truetype(str(font_path), 22)
    small = ImageFont.truetype(str(font_path), 17)
    d.text((32, 20), 'FARMER+ / REALISTIC VANILLA+ / NATIVE 32 x 32 PIXEL ART', fill='#eed18a', font=font)
    for age in range(8):
        x = 32 + 174 * age
        d.rectangle((x, 78, x + 159, 237), fill='#354438')
        im = crop(age).resize((160, 160), Image.Resampling.NEAREST)
        sheet.paste(im, (x, 78), im)
        d.text((x + 35, 250), f'AGE {age}', fill='#e3d6b3', font=font)
        d.text((x, 282), f'{[15,15,15,15,17,19,21,23][age] + 1}/16 model', fill='#a6b39a', font=small)
    paths = [FP / f'textures/item/{n}.png' for n in ('flour', 'dough', 'wheat_porridge', 'wheat_sheaf')]
    paths += [MC / f'textures/item/{n}.png' for n in ('wheat', 'wheat_seeds')]
    paths += [FP / 'textures/block/wheat_sheaf_stalks.png', FP / 'textures/block/wheat_sheaf_ears.png']
    for index, path in enumerate(paths):
        x = 32 + index * 174
        im = Image.open(path).resize((160, 160), Image.Resampling.NEAREST)
        d.rectangle((x, 366, x + 159, 525), fill='#354438')
        sheet.paste(im, (x, 366), im)
        d.text((x, 550), path.stem.replace('wheat_sheaf_', 'sheaf_'), fill='#e3d6b3', font=small)
    d.text((32, 635), 'Exact pixels, binary alpha, original limited palettes. This sheet shows textures, not in-game height.', fill='#a6b39a', font=small)
    save_texture(PREVIEWS / 'wheat-textures.png', sheet)
    variants = Image.new('RGB', (880, 290), '#202b25')
    d = ImageDraw.Draw(variants)
    d.text((24, 16), 'AGE 7 / FOUR BOTANICAL VARIATIONS / 32 x 32', font=font, fill='#eed18a')
    for variant in range(4):
        im = crop(7, variant).resize((192, 192), Image.Resampling.NEAREST)
        variants.paste(im, (24 + variant * 216, 60), im)
        d.text((24 + variant * 216, 260), f'VARIANT {variant + 1}', font=small, fill='#e3d6b3')
    save_texture(PREVIEWS / 'wheat-variants.png', variants)


def build():
    crops()
    items()
    sheaf()
    contact()
