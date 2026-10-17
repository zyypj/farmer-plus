from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets'
OUT = ROOT / 'build/art/previews/trampled-wheat.png'
SCALE = 9
VIEW_YAW = math.radians(20)
VIEW_PITCH = math.radians(32)
FARMLAND = (92, 60, 36)
FARMLAND_EDGE = (70, 44, 26)
BACKGROUND = (32, 40, 36)


def load_model(identifier):
    namespace, path = identifier.split(':')
    model = json.loads((ASSETS / namespace / 'models' / f'{path}.json').read_text(encoding='utf-8'))
    if 'parent' in model and 'elements' not in model:
        parent = load_model(model['parent'])
        parent['textures'] = {**parent.get('textures', {}), **model.get('textures', {})}
        return parent
    return model


def texture(model, reference):
    while reference.startswith('#'):
        reference = model['textures'][reference[1:]]
    namespace, path = reference.split(':')
    return Image.open(ASSETS / namespace / 'textures' / f'{path}.png').convert('RGBA')


def rotation_matrix(rotation):
    if 'axis' in rotation:
        angle = math.radians(rotation['angle'])
        c, s = math.cos(angle), math.sin(angle)
        return {
            'x': np.array([[1, 0, 0], [0, c, -s], [0, s, c]]),
            'y': np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]),
            'z': np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]]),
        }[rotation['axis']]
    x, y, z = (math.radians(rotation.get(axis, 0)) for axis in ('x', 'y', 'z'))
    rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
    ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])
    return rz @ ry @ rx


def face_corners(element, face):
    (x0, y0, z0), (x1, y1, z1) = element['from'], element['to']
    return {
        'north': [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)],
        'south': [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)],
        'west': [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)],
        'east': [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)],
        'up': [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        'down': [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)],
    }[face]


def block_rotation(facing_y):
    angle = math.radians(-facing_y)
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def quads(model, offset, facing_y):
    turn = block_rotation(facing_y)
    centre = np.array([8, 0, 8])
    for element in model['elements']:
        rotation = element.get('rotation')
        matrix = rotation_matrix(rotation) if rotation else np.eye(3)
        origin = np.array(rotation['origin']) if rotation else np.zeros(3)
        for name, face in element['faces'].items():
            points = []
            for corner in face_corners(element, name):
                point = matrix @ (np.array(corner, dtype=float) - origin) + origin
                point = turn @ (point - centre) + centre
                points.append(point + offset)
            yield points, face, texture(model, face['texture'])


def project(point):
    x, y, z = point
    xr = x * math.cos(VIEW_YAW) - z * math.sin(VIEW_YAW)
    zr = x * math.sin(VIEW_YAW) + z * math.cos(VIEW_YAW)
    screen_y = -y * math.cos(VIEW_PITCH) + zr * math.sin(VIEW_PITCH)
    depth = zr * math.cos(VIEW_PITCH) + y * math.sin(VIEW_PITCH)
    return np.array([xr * SCALE, screen_y * SCALE]), depth


def homography(source, target):
    rows = []
    for (x, y), (u, v) in zip(source, target):
        rows.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        rows.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(rows, dtype=float), np.array(target, dtype=float).reshape(8))


def draw_quad(canvas, screen, face, image, origin):
    u0, v0, u1, v1 = face['uv']
    w, h = image.size
    tex = [(u0 * w / 16, v0 * h / 16), (u1 * w / 16, v0 * h / 16), (u1 * w / 16, v1 * h / 16), (u0 * w / 16, v1 * h / 16)]
    points = [tuple(p + origin) for p in screen]
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    left, top = int(math.floor(min(xs))), int(math.floor(min(ys)))
    right, bottom = int(math.ceil(max(xs))), int(math.ceil(max(ys)))
    if right - left < 1 or bottom - top < 1:
        return
    local = [(x - left, y - top) for x, y in points]
    try:
        coefficients = homography(local, tex)
    except np.linalg.LinAlgError:
        return
    patch = image.transform((right - left, bottom - top), Image.PERSPECTIVE, tuple(coefficients), Image.NEAREST)
    mask = Image.new('L', patch.size, 0)
    ImageDraw.Draw(mask).polygon(local, fill=255)
    alpha = Image.composite(patch.getchannel('A'), mask, mask)
    alpha = Image.eval(Image.merge('L', [alpha]), lambda value: 255 if value >= 128 else 0)
    canvas.paste(patch, (left, top), Image.composite(alpha, Image.new('L', patch.size, 0), mask))


def models_for(name):
    return [load_model(name), load_model(name + '_variant1')]


def render_field(model_at, size, scale, width=560, height=460):
    global SCALE
    SCALE = scale
    canvas = Image.new('RGB', (width, height), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    middle = np.array([size * 8, 0, size * 8])
    origin = np.array([width / 2, height * 0.62]) - project(middle)[0]
    for gx in range(size):
        for gz in range(size):
            corners = [np.array([gx * 16 + dx, -1, gz * 16 + dz]) for dx, dz in ((0, 0), (16, 0), (16, 16), (0, 16))]
            draw.polygon([tuple(project(c)[0] + origin) for c in corners], fill=FARMLAND, outline=FARMLAND_EDGE)
    items = []
    for gx in range(size):
        for gz in range(size):
            models = model_at(gx, gz)
            model = models[(gx * 7 + gz * 3) % len(models)]
            for points, face, image in quads(model, np.array([gx * 16, 0, gz * 16]), 0):
                projected = [project(p) for p in points]
                items.append((sum(d for _, d in projected) / 4, [s for s, _ in projected], face, image))
    for _, screen, face, image in sorted(items, key=lambda item: -item[0]):
        draw_quad(canvas, screen, face, image, origin)
    return canvas


def build():
    standing = [load_model('minecraft:block/wheat_stage7'), load_model('farmerplus:block/wheat_stage7_variant1'),
                load_model('farmerplus:block/wheat_stage7_variant2'), load_model('farmerplus:block/wheat_stage7_variant3')]
    stages = [('standing', standing)] + [(label, models_for(f'farmerplus:block/trampled_wheat_stage7_{level}'))
                                         for label, level in (('bent', 1), ('flattened', 2), ('crushed', 3))]
    sheet = Image.new('RGB', (1120, 1020), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((16, 12), 'Farmer+ trampled wheat - offline render of the shipped block models (AGE 7, falling north = away from the camera)', fill=(238, 209, 138), font=font)
    for index, (label, models) in enumerate(stages):
        tile = render_field(lambda gx, gz, m=models: m, 2, 7, 280, 300)
        sheet.paste(tile, (index * 280, 36))
        draw.text((index * 280 + 12, 44), label, fill=(230, 214, 170), font=font)
    path = {2: models_for('farmerplus:block/trampled_wheat_stage7_3')}
    edge = {1: models_for('farmerplus:block/trampled_wheat_stage7_2'), 3: models_for('farmerplus:block/trampled_wheat_stage7_1')}
    field = render_field(lambda gx, gz: path.get(gx) or edge.get(gx) or standing, 5, 6, 1120, 640)
    sheet.paste(field, (0, 360))
    draw.text((16, 370), 'A path: crushed centre, flattened and bent edges, standing field around it', fill=(230, 214, 170), font=font)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT)
    print(OUT)


if __name__ == '__main__':
    build()
