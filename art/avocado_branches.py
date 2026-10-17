import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'common/src/main/resources/assets/farmerplus'
BRANCHES = {'avocado_trunk': 10, 'avocado_branch': 6}
BARK = 'farmerplus:block/avocado_log'
END = 'farmerplus:block/avocado_log_top'
ARMS = {
    'north': {},
    'east': {'y': 90},
    'south': {'y': 180},
    'west': {'y': 270},
    'up': {'x': 270},
    'down': {'x': 90},
}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8', newline='\n')


def textures():
    return {'bark': BARK, 'end': END, 'particle': BARK}


def core(lo, hi):
    side = {'uv': [lo, lo, hi, hi], 'texture': '#bark'}
    cap = {'uv': [lo, lo, hi, hi], 'texture': '#end'}
    return {
        'textures': textures(),
        'elements': [{
            'from': [lo, lo, lo],
            'to': [hi, hi, hi],
            'faces': {'north': side, 'east': side, 'south': side, 'west': side, 'up': cap, 'down': cap},
        }],
    }


def arm(lo, hi):
    along = {'uv': [lo, 0, hi, lo], 'texture': '#bark'}
    turned = {'uv': [lo, 0, hi, lo], 'texture': '#bark', 'rotation': 90}
    return {
        'textures': textures(),
        'elements': [{
            'from': [lo, lo, 0],
            'to': [hi, hi, lo],
            'faces': {
                'north': {'uv': [lo, lo, hi, hi], 'texture': '#end', 'cullface': 'north'},
                'up': along,
                'down': along,
                'east': turned,
                'west': turned,
            },
        }],
    }


def inventory(lo, hi):
    side = {'uv': [lo, 0, hi, 16], 'texture': '#bark'}
    cap = {'uv': [lo, lo, hi, hi], 'texture': '#end'}
    return {
        'parent': 'minecraft:block/block',
        'textures': textures(),
        'elements': [{
            'from': [lo, 0, lo],
            'to': [hi, 16, hi],
            'faces': {'north': side, 'east': side, 'south': side, 'west': side, 'up': cap, 'down': cap},
        }],
    }


def blockstate(name):
    parts = [{'apply': {'model': f'farmerplus:block/{name}_core'}}]
    for direction, rotation in ARMS.items():
        parts.append({'apply': {'model': f'farmerplus:block/{name}_arm', **rotation}, 'when': {direction: 'true'}})
    return {'multipart': parts}


def main():
    for name, size in BRANCHES.items():
        lo = (16 - size) // 2
        hi = lo + size
        write(ASSETS / f'models/block/{name}_core.json', core(lo, hi))
        write(ASSETS / f'models/block/{name}_arm.json', arm(lo, hi))
        write(ASSETS / f'models/block/{name}_inventory.json', inventory(lo, hi))
        write(ASSETS / f'blockstates/{name}.json', blockstate(name))
        write(ASSETS / f'items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'farmerplus:block/{name}_inventory'}})
        print(name, size)


if __name__ == '__main__':
    main()
