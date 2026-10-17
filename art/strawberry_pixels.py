from pathlib import Path
from PIL import Image, ImageDraw

ASSET = Path(__file__).resolve().parents[1] / 'common/src/main/resources/assets/farmerplus'


def save(name, image, item=False):
    assert image.size == (16, 16)
    image.save(ASSET / 'textures' / ('item' if item else 'block') / (name + '.png'))


def leaf(kind):
    palettes = {
        'mature': ['254b2b', '356c37', '488644', '69a854', '91bf68'],
        'young': ['396b36', '50863e', '6ba54d', '8dc364', 'b2d786'],
        'aged': ['465733', '617340', '7c8b46', '9da455', 'b9bc6e'],
        'under': ['476744', '5b8050', '73965c', '8caa70', 'a6bd87']
    }
    p = ['#' + c for c in palettes[kind]]
    image = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(image)
    d.line([(8, 15), (8, 7)], fill=p[2], width=1)
    d.line([(8, 12), (4, 10)], fill=p[2], width=1)
    d.line([(8, 12), (12, 10)], fill=p[2], width=1)
    middle = [(8, 0), (10, 1), (10, 2), (11, 3), (10, 4), (11, 5), (10, 6), (10, 7), (8, 9), (6, 8), (6, 7), (5, 6), (6, 5), (5, 4), (6, 3), (6, 2)]
    left = [(1, 5), (3, 5), (4, 4), (5, 6), (6, 6), (6, 8), (7, 9), (5, 11), (4, 12), (3, 11), (1, 11), (1, 9), (0, 8), (1, 7)]
    for shape in [left, [(15 - x, y) for x, y in left], middle]:
        d.polygon(shape, fill=p[1])
    d.polygon([(8, 1), (7, 3), (6, 5), (7, 7), (8, 8), (9, 6), (9, 2)], fill=p[2])
    d.line([(8, 2), (8, 8)], fill=p[4], width=1)
    d.line([(8, 5), (6, 3)], fill=p[3], width=1)
    d.line([(8, 7), (10, 5)], fill=p[0], width=1)
    for mirrored in [False, True]:
        def pt(x, y):
            return (15 - x, y) if mirrored else (x, y)
        d.polygon([pt(x, y) for x, y in [(2, 6), (4, 6), (5, 8), (5, 10), (3, 10), (2, 8)]], fill=p[2])
        d.line([pt(2, 6), pt(5, 10)], fill=p[3], width=1)
        d.point(pt(2, 9), fill=p[0])
    return image


def fruit_palette(red, green):
    image = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(image)
    for ox, palette in [(0, red), (8, green)]:
        p = ['#' + c for c in palette]
        d.rectangle((ox, 0, ox + 7, 7), fill=p[2])
        d.polygon([(ox, 0), (ox + 4, 0), (ox + 3, 4), (ox, 5)], fill=p[3])
        d.polygon([(ox + 6, 0), (ox + 7, 1), (ox + 7, 7), (ox + 3, 7), (ox + 5, 5)], fill=p[1])
        d.line([(ox + 7, 4), (ox + 7, 7), (ox + 5, 7)], fill=p[0], width=1)
        d.line([(ox + 1, 1), (ox + 2, 1)], fill=p[4], width=1)
        for x, y in [(2, 3), (5, 2), (5, 5), (1, 6)]:
            d.point((ox + x, y), fill='#f0ce70' if ox == 0 else '#d6cb87')
        d.rectangle((ox, 8, ox + 7, 15), fill=p[2])
        d.polygon([(ox + 4, 8), (ox + 5, 10), (ox + 7, 10), (ox + 5, 12), (ox + 6, 15), (ox + 4, 13), (ox + 1, 15), (ox + 2, 12), (ox, 10), (ox + 3, 10)], fill='#355f32')
        d.line([(ox + 4, 9), (ox + 4, 12), (ox + 2, 13)], fill='#8eb454', width=1)
        d.point((ox + 5, 11), fill='#66963d')
        for x, y in [(0, 0), (7, 0), (0, 8), (7, 8), (0, 15), (7, 15)]:
            d.point((ox + x, y), fill=(0, 0, 0, 0))
    return image


def textures():
    for suffix, kind in [('', 'mature'), ('_young', 'young'), ('_aged', 'aged'), ('_under', 'under')]:
        save('strawberry_leaf' + suffix, leaf(kind))
    flower = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(flower)
    petals = [([(7, 5), (6, 3), (7, 1), (9, 1), (10, 3), (9, 5)]), ([(9, 4), (12, 3), (14, 4), (13, 6), (10, 7)]), ([(9, 7), (12, 7), (12, 10), (10, 11), (8, 8)]), ([(7, 7), (7, 10), (5, 11), (3, 9), (4, 7)]), ([(6, 4), (4, 3), (2, 4), (2, 6), (5, 7)])]
    for petal in petals:
        d.polygon(petal, fill='#e1e5cf')
    for x, y in [(7, 2), (8, 2), (12, 4), (10, 9), (5, 9), (3, 4)]:
        d.point((x, y), fill='#fff9e4')
    d.rectangle((6, 5, 9, 7), fill='#c4a441')
    d.rectangle((7, 5, 8, 6), fill='#f2da73')
    d.line([(1, 15), (2, 13), (4, 14)], fill='#65863c', width=1)
    d.line([(1, 13), (4, 13)], fill='#f5efd8', width=1)
    save('strawberry_flower', flower)
    for suffix, red, green in [
        ('', ['6e252f', 'a72c38', 'ce3b42', 'ec5152', 'fa9c87'], ['658244', '91a35c', 'bdc382', 'dfd8ad', 'fff1dc']),
        ('_rose', ['8b3039', 'bd3f45', 'e05257', 'f16d68', 'ffb69a'], ['8a945f', 'b0b78a', 'd1d1b0', 'e5dfc8', 'fff5e4']),
        ('_deep', ['59232f', '8e2939', 'b32e40', 'd9414f', 'ffab92'], ['50723e', '7a9851', 'a6b771', 'c8ce96', 'f3ebce'])
    ]:
        save('strawberry_fruit' + suffix, fruit_palette(red, green))
    stem = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(stem)
    d.line([(0, 0), (0, 15)], fill='#6d9749', width=1)
    d.polygon([(11, 8), (13, 10), (15, 10), (14, 12), (15, 14), (13, 14), (12, 15), (10, 14), (8, 14), (9, 12), (8, 10), (10, 10)], fill='#49703a')
    d.polygon([(11, 10), (13, 11), (13, 13), (11, 14), (10, 12)], fill='#78964b')
    d.point((11, 12), fill='#826c41')
    save('strawberry_stem', stem)
    peduncle = Image.new('RGBA', (16, 16))
    ImageDraw.Draw(peduncle).line([(0, 15), (3, 10), (7, 3), (12, 5), (15, 8)], fill='#6b994b', width=1)
    save('strawberry_peduncle', peduncle)
    paired = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(paired)
    for points in [[(8, 15), (5, 9), (3, 5), (1, 6), (0, 8)], [(8, 15), (10, 9), (12, 5), (14, 6), (15, 8)]]:
        d.line(points, fill='#608c45', width=1)
    save('strawberry_peduncle_pair', paired)
    item = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(item)
    d.polygon([(3, 4), (6, 3), (8, 4), (11, 3), (14, 5), (14, 8), (12, 11), (8, 15), (6, 14), (3, 10), (1, 7), (1, 5)], fill='#7c2533')
    d.polygon([(3, 5), (6, 4), (8, 5), (11, 4), (13, 6), (13, 8), (10, 12), (8, 14), (6, 12), (3, 9), (2, 6)], fill='#ce3544')
    d.polygon([(4, 5), (7, 5), (9, 6), (10, 8), (7, 12), (4, 9), (3, 7)], fill='#ec5152')
    d.line([(4, 6), (6, 5)], fill='#ffac91', width=1)
    for x, y in [(3, 8), (6, 10), (9, 7), (11, 9), (8, 13)]:
        d.point((x, y), fill='#f5d57b')
    d.polygon([(3, 3), (6, 3), (6, 1), (8, 3), (11, 1), (10, 3), (14, 4), (11, 5), (12, 6), (8, 5), (6, 7), (6, 5), (2, 5)], fill='#305d32')
    d.line([(5, 4), (8, 4), (10, 2)], fill='#88b953', width=1)
    d.line([(8, 3), (8, 1), (9, 0)], fill='#668b3c', width=1)
    save('strawberry', item, item=True)
