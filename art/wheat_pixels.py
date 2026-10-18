from PIL import Image, ImageDraw


PALETTES = [
    ['30472d', '486637', '618944', '83ac55', 'b5cf7c', '73984b'],
    ['30472d', '486637', '618944', '83ac55', 'b5cf7c', '73984b'],
    ['344c2d', '4b6d36', '6b9145', '90b35c', 'bfd183', '7c9e4d'],
    ['3b522e', '567539', '779b49', '9cb960', 'c9d58a', '88a651'],
    ['42562e', '617d3b', '85a34e', 'a7be66', 'd1da91', '92ae58'],
    ['585e33', '7d8641', 'a1a650', 'c1c373', 'e2dda0', 'a5af62'],
    ['706537', '988746', 'b8a15a', 'd4bf79', 'ecdaa0', '9eaa60'],
    ['796039', 'a08248', 'c4a45b', 'dfc17a', 'f4dda0', 'b49d60'],
]


def blank():
    return Image.new('RGBA', (16, 16))


def palette(age, variant=0):
    shift = [(0, 0, 0), (-4, 1, -3), (3, 2, 0), (1, -3, -2)][variant]
    return [tuple(max(0, min(255, c + shift[i])) for i, c in enumerate(bytes.fromhex(h))) + (255,) for h in PALETTES[age]]


def blade(draw, root, side, reach, rise, p):
    x, y = root
    shoulder = (x + side * max(1, reach - 1), y - rise)
    tip = (x + side * reach, y - max(0, rise - 1))
    draw.line([root, shoulder, tip], fill=p[2])
    if reach > 2:
        draw.line([(x + side, y - 1), shoulder], fill=p[3])
    draw.point(tip, fill=p[4])


def ear(draw, x, y, length, lean, p, awns=True):
    def axis(row):
        return x + (lean if row < 2 else 0)
    draw.line([(axis(0), y), (x, y + length)], fill=p[2])
    for row in range(1, length):
        centre = axis(row)
        left = -1 if row < length - 1 else 0
        right = 1 if row > 1 else 0
        draw.line([(centre + left, y + row), (centre + right, y + row)], fill=p[2])
        draw.point((centre + left, y + row), fill=p[4 if row % 2 else 3])
        if row > 1:
            draw.point((centre + right, y + row), fill=p[3 if row % 2 == 0 else 2])
        if row % 2 == 0:
            draw.point((centre, y + row), fill=p[1])
    draw.point((x, y + length - 1), fill=p[2])
    draw.point((axis(0), y), fill=p[4])
    if awns:
        draw.point((axis(0), y - 1), fill=p[3])
        draw.point((axis(2) - 1, y + 1), fill=p[3])
        if length > 5:
            draw.point((axis(4) + 1, y + 3), fill=p[3])


def crop(age, variant=0):
    image = blank()
    d = ImageDraw.Draw(image)
    p = palette(age, variant)
    if age >= 6:
        layouts = [
            [(2, 2, -1), (6, 1, 0), (10, 2, 0), (13, 3, 1)],
            [(2, 3, -1), (6, 2, 0), (10, 1, 1), (13, 2, 0)],
            [(2, 2, 0), (6, 3, -1), (10, 1, 0), (13, 3, 1)],
            [(2, 3, -1), (6, 1, 0), (10, 2, 1), (13, 2, 0)],
        ]
        for index, (x, y, lean) in enumerate(layouts[variant]):
            length = 7 if age == 7 else 6
            neck = y + length
            d.line([(x, 15), (x, neck)], fill=p[2])
            if index in (1, 2):
                d.line([(x, 13), (x, neck + 1)], fill=p[3 if age == 7 else 5])
            if index == 1:
                blade(d, (x, 14), -1 if variant % 2 == 0 else 1, 2, 2, p)
            ear(d, x, y, length, lean, p)
        return image
    layouts = [
        [(3, 0, -1), (8, 1, 1), (12, 0, -1)],
        [(2, 1, 1), (7, 0, -1), (13, 2, 1)],
        [(3, 1, -1), (8, 0, 1), (13, 1, -1)],
        [(2, 0, 1), (7, 2, 1), (12, 1, -1)],
    ]
    heights = [3, 5, 7, 10, 12, 14]
    for index, (root, stagger, lean) in enumerate(layouts[variant]):
        top = max(1, 16 - heights[age] + stagger)
        head = 0 if age < 4 else 3 if age == 4 else 5
        neck = min(14, top + head)
        upper = root + (lean if age >= 3 else 0)
        d.line([(root, 15), (root, max(12, neck + 1)), (upper, neck)], fill=p[2])
        d.point((root, 14), fill=p[3])
        if age <= 1:
            blade(d, (root, 15), lean, 2 + age, 2 + age, p)
            if age == 1:
                blade(d, (root, 14), -lean, 2, 2, p)
        else:
            blade(d, (root, 14), -1, 3, 2 + age // 2, p)
            blade(d, (root, 12), 1, 3, 2 + age // 2, p)
            if age == 3:
                blade(d, (upper, 10), lean, 2, 3, p)
        if head:
            ear(d, upper, top, head, lean, p, awns=age >= 5)
    return image


def layered_foliage(age, variant):
    image = blank()
    d = ImageDraw.Draw(image)
    p = palette(age, variant)
    centre = [8, 8, 7, 8, 7, 7, 6, 6, 6, 6, 7, 7, 8, 8, 8, 8]
    for y, x in enumerate(centre):
        x += 1 if variant == 3 and 4 <= y <= 10 else 0
        half = 1 if 3 <= y <= 12 else 0
        d.line([(x - half, y), (x + half, y)], fill=p[2 if age == 7 else 5])
        d.point((x - half, y), fill=p[3])
        if 6 <= y <= 9:
            d.point((x, y), fill=p[4])
    return image


def sheaf_textures():
    p = [tuple(bytes.fromhex(h)) + (255,) for h in ['8b7044', 'a78b50', 'c4a563', 'ddbf7b', 'f0d69d']]
    side = Image.new('RGBA', (16, 16), p[2])
    d = ImageDraw.Draw(side)
    for index, x in enumerate((0, 3, 5, 8, 11, 14)):
        d.line([(x, 0), (x, 15)], fill=p[1])
        d.line([(x + 1, 0), (x + 1, 15)], fill=p[3])
        y = 2 + index % 4
        d.line([(x + 1, y), (x + 1, y + 3)], fill=p[4])
    top = Image.new('RGBA', (16, 16), p[1])
    d = ImageDraw.Draw(top)
    for y in range(0, 16, 3):
        for x in range(-1 + (y % 2), 16, 3):
            d.rectangle((x, y, x + 1, y + 1), fill=p[3])
            d.point((x, y), fill=p[4])
            d.point((x + 1, y + 1), fill=p[2])
    twine = blank()
    rope = [tuple(bytes.fromhex(h)) + (255,) for h in ['806443', 'ac8b5d', 'cfb283']]
    for y in range(16):
        for x in range(16):
            twine.putpixel((x, y), rope[(x + y) % 4 // 2 if (x + y) % 4 else 2])
    stalks = side.copy()
    mask = Image.new('L', (16, 16))
    m = ImageDraw.Draw(mask)
    m.polygon([(5, 0), (10, 0), (14, 14), (13, 15), (2, 15), (1, 14)], fill=255)
    for x in (2, 5, 9, 12, 14):
        m.point((x, 15), fill=0)
    stalks.putalpha(mask)
    ears = blank()
    d = ImageDraw.Draw(ears)
    for index, (x, y, lean) in enumerate([(2, 3, -1), (5, 1, -1), (8, 1, 0), (11, 2, 0), (14, 4, 0)]):
        d.line([(6 + index, 15), (x, y + 6)], fill=p[2 if index % 2 else 3])
        ear(d, x, y, 6, lean, p)
    return {'side': side, 'top': top, 'twine': twine, 'stalks': stalks, 'bound_stalks': stalks.copy(), 'ears': ears}
