from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from avocado_pixels import WOOD, color, planks, stripped, save


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets'


def icon(kind):
    p = color(WOOD)
    im = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(im)
    if kind in ('sign', 'hanging_sign'):
        if kind == 'sign':
            d.rectangle((7, 10, 8, 15), fill=p[1])
            d.line([(7, 10), (7, 15)], fill=p[4])
        else:
            for x in (4, 11):
                d.line([(x, 1), (x, 6)], fill='#797b70')
                d.point((x - 1, 2), fill='#b8b8a2')
                d.point((x + 1, 4), fill='#b8b8a2')
        d.rectangle((1, 5, 14, 11), fill=p[1])
        d.rectangle((1, 5, 13, 10), fill=p[3])
        d.line([(2, 5), (12, 5)], fill=p[5])
        d.line([(3, 8), (9, 8)], fill=p[2])
    else:
        d.polygon([(1, 9), (4, 7), (12, 7), (15, 9), (12, 13), (4, 13)], fill=p[0])
        d.polygon([(2, 9), (5, 8), (11, 8), (14, 9), (11, 11), (5, 11)], fill=p[4])
        d.line([(4, 12), (11, 12)], fill=p[2])
        d.line([(1, 6), (7, 12)], fill=p[1])
        d.line([(9, 8), (14, 3)], fill=p[1])
        d.line([(1, 5), (2, 6)], fill=p[4], width=2)
        d.line([(14, 2), (15, 3)], fill=p[4], width=2)
        if kind == 'chest_boat':
            d.rectangle((6, 4, 11, 9), fill='#805b39')
            d.rectangle((6, 4, 10, 7), fill='#c4985a')
            d.line([(6, 7), (11, 7)], fill='#654b32')
            d.point((9, 7), fill='#e6c77d')
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
    for kind in ('sign', 'hanging_sign', 'boat', 'chest_boat'):
        save('avocado_' + kind, icon(kind), 'item')
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
    hanging = icon('hanging_sign')
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
    build()
