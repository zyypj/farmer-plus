from pathlib import Path
from zipfile import ZipFile
from PIL import Image
import json
import hashlib
from io import BytesIO
import base64
import math

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'common/src/main/resources'
JAR = Path.home() / '.gradle/caches/neoformruntime/artifacts/minecraft_26.3_client.jar'
errors = []
checks = []


def check(condition, message):
    (checks if condition else errors).append(message)


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


with ZipFile(JAR) as vanilla:
    official = set(vanilla.namelist())
    version = json.loads(vanilla.read('version.json'))
    check(version['id'] == '26.3', 'Official client version is 26.3')
    pack_format = version['pack_version']
    expected = [pack_format['resource_major'], pack_format['resource_minor']]
    metadata = load(RES / 'pack.mcmeta')['pack']
    data_format = pack_format['data_major']
    check(metadata['min_format'] == expected and metadata['max_format'] == data_format, f'Pack format covers resources {expected} and data {data_format}')


STRAWBERRY_BUDGETS = {0: 8, 1: 12, 2: 16, 3: 20, 4: 20}


def element_budget(stem):
    if stem in ('avocado_fruit_flowering', 'avocado_fruit_unripe', 'avocado_fruit_ripe'):
        return 8
    if stem == 'wheat_sheaf':
        return 24
    if stem.startswith(('wheat_stage6', 'wheat_stage7')):
        return 16
    if stem.startswith('strawberry_plant_stage'):
        return STRAWBERRY_BUDGETS[int(stem[len('strawberry_plant_stage')])]
    if stem.startswith('strawberry_plant_trampled_stage'):
        return STRAWBERRY_BUDGETS[int(stem[len('strawberry_plant_trampled_stage')])]
    return 12


def resolve(identifier, kind):
    namespace, name = identifier.split(':') if ':' in identifier else ('minecraft', identifier)
    suffix = '.png' if kind == 'textures' else '.json'
    path = f'assets/{namespace}/{kind}/{name}{suffix}'
    return (RES / path).is_file() or path in official


for path in (RES / 'assets').rglob('*.json'):
    value = load(path)
    if 'models' in path.parts:
        if 'parent' in value:
            check(resolve(value['parent'], 'models'), f'{path.name}: parent resolves')
        for key, texture in value.get('textures', {}).items():
            if isinstance(texture, dict):
                texture = texture['sprite']
            if not texture.startswith('#'):
                check(resolve(texture, 'textures'), f'{path.name}: texture {key} resolves')
        elements = value.get('elements', [])
        if elements:
            budget = element_budget(path.stem)
            check(len(elements) <= budget, f'{path.name}: {len(elements)} elements, maximum {budget}')
        for el in elements:
            check('shade' not in el, f'{path.name}: no removed shade property')
            rotation = el.get('rotation', {})
            check(all(-180 <= rotation.get(axis, 0) <= 180 for axis in ('angle', 'x', 'y', 'z')), f'{path.name}: supported rotation')
            for face in el.get('faces', {}).values():
                check(all(0 <= v <= 16 for v in face['uv']), f'{path.name}: UV bounds')
                check(face['texture'].removeprefix('#') in value.get('textures', {}), f'{path.name}: texture variable resolves')

VANILLA_LAYOUT_SIZES = {('entity', 'boat'): (128, 64), ('entity', 'chest_boat'): (128, 128), ('gui', 'signs'): (24, 26), ('gui', 'hanging_signs'): (16, 16)}

for path in (RES / 'assets').rglob('*.png'):
    image = Image.open(path)
    expected_size = (512, 512) if path.name == 'icon.png' else (32, 32) if path.parent.name == 'block' and path.stem.startswith('wheat') and not (path.stem.endswith('_crushed') and int(path.stem[11]) >= 2) else VANILLA_LAYOUT_SIZES.get(path.relative_to(RES / 'assets').parts[2:4], (16, 16))
    check(image.size == expected_size, f'{path.name}: dimensions {expected_size}')
    check(image.mode == 'RGBA', f'{path.name}: RGBA')
    if not path.stem.endswith('_glass'):
        check(set(image.getchannel('A').get_flattened_data()) <= {0, 255}, f'{path.name}: binary alpha')
    check(image.getcolors(256) is not None, f'{path.name}: limited palette')

variants = load(RES / 'assets/minecraft/blockstates/wheat.json')['variants']
check(set(variants) == {f'age={i}' for i in range(8)}, 'Exactly eight vanilla wheat ages')
for age in range(8):
    entries = variants[f'age={age}']
    check(len(entries) == 16, f'Age {age}: four botanical models times four rotations')
    check({entry['y'] for entry in entries} == {0, 90, 180, 270}, f'Age {age}: four spatial rotations')
    for entry in entries:
        check(resolve(entry['model'], 'models'), f'Age {age}: model resolves')
    source = load(ROOT / f'art/blockbench/wheat_stage{age}.bbmodel')
    check(source['meta']['model_format'] == 'java_block', f'Age {age}: editable Java Blockbench project')
    expected_elements = 16 if age >= 6 else 4
    check(len(source['elements']) == expected_elements, f'Age {age}: {expected_elements} elements within crop budget')
    if age >= 6:
        model = load(RES / f'assets/farmerplus/models/block/wheat_stage{age}.json')
        height_models = [model]
        for variation in (1, 2, 3):
            name = f'wheat_stage{age}_variant{variation}'
            height_model = load(RES / f'assets/farmerplus/models/block/{name}.json')
            height_models.append(height_model)
            native = load(ROOT / f'art/blockbench/{name}.bbmodel')
            check(len(native['elements']) == len(height_model['elements']) == 16, f'{name}: height variation preserves element count')
            check(native['resolution'] == {'width': 32, 'height': 32}, f'{name}: native 32x32 project resolution')
            for texture in native['textures']:
                pixels = Image.open(BytesIO(base64.b64decode(texture['source'].split(',')[1]))).convert('RGBA')
                path = RES / f"assets/farmerplus/textures/block/{texture['name']}"
                check(pixels.tobytes() == Image.open(path).convert('RGBA').tobytes(), f'{name}: embedded {texture["name"]} matches final pixels')
        upper_y = [m['elements'][0]['to'][1] for m in height_models]
        check(len(set(upper_y)) == 4 and max(upper_y) - min(upper_y) >= 6, f'Age {age}: four visibly distinct crop heights')
        check(all(e['from'][1] == -1 for m in height_models for e in m['elements'][:4]), f'Age {age}: every height variant stays grounded at farmland')
        leaves = {element['name']: element for element in model['elements'] if '_leaf_' in element['name']}
        for prefix, direction in [('front_leaf', -1), ('rear_leaf', 1), ('left_leaf', -1), ('right_leaf', 1), ('front_lower_leaf', -1), ('rear_upper_leaf', 1)]:
            base, tip = leaves[f'{prefix}_base'], leaves[f'{prefix}_tip']

            def edge_point(element, end):
                coordinate = 2 if element['rotation']['axis'] == 'x' else 0
                along = element['to'][coordinate] if end else element['from'][coordinate]
                x = (element['from'][0] + element['to'][0]) / 2
                z = (element['from'][2] + element['to'][2]) / 2
                y = element['from'][1]
                origin = element['rotation']['origin']
                angle = math.radians(element['rotation']['angle'])
                if coordinate == 2:
                    z = along
                    return [x, origin[1] + (y - origin[1]) * math.cos(angle) - (z - origin[2]) * math.sin(angle), origin[2] + (y - origin[1]) * math.sin(angle) + (z - origin[2]) * math.cos(angle)]
                x = along
                return [origin[0] + (x - origin[0]) * math.cos(angle) - (y - origin[1]) * math.sin(angle), origin[1] + (x - origin[0]) * math.sin(angle) + (y - origin[1]) * math.cos(angle), z]

            left = edge_point(base, direction > 0)
            right = edge_point(tip, direction < 0)
            gap = math.dist(left, right)
            check(gap < 0.001, f'Age {age}: {prefix} joins without a gap ({gap:.6f} units)')
            root, end = edge_point(base, direction < 0), edge_point(tip, direction > 0)
            outward = (end[0] - root[0]) * (root[0] - 8) + (end[2] - root[2]) * (root[2] - 8)
            check(outward > 0, f'Age {age}: {prefix} opens away from the crop centre')
    check(source['resolution'] == {'width': 32, 'height': 32}, f'Age {age}: native 32x32 project resolution')
    check(all(t.get('source', '').startswith('data:image/png;base64,') for t in source['textures']), f'Age {age}: embedded portable textures')
    signatures = []
    for suffix in ('', '_alternate', '_variant2', '_variant3'):
        tex = Image.open(RES / f'assets/farmerplus/textures/block/wheat_stage{age}{suffix}.png').convert('RGBA')
        signatures.append(hashlib.sha256(tex.tobytes()).hexdigest())
    check(len(set(signatures)) == 4, f'Age {age}: four distinct original sprites')
    for texture in source['textures']:
        embedded = Image.open(BytesIO(base64.b64decode(texture['source'].split(',')[1]))).convert('RGBA')
        path = RES / f"assets/farmerplus/textures/block/{texture['name']}"
        check(embedded.size == (32, 32) and embedded.tobytes() == Image.open(path).convert('RGBA').tobytes(), f'Age {age}: embedded {texture["name"]} matches final pixels')

clearance = load(ROOT / 'build/art/validation/leaf-clearance.json')
check(not clearance['uvErrors'], 'Leaf UVs agree across both surfaces and connected segments')
check(len(clearance['results']) == 8 and all(not row['collisions'] for row in clearance['results']), 'All eight mature model combinations pass sampled opaque-leaf clearance')
for path, digest in clearance['assetHashes'].items():
    check(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, f'Leaf clearance uses current {path}')

sheaf = load(ROOT / 'art/blockbench/wheat_sheaf.bbmodel')
sheaf_item = load(RES / 'assets/farmerplus/items/wheat_sheaf.json')['model']
check(sheaf_item['type'] == 'minecraft:select' and sheaf_item['property'] == 'minecraft:display_context', 'Sheaf uses vanilla display-context selection')
check(any('gui' in case['when'] and resolve(case['model']['model'], 'models') for case in sheaf_item['cases']), 'Sheaf inventory model resolves')
check(resolve(sheaf_item['fallback']['model'], 'models'), 'Sheaf 3D hand and placed-model fallback resolves')
check(len(sheaf['elements']) <= 24, 'Sheaf stays within the 24-element solid-binding allowance')
binding = load(ROOT / 'build/art/validation/sheaf-redesign.json')
check(binding['allCordPartsConnected'] and binding['bandClosed'] and binding['waistInsideBand'] and binding['waistTouchesEveryWrapSection'], 'The solid binding grips all four sides of the waist and connects to knot, loops and tails')
check(len(binding['apertures']) == 2 and all(a['fourConnectedSegments'] and a['openingIsEmpty'] for a in binding['apertures']), 'Both bow loops are connected and have real open centres')
for path, digest in binding['assetHashes'].items():
    check(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, f'Binding inspection uses current {path}')
check(sheaf['resolution'] == {'width': 32, 'height': 32}, 'Sheaf uses 32x32 texture resolution')
for texture in sheaf['textures']:
    embedded = Image.open(BytesIO(base64.b64decode(texture['source'].split(',')[1]))).convert('RGBA')
    path = RES / f"assets/farmerplus/textures/block/{texture['name']}"
    check(embedded.size == (32, 32) and embedded.tobytes() == Image.open(path).convert('RGBA').tobytes(), f'Sheaf: embedded {texture["name"]} matches final pixels')

for loader in ('fabric', 'neoforge', 'forge'):
    jars = [p for p in (ROOT / loader / 'build/libs').glob('*.jar') if 'sources' not in p.name]
    check(bool(jars), f'{loader}: compiled jar exists')
    for jar in jars:
        with ZipFile(jar) as archive:
            names = set(archive.namelist())
            for path in (RES / 'assets').rglob('*'):
                if path.is_file():
                    relative = path.relative_to(RES).as_posix()
                    check(relative in names and archive.read(relative) == path.read_bytes(), f'{loader}: packaged current {relative}')

packs = list((ROOT / 'build/resourcepacks').glob('*.zip'))
check(len(packs) == 1, 'One standalone resource pack')
for pack in packs:
    with ZipFile(pack) as archive:
        names = set(archive.namelist())
        check('pack.mcmeta' in names and 'pack.png' in names, 'Standalone pack has root metadata and icon')
        for name in names:
            if name.startswith('assets/') and not name.endswith('/'):
                check(archive.read(name) == (RES / name).read_bytes(), f'Standalone pack: current {name}')
        check(not any(n.startswith('data/') or n.endswith('.class') for n in names), 'Standalone pack contains visuals only')
        for name in names:
            if '/models/' in name and name.endswith('.json'):
                model = json.loads(archive.read(name))
                for kind, identifier in [('models', model.get('parent', ''))] + [('textures', t) for t in model.get('textures', {}).values()]:
                    if isinstance(identifier, dict):
                        identifier = identifier['sprite']
                    if not identifier or identifier.startswith('#'):
                        continue
                    namespace, resource = identifier.split(':') if ':' in identifier else ('minecraft', identifier)
                    target = f'assets/{namespace}/{kind}/{resource}' + ('.png' if kind == 'textures' else '.json')
                    check(target in names or target in official, f'Standalone pack: dependency {identifier} is available without mod')

from validate_strawberries import validate as validate_strawberries

strawberries = validate_strawberries(quiet=True)
check(len(strawberries['models']) == 30, 'Thirty native cultivated/wild strawberry model arrangements')
for error in strawberries['errors']:
    check(False, error)
check(not strawberries['errors'], 'Strawberry native sources, solid berries, stage variation, textures and shapes pass')

jam_models = []
for level in range(1, 4):
    name = f'strawberry_jam_{level}'
    model = load(RES / f'assets/farmerplus/models/block/{name}.json')
    native = load(ROOT / f'art/blockbench/{name}.bbmodel')
    check(native['meta']['model_format'] == 'java_block' and native['resolution'] == {'width': 16, 'height': 16}, f'{name}: native 16x16 Java Blockbench source')
    check(len(model['elements']) == len(native['elements']) == 12, f'{name}: twelve real model elements')
    check(model.get('ambientocclusion') is False and 'particle' in model['textures'], f'{name}: ambient occlusion disabled and particle assigned')
    check(model['textures']['glass'].get('force_translucent') is True, f'{name}: native 26.3 translucent glass material')
    check(all(slot in model.get('display', {}) for slot in ('gui', 'ground', 'fixed', 'thirdperson_righthand', 'firstperson_righthand')), f'{name}: item display transforms')
    by_name = {element['name']: element for element in model['elements']}
    label = by_name['cream_strawberry_label_north']
    check(set(label['faces']) == {'north'} and label['from'][2] < 5, f'{name}: cream label faces north outside glass')
    check(min(element['from'][1] for element in model['elements']) == 0, f'{name}: foot rests on y=0')
    drapes = [by_name['cloth_drape_' + side] for side in ('north', 'south', 'west', 'east')]
    check(len(drapes) == 4 and all(bool(drape.get('rotation')) and all(drape['to'][axis] > drape['from'][axis] for axis in range(3)) for drape in drapes), f'{name}: four solid cloth panels drape from cap edges')
    check(all(drape['to'][1] == by_name['gingham_cap']['from'][1] for drape in drapes), f'{name}: all four cloth folds connect to cap rim')
    check('folded_cloth_corner' not in by_name and 'hanging_gingham_hem' not in by_name, f'{name}: isolated flap and box hem removed')
    check(all(by_name[key]['to'][1] > by_name[key]['from'][1] for key in ('jam_body', 'gingham_cap', 'raised_twine_wrap')), f'{name}: jam, cap and twine have real volume')
    check(len(native['textures']) == 4, f'{name}: four embedded atlases')
    for texture in native['textures']:
        embedded = Image.open(BytesIO(base64.b64decode(texture['source'].split(',')[1]))).convert('RGBA')
        final = Image.open(RES / f"assets/farmerplus/textures/block/{texture['name']}").convert('RGBA')
        check(embedded.size == (16, 16) and embedded.tobytes() == final.tobytes(), f'{name}: embedded {texture["name"]} matches final pixels')
    jam_models.append(by_name)

check(all(jam_models[i]['jam_body']['to'][1] < jam_models[i + 1]['jam_body']['to'][1] for i in range(2)), 'Jam: increasing real fill heights')
for name in jam_models[0]:
    if not name.startswith('jam_'):
        check(all(model[name] == jam_models[0][name] for model in jam_models[1:]), f'Jam: shared jar geometry {name}')
jam_item = load(RES / 'assets/farmerplus/items/strawberry_jam.json')['model']
check(jam_item['property'] == 'minecraft:block_state' and jam_item['block_state_property'] == 'portions', 'Jam: portion selection preserved')
for case in jam_item['cases']:
    selection = case['model']
    level = case['when']
    check(selection['property'] == 'minecraft:display_context' and selection['fallback']['model'] == f'farmerplus:block/strawberry_jam_{level}', f'Jam {level}: real 3D model outside GUI')
    check(selection['cases'][0]['when'] == ['gui'] and selection['cases'][0]['model']['model'] == f'farmerplus:item/strawberry_jam_{level}', f'Jam {level}: dedicated inventory icon')
from validate_avocado_art import validate as validate_avocado_art

avocado = validate_avocado_art()
for error in avocado['errors']:
    check(False, error)
check(not avocado['errors'], 'Avocado native sources, pear geometry, bounds and twelve native crushed sprites pass')
report = {'passed': len(checks), 'errors': errors, 'avocado_and_crushed': avocado, 'official_version': version, 'official_client_sha1': hashlib.file_digest(JAR.open('rb'), 'sha1').hexdigest()}
out = ROOT / 'build/art/validation/wheat-art-validation.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'passed': len(checks), 'errors': errors, 'report': str(out)}, indent=2))
raise SystemExit(bool(errors))
