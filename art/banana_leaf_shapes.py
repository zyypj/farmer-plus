import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets/farmerplus'
OUTPUT = ROOT / 'common/src/main/resources/farmerplus/shapes/banana_leaf.json'
CELL = 2
GRID = 16 // CELL
MIN_Y = -16 // CELL
MAX_Y = 32 // CELL
STEP = 0.5
AGES = ('young', 'mature', 'dry')
DIRECTIONS = ('north', 'north_east', 'east', 'south_east', 'south', 'south_west', 'west', 'north_west')


def matrix(rotation):
    if not rotation:
        return None
    if 'axis' in rotation:
        angles = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        angles[rotation['axis']] = rotation.get('angle', 0.0)
    else:
        angles = {axis: rotation.get(axis, 0.0) for axis in 'xyz'}
    ax, ay, az = (math.radians(angles[a]) for a in 'xyz')
    rx = [[1, 0, 0], [0, math.cos(ax), -math.sin(ax)], [0, math.sin(ax), math.cos(ax)]]
    ry = [[math.cos(ay), 0, math.sin(ay)], [0, 1, 0], [-math.sin(ay), 0, math.cos(ay)]]
    rz = [[math.cos(az), -math.sin(az), 0], [math.sin(az), math.cos(az), 0], [0, 0, 1]]
    return multiply(rz, multiply(ry, rx))


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def apply(m, point, origin):
    p = [point[i] - origin[i] for i in range(3)]
    return [sum(m[i][k] * p[k] for k in range(3)) + origin[i] for i in range(3)]


def samples(start, end):
    counts = [max(1, math.ceil(abs(end[i] - start[i]) / STEP)) for i in range(3)]
    for i in range(counts[0] + 1):
        for j in range(counts[1] + 1):
            for k in range(counts[2] + 1):
                yield [start[0] + (end[0] - start[0]) * i / counts[0],
                       start[1] + (end[1] - start[1]) * j / counts[1],
                       start[2] + (end[2] - start[2]) * k / counts[2]]


def cells(model_name, y_rotation):
    model = json.loads((ASSETS / 'models/block' / (model_name + '.json')).read_text(encoding='utf-8'))
    angle = math.radians(-y_rotation)
    state = [[math.cos(angle), 0, math.sin(angle)], [0, 1, 0], [-math.sin(angle), 0, math.cos(angle)]]
    filled = set()
    for element in model['elements']:
        rotation = matrix(element.get('rotation'))
        origin = element.get('rotation', {}).get('origin', [8, 8, 8])
        for point in samples(element['from'], element['to']):
            if rotation:
                point = apply(rotation, point, origin)
            point = apply(state, point, [8, 8, 8])
            cell = tuple(int(math.floor(point[i] / CELL)) for i in range(3))
            if 0 <= cell[0] < GRID and 0 <= cell[2] < GRID and MIN_Y <= cell[1] < MAX_Y:
                filled.add(cell)
    return filled


def merge(filled):
    remaining = set(filled)
    boxes = []
    for cell in sorted(filled, key=lambda c: (c[1], c[2], c[0])):
        if cell not in remaining:
            continue
        x0, y0, z0 = cell
        x1 = x0
        while (x1 + 1, y0, z0) in remaining:
            x1 += 1
        z1 = z0
        while all((x, y0, z1 + 1) in remaining for x in range(x0, x1 + 1)):
            z1 += 1
        y1 = y0
        while all((x, y1 + 1, z) in remaining for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)):
            y1 += 1
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    remaining.discard((x, y, z))
        boxes.append([x0 * CELL, y0 * CELL, z0 * CELL, (x1 + 1) * CELL, (y1 + 1) * CELL, (z1 + 1) * CELL])
    return boxes


def main():
    variants = json.loads((ASSETS / 'blockstates/banana_leaf.json').read_text(encoding='utf-8'))['variants']
    shapes, index_of, states = [], {}, []
    for age in AGES:
        for direction in DIRECTIONS:
            for segment in range(3):
                variant = variants['age=%s,direction=%s,segment=%d' % (age, direction, segment)]
                variant = variant[0] if isinstance(variant, list) else variant
                key = (variant['model'], variant.get('y', 0))
                if key not in index_of:
                    index_of[key] = len(shapes)
                    shapes.append(merge(cells(variant['model'].split('/')[-1], variant.get('y', 0))))
                states.append(index_of[key])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({'cell': CELL, 'states': states, 'shapes': shapes}, separators=(',', ':')) + '\n', encoding='utf-8', newline='\n')
    print(OUTPUT, len(shapes), 'shapes', sum(len(s) for s in shapes), 'boxes')


if __name__ == '__main__':
    main()
