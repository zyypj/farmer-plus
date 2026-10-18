from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import math


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'common/src/main/resources/assets/farmerplus'
WOOD = ['9d7e69', 'b99a80', 'd0b297', 'e2c5a7', 'efd6b7', 'fae5c7']
BARK = ['514b43', '655d52', '776e60', '8a7f70', 'a09380', 'afa18c']
LEAF = ['203a29', '2d4d32', '3c6140', '50784b', '72965b', '91ac70']


def color(hexes):
    return ['#' + value for value in hexes]


def save(name, image, folder='block'):
    assert image.size == (16, 16) and image.mode == 'RGBA'
    image.save(ASSET / 'textures' / folder / (name + '.png'))


def bark():
    p = color(BARK)
    im = Image.new('RGBA', (16, 16), p[2])
    d = ImageDraw.Draw(im)
    for x, offsets in [(1, [0, 1, 0, -1, 0]), (5, [1, 0, 0, 1, 0]), (9, [0, -1, 0, 0, 1]), (13, [0, 1, 0, -1, 0])]:
        pts = [(x + offsets[i], i * 4) for i in range(5)]
        d.line(pts, fill=p[0])
        d.line([(xx + 1, yy) for xx, yy in pts], fill=p[3])
    for x, y, width in [(2, 3, 3), (6, 7, 3), (10, 4, 3), (12, 11, 3), (2, 12, 3), (7, 15, 2)]:
        d.line([(x, y), (x + width, y - 1)], fill=p[1])
        d.line([(x, y + 1), (x + width - 1, y)], fill=p[4])
    for xy in [(3, 1), (7, 10), (11, 7), (15, 2), (3, 8), (11, 14)]:
        d.point(xy, fill=p[3])
    return im


def endgrain(stripped=False):
    p = color(WOOD)
    im = Image.new('RGBA', (16, 16), p[2] if stripped else '#' + BARK[1])
    d = ImageDraw.Draw(im)
    inset = 0 if stripped else 2
    d.polygon([(inset + 1, inset), (14 - inset, inset), (15 - inset, inset + 2), (15 - inset, 14 - inset), (13 - inset, 15 - inset), (inset, 15 - inset), (inset, inset + 2)], fill=p[3])
    d.line([(3, 4), (5, 2), (11, 2), (13, 4), (13, 11), (11, 13), (4, 13), (2, 11), (2, 5)], fill=p[2])
    d.line([(4, 5), (6, 4), (10, 4), (11, 6), (11, 10), (9, 11), (5, 11), (4, 9), (4, 5)], fill=p[4])
    d.line([(6, 6), (9, 6), (10, 8), (9, 9), (6, 9), (6, 7)], fill=p[2])
    d.point((8, 8), fill=p[1])
    d.line([(7, 10), (9, 10)], fill=p[5])
    if not stripped:
        d.line([(0, 0), (4, 0), (5, 1)], fill='#' + BARK[3])
        d.line([(15, 7), (15, 14), (13, 15)], fill='#' + BARK[0])
        d.point((1, 9), fill='#' + BARK[4])
    return im


def stripped():
    p = color(WOOD)
    im = Image.new('RGBA', (16, 16), p[3])
    d = ImageDraw.Draw(im)
    for x, y0, y1 in [(1, 0, 6), (4, 7, 15), (7, 1, 9), (11, 0, 4), (13, 7, 14)]:
        d.line([(x, y0), (x, y1)], fill=p[2])
        d.line([(x + 1, y0 + 1), (x + 1, y1)], fill=p[4])
    d.line([(8, 11), (9, 10), (10, 11), (9, 13), (8, 12)], fill=p[2])
    d.line([(0, 2), (0, 12)], fill=p[4])
    return im


def planks():
    p = color(WOOD)
    im = Image.new('RGBA', (16, 16), p[3])
    d = ImageDraw.Draw(im)
    for row, seam in enumerate([6, 12, 3, 10]):
        y = row * 4
        d.rectangle((0, y, 15, y + 2), fill=p[3 if row % 2 == 0 else 2])
        d.line([(0, y), (15, y)], fill=p[4])
        d.line([(0, y + 3), (15, y + 3)], fill=p[1])
        d.line([(seam, y), (seam, y + 2)], fill=p[1])
        d.line([(seam + 1, y), (seam + 1, y + 1)], fill=p[5])
        d.line([(1 + row, y + 1), (4 + row, y + 1)], fill=p[4])
        d.line([(9 - row, y + 2), (13 - row, y + 2)], fill=p[2 if row % 2 == 0 else 3])
    return im


def door(top):
    p = color(WOOD)
    im = stripped()
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1, 15), fill=p[2])
    d.line([(2, 0), (2, 15)], fill=p[5])
    d.rectangle((13, 0, 15, 15), fill=p[1])
    d.line([(13, 0), (13, 15)], fill=p[4])
    for y in ([0, 12, 15] if top else [0, 13, 15]):
        d.line([(2, y), (12, y)], fill=p[1])
        if y < 15:
            d.line([(2, y + 1), (12, y + 1)], fill=p[4])
    if top:
        d.rectangle((3, 2, 12, 11), fill=p[1])
        d.rectangle((4, 3, 11, 10), fill=(0, 0, 0, 0))
        d.line([(7, 3), (7, 10)], fill=p[3])
        d.line([(4, 7), (11, 7)], fill=p[3])
        d.line([(3, 2), (12, 2)], fill=p[5])
    else:
        for x in (4, 9):
            d.rectangle((x, 3, x + 2, 11), fill=p[2])
            d.line([(x, 3), (x, 11)], fill=p[1])
            d.line([(x + 1, 4), (x + 2, 4)], fill=p[4])
        d.rectangle((11, 2, 12, 3), fill='#987647')
        d.point((11, 2), fill='#d6b36a')
    return im


def trapdoor():
    im = planks()
    d = ImageDraw.Draw(im)
    p = color(WOOD)
    d.rectangle((1, 1, 14, 14), outline=p[1])
    for x in (3, 9):
        for y in (3, 9):
            d.rectangle((x, y, x + 3, y + 3), fill=(0, 0, 0, 0))
            d.line([(x - 1, y - 1), (x + 3, y - 1)], fill=p[5])
            d.line([(x + 4, y), (x + 4, y + 4)], fill=p[1])
    d.rectangle((1, 6, 1, 9), fill='#8b795e')
    return im


def leaf(draw, cx, cy, length, width, angle, p):
    a = math.radians(angle)
    def pt(u, v):
        return (round(cx + u * math.cos(a) - v * math.sin(a)), round(cy + u * math.sin(a) + v * math.cos(a)))
    draw.polygon([pt(-length / 2, 0), pt(-length / 4, -width / 2), pt(length / 4, -width / 2), pt(length / 2, 0), pt(length / 5, width / 2), pt(-length / 4, width / 2)], fill=p[2])
    draw.polygon([pt(-length / 2 + 1, 0), pt(-length / 4, -width / 2), pt(length / 4, -width / 2), pt(length / 2 - 1, 0), pt(-length / 4, 0)], fill=p[3])
    draw.line([pt(-length / 3, 0), pt(length / 4, 0)], fill=p[4])
    draw.line([pt(-length / 5, width / 2), pt(length / 5, width / 2)], fill=p[1])
    draw.point(pt(-length / 4, -1), fill=p[5])


def leaves():
    p = color(LEAF)
    large = Image.new('RGBA', (48, 48), p[1])
    d = ImageDraw.Draw(large)
    for dx in (0, 16, 32):
        for dy in (0, 16, 32):
            d.polygon([(dx, dy + 5), (dx + 4, dy + 4), (dx + 6, dy + 8), (dx + 1, dy + 10)], fill=p[0])
            d.polygon([(dx + 8, dy + 9), (dx + 13, dy + 8), (dx + 16, dy + 12), (dx + 13, dy + 15), (dx + 9, dy + 13)], fill=p[0])
            for x, y, length, width, angle in [(1, 1, 7, 3, -30), (9, 2, 8, 4, 25), (15, 7, 7, 3, -48), (5, 7, 8, 4, -32), (2, 13, 8, 3, 35), (10, 13, 8, 4, -20)]:
                leaf(d, dx + x, dy + y, length, width, angle, p)
            for x, y in [(10, 0), (11, 0), (11, 1), (2, 3), (3, 3), (3, 4), (8, 7), (8, 8), (7, 8), (14, 6), (15, 6), (15, 7), (0, 11), (1, 11), (1, 12), (12, 10), (12, 11), (11, 11), (5, 13), (6, 13), (6, 14), (0, 7), (7, 3), (8, 3), (4, 10), (9, 15), (10, 15), (15, 13), (15, 14), (14, 14)]:
                d.point((dx + x, dy + y), fill=(0, 0, 0, 0))
    return large.crop((16, 16, 32, 32))


def sapling():
    im = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(im)
    d.line([(8, 15), (8, 5), (9, 2)], fill='#725e3c')
    d.line([(7, 15), (7, 9)], fill='#ae9768')
    for x, y in [(3, 5), (12, 6), (4, 10), (11, 11), (8, 2)]:
        d.line([(8, y + 2), (x, y)], fill='#58713c')
    p = color(LEAF)
    for x, y, length, width, angle in [(3, 5, 7, 3, 28), (12, 6, 7, 4, -30), (4, 10, 7, 4, 18), (11, 11, 7, 3, -26), (8, 2, 5, 3, -60)]:
        leaf(d, x, y, length, width, angle, p)
    return im


def flowers():
    im = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(im)
    for dx in (0, 8):
        d.line([(dx + 4, 0), (dx + 4, 9)], fill='#7d9251')
        for x, y in [(1, 4), (6, 3), (2, 8), (5, 9)]:
            d.line([(dx + 4, y - 2), (dx + x, y)], fill='#718548')
            d.line([(dx + x - 1, y), (dx + x + 1, y)], fill='#d2d28b')
            d.line([(dx + x, y - 1), (dx + x, y + 1)], fill='#b4bd71')
            d.point((dx + x, y), fill='#f0dda0')
    d.rectangle((12, 12, 15, 15), fill='#798f4d')
    d.line([(12, 12), (12, 15)], fill='#b0b56d')
    d.rectangle((0, 12, 7, 15), fill='#acb96a')
    for xy in [(1, 12), (4, 13), (6, 14), (2, 15)]:
        d.point(xy, fill='#e1d78c')
    return im


def fruit(ripe):
    p = color(['25252c', '303330', '3e4939', '526044', '69764e', '929268'] if ripe else ['315a32', '477738', '5d9143', '79a953', '9bc46c', 'bed98c'])
    im = Image.new('RGBA', (16, 16), p[2])
    d = ImageDraw.Draw(im)
    for x in range(12):
        shade = 4 if x < 3 else 3 if x < 6 else 2 if x < 9 else 1
        d.line([(x, 0), (x, 11)], fill=p[shade])
    d.rectangle((1, 1, 3, 3), fill=p[5 if not ripe else 4])
    d.line([(0, 11), (11, 11)], fill=p[0])
    if ripe:
        for x, y in [(1, 5), (3, 8), (5, 3), (6, 7), (8, 2), (9, 9), (4, 10), (10, 4), (7, 5), (2, 2), (0, 9), (10, 7)]:
            d.point((x, y), fill=p[0 if (x + y) % 2 else 3])
            d.point((x, y - 1), fill=p[4 if x < 6 else 2])
    else:
        d.line([(1, 4), (1, 7)], fill=p[4])
        d.line([(6, 2), (7, 3)], fill=p[3])
    d.rectangle((12, 0, 15, 11), fill='#586238')
    d.line([(12, 0), (12, 11)], fill='#9b9b61')
    d.line([(15, 0), (15, 11)], fill='#3f4a2e')
    d.rectangle((0, 12, 7, 15), fill=p[2])
    d.rectangle((0, 12, 2, 15), fill=p[3])
    d.line([(0, 12), (7, 12)], fill=p[4])
    d.rectangle((8, 12, 15, 15), fill=p[1])
    d.line([(8, 12), (15, 12)], fill=p[2])
    d.point((12, 15), fill=p[0])
    return im


def avocado_item():
    im = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(im)
    d.line([(8, 2), (9, 0)], fill='#99905b')
    d.point((10, 0), fill='#5e633b')
    d.polygon([(7, 2), (9, 2), (10, 5), (13, 8), (14, 11), (13, 14), (10, 15), (5, 15), (2, 13), (2, 10), (4, 7), (6, 5)], fill='#25252c')
    d.polygon([(7, 3), (8, 3), (9, 6), (12, 9), (13, 12), (11, 14), (5, 14), (3, 12), (4, 9), (6, 6)], fill='#46533c')
    d.polygon([(7, 3), (8, 4), (8, 7), (6, 10), (5, 13), (3, 11), (5, 8), (6, 6)], fill='#69764e')
    d.line([(6, 7), (5, 9)], fill='#929268')
    for x, y in [(7, 10), (10, 8), (11, 12), (8, 13), (4, 11), (9, 6)]:
        d.point((x, y), fill='#303330')
        d.point((x, y - 1), fill='#526044')
    return im


def door_item():
    im = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(im)
    p = color(WOOD)
    d.rectangle((3, 0, 12, 15), fill=p[0])
    d.rectangle((3, 0, 11, 14), fill=p[3])
    d.line([(4, 0), (10, 0)], fill=p[5])
    d.line([(3, 1), (3, 14)], fill=p[4])
    for x in (5, 9):
        for y in (2, 5):
            d.rectangle((x, y, x + 1, y + 1), fill=(0, 0, 0, 0))
        d.rectangle((x, 10, x + 1, 13), fill=p[1])
        d.line([(x, 10), (x, 12)], fill=p[2])
        d.point((x + 1, 10), fill=p[4])
    d.line([(4, 8), (10, 8)], fill=p[2])
    d.point((11, 8), fill='#856b43')
    d.point((10, 8), fill='#d9b86b')
    return im


def textures():
    for name, im in [('avocado_log', bark()), ('avocado_log_top', endgrain()), ('stripped_avocado_log', stripped()), ('stripped_avocado_log_top', endgrain(True)), ('avocado_planks', planks()), ('avocado_door_top', door(True)), ('avocado_door_bottom', door(False)), ('avocado_trapdoor', trapdoor()), ('avocado_leaves', leaves()), ('avocado_sapling', sapling()), ('avocado_flowers', flowers()), ('avocado_fruit_unripe', fruit(False)), ('avocado_fruit_ripe', fruit(True))]:
        save(name, im)
    save('avocado', avocado_item(), 'item')
    save('avocado_door', door_item(), 'item')


def cube(name, start, end, uv, rotation=None):
    value = {'name': name, 'from': start, 'to': end, 'faces': {side: {'texture': '#fruit', 'uv': uv.copy()} for side in ('north', 'south', 'east', 'west', 'up', 'down')}}
    if rotation:
        value['rotation'] = rotation
    return value


def model(stage):
    elements = []
    if stage == 'flowers':
        for index, (x, z, yaw) in enumerate([(4.5, 5, 20), (11, 10, -25)]):
            elements.append(cube(f'panicle_{index}_stem', [x - .13, -1.5, z - .13], [x + .13, 0, z + .13], [12, 12, 14, 16]))
            for turn in (0, 90):
                card = cube(f'panicle_{index}_flowers_{turn}', [x - 1.7, -3.3, z], [x + 1.7, -.8, z], [index * 8, 0, index * 8 + 8, 12], {'origin': [x, -1.5, z], 'axis': 'y', 'angle': yaw + turn})
                card['faces'] = {side: card['faces'][side] for side in ('north', 'south')}
                elements.append(card)
            elements.append(cube(f'panicle_{index}_florets', [x - .4, -2.45, z - .4], [x + .4, -1.9, z + .4], [0, 12, 8, 16]))
        texture = 'avocado_flowers'
    else:
        ripe = stage == 'ripe'
        x, z, length, scale = (8.5, 8, .9, 1 if ripe else .78)
        width_scale, height_scale = scale * 1.65, scale * 1.30
        elements.append(cube('fruit_0_stalk', [x - .23, -length - .08, z - .23], [x + .23, 0, z + .23], [12, 0, 14, 8]))
        rotation = {'origin': [x, -length, z], 'x': 0, 'y': -12, 'z': 5}
        for part, width, low, high, uv in [
            ('neck', .42, -.9, .02, [0, 12, 8, 16]),
            ('upper_shoulders', .68, -1.5, -.86, [0, 0, 12, 12]),
            ('lower_shoulders', 1.05, -2.15, -1.46, [0, 0, 12, 12]),
            ('upper_belly', 1.42, -2.95, -2.11, [0, 0, 12, 12]),
            ('full_belly', 1.62, -3.95, -2.91, [0, 0, 12, 12]),
            ('lower_belly', 1.36, -4.65, -3.91, [0, 0, 12, 12]),
            ('rounded_base', .9, -5.1, -4.61, [8, 12, 16, 16]),
        ]:
            section = cube('fruit_0_' + part, [x - width * width_scale, -length + low * height_scale, z - width * width_scale], [x + width * width_scale, -length + high * height_scale, z + width * width_scale], uv, rotation)
            if part not in ('neck', 'rounded_base'):
                for side in ('north', 'south', 'east', 'west'):
                    section['faces'][side]['uv'] = [0, max(0, -high / 5.1 * 12), 12, min(12, -low / 5.1 * 12)]
                section['faces']['up']['uv'] = [1, 1, 9, 4]
            elements.append(section)
        texture = 'avocado_fruit_' + stage
    return {'texture_size': [16, 16], 'ambientocclusion': False, 'textures': {'particle': 'farmerplus:block/' + texture, 'fruit': 'farmerplus:block/' + texture}, 'elements': elements}


def preview():
    names = ['avocado_log', 'avocado_log_top', 'stripped_avocado_log', 'stripped_avocado_log_top', 'avocado_planks', 'avocado_door_top', 'avocado_door_bottom', 'avocado_trapdoor', 'avocado_leaves', 'avocado_sapling', 'avocado_flowers', 'avocado_fruit_unripe', 'avocado_fruit_ripe', 'avocado', 'avocado_door']
    sheet = Image.new('RGB', (1000, 600), '#24312c')
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14)
    for index, name in enumerate(names):
        folder = 'item' if index >= 13 else 'block'
        image = Image.open(ASSET / 'textures' / folder / (name + '.png')).convert('RGBA')
        x, y = index % 5 * 200 + 20, index // 5 * 200 + 12
        for row in range(8):
            for col in range(8):
                d.rectangle((x + col * 18, y + row * 18, x + col * 18 + 17, y + row * 18 + 17), fill='#35463b' if (row + col) % 2 else '#425348')
        image = image.resize((144, 144), Image.Resampling.NEAREST)
        sheet.paste(image, (x, y), image)
        d.text((x - 5, y + 151), name.replace('avocado_', '').replace('stripped_', 'stripped '), font=font, fill='#f3dfbd')
    path = ROOT / 'build/art/previews/avocado-textures.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def build():
    textures()
    for stage in ('flowers', 'unripe', 'ripe'):
        name = 'avocado_leaves_' + stage
        path = ROOT / 'art/model-inputs' / (name + '.json')
        path.write_text(json.dumps(model(stage), indent=2) + '\n', encoding='utf-8')
    preview()


if __name__ == '__main__':
    build()
