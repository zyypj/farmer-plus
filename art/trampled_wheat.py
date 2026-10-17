from pathlib import Path
from PIL import Image, ImageEnhance
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets/farmerplus'
TEXTURES = ASSETS / 'textures/block'
MODELS = ASSETS / 'models/block'

AGES = range(8)
FACINGS = {'north': 0, 'east': 90, 'south': 180, 'west': 270}
GROUND = -1.0

BENT = 1
FLATTENED = 2
CRUSHED = 3

BENT_CARDS = [
    {'z': 13.0, 'tilt': 36, 'yaw': -8, 'texture': 'crop'},
    {'z': 10.5, 'tilt': 47, 'yaw': 6, 'texture': 'alternate'},
    {'z': 8.0, 'tilt': 30, 'yaw': -3, 'texture': 'crop'},
    {'z': 5.5, 'tilt': 42, 'yaw': 10, 'texture': 'alternate'},
]
BENT_SIDE_CARDS = [
    {'x': 4.5, 'lean': 24, 'texture': 'alternate'},
    {'x': 11.5, 'lean': 31, 'texture': 'crop'},
]
FLATTENED_CARDS = [
    {'z': 13.5, 'stub': 4.0, 'tilt': 74, 'yaw': -10, 'texture': 'alternate'},
    {'z': 11.0, 'stub': 3.0, 'tilt': 80, 'yaw': 8, 'texture': 'crop'},
    {'z': 8.5, 'stub': 4.5, 'tilt': 70, 'yaw': -4, 'texture': 'alternate'},
    {'z': 6.0, 'stub': 3.5, 'tilt': 78, 'yaw': 12, 'texture': 'crop'},
]
CRUSHED_CARDS = [
    {'z': 14.0, 'stub': 1.2, 'tilt': 86, 'yaw': -18, 'texture': 'crop'},
    {'z': 11.5, 'stub': 1.5, 'tilt': 88, 'yaw': -6, 'texture': 'alternate'},
    {'z': 9.0, 'stub': 1.8, 'tilt': 87, 'yaw': 7, 'texture': 'crop'},
    {'z': 6.5, 'stub': 2.1, 'tilt': 89, 'yaw': 16, 'texture': 'alternate'},
]


def card_height(age):
    return {4: 18.0, 5: 20.0, 6: 22.0, 7: 24.0}.get(age, 16.0)


def faces_z(texture, v0, v1):
    return {
        'north': {'uv': [0, v0, 16, v1], 'texture': '#' + texture},
        'south': {'uv': [16, v0, 0, v1], 'texture': '#' + texture},
    }


def faces_x(texture, u0, u1, v0, v1):
    return {
        'east': {'uv': [u1, v0, u0, v1], 'texture': '#' + texture},
        'west': {'uv': [u0, v0, u1, v1], 'texture': '#' + texture},
    }


def element(name, start, end, rotation, faces):
    return {
        'name': name,
        'from': [round(value, 3) for value in start],
        'to': [round(value, 3) for value in end],
        'shade_direction_override': 'up',
        'rotation': rotation,
        'faces': faces,
    }


def euler(origin, tilt, yaw):
    return {'origin': [round(value, 3) for value in origin], 'x': -tilt, 'y': yaw}


def uv_split(height, stub):
    return round(16 * (1 - stub / height), 3)


def bent_elements(height):
    elements = []
    for index, card in enumerate(BENT_CARDS):
        z = card['z']
        elements.append(element(
            f'bent_stalks_{index}', [0, GROUND, z], [16, GROUND + height, z],
            euler([8, GROUND, z], card['tilt'], card['yaw']),
            faces_z(card['texture'], 0, 16)))
    for index, card in enumerate(BENT_SIDE_CARDS):
        x = card['x']
        elements.append(element(
            f'leaning_side_{index}', [x, GROUND, 5], [x, GROUND + height, 11],
            {'origin': [x, GROUND, 8], 'axis': 'x', 'angle': -card['lean']},
            faces_x(card['texture'], 5, 11, 0, 16)))
    return elements


def kinked_elements(height, cards, prefix):
    elements = []
    for index, card in enumerate(cards):
        z = card['z']
        stub = card['stub']
        split = uv_split(height, stub)
        elements.append(element(
            f'{prefix}_stub_{index}', [0, GROUND, z], [16, GROUND + stub, z],
            euler([8, GROUND, z], 8, card['yaw']),
            faces_z(card['texture'], split, 16)))
        elements.append(element(
            f'{prefix}_fallen_{index}', [0, GROUND + stub, z], [16, GROUND + height, z],
            euler([8, GROUND + stub, z], card['tilt'], card['yaw']),
            faces_z(card['texture'], 0, split)))
    return elements


def model(age, flattening):
    height = card_height(age)
    if flattening == BENT:
        elements = bent_elements(height)
        crop, alternate = f'wheat_stage{age}', f'wheat_stage{age}_alternate'
    elif flattening == FLATTENED:
        elements = kinked_elements(height, FLATTENED_CARDS, 'flattened')
        crop, alternate = f'wheat_stage{age}', f'wheat_stage{age}_alternate'
    else:
        elements = kinked_elements(height, CRUSHED_CARDS, 'crushed')
        crop, alternate = f'wheat_stage{age}_crushed', f'wheat_stage{age}_alternate_crushed'
    return {
        'ambientocclusion': False,
        'textures': {
            'particle': f'farmerplus:block/{crop}',
            'crop': f'farmerplus:block/{crop}',
            'alternate': f'farmerplus:block/{alternate}',
        },
        'elements': elements,
    }


def variant(base, model_data):
    textures = model_data['textures']
    return {
        'parent': base,
        'textures': {
            'particle': textures['alternate'],
            'crop': textures['alternate'],
            'alternate': textures['crop'],
        },
    }


def crushed_texture(source, target):
    age = int(source.stem.removeprefix('wheat_stage').split('_')[0])
    if age >= 2:
        from crushed_pixels import crushed
        crushed(age, 'alternate' in source.stem).save(target)
        return
    image = Image.open(source).convert('RGBA')
    alpha = image.getchannel('A')
    rgb = ImageEnhance.Color(image.convert('RGB')).enhance(0.55)
    rgb = ImageEnhance.Brightness(rgb).enhance(0.72)
    tint = Image.new('RGB', rgb.size, (92, 74, 46))
    rgb = Image.blend(rgb, tint, 0.18)
    result = rgb.convert('RGBA')
    result.putalpha(alpha.point(lambda value: 255 if value >= 128 else 0))
    result.save(target)


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def build():
    variants = {}
    for age in AGES:
        for name in (f'wheat_stage{age}', f'wheat_stage{age}_alternate'):
            crushed_texture(TEXTURES / f'{name}.png', TEXTURES / f'{name}_crushed.png')
        for flattening in (BENT, FLATTENED, CRUSHED):
            name = f'trampled_wheat_stage{age}_{flattening}'
            data = model(age, flattening)
            save_json(MODELS / f'{name}.json', data)
            save_json(MODELS / f'{name}_variant1.json', variant(f'farmerplus:block/{name}', data))
            for facing, rotation in FACINGS.items():
                variants[f'age={age},facing={facing},flattening={flattening}'] = [
                    {'model': f'farmerplus:block/{name}', 'y': rotation},
                    {'model': f'farmerplus:block/{name}_variant1', 'y': rotation},
                ]
    save_json(ASSETS / 'blockstates/trampled_wheat.json', {'variants': variants})


if __name__ == '__main__':
    build()
