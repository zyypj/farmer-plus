from pathlib import Path
from PIL import Image
from io import BytesIO
import base64
import json
import math


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'common/src/main/resources/assets/farmerplus'


def rotated(point, rotation):
    origin = rotation.get('origin', [0, 0, 0])
    angles = {axis: rotation.get(axis, 0) for axis in ('x', 'y', 'z')}
    if 'axis' in rotation:
        angles[rotation['axis']] = rotation['angle']
    x, y, z = [point[i] - origin[i] for i in range(3)]
    ax, ay, az = [math.radians(angles[axis]) for axis in ('x', 'y', 'z')]
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    x, y = x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az)
    return [x + origin[0], y + origin[1], z + origin[2]]


def validate():
    errors = []
    records = []
    def check(value, message):
        if not value:
            errors.append(message)
    for stage in ('flowers', 'unripe', 'ripe'):
        name = 'avocado_leaves_' + stage
        model = json.loads((ASSET / 'models/block' / (name + '.json')).read_text(encoding='utf-8'))
        source = json.loads((ROOT / 'art/blockbench' / (name + '.bbmodel')).read_text(encoding='utf-8'))
        check(source['meta']['model_format'] == 'java_block' and source['resolution'] == {'width': 16, 'height': 16}, name + ': portable native 16x16 project')
        check(len(model['elements']) == len(source['elements']) == 8, name + ': eight elements')
        check(model.get('ambientocclusion') is False and 'particle' in model['textures'], name + ': material settings')
        vertices = []
        for element in model['elements']:
            vertices += [rotated([x, y, z], element.get('rotation', {})) for x in (element['from'][0], element['to'][0]) for y in (element['from'][1], element['to'][1]) for z in (element['from'][2], element['to'][2])]
        check(all(-8 - 1e-6 <= p[1] <= 1e-6 and 0 <= p[0] <= 16 and 0 <= p[2] <= 16 for p in vertices), name + ': all rotated vertices below leaves within model limits')
        for texture in source['textures']:
            final = Image.open(ASSET / 'textures/block' / texture['name']).convert('RGBA')
            embedded = Image.open(BytesIO(base64.b64decode(texture['source'].split(',')[1]))).convert('RGBA')
            check(embedded.size == (16, 16) and embedded.tobytes() == final.tobytes(), name + ': embedded texture matches final pixels')
        if stage != 'flowers':
            by_name = {element['name']: element for element in model['elements']}
            check(all(all(element['to'][i] > element['from'][i] for i in range(3)) for element in model['elements']), name + ': fruit and stalk use solid cuboids')
            neck = by_name['fruit_0_neck']
            belly = by_name['fruit_0_full_belly']
            check(belly['to'][0] - belly['from'][0] > 3 * (neck['to'][0] - neck['from'][0]), name + ': narrow pear neck and full lower belly')
            check(by_name['fruit_0_stalk']['to'][1] == 0, name + ': stalk reaches leaf underside')
        records.append({'name': name, 'elements': len(model['elements']), 'min_y': min(p[1] for p in vertices), 'max_y': max(p[1] for p in vertices)})
    multipart = json.loads((ASSET / 'blockstates/avocado_leaves.json').read_text(encoding='utf-8'))['multipart']
    check({part['when']['fruit'] for part in multipart if 'when' in part} == {'1', '2', '3'}, 'Avocado: flowering and two fruit states preserved')
    crushed = []
    for age in range(2, 8):
        masks = []
        for suffix in ('', '_alternate'):
            name = f'wheat_stage{age}{suffix}_crushed'
            image = Image.open(ASSET / 'textures/block' / (name + '.png'))
            alpha = image.getchannel('A')
            coverage = sum(value != 0 for value in alpha.get_flattened_data()) / 256
            check(image.size == (16, 16) and image.mode == 'RGBA' and set(alpha.get_flattened_data()) <= {0, 255}, name + ': native hard 16x16 pixels')
            check(.10 < coverage < .45, name + ': broken stalks leave visible soil gaps')
            check(sum(alpha.getpixel((x, 15)) > 0 for x in range(16)) >= 3, name + ': snapped basal stubs')
            masks.append(alpha.tobytes())
            crushed.append({'name': name, 'coverage': coverage})
        check(masks[0] != masks[1], f'Crushed age {age}: alternate has a distinct arrangement')
    return {'models': records, 'crushed_textures': crushed, 'errors': errors}


if __name__ == '__main__':
    result = validate()
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['errors']))
