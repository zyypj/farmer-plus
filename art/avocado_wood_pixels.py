from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from avocado_pixels import WOOD, color, planks, stripped, save, door_item
import argparse


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets'


def icon(kind):
    p = color(WOOD)
    im = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(im)
    if kind in ('sign', 'hanging_sign'):
        suspended = kind == 'hanging_sign'
        top, bottom = (6, 14) if suspended else (2, 10)
        if suspended:
            d.rectangle((0, 0, 15, 1), fill=p[1])
            d.line([(1, 0), (14, 0)], fill=p[4])
            for x in (3, 12):
                d.line([(x, 2), (x, 6)], fill='#686c65')
                d.point((x, 2), fill='#c5c4ac')
                d.point((x - 1, 4), fill='#b0b2a0')
                d.point((x, 5), fill='#969c8a')
        else:
            d.rectangle((7, 10, 8, 15), fill=p[0])
            d.line([(7, 11), (7, 15)], fill=p[2])
            d.point((7, 12), fill=p[4])
        d.rectangle((1, top, 14, bottom), fill=p[0])
        d.rectangle((1, top, 13, bottom - 1), fill=p[3])
        d.line([(2, top), (12, top)], fill=p[5])
        d.line([(1, top + 1), (1, bottom - 1)], fill=p[4])
        for y in (top + 3, top + 6):
            d.line([(2, y), (12, y)], fill=p[2])
        d.line([(3, top + 2), (5, top + 2)], fill=p[1])
        d.line([(9, top + 5), (11, top + 5)], fill=p[4])
        d.point((6, top + 7), fill=p[2])
    else:
        d.polygon([(5, 1), (7, 1), (8, 3), (6, 4), (4, 3)], fill=p[0])
        d.line([(5, 2), (6, 3)], fill=p[3])
        d.line([(6, 3), (8, 7)], fill=p[1])
        d.polygon([(2, 5), (5, 3), (9, 4), (12, 6), (12, 10), (9, 13), (5, 12), (2, 10), (1, 7)], fill=p[0])
        d.polygon([(1, 7), (3, 8), (5, 10), (9, 11), (12, 9), (11, 11), (9, 12), (5, 11), (2, 9)], fill=p[2])
        d.polygon([(2, 5), (5, 3), (9, 4), (12, 6), (11, 8), (8, 10), (5, 9), (2, 7)], fill=p[4])
        d.polygon([(3, 5), (5, 4), (8, 5), (10, 6), (10, 8), (8, 9), (5, 8), (3, 7)], fill=p[0])
        d.polygon([(4, 6), (6, 5), (9, 6), (9, 8), (7, 8), (5, 7)], fill=p[2])
        d.line([(3, 5), (5, 4), (8, 5), (10, 6)], fill=p[5])
        d.line([(2, 7), (5, 9), (8, 10), (11, 8)], fill=p[3])
        d.line([(3, 10), (5, 11), (8, 12)], fill=p[1])
        if kind == 'chest_boat':
            d.polygon([(5, 5), (8, 3), (11, 5), (11, 8), (8, 10), (5, 8)], fill='#65472e')
            d.polygon([(5, 5), (8, 3), (10, 4), (7, 6)], fill='#cc9f5b')
            d.polygon([(5, 6), (7, 7), (7, 9), (5, 8)], fill='#9a703d')
            d.polygon([(8, 7), (10, 5), (10, 8), (8, 9)], fill='#b88948')
            d.line([(5, 6), (7, 7), (10, 5)], fill='#65472e')
            d.line([(8, 7), (8, 8)], fill='#ecd094')
        d.line([(8, 8), (12, 11)], fill=p[0])
        d.line([(8, 7), (12, 10)], fill=p[3])
        d.polygon([(12, 10), (14, 11), (14, 13), (12, 13), (10, 11)], fill=p[0])
        d.line([(12, 11), (13, 12)], fill=p[4], width=2)
    return im


def native_layout(size, chest=False):
    im = Image.new('RGBA', size)
    tile = planks()
    for y in range(0, size[1], 16):
        for x in range(0, size[0], 16):
            im.paste(tile, (x, y))
    d = ImageDraw.Draw(im)
    p = color(WOOD)
    for y in [0, 18, 19, 26, 27, 34, 35, 42, 43, 50]:
        d.line([(0, y), (59, y)], fill=p[1])
        d.line([(0, y + 1), (59, y + 1)], fill=p[4])
    if chest:
        d.rectangle((0, 59, 47, 95), fill=p[2])
        for y in [59, 70, 74, 76, 87, 95]:
            d.line([(0, y), (47, y)], fill=p[0])
            if y < 95:
                d.line([(1, y + 1), (46, y + 1)], fill=p[4])
        for x in [0, 11, 23, 35, 47]:
            d.line([(x, 59), (x, 95)], fill=p[1])
        d.rectangle((0, 59, 5, 64), fill='#b99b63')
        d.line([(1, 60), (3, 60)], fill='#ecd296')
        d.point((2, 63), fill='#78643f')
    return im


def hanging_screen():
    p = color(WOOD)
    im = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(im)
    for x in (4, 11):
        d.line([(x, 1), (x, 6)], fill='#797b70')
        d.point((x - 1, 2), fill='#b8b8a2')
        d.point((x + 1, 4), fill='#b8b8a2')
    d.rectangle((1, 5, 14, 11), fill=p[1])
    d.rectangle((1, 5, 13, 10), fill=p[3])
    d.line([(2, 5), (12, 5)], fill=p[5])
    d.line([(3, 8), (9, 8)], fill=p[2])
    return im


def item_icons():
    for kind in ('sign', 'hanging_sign', 'boat', 'chest_boat'):
        save('avocado_' + kind, icon(kind), 'item')
    save('avocado_door', door_item(), 'item')
    names = [('boat', 'Barco'), ('chest_boat', 'Barco com baú'), ('sign', 'Placa'), ('hanging_sign', 'Placa suspensa'), ('door', 'Porta')]
    sheet = Image.new('RGB', (900, 280), '#25362e')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 17)
    for index, (name, label) in enumerate(names):
        image = icon(name) if name != 'door' else door_item()
        big = image.resize((144, 144), Image.Resampling.NEAREST)
        x = index * 180 + 18
        for y in range(8):
            for col in range(8):
                draw.rectangle((x + col * 18, 16 + y * 18, x + col * 18 + 17, 33 + y * 18), fill='#3b4c41' if (col + y) % 2 else '#46574b')
        sheet.paste(big, (x, 16), big)
        draw.text((x, 175), label, font=font, fill='#edddbd')
        sheet.paste(image, (x + 64, 211), image)
    draw.text((18, 246), '16 × 16 · madeira de abacateiro · pixels nativos', font=font, fill='#b9c6ad')
    path = ROOT / 'build/art/previews/avocado-items-refined.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def build():
    save('avocado_sign', planks())
    hanging = stripped()
    d = ImageDraw.Draw(hanging)
    d.rectangle((10, 0, 15, 6), fill=(0, 0, 0, 0))
    for x, y in [(11, 3), (14, 4)]:
        d.rectangle((x, y, x + 1, y + 2), outline='#a5a696')
        d.point((x, y), fill='#d1ceba')
    save('avocado_hanging_sign', hanging)
    shelf = planks()
    d = ImageDraw.Draw(shelf)
    d.rectangle((8, 0, 15, 7), fill='#b99a80')
    d.line([(8, 0), (15, 0)], fill='#efd6b7')
    d.line([(8, 7), (15, 7)], fill='#9d7e69')
    save('avocado_shelf', shelf)
    item_icons()
    for kind, size in [('boat', (128, 64)), ('chest_boat', (128, 128))]:
        native_layout(size, kind == 'chest_boat').save(ASSETS / 'farmerplus/textures/entity' / kind / 'avocado.png')
    p = color(WOOD)
    sign = Image.new('RGBA', (24, 26))
    d = ImageDraw.Draw(sign)
    d.rectangle((0, 0, 23, 13), fill=p[3])
    d.line([(0, 0), (23, 0)], fill=p[5])
    for y in (6, 13):
        d.line([(0, y), (23, y)], fill=p[1])
    d.line([(2, 3), (10, 3)], fill=p[4])
    d.line([(13, 10), (21, 10)], fill=p[2])
    d.rectangle((10, 14, 13, 25), fill=p[2])
    d.line([(10, 14), (10, 25)], fill=p[4])
    sign.save(ASSETS / 'minecraft/textures/gui/signs/farmerplus/avocado.png')
    hanging = hanging_screen()
    hanging.save(ASSETS / 'minecraft/textures/gui/hanging_signs/farmerplus/avocado.png')
    paths = [ASSETS / 'farmerplus/textures/block' / f'avocado_{name}.png' for name in ('sign', 'hanging_sign', 'shelf')]
    paths += [ASSETS / 'farmerplus/textures/item' / f'avocado_{name}.png' for name in ('sign', 'hanging_sign', 'boat', 'chest_boat')]
    paths += [ASSETS / 'farmerplus/textures/entity' / name / 'avocado.png' for name in ('boat', 'chest_boat')]
    paths += [ASSETS / 'minecraft/textures/gui' / name / 'farmerplus/avocado.png' for name in ('signs', 'hanging_signs')]
    sheet = Image.new('RGB', (800, 600), '#24312c')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14)
    for index, path in enumerate(paths):
        image = Image.open(path).convert('RGBA')
        x, y = index % 4 * 200 + 20, index // 4 * 200 + 10
        draw.rectangle((x, y, x + 143, y + 143), fill='#425348')
        ratio = min(144 / image.width, 144 / image.height)
        image = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.NEAREST)
        sheet.paste(image, (x, y), image)
        parts = path.relative_to(ASSETS).parts
        label = path.parent.name + ': ' + path.stem.replace('avocado_', '')
        if 'entity' in parts:
            label = path.parent.name + ' atlas'
        elif 'gui' in parts:
            label = parts[3] + ' screen'
        draw.text((x - 4, y + 148), label, font=font, fill='#f3dfbd')
    sheet.save(ROOT / 'build/art/previews/avocado-wood-extras.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--items-only', action='store_true')
    args = parser.parse_args()
    item_icons() if args.items_only else build()
