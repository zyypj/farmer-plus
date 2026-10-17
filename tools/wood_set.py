import argparse
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / 'common/src/main/resources'
VANILLA_JAR = ROOT / 'common/build/moddev/artifacts/vanilla-26.3-1-merged.jar'
TEMPLATE = 'oak'
NAMESPACE = 'farmerplus'

WOOD_BLOCKS = ['log', 'wood', 'planks', 'stairs', 'slab', 'fence', 'fence_gate', 'door', 'trapdoor', 'pressure_plate', 'button']
STRIPPED_BLOCKS = ['log', 'wood']
TREE_BLOCKS = ['leaves', 'sapling']
RECIPES = ['planks', 'wood', 'stairs', 'slab', 'fence', 'fence_gate', 'door', 'trapdoor', 'pressure_plate', 'button']
STRIPPED_RECIPES = ['wood']
GENERATED_TREE_ASSETS = ['sapling']


def block_ids(wood, template):
    ids = {f'{template}_{suffix}': f'{wood}_{suffix}' for suffix in WOOD_BLOCKS}
    ids.update({f'stripped_{template}_{suffix}': f'stripped_{wood}_{suffix}' for suffix in STRIPPED_BLOCKS})
    return ids


def tree_ids(wood, template):
    return {f'{template}_{suffix}': f'{wood}_{suffix}' for suffix in TREE_BLOCKS}


def rename(text, wood, template):
    text = text.replace(f'#minecraft:{template}_logs', f'#{NAMESPACE}:{wood}_logs')
    return re.sub(rf'minecraft:((?:[a-z_]+/)*)(stripped_)?{template}_', rf'{NAMESPACE}:\1\2{wood}_', text)


class Vanilla:
    def __init__(self, jar):
        self.zip = zipfile.ZipFile(jar)
        self.names = set(self.zip.namelist())

    def text(self, path):
        return self.zip.read(path).decode('utf-8') if path in self.names else None

    def files(self, prefix):
        return [name for name in self.names if name.startswith(prefix) and name.endswith('.json')]


def write(relative, text):
    path = RESOURCES / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json.loads(text), indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def copy(vanilla, source, target, wood, template):
    text = vanilla.text(source)
    if text is None:
        raise FileNotFoundError(source)
    write(target, rename(text, wood, template))
    return text


def referenced_models(text, template):
    return set(re.findall(rf'minecraft:((?:block|item)/(?:stripped_)?{template}_[a-z_]+)', text))


def copy_assets(vanilla, names, wood, template):
    models = set()
    for vanilla_id, new_id in names.items():
        models |= referenced_models(copy(vanilla, f'assets/minecraft/blockstates/{vanilla_id}.json', f'assets/{NAMESPACE}/blockstates/{new_id}.json', wood, template), template)
        models |= referenced_models(copy(vanilla, f'assets/minecraft/items/{vanilla_id}.json', f'assets/{NAMESPACE}/items/{new_id}.json', wood, template), template)
    for model in sorted(models):
        target = rename(f'minecraft:{model}', wood, template).split(':', 1)[1]
        copy(vanilla, f'assets/minecraft/models/{model}.json', f'assets/{NAMESPACE}/models/{target}.json', wood, template)


def copy_data(vanilla, names, wood, template):
    for vanilla_id, new_id in names.items():
        copy(vanilla, f'data/minecraft/loot_table/blocks/{vanilla_id}.json', f'data/{NAMESPACE}/loot_table/blocks/{new_id}.json', wood, template)

    recipes = {f'{template}_{suffix}': f'{wood}_{suffix}' for suffix in RECIPES}
    recipes.update({f'stripped_{template}_{suffix}': f'stripped_{wood}_{suffix}' for suffix in STRIPPED_RECIPES})
    advancements = {Path(name).stem: name for name in vanilla.files('data/minecraft/advancement/recipes/')}
    for vanilla_id, new_id in recipes.items():
        copy(vanilla, f'data/minecraft/recipe/{vanilla_id}.json', f'data/{NAMESPACE}/recipe/{new_id}.json', wood, template)
        source = advancements[vanilla_id]
        category = Path(source).parent.name
        copy(vanilla, source, f'data/{NAMESPACE}/advancement/recipes/{category}/{new_id}.json', wood, template)


def mirror_tags(vanilla, names, wood, template):
    for path in vanilla.files('data/minecraft/tags/'):
        values = json.loads(vanilla.text(path)).get('values', [])
        kind = path.split('/')[3]
        if Path(path).stem == f'{template}_logs':
            own = [f'{NAMESPACE}:{names[value.split(":")[1]]}' for value in values if value.split(':')[1] in names]
            write(f'data/{NAMESPACE}/tags/{kind}/{wood}_logs.json', json.dumps({'values': own}))
            continue
        additions = []
        for value in values:
            if value == f'#minecraft:{template}_logs':
                additions.append(f'#{NAMESPACE}:{wood}_logs')
            elif isinstance(value, str) and value.startswith('minecraft:') and value.split(':')[1] in names:
                additions.append(f'{NAMESPACE}:{names[value.split(":")[1]]}')
        if additions:
            merge_tag(path, additions)


def merge_tag(relative, additions):
    path = RESOURCES / relative
    data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'values': []}
    for value in additions:
        if value not in data['values']:
            data['values'].append(value)
    write(relative, json.dumps(data))


def main():
    parser = argparse.ArgumentParser(description='Generate the data and assets of a vanilla-style wood set from the oak templates.')
    parser.add_argument('wood')
    parser.add_argument('--jar', default=str(VANILLA_JAR))
    args = parser.parse_args()

    vanilla = Vanilla(args.jar)
    wood_names = block_ids(args.wood, TEMPLATE)
    tree_names = tree_ids(args.wood, TEMPLATE)
    generated_tree = {f'{TEMPLATE}_{suffix}': f'{args.wood}_{suffix}' for suffix in GENERATED_TREE_ASSETS}

    copy_assets(vanilla, wood_names | generated_tree, args.wood, TEMPLATE)
    copy_data(vanilla, wood_names | generated_tree, args.wood, TEMPLATE)
    mirror_tags(vanilla, wood_names | tree_names, args.wood, TEMPLATE)
    print(json.dumps({'wood': args.wood, 'blocks': len(wood_names) + len(generated_tree)}))


if __name__ == '__main__':
    main()
