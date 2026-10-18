from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import math
from copy import deepcopy
from wheat_pixels import crop, layered_foliage, sheaf_textures

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'common/src/main/resources'
ART = ROOT / 'art'
PREVIEWS = ROOT / 'build/art/previews'
FP = RES / 'assets/farmerplus'
MC = RES / 'assets/minecraft'
def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def save_texture(path, image):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert('RGBA').save(path)


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
            'texture_size': [16, 16], 'ambientocclusion': False,
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
    from item_pixels import items as item_textures
    item_textures()
    for name in ('wheat', 'wheat_seeds'):
        save_json(MC / f'items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'minecraft:item/{name}'}})
        save_json(MC / f'models/item/{name}.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'minecraft:item/{name}'}})


def sheaf():
    for suffix, image in sheaf_textures().items():
        save_texture(FP / f'textures/block/wheat_sheaf_{suffix}.png', image)
    from item_pixels import sheaf as sheaf_icon, write
    write('wheat_sheaf', sheaf_icon())
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
        'texture_size': [16, 16],
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
    d.text((32, 20), 'FARMER+ / REALISTIC VANILLA+ / BLOCKS + ITEMS 16 x 16', fill='#eed18a', font=font)
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
    d.text((24, 16), 'AGE 7 / FOUR BOTANICAL VARIATIONS / 16 x 16', font=font, fill='#eed18a')
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
