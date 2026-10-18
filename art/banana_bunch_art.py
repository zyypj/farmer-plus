import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / 'common/src/main/resources'
ASSETS = RESOURCES / 'assets/farmerplus'
DATA = RESOURCES / 'data/farmerplus'
MAX_BANANAS = 8
HANDS = [(tier, half) for tier in range(4) for half in range(2)]
FACINGS = {'north': 0, 'east': 90, 'south': 180, 'west': 270}
CARRY_DISPLAY = {
    'thirdperson_righthand': {'rotation': [45, 0, 165], 'translation': [1.5, 5.42, 6.35], 'scale': [1.1, 1.1, 1.1]},
    'firstperson_righthand': {'rotation': [0, 30, -8], 'translation': [3, 11, 0], 'scale': [0.85, 0.85, 0.85]},
    'gui': {'rotation': [20, 135, 0], 'translation': [0, -1.5, 0], 'scale': [0.62, 0.62, 0.62]},
    'ground': {'rotation': [0, 0, 0], 'translation': [0, 3, 0], 'scale': [0.4, 0.4, 0.4]},
    'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [0.6, 0.6, 0.6]},
}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8', newline='\n')


def faces(side_uv, end_uv, texture, end_texture):
    data = {side: {'uv': side_uv, 'texture': texture} for side in ('north', 'east', 'south', 'west')}
    data['up'] = {'uv': end_uv, 'texture': end_texture}
    data['down'] = {'uv': end_uv, 'texture': end_texture}
    return data


def stalk_model():
    return {
        'ambientocclusion': False,
        'textures': {'particle': 'farmerplus:block/banana_stem', 'stalk': 'farmerplus:block/banana_stem', 'cut': 'farmerplus:block/banana_stem_top'},
        'elements': [
            {'name': 'rachis', 'from': [7.4, 0, 7.9], 'to': [8.6, 16, 9.1], 'faces': faces([7, 0, 9, 16], [7, 7, 9, 9], '#stalk', '#cut')},
            {'name': 'stub', 'from': [7, 16, 7.5], 'to': [9, 19.5, 9.5], 'faces': faces([7, 0, 9, 3.5], [7, 7, 9, 9], '#stalk', '#cut')},
        ],
    }


def hand_model(index):
    tier, half = HANDS[index]
    return 'farmerplus:block/banana_bunch_ripe_hand_%d_%d' % (tier, half)


def blockstate():
    parts = []
    for facing, angle in FACINGS.items():
        rotation = {'y': angle} if angle else {}
        parts.append({'when': {'facing': facing}, 'apply': dict({'model': 'farmerplus:block/harvested_banana_bunch_stalk'}, **rotation)})
        for index in range(MAX_BANANAS):
            counts = '|'.join(str(count) for count in range(index + 1, MAX_BANANAS + 1))
            condition = {'facing': facing}
            if index:
                condition['bananas'] = counts
            parts.append({'when': condition, 'apply': dict({'model': hand_model(index)}, **rotation)})
    return {'multipart': parts}


def item():
    pieces = [('banana_bunch_stalk', 'farmerplus:block/harvested_banana_bunch_stalk')]
    pieces += [('banana_bunch_hand_%d_%d' % HANDS[index], hand_model(index)) for index in range(MAX_BANANAS)]
    for name, parent in pieces:
        write(ASSETS / 'models/item' / (name + '.json'), {'parent': parent, 'display': CARRY_DISPLAY})
    return {'model': {'type': 'minecraft:composite', 'models': [{'type': 'minecraft:model', 'model': 'farmerplus:item/' + name} for name, _ in pieces]}}


def loot():
    full = {'type': 'minecraft:item', 'name': 'farmerplus:banana_bunch',
            'condition': {'type': 'minecraft:match_block', 'blocks': 'farmerplus:harvested_banana_bunch', 'state': {'bananas': str(MAX_BANANAS)}}}
    partial = [{'type': 'minecraft:item', 'name': 'farmerplus:banana',
                'condition': {'type': 'minecraft:match_block', 'blocks': 'farmerplus:harvested_banana_bunch', 'state': {'bananas': str(count)}},
                'modifier': [{'type': 'minecraft:set_count', 'count': count}]} for count in range(1, MAX_BANANAS)]
    return {'type': 'minecraft:block', 'pools': [{'rolls': 1, 'condition': {'type': 'minecraft:survives_explosion'},
                                                  'entries': [{'type': 'minecraft:alternatives', 'children': [full] + partial}]}],
            'random_sequence': 'farmerplus:blocks/harvested_banana_bunch'}


def main():
    for old in (ASSETS / 'models/block').glob('harvested_banana_bunch_[0-9].json'):
        old.unlink()
    old_item = ASSETS / 'models/item/banana_bunch.json'
    if old_item.exists():
        old_item.unlink()
    write(ASSETS / 'models/block/harvested_banana_bunch_stalk.json', stalk_model())
    write(ASSETS / 'blockstates/harvested_banana_bunch.json', blockstate())
    write(ASSETS / 'items/banana_bunch.json', item())
    write(DATA / 'loot_table/blocks/harvested_banana_bunch.json', loot())
    print('banana bunch art written')


if __name__ == '__main__':
    main()
