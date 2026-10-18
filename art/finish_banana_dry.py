import json

from banana_models import MODELS, ROOT, bunches, leaves, stems


def main():
    leaves()
    stems()
    bunches()
    name = 'banana_leaf_dry_diagonal'
    destination = ROOT / 'art/model-inputs' / (name + '.json')
    destination.write_text(json.dumps(MODELS[name], indent=2) + '\n', encoding='utf-8', newline='\n')
    manifest = ROOT / 'build/art/banana-models.json'
    manifest.parent.mkdir(parents=True, exist_ok=True)
    names = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else list(MODELS)
    if name not in names:
        names.append(name)
    manifest.write_text(json.dumps(names), encoding='utf-8', newline='\n')
    path = ROOT / 'common/src/main/resources/assets/farmerplus/blockstates/banana_leaf.json'
    state = json.loads(path.read_text(encoding='utf-8'))
    for key, variant in state['variants'].items():
        if key.startswith('age=dry,') and any(direction in key for direction in ('north_east', 'south_east', 'south_west', 'north_west')):
            variant['model'] = 'farmerplus:block/' + name
    path.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Diagonal dry leaf input and blockstate prepared; export before regenerating hitboxes')


if __name__ == '__main__':
    main()
