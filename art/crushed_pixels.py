from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TEXTURES = ROOT / 'common/src/main/resources/assets/farmerplus/textures/block'
PALETTES = {
    2: ['2e4c30', '446839', '618447', '8ca55c', 'b6bd78'],
    3: ['344f31', '4b6b3d', '6d884b', '98a966', 'bec58a'],
    4: ['405335', '5d7141', '809351', 'a8af70', 'c9c58c'],
    5: ['56603a', '7b8049', 'a2a064', 'bcbc83', 'd5cea0'],
    6: ['6a6c48', '85855c', '9d9d70', 'b3b081', 'cac69a'],
    7: ['7d7557', '948b69', 'aaa17c', 'bdb490', 'cfc6a5'],
}


def crushed(age, alternate=False):
    p = ['#' + h for h in PALETTES[age]]
    im = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(im)
    paths = [[(3, 15), (3, 13), (5, 11), (3, 8), (5, 6), (3, 4)],
             [(8, 15), (8, 13), (6, 10), (9, 8), (8, 6), (10, 3)],
             [(12, 15), (12, 14), (10, 12), (12, 9), (10, 7), (13, 5)]]
    if alternate:
        paths = [[(2, 15), (3, 13), (1, 11), (4, 9), (3, 6), (5, 3)],
                 [(7, 15), (7, 13), (9, 11), (7, 9), (10, 7), (9, 4)],
                 [(13, 15), (12, 13), (14, 10), (11, 8), (13, 6), (12, 2)]]
    for index, points in enumerate(paths):
        keep = min(6, age + 2)
        points = points[:keep]
        d.line(points, fill=p[1], width=1)
        d.line(points[:2], fill=p[3], width=1)
        d.line(points[3:5], fill=p[2], width=1)
        x, y = points[2]
        d.point((x, y), fill=p[0])
        d.line([(x - 1, y), (x - 2, y - 1)], fill=p[4])
        if age < 5:
            x, y = points[-2]
            direction = -1 if (index + alternate) % 2 else 1
            d.polygon([(x, y + 1), (x + direction * 3, y - 1), (x + direction * 2, y + 1)], fill=p[2])
            d.point((x + direction * 3, y - 1), fill=(0, 0, 0, 0))
        else:
            x, y = points[-1]
            for dx, dy in [(-1, 0), (1, 1), (0, 2)]:
                d.line([(x + dx, y + dy), (x + dx + 1, y + dy)], fill=p[3 if dx < 1 else 2])
            d.point((x, y + 1), fill=p[0])
            d.point((x - 2, y + 2), fill=p[4])
        bx, by = points[0]
        d.point((bx, by - 1), fill=p[4])
    d.line([(5, 12), (7, 11)], fill=p[2])
    if age >= 6:
        for xy in ([(1, 3), (7, 2), (14, 7)] if not alternate else [(1, 7), (6, 4), (14, 1)]):
            d.point(xy, fill=p[3])
    return im


def build():
    sheet = Image.new('RGB', (1008, 420), '#28392e')
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
    for age in range(2, 8):
        for alternate in (False, True):
            name = f'wheat_stage{age}' + ('_alternate' if alternate else '') + '_crushed'
            im = crushed(age, alternate)
            im.save(TEXTURES / (name + '.png'))
            x, y = (age - 2) * 168 + 12, int(alternate) * 200 + 30
            d.rectangle((x, y, x + 143, y + 143), fill='#61492f')
            big = im.resize((144, 144), Image.Resampling.NEAREST)
            sheet.paste(big, (x, y), big)
            d.text((x + 30, y + 151), f'AGE {age}', font=font, fill='#e4d6af')
    path = ROOT / 'build/art/previews/crushed-wheat-textures.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


if __name__ == '__main__':
    build()
