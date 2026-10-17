from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import math


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets/farmerplus'
BLOCK = ASSETS / 'textures/block'
PREVIEWS = ROOT / 'build/art/previews'
SIDES = ('north', 'south', 'east', 'west')


def save(name, image, folder='block'):
    path = ASSETS / 'textures' / folder / f'{name}.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def textures():
    glass = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(glass)
    d.rectangle((0, 0, 7, 11), fill=(147, 198, 188, 18))
    d.line([(0, 0), (0, 11)], fill=(109, 169, 163, 105))
    d.line([(7, 0), (7, 11)], fill=(90, 146, 143, 92))
    d.line([(0, 0), (7, 0)], fill=(207, 231, 219, 135))
    d.line([(0, 11), (7, 11)], fill=(120, 182, 177, 130))
    d.line([(1, 2), (1, 8)], fill=(232, 247, 235, 175))
    d.line([(2, 1), (2, 3)], fill=(211, 238, 221, 110))
    d.line([(6, 8), (6, 9)], fill=(193, 224, 206, 90))
    d.rectangle((8, 0, 11, 11), fill=(116, 174, 164, 38))
    d.line([(8, 0), (11, 0)], fill=(195, 225, 211, 135))
    d.line([(8, 11), (11, 11)], fill=(126, 179, 166, 130))
    d.line([(8, 1), (8, 10)], fill=(168, 212, 193, 95))
    d.point((10, 7), fill=(165, 38, 53, 220))
    d.point((10, 8), fill=(188, 46, 59, 130))
    d.rectangle((12, 0, 15, 11), fill=(151, 201, 180, 30))
    d.line([(12, 2), (15, 2)], fill=(197, 226, 205, 170))
    d.line([(12, 10), (15, 10)], fill=(106, 164, 155, 120))
    d.rectangle((0, 12, 15, 15), fill=(117, 178, 163, 80))
    d.line([(0, 12), (15, 12)], fill=(206, 232, 211, 180))
    d.line([(0, 15), (15, 15)], fill=(82, 141, 133, 150))
    save('strawberry_jam_glass', glass)

    jam = Image.new('RGBA', (16, 16), '#ad2038')
    d = ImageDraw.Draw(jam)
    d.rectangle((0, 0, 7, 11), fill='#b7273e')
    d.rectangle((0, 0, 1, 11), fill='#d4394a')
    d.rectangle((6, 0, 7, 11), fill='#8b1931')
    d.line([(0, 11), (7, 11)], fill='#73182f')
    d.line([(1, 0), (6, 0)], fill='#e64d55')
    for x, y in [(2, 3), (4, 7), (1, 9), (5, 2)]:
        d.rectangle((x, y, x + 1, y), fill='#de4a52')
        d.point((x + 1, y + 1), fill='#c63849')
    for x, y in [(3, 5), (5, 10), (1, 6), (6, 4)]:
        d.point((x, y), fill='#7b1830')
    d.rectangle((8, 0, 15, 7), fill='#c83145')
    d.line([(9, 1), (13, 1), (14, 2)], fill='#f26568')
    d.line([(9, 2), (9, 3)], fill='#ec515b')
    d.line([(10, 6), (14, 6), (14, 5)], fill='#a51f37')
    d.rectangle((11, 3, 12, 4), fill='#dd4352')
    d.point((13, 3), fill='#8c2033')
    d.point((10, 5), fill='#8c2033')
    save('strawberry_jam_fill', jam)

    lid = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(lid)
    for y in range(12):
        for x in range(16):
            a, b = (x // 2) % 2, (y // 2) % 2
            shade = '#a92c3d' if a and b else '#e68686' if a or b else '#fff0d7'
            if y >= 8 and y == 11 and x % 5 in (0, 4):
                continue
            d.point((x, y), fill=shade)
    for x, y in [(0, 0), (7, 0), (0, 7), (7, 7)]:
        d.point((x, y), fill=(0, 0, 0, 0))
    for x in range(16):
        d.point((x, 12), fill='#e1c48c' if x % 3 else '#b38b58')
        d.point((x, 13), fill='#936b46' if x % 3 else '#c29b66')
        d.point((x, 14), fill='#c7c6ab')
        d.point((x, 15), fill='#797e76')
    d.rectangle((7, 12, 8, 13), fill='#c5a06a')
    d.point((7, 12), fill='#f0d4a0')
    save('strawberry_jam_lid', lid)

    label = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(label)
    d.polygon([(2, 0), (13, 0), (15, 2), (15, 13), (13, 15), (2, 15), (0, 13), (0, 2)], fill='#bda775')
    d.polygon([(2, 1), (13, 1), (14, 2), (14, 12), (12, 14), (2, 14), (1, 12), (1, 3)], fill='#f5e5ba')
    d.line([(3, 2), (12, 2)], fill='#fff2d6')
    d.polygon([(4, 6), (6, 5), (8, 6), (10, 5), (12, 7), (11, 10), (8, 13), (5, 10)], fill='#b5253c')
    d.polygon([(4, 6), (7, 6), (9, 7), (9, 10), (7, 11), (5, 9)], fill='#e64b55')
    d.line([(5, 6), (6, 6)], fill='#f67a72')
    d.line([(5, 5), (7, 5), (8, 3), (8, 5), (11, 4), (9, 6)], fill='#517848')
    d.point((6, 8), fill='#f3ca75')
    d.point((10, 8), fill='#e8b35c')
    d.point((8, 11), fill='#e8b35c')
    save('strawberry_jam_label', label)


def element(name, start, end, texture, uv, directions=None, rotation=None):
    faces = {side: {'texture': '#' + texture, 'uv': uv.copy()} for side in directions or (*SIDES, 'up', 'down')}
    result = {'name': name, 'from': start, 'to': end, 'faces': faces}
    if rotation:
        result['rotation'] = rotation
    return result


def model(level):
    body = []
    body.append(element('glass_front_back', [6, 0, 5], [10, 6.5, 11], 'glass', [0, 0, 8, 12], ['north', 'south', 'down']))
    body.append(element('glass_sides', [5, 0, 6], [11, 6.5, 10], 'glass', [0, 0, 8, 12], ['east', 'west', 'down']))
    for base in body:
        base['faces']['down']['uv'] = [0, 12, 16, 16]
    radius = 2.5 * math.sqrt(2)
    half = math.sqrt(.5)
    for angle, name in [(45, 'glass_bevel_nw_se'), (-45, 'glass_bevel_ne_sw')]:
        body.append(element(name, [8 - half, 0, 8 - radius], [8 + half, 6.5, 8 + radius], 'glass', [8, 0, 12, 12], ['north', 'south'], {'origin': [8, 0, 8], 'axis': 'y', 'angle': angle}))
    top = .55 + level * 1.9
    jam = element('jam_body', [5.55, .55, 5.55], [10.45, top, 10.45], 'jam', [0, 0, 8, 12])
    jam['faces']['up']['uv'] = [8, 0, 16, 8]
    body.append(jam)
    cap = element('gingham_cap', [5.1, 7.65, 5.1], [10.9, 8, 10.9], 'lid', [0, 8, 8, 9])
    cap['faces']['up']['uv'] = [0, 0, 8, 8]
    cap['faces']['down']['uv'] = [0, 14, 16, 16]
    body.append(cap)
    for name, start, end, origin, axis, angle in [
        ('cloth_drape_north', [5.1, 6.05, 5], [10.9, 7.65, 5.2], [8, 7.65, 5.1], 'x', 24),
        ('cloth_drape_south', [5.1, 6.25, 10.8], [10.9, 7.65, 11], [8, 7.65, 10.9], 'x', -20),
        ('cloth_drape_west', [5, 6.15, 5.1], [5.2, 7.65, 10.9], [5.1, 7.65, 8], 'z', -22),
        ('cloth_drape_east', [10.8, 6.05, 5.1], [11, 7.65, 10.9], [10.9, 7.65, 8], 'z', 18),
    ]:
        body.append(element(name, start, end, 'lid', [0, 8, 8, 12], rotation={'origin': origin, 'axis': axis, 'angle': angle}))
    body.append(element('raised_twine_wrap', [4.82, 7.0, 4.82], [11.18, 7.5, 11.18], 'lid', [0, 12, 16, 14], list(SIDES)))
    body.append(element('cream_strawberry_label_north', [6.45, 2.6, 4.97], [9.55, 5.1, 4.97], 'label', [0, 0, 16, 16], ['north']))
    return {
        'texture_size': [16, 16], 'ambientocclusion': False,
        'textures': {'particle': 'farmerplus:block/strawberry_jam_fill',
                     'glass': {'sprite': 'farmerplus:block/strawberry_jam_glass', 'force_translucent': True},
                     'jam': 'farmerplus:block/strawberry_jam_fill', 'lid': 'farmerplus:block/strawberry_jam_lid',
                     'label': 'farmerplus:block/strawberry_jam_label'},
        'elements': body,
        'display': {
            'gui': {'rotation': [22, 205, 0], 'translation': [0, 2, 0], 'scale': [1.4] * 3},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 3, 0], 'scale': [.65] * 3},
            'fixed': {'rotation': [0, 180, 0], 'translation': [0, 2, 0], 'scale': [1.1] * 3},
            'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [.7] * 3},
            'thirdperson_lefthand': {'rotation': [75, 225, 0], 'translation': [0, 2.5, 0], 'scale': [.7] * 3},
            'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 2, 0], 'scale': [.9] * 3},
            'firstperson_lefthand': {'rotation': [0, 225, 0], 'translation': [0, 2, 0], 'scale': [.9] * 3},
        },
    }


def icon(level):
    image = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(image)
    d.polygon([(4, 3), (11, 3), (13, 5), (13, 12), (11, 14), (4, 14), (2, 12), (2, 5)], fill='#719d94')
    d.polygon([(4, 4), (11, 4), (12, 5), (12, 12), (10, 13), (4, 13), (3, 12), (3, 5)], fill='#b6ceae')
    d.rectangle((4, 5, 11, 11), fill='#d1ddc1')
    y = 12 - level * 2
    d.polygon([(3, y), (12, y), (12, 12), (10, 13), (4, 13), (3, 12)], fill='#a81f36')
    d.line([(4, y), (10, y)], fill='#f25d62')
    d.rectangle((3, y + 1, 4, 11), fill='#cf3448')
    d.line([(4, 13), (10, 13)], fill='#80233a')
    d.line([(3, 5), (3, 9)], fill='#e5eed5')
    d.point((11, y + 1), fill='#d95359')
    if level == 1:
        d.point((10, 7), fill='#bc3a4b')
    d.rectangle((5, 7, 10, 10), fill='#d6bc87')
    d.rectangle((5, 7, 9, 9), fill='#f8e8be')
    d.line([(7, 7), (8, 7)], fill='#557b47')
    d.rectangle((7, 8, 8, 9), fill='#d83546')
    d.point((7, 8), fill='#f26e61')
    d.polygon([(3, 1), (12, 1), (13, 2), (13, 4), (11, 4), (11, 5), (9, 4), (6, 4), (4, 5), (2, 4), (2, 2)], fill='#a52b3b')
    for yy in range(1, 4):
        for xx in range(3, 13):
            if xx // 2 % 2 == 0 and yy % 2 == 1:
                d.point((xx, yy), fill='#fff0d7')
            elif xx // 2 % 2 == 0 or yy % 2 == 1:
                d.point((xx, yy), fill='#e68686')
    d.line([(3, 4), (12, 4)], fill='#a78150')
    d.line([(3, 3), (12, 3)], fill='#e6c996')
    d.point((8, 4), fill='#f4d9a4')
    return image


def preview_icons():
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (600, 260), '#26352f')
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 21)
    for level in range(1, 4):
        image = icon(level)
        big = image.resize((160, 160), Image.Resampling.NEAREST)
        x = 20 + (level - 1) * 200
        sheet.paste(big, (x, 15), big)
        d.text((x + 52, 185), f'{level}/3', font=font, fill='#f5e5ba')
        sheet.paste(image, (x + 72, 222), image)
    sheet.save(PREVIEWS / 'strawberry-jam-icons.png')


def build():
    textures()
    for level in range(1, 4):
        name = f'strawberry_jam_{level}'
        p = ROOT / 'art/model-inputs' / f'{name}.json'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(model(level), indent=2) + '\n', encoding='utf-8')
        save(name, icon(level), 'item')
    def item_model(level):
        return {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                'cases': [{'when': ['gui'], 'model': {'type': 'minecraft:model', 'model': f'farmerplus:item/strawberry_jam_{level}'}}],
                'fallback': {'type': 'minecraft:model', 'model': f'farmerplus:block/strawberry_jam_{level}'}}
    definition = {'model': {'type': 'minecraft:select', 'property': 'minecraft:block_state', 'block_state_property': 'portions',
                            'cases': [{'when': str(level), 'model': item_model(level)} for level in range(1, 4)],
                            'fallback': item_model(3)}}
    (ASSETS / 'items/strawberry_jam.json').write_text(json.dumps(definition, indent=2) + '\n', encoding='utf-8')
    preview_icons()


if __name__ == '__main__':
    build()
