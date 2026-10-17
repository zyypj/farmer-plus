from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets'


def sprite(rows, palette):
    image = Image.new('RGBA', (16, 16))
    for y, row in enumerate(rows):
        for x, key in enumerate(row):
            if key != '.':
                image.putpixel((x, y), tuple(bytes.fromhex(palette[int(key)])) + (255,))
    return image


def flour():
    return sprite([
        '................',
        '................',
        '................',
        '................',
        '.......5........',
        '......554.......',
        '......543.......',
        '.....55433......',
        '.....544332.....',
        '....5544332.....',
        '...554443332....',
        '..55444433322...',
        '.5544444333322..',
        '..43333332221...',
        '...2211111...4..',
        '................',
    ], ['85705a', 'ad9475', 'c9b99b', 'ded1b5', 'ede3cc', 'fff1da'])


def dough():
    return sprite([
        '................',
        '................',
        '................',
        '.....34443......',
        '...345655432....',
        '..45666555432...',
        '..566655544321..',
        '.4565555444321..',
        '.45555444343221.',
        '.34554444332221.',
        '.34444443223221.',
        '..344443223321..',
        '..23443223321...',
        '...122222211....',
        '.....11111......',
        '................',
    ], ['906c45', 'ad8655', 'c3a06a', 'dab984', 'e9ce9c', 'f4dfb6', 'ffebc5'])


def porridge():
    return sprite([
        '................',
        '................',
        '................',
        '....44444444....',
        '..448888898744..',
        '.47896887888773.',
        '.38888868968873.',
        '.23788887887732.',
        '.12337777733221.',
        '..123333332211..',
        '..123222222211..',
        '...1233332210...',
        '....12222210....',
        '.....100001.....',
        '................',
        '................',
    ], ['423026', '63432e', '815a38', 'a07549', 'c39a62',
        'af8c55', 'ccad72', 'dfc48d', 'f8e7c3', 'fff0d2'])


def ear(draw, x, y, lean=0):
    p = ['806039', 'a47b3e', 'bd944d', 'd3ad5c', 'e5c577', 'f4dca0']
    draw.point((x, y), fill='#' + p[5])
    for row in range(3):
        cx = x + round(lean * row / 2)
        cy = y + row * 2 + 1
        draw.line([(cx - 1, cy), (cx, cy + 1)], fill='#' + p[4])
        draw.point((cx - 1, cy - 1), fill='#' + p[5 if row == 0 else 3])
        draw.line([(cx + 1, cy + 1), (cx, cy + 2)], fill='#' + p[2])
        draw.point((cx + 1, cy), fill='#' + p[3])


def wheat():
    image = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(image)
    d.line([(4, 14), (6, 11), (4, 8)], fill='#a47b3e')
    d.line([(5, 14), (8, 10), (9, 6)], fill='#e5c577')
    d.line([(6, 14), (10, 11), (13, 9)], fill='#bd944d')
    d.polygon([(6, 12), (3, 11), (2, 9), (5, 10)], fill='#a69b53')
    d.line([(7, 12), (11, 11)], fill='#d3ad5c')
    ear(d, 3, 3, 1)
    ear(d, 9, 0, -1)
    ear(d, 13, 4, -1)
    return image


def seeds():
    image = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(image)
    for x, y, lean in [(2, 3, -1), (10, 2, 1), (6, 7, -1), (1, 12, 1), (10, 11, -1)]:
        d.polygon([(x, y), (x + 2, y + lean - 1), (x + 4, y + lean),
                   (x + 4, y + lean + 1), (x + 2, y + 2), (x + 1, y + 1)], fill='#a18343')
        d.line([(x, y), (x + 2, y + lean - 1), (x + 3, y + lean)], fill='#ead6a0')
        d.point((x + 1, y + (lean - 1) // 2), fill='#f7e8bb')
        d.line([(x + 1, y + 1), (x + 3, y + lean + 1)], fill='#806139')
        d.point((x + 3, y + lean + 2), fill='#d2bb78')
    return image


def sheaf():
    image = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(image)
    d.polygon([(5, 9), (10, 9), (12, 14), (11, 15), (3, 15)], fill='#aa8d52')
    for bottom, top in [(3, 6), (5, 6), (7, 7), (9, 8), (11, 9), (12, 9)]:
        d.line([(bottom, 14), (top, 9)], fill='#ecd39a' if bottom % 2 else '#c3a563')
    for x, y, lean in [(2, 3, 1), (5, 1, 1), (8, 0, 0), (11, 1, -1), (14, 3, -1)]:
        d.line([(7 + lean, 10), (x + lean, y + 6)], fill='#dabb78')
        ear(d, x, y, lean)
    d.line([(5, 10), (10, 10)], fill='#67503a', width=2)
    d.line([(5, 9), (10, 9)], fill='#c7a778')
    d.line([(7, 10), (4, 8), (3, 9), (4, 11), (7, 10), (11, 8), (12, 9), (11, 11), (8, 10)], fill='#67503a')
    d.line([(4, 8), (6, 9)], fill='#dec494')
    d.line([(10, 9), (11, 8)], fill='#dec494')
    d.line([(7, 11), (5, 13)], fill='#8e6f4b')
    d.line([(8, 11), (10, 13)], fill='#8e6f4b')
    d.rectangle((7, 9, 8, 10), fill='#ae8c5e')
    d.point((7, 9), fill='#dec494')
    return image


def write(name, image, namespace='farmerplus'):
    path = ASSETS / namespace / 'textures/item' / f'{name}.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def items():
    for name, image, namespace in [
        ('flour', flour(), 'farmerplus'),
        ('dough', dough(), 'farmerplus'),
        ('wheat_porridge', porridge(), 'farmerplus'),
        ('wheat', wheat(), 'minecraft'),
        ('wheat_seeds', seeds(), 'minecraft'),
    ]:
        write(name, image, namespace)


def preview():
    names = [('flour', 'Farinha'), ('dough', 'Massa'), ('wheat_porridge', 'Mingau'),
             ('wheat_sheaf', 'Feixe'), ('wheat', 'Trigo'), ('wheat_seeds', 'Sementes'),
             ('strawberry', 'Morango')]
    sheet = Image.new('RGB', (1008, 232), '#202b29')
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 17)
    for index, (name, label) in enumerate(names):
        namespace = 'minecraft' if name in ('wheat', 'wheat_seeds') else 'farmerplus'
        image = Image.open(ASSETS / namespace / 'textures/item' / f'{name}.png').convert('RGBA')
        x = index * 144
        for yy in range(8):
            for xx in range(8):
                d.rectangle((x + 8 + xx * 16, 10 + yy * 16, x + 23 + xx * 16, 25 + yy * 16), fill='#35433e' if (xx + yy) % 2 else '#3d4c46')
        sheet.paste(image.resize((128, 128), Image.Resampling.NEAREST), (x + 8, 10), image.resize((128, 128), Image.Resampling.NEAREST))
        d.text((x + 12, 147), label, font=font, fill='#f0e5c6')
        sheet.paste(image, (x + 64, 180), image)
    d.text((12, 207), '16 × 16 · pixels nativos · ampliação sem suavização', font=font, fill='#adbaac')
    path = ROOT / 'build/art/previews/items-16.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


if __name__ == '__main__':
    items()
    write('wheat_sheaf', sheaf())
    preview()
