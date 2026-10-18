import json
from pathlib import Path

from PIL import Image

from banana_bunch_art import CARRY_DISPLAY, faces
from preview_world_models import apply, multiply, rotation_matrix

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets/farmerplus'
PALETTE = {'s': '#758342', 'b': '#94a454', 'l': '#b4bf74', 'h': '#cdd298', 'f': '#ddd5a6', 't': '#a58c58', 'd': '#796542'}
FIBRES = [
    'bblhbbslbblhbbsb', 'bblhbbsllblhbbsb', 'bblhbbsllblhbbsb', 'bblhbbslbblhbbsb',
    'bblhbbslbblhbbsl', 'bblhbbslbblhbbsl', 'bblhbbsllblhbbsl', 'bblhbbsllblhbbsb',
    'bblhbbslbblhbbsb', 'bblhbbslbblhbbsb', 'bbfhbbslbblhbbsl', 'bbftbbslbblhbbsl',
    'bbftbbslbblhbbsl', 'bbftbbslbblhbbsl', 'bbtddbsllblhbbsb', 'bbtddbsllblhbbsb',
]


def item_rotation(angles):
    return multiply(rotation_matrix({'x': angles[0]}), multiply(rotation_matrix({'y': angles[1]}), rotation_matrix({'z': angles[2]})))


def shoulder_display():
    previous = CARRY_DISPLAY['thirdperson_righthand']
    angles = [57, 0, 156]
    grip = [0, 9.75 * 1.1, 0.5 * 1.1]
    before = apply(item_rotation(previous['rotation']), grip, [0, 0, 0])
    after = apply(item_rotation(angles), grip, [0, 0, 0])
    translation = [previous['translation'][axis] + before[axis] - after[axis] for axis in range(3)]
    return {'rotation': angles, 'translation': [round(value, 5) for value in translation], 'scale': [1.1, 1.1, 1.1]}


def stalk_model():
    side = lambda uv, cut=(0, 0, 16, 16): faces(uv, cut, '#stalk', '#cut')
    return {'ambientocclusion': False,
            'textures': {'particle': 'farmerplus:block/banana_bunch_stalk', 'stalk': 'farmerplus:block/banana_bunch_stalk', 'cut': 'farmerplus:block/banana_stem_top'},
            'elements': [
                {'name': 'rachis_inside_hands', 'from': [7.4, 0, 7.9], 'to': [8.6, 16, 9.1], 'faces': side([4, 0, 8, 16])},
                {'name': 'grip_stub', 'from': [7, 16, 7.5], 'to': [9, 19.25, 9.5], 'faces': side([1, 0, 5, 13])},
                {'name': 'fresh_cut_bevel', 'from': [7.12, 19.25, 7.62], 'to': [8.88, 19.5, 9.38], 'faces': side([1, 0, 5, 1])},
                {'name': 'leaf_scar_collar', 'from': [7.15, 15.4, 7.65], 'to': [8.85, 16.25, 9.35], 'faces': side([8, 12, 13, 16])},
                {'name': 'peeling_fibre_front', 'from': [7.12, 15.1, 9.45], 'to': [7.5, 17.9, 9.63], 'faces': side([2, 10, 4, 16]),
                 'rotation': {'origin': [7.3, 17.9, 9.5], 'x': 8, 'y': 0, 'z': -8}},
                {'name': 'peeling_fibre_side', 'from': [8.95, 16, 8], 'to': [9.12, 18.4, 8.35], 'faces': side([2, 10, 4, 16]),
                 'rotation': {'origin': [9, 18.4, 8.2], 'x': 0, 'y': 0, 'z': 7}},
            ]}


def main():
    (ROOT / 'build/art').mkdir(parents=True, exist_ok=True)
    image = Image.new('RGBA', (16, 16))
    for row, values in enumerate(FIBRES):
        assert len(values) == 16
        for column, token in enumerate(values):
            image.putpixel((column, row), tuple(bytes.fromhex(PALETTE[token][1:])) + (255,))
    image.save(ASSETS / 'textures/block/banana_bunch_stalk.png')
    folder = ROOT / 'art/model-inputs'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'harvested_banana_bunch_stalk.json').write_text(json.dumps(stalk_model(), indent=2) + '\n', encoding='utf-8', newline='\n')
    display = json.loads(json.dumps(CARRY_DISPLAY))
    display['thirdperson_righthand'] = shoulder_display()
    display['gui']['translation'] = [0, -1.25, 0]
    display['ground']['translation'] = [0, 3.2, 0]
    display['fixed']['rotation'] = [0, 15, 0]
    (ROOT / 'build/art/banana-carry-display.json').write_text(json.dumps(display, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Hand-authored stalk atlas and Blockbench input prepared; fruit geometry preserved')


if __name__ == '__main__':
    main()
