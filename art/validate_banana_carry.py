import base64
import json
import math
import re
from io import BytesIO
from pathlib import Path

from PIL import Image

from preview_world_models import apply, rotation_matrix, variants_for
from finish_banana_bunch import CARRY_DISPLAY, item_rotation

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets/farmerplus'


def main():
    checks, errors = [], []

    def check(condition, label):
        (checks if condition else errors).append(label)

    def load(path):
        return json.loads(path.read_text(encoding='utf-8'))

    paths = sorted((ASSETS / 'models/item').glob('banana_bunch_*.json'))
    displays = [load(path)['display'] for path in paths]
    check(len(paths) == 9, 'Nine item components')
    check(all(display == displays[0] for display in displays), 'Identical display in every component')
    check(displays[0]['thirdperson_righthand']['scale'] == [1.1] * 3, 'Original life-size shoulder scale')
    check(displays[0]['thirdperson_righthand']['rotation'] == [57, 0, 156], 'Shoulder inclination refined around the hand grip')
    positions = []
    for display in (CARRY_DISPLAY['thirdperson_righthand'], displays[0]['thirdperson_righthand']):
        grip = apply(item_rotation(display['rotation']), [0, 9.75 * 1.1, 0.5 * 1.1], [0, 0, 0])
        positions.append([grip[axis] + display['translation'][axis] for axis in range(3)])
    check(math.dist(*positions) < 0.001, 'Third-person cut-stub grip stays at the original hand position')
    check(displays[0]['firstperson_righthand']['translation'][1] >= 10, 'First-person upper-screen placement')
    components = load(ASSETS / 'items/banana_bunch.json')['model']
    check(components['type'] == 'minecraft:composite' and len(components['models']) == 9, 'Composite item contains all nine pieces')
    for part in components['models']:
        path = ASSETS / 'models/item' / (part['model'].split('/')[-1] + '.json')
        check(path.exists() and 'parent' in load(path), part['model'] + ': parent resolves')
    source = (ROOT / 'common/src/main/java/com/zyypj/farmerplus/content/banana/HarvestedBananaBunchBlock.java').read_text(encoding='utf-8')
    array = re.search(r'HAND_CENTERS\s*=\s*\{(.*?)\};', source, re.S).group(1)
    expected = [list(map(float, values.split(','))) for values in re.findall(r'\{([^{}]+)\}', array)]
    centres = []
    for tier in range(4):
        for half in range(2):
            model = load(ASSETS / 'models/block' / ('banana_bunch_ripe_hand_%d_%d.json' % (tier, half)))
            positions = []
            for element in model['elements']:
                centre = [(element['from'][axis] + element['to'][axis]) / 2 for axis in range(3)]
                positions.append(apply(rotation_matrix(element['rotation']), centre, element['rotation']['origin']))
            centre = [sum(point[axis] for point in positions) / len(positions) for axis in range(3)]
            centres.append(centre)
            check(math.dist(centre, expected[tier * 2 + half]) < 0.02, 'HAND_CENTERS matches piece %d/%d' % (tier, half))
    state = load(ASSETS / 'blockstates/harvested_banana_bunch.json')
    for facing in ('north', 'east', 'south', 'west'):
        for count in range(1, 9):
            selected = variants_for(state, {'facing': facing, 'bananas': str(count)})
            check(len(selected) == count + 1, 'Upright multipart %s/%d' % (facing, count))
            hands = [part['model'] for part in selected if 'ripe_hand' in part['model']]
            check(hands == ['farmerplus:block/banana_bunch_ripe_hand_%d_%d' % (index // 2, index % 2) for index in range(count)], 'Bottom-up removal %s/%d' % (facing, count))
    core = load(ASSETS / 'models/block/harvested_banana_bunch_stalk.json')
    check(len(core['elements']) <= 12 and core['ambientocclusion'] is False, 'Core budget and lighting')
    cut = next(element for element in core['elements'] if element['name'] == 'fresh_cut_bevel')
    check(cut['faces']['up']['texture'] == '#cut' and cut['faces']['up']['uv'] == [0, 0, 16, 16], 'Pale concentric cut on grip top')
    check(cut['to'][1] == 19.5, 'Grip endpoint unchanged')
    source = load(ROOT / 'art/blockbench/harvested_banana_bunch_stalk.bbmodel')
    for texture in source['textures']:
        embedded = Image.open(BytesIO(base64.b64decode(texture['source'].split(',')[1]))).convert('RGBA')
        actual = Image.open(ASSETS / 'textures/block' / texture['name']).convert('RGBA')
        check(embedded.tobytes() == actual.tobytes(), 'Portable embedded texture ' + texture['name'])
        check(actual.size == (16, 16) and set(actual.getchannel('A').get_flattened_data()) <= {0, 255}, 'Hard-pixel 16x16 ' + texture['name'])
    report = {'passed': len(checks), 'errors': errors, 'hand_centres': centres, 'display': displays[0]}
    path = ROOT / 'build/art/validation/banana-carry.json'
    path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
