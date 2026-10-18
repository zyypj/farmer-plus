import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

from preview_world_trees import DEFAULT_WORLD, read_chunk

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets'
BACKGROUND = (196, 214, 226, 255)
SOLID = {'minecraft:grass_block': (96, 140, 70), 'minecraft:dirt': (121, 85, 58), 'minecraft:coarse_dirt': (110, 80, 55)}
DEFAULTS = {
    'farmerplus:banana_stem': {'segment': 'middle', 'fruited': 'false'},
    'farmerplus:banana_leaf': {'direction': 'north', 'segment': '0'},
    'farmerplus:banana_bunch': {'facing': 'north', 'stage': '0'},
}
SHADE = {'up': 1.0, 'down': 0.55, 'north': 0.8, 'south': 0.8, 'east': 0.65, 'west': 0.65}


def palette_entry(entry):
    if isinstance(entry, dict):
        name = str(entry.get('id', entry.get('Name', entry.get('', ''))))
        properties = entry.get('properties', entry.get('Properties', {}))
        return name, {str(k): str(v) for k, v in dict(properties).items()}
    return str(entry), {}


def collect(world, box):
    min_x, max_x, min_z, max_z, min_y, max_y = box
    blocks = {}
    region_dir = world / 'dimensions/minecraft/overworld/region'
    for chunk_x in range(min_x >> 4, (max_x >> 4) + 1):
        for chunk_z in range(min_z >> 4, (max_z >> 4) + 1):
            path = region_dir / f'r.{chunk_x >> 5}.{chunk_z >> 5}.mca'
            chunk = read_chunk(path.read_bytes(), chunk_x, chunk_z) if path.exists() else None
            if chunk is None:
                continue
            for section in chunk['sections']:
                states = section.get('block_states')
                section_y = int(section['Y'])
                if states is None or section_y * 16 + 15 < min_y or section_y * 16 > max_y:
                    continue
                palette = [palette_entry(entry) for entry in states['palette']]
                bits = max(4, math.ceil(math.log2(len(palette)))) if len(palette) > 1 else 0
                data = [int(v) & 0xFFFFFFFFFFFFFFFF for v in states['data']] if bits else []
                for i in range(4096):
                    if bits:
                        per_long = 64 // bits
                        index = (data[i // per_long] >> ((i % per_long) * bits)) & ((1 << bits) - 1)
                    else:
                        index = 0
                    name, properties = palette[index]
                    if name == 'minecraft:air':
                        continue
                    x, z, y = chunk_x * 16 + (i & 15), chunk_z * 16 + ((i >> 4) & 15), section_y * 16 + (i >> 8)
                    if min_x <= x <= max_x and min_z <= z <= max_z and min_y <= y <= max_y:
                        blocks[(x, y, z)] = (name, dict(DEFAULTS.get(name, {}), **properties))
    return blocks


class Models:
    def __init__(self):
        self.cache = {}
        self.textures = {}

    def load(self, identifier):
        if identifier not in self.cache:
            namespace, path = identifier.split(':') if ':' in identifier else ('minecraft', identifier)
            file = ASSETS / namespace / 'models' / (path + '.json')
            data = json.loads(file.read_text(encoding='utf-8')) if file.exists() else {}
            if 'parent' in data and data['parent'].endswith('block/cross'):
                cross = data['textures']['cross']
                data = {'textures': {'cross': cross}, 'elements': [
                    {'from': [0.8, 0, 8], 'to': [15.2, 16, 8], 'rotation': {'origin': [8, 8, 8], 'axis': 'y', 'angle': 45},
                     'faces': {'north': {'uv': [0, 0, 16, 16], 'texture': '#cross'}, 'south': {'uv': [0, 0, 16, 16], 'texture': '#cross'}}},
                    {'from': [8, 0, 0.8], 'to': [8, 16, 15.2], 'rotation': {'origin': [8, 8, 8], 'axis': 'y', 'angle': 45},
                     'faces': {'west': {'uv': [0, 0, 16, 16], 'texture': '#cross'}, 'east': {'uv': [0, 0, 16, 16], 'texture': '#cross'}}}]}
            self.cache[identifier] = data
        return self.cache[identifier]

    def texture(self, identifier):
        if identifier not in self.textures:
            namespace, path = identifier.split(':') if ':' in identifier else ('minecraft', identifier)
            file = ASSETS / namespace / 'textures' / (path + '.png')
            self.textures[identifier] = Image.open(file).convert('RGBA') if file.exists() else None
        return self.textures[identifier]


def variant_for(blockstate, properties):
    for key, value in blockstate.get('variants', {}).items():
        wanted = dict(part.split('=') for part in key.split(',') if part)
        if all(properties.get(k) == v for k, v in wanted.items()):
            return value[0] if isinstance(value, list) else value
    return None


def variants_for(blockstate, properties):
    if 'variants' in blockstate:
        variant = variant_for(blockstate, properties)
        return [variant] if variant else []

    def matches(condition):
        if 'OR' in condition:
            return any(matches(part) for part in condition['OR'])
        if 'AND' in condition:
            return all(matches(part) for part in condition['AND'])
        return all(properties.get(key) in str(value).split('|') for key, value in condition.items())

    result = []
    for part in blockstate.get('multipart', []):
        if matches(part.get('when', {})):
            applied = part['apply']
            result.append(applied[0] if isinstance(applied, list) else applied)
    return result


def rotation_matrix(rotation):
    if not rotation:
        return None
    if 'axis' in rotation:
        angles = {'x': 0, 'y': 0, 'z': 0}
        angles[rotation['axis']] = rotation.get('angle', 0)
    else:
        angles = {axis: rotation.get(axis, 0) for axis in 'xyz'}
    ax, ay, az = (math.radians(angles[a]) for a in 'xyz')
    rx = [[1, 0, 0], [0, math.cos(ax), -math.sin(ax)], [0, math.sin(ax), math.cos(ax)]]
    ry = [[math.cos(ay), 0, math.sin(ay)], [0, 1, 0], [-math.sin(ay), 0, math.cos(ay)]]
    rz = [[math.cos(az), -math.sin(az), 0], [math.sin(az), math.cos(az), 0], [0, 0, 1]]
    return multiply(rz, multiply(ry, rx))


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def apply(matrix, point, origin):
    p = [point[i] - origin[i] for i in range(3)]
    return [sum(matrix[i][k] * p[k] for k in range(3)) + origin[i] for i in range(3)]


def face_corners(direction, start, end):
    x0, y0, z0 = start
    x1, y1, z1 = end
    return {
        'up': [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        'down': [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)],
        'north': [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)],
        'south': [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)],
        'west': [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)],
        'east': [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)],
    }[direction]


def bilinear(corners, s, t):
    top = [corners[0][i] + (corners[1][i] - corners[0][i]) * s for i in range(3)]
    bottom = [corners[3][i] + (corners[2][i] - corners[3][i]) * s for i in range(3)]
    return [top[i] + (bottom[i] - top[i]) * t for i in range(3)]


def quads_for(models, name, properties, position):
    namespace, path = name.split(':')
    if name in SOLID:
        color = SOLID[name]
        for direction in ('up', 'north', 'south', 'east', 'west'):
            corners = [[c[i] / 16 + position[i] for i in range(3)] for c in face_corners(direction, (0, 0, 0), (16, 16, 16))]
            yield corners, tuple(int(c * SHADE[direction]) for c in color)
        return
    blockstate_file = ASSETS / namespace / 'blockstates' / (path + '.json')
    if not blockstate_file.exists():
        return
    for variant in variants_for(json.loads(blockstate_file.read_text(encoding='utf-8')), properties):
        yield from quads_for_variant(models, variant, position)


def quads_for_variant(models, variant, position):
    data = models.load(variant['model'])
    angle = math.radians(-variant.get('y', 0))
    state_matrix = [[math.cos(angle), 0, math.sin(angle)], [0, 1, 0], [-math.sin(angle), 0, math.cos(angle)]]
    textures = data.get('textures', {})
    for element in data.get('elements', []):
        matrix = rotation_matrix(element.get('rotation'))
        origin = element.get('rotation', {}).get('origin', [8, 8, 8])
        for direction, info in element['faces'].items():
            reference = info['texture']
            while reference.startswith('#'):
                reference = textures.get(reference[1:], '')
            image = models.texture(reference) if reference else None
            if image is None:
                continue
            corners = face_corners(direction, element['from'], element['to'])
            if matrix:
                corners = [apply(matrix, c, origin) for c in corners]
            corners = [apply(state_matrix, c, [8, 8, 8]) for c in corners]
            u0, v0, u1, v1 = info.get('uv', [0, 0, 16, 16])
            steps_u = max(1, min(16, math.ceil(abs(u1 - u0))))
            steps_v = max(1, min(16, math.ceil(abs(v1 - v0))))
            for i in range(steps_u):
                for j in range(steps_v):
                    u = u0 + (u1 - u0) * (i + 0.5) / steps_u
                    v = v0 + (v1 - v0) * (j + 0.5) / steps_v
                    pixel = image.getpixel((min(15, max(0, int(u))), min(15, max(0, int(v)))))
                    if pixel[3] < 128:
                        continue
                    quad = [bilinear(corners, (i + a) / steps_u, (j + b) / steps_v) for a, b in ((0, 0), (1, 0), (1, 1), (0, 1))]
                    world = [[q[k] / 16 + position[k] for k in range(3)] for q in quad]
                    yield world, tuple(int(c * SHADE[direction]) for c in pixel[:3])


def render(blocks, scale, yaw_degrees, tilt):
    models = Models()
    yaw = math.radians(yaw_degrees)
    cos_yaw, sin_yaw = math.cos(yaw), math.sin(yaw)

    def project(p):
        rx = p[0] * cos_yaw - p[2] * sin_yaw
        rz = p[0] * sin_yaw + p[2] * cos_yaw
        return (rx - rz) * scale * 0.87, (rx + rz) * scale * tilt - p[1] * scale, rx + rz + p[1] * 0.01

    polygons = []
    for position, (name, properties) in blocks.items():
        for quad, color in quads_for(models, name, properties, position):
            points = [project(p) for p in quad]
            polygons.append((sum(p[2] for p in points) / 4, [(p[0], p[1]) for p in points], color))
    if not polygons:
        raise SystemExit('nothing to render')
    us = [p[0] for _, pts, _ in polygons for p in pts]
    vs = [p[1] for _, pts, _ in polygons for p in pts]
    min_u, min_v = min(us) - 20, min(vs) - 20
    image = Image.new('RGBA', (int(max(us) - min_u) + 20, int(max(vs) - min_v) + 20), BACKGROUND)
    draw = ImageDraw.Draw(image)
    for _, points, color in sorted(polygons, key=lambda polygon: polygon[0]):
        draw.polygon([(u - min_u, v - min_v) for u, v in points], fill=color)
    return image


def main():
    parser = argparse.ArgumentParser(description='Render blocks from a saved test world with their real models and textures.')
    parser.add_argument('--world', default=str(DEFAULT_WORLD))
    parser.add_argument('--box', nargs=6, type=int, required=True, metavar=('MIN_X', 'MAX_X', 'MIN_Z', 'MAX_Z', 'MIN_Y', 'MAX_Y'))
    parser.add_argument('--scale', type=float, default=24.0)
    parser.add_argument('--yaw', type=float, default=0.0)
    parser.add_argument('--tilt', type=float, default=0.5)
    parser.add_argument('--out', default=str(ROOT / 'build/art/previews/world-models.png'))
    args = parser.parse_args()
    blocks = collect(Path(args.world), args.box)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    render(blocks, args.scale, args.yaw, args.tilt).convert('RGB').save(out)
    print(out, len(blocks))


if __name__ == '__main__':
    main()
