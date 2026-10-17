import argparse
import io
import math
import struct
import zlib
from pathlib import Path

import nbtlib
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORLD = ROOT / 'fabric/runs/server/world'
COLORS = {
    'trunk': (118, 92, 70),
    'branch': (118, 92, 70),
    'log': (118, 92, 70),
    'wood': (118, 92, 70),
    'leaves': (52, 104, 48),
    'grass_block': (96, 140, 70),
}
THICKNESS = {'trunk': 10 / 16, 'branch': 6 / 16}
WOOD = {'trunk', 'branch', 'log', 'wood'}
FACE_SHADE = {'top': 1.0, 'left': 0.78, 'right': 0.62}
BACKGROUND = (196, 214, 226)


def read_chunk(region, chunk_x, chunk_z):
    index = 4 * ((chunk_x & 31) + (chunk_z & 31) * 32)
    location = struct.unpack('>I', region[index:index + 4])[0]
    offset, sectors = location >> 8, location & 0xFF
    if offset == 0 or sectors == 0:
        return None
    start = offset * 4096
    length = struct.unpack('>I', region[start:start + 4])[0]
    compression = region[start + 4]
    payload = region[start + 5:start + 4 + length]
    if compression != 2:
        raise ValueError(f'unsupported compression {compression}')
    return nbtlib.File.parse(io.BytesIO(zlib.decompress(payload)))


def block_name(entry):
    if isinstance(entry, dict):
        for key in ('id', 'Name', ''):
            if key in entry:
                return str(entry[key])
        return ''
    return str(entry)


def section_blocks(section):
    states = section.get('block_states')
    if states is None:
        return
    palette = [block_name(entry) for entry in states['palette']]
    if len(palette) == 1:
        if palette[0] != 'minecraft:air':
            for i in range(4096):
                yield i, palette[0]
        return
    bits = max(4, math.ceil(math.log2(len(palette))))
    per_long = 64 // bits
    mask = (1 << bits) - 1
    data = [int(value) & 0xFFFFFFFFFFFFFFFF for value in states['data']]
    for i in range(4096):
        value = (data[i // per_long] >> ((i % per_long) * bits)) & mask
        yield i, palette[value]


def collect(world, min_x, max_x, min_z, max_z, min_y, max_y):
    blocks = {}
    region_dir = world / 'dimensions/minecraft/overworld/region'
    for chunk_x in range(min_x >> 4, (max_x >> 4) + 1):
        for chunk_z in range(min_z >> 4, (max_z >> 4) + 1):
            path = region_dir / f'r.{chunk_x >> 5}.{chunk_z >> 5}.mca'
            if not path.exists():
                continue
            chunk = read_chunk(path.read_bytes(), chunk_x, chunk_z)
            if chunk is None:
                continue
            for section in chunk['sections']:
                section_y = int(section['Y'])
                if section_y * 16 + 15 < min_y or section_y * 16 > max_y:
                    continue
                for i, name in section_blocks(section):
                    x = chunk_x * 16 + (i & 15)
                    z = chunk_z * 16 + ((i >> 4) & 15)
                    y = section_y * 16 + (i >> 8)
                    if min_x <= x <= max_x and min_z <= z <= max_z and min_y <= y <= max_y:
                        kind = next((key for key in COLORS if name.endswith(key)), None)
                        if kind and (kind != 'grass_block' or y == min_y):
                            blocks[(x, y, z)] = kind
    return blocks


def boxes(blocks, pos):
    x, y, z = pos
    kind = blocks[pos]
    size = THICKNESS.get(kind)
    if size is None:
        return [(x, y, z, x + 1, y + 1, z + 1)]
    lo, hi = (1 - size) / 2, (1 + size) / 2
    result = [(x + lo, y + lo, z + lo, x + hi, y + hi, z + hi)]
    for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
        neighbour = blocks.get((x + dx, y + dy, z + dz))
        if neighbour in WOOD or (dy == -1 and neighbour == 'grass_block'):
            start = [lo if d == 0 else (hi if d > 0 else 0) for d in (dx, dy, dz)]
            end = [hi if d == 0 else (1 if d > 0 else lo) for d in (dx, dy, dz)]
            result.append((x + start[0], y + start[1], z + start[2], x + end[0], y + end[1], z + end[2]))
    return result


def render(blocks, scale, yaw_degrees, tilt):
    yaw = math.radians(yaw_degrees)
    cos_yaw, sin_yaw = math.cos(yaw), math.sin(yaw)

    def project(x, y, z):
        rx = x * cos_yaw - z * sin_yaw
        rz = x * sin_yaw + z * cos_yaw
        return (rx - rz) * scale * 0.87, (rx + rz) * scale * tilt - y * scale

    corners = [project(x + dx, y + dy, z + dz) for (x, y, z) in blocks for dx in (0, 1) for dy in (0, 1) for dz in (0, 1)]
    min_u = min(c[0] for c in corners) - 20
    min_v = min(c[1] for c in corners) - 20
    width = int(max(c[0] for c in corners) - min_u) + 20
    height = int(max(c[1] for c in corners) - min_v) + 20
    image = Image.new('RGB', (width, height), BACKGROUND)
    draw = ImageDraw.Draw(image)

    def point(x, y, z):
        u, v = project(x, y, z)
        return u - min_u, v - min_v

    order = sorted(blocks, key=lambda p: (p[0] * cos_yaw - p[2] * sin_yaw) + (p[0] * sin_yaw + p[2] * cos_yaw) + p[1] * 0.001)
    for pos in order:
        base = COLORS[blocks[pos]]
        for x0, y0, z0, x1, y1, z1 in boxes(blocks, pos):
            faces = {
                'top': [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
                'left': [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
                'right': [(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)],
            }
            for face, quad in faces.items():
                shade = FACE_SHADE[face]
                draw.polygon([point(*c) for c in quad], fill=tuple(int(c * shade) for c in base), outline=tuple(int(c * shade * 0.85) for c in base))
    return image


def main():
    parser = argparse.ArgumentParser(description='Render trees from a saved test world as an isometric voxel image.')
    parser.add_argument('--world', default=str(DEFAULT_WORLD))
    parser.add_argument('--box', nargs=6, type=int, required=True, metavar=('MIN_X', 'MAX_X', 'MIN_Z', 'MAX_Z', 'MIN_Y', 'MAX_Y'))
    parser.add_argument('--scale', type=float, default=8.0)
    parser.add_argument('--yaw', type=float, default=0.0)
    parser.add_argument('--tilt', type=float, default=0.5)
    parser.add_argument('--wood-only', action='store_true')
    parser.add_argument('--out', default=str(ROOT / 'build/art/previews/world-trees.png'))
    args = parser.parse_args()
    blocks = collect(Path(args.world), *args.box)
    if args.wood_only:
        blocks = {pos: kind for pos, kind in blocks.items() if kind != 'leaves'}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    render(blocks, args.scale, args.yaw, args.tilt).save(out)
    print(out, len(blocks))


if __name__ == '__main__':
    main()
