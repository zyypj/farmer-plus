import json
from pathlib import Path

from PIL import Image, ImageDraw

from preview_world_models import ASSETS, collect, render, variants_for
from preview_world_trees import DEFAULT_WORLD

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / 'docs/images'


def sheet(cells, columns, destination):
    width = max(image.width for label, image in cells) + 24
    height = max(image.height for label, image in cells) + 40
    output = Image.new('RGB', (width * columns, height * ((len(cells) + columns - 1) // columns)), '#c4d6e2')
    draw = ImageDraw.Draw(output)
    for index, (label, image) in enumerate(cells):
        left, top = index % columns * width, index // columns * height
        output.paste(image.convert('RGB'), (left + (width - image.width) // 2, top + 30))
        draw.text((left + 12, top + 8), label, fill='#293f30')
    output.save(IMAGES / destination)


def main():
    cells = []
    for stage, name in enumerate(('Bud', 'Flowering', 'Green', 'Ripe')):
        blocks = {(0, 0, 0): ('farmerplus:banana_bunch', {'stage': str(stage), 'facing': 'north'})}
        cells.append((name, render(blocks, 155, 120, 0.35)))
    sheet(cells, 4, 'banana-bunch-stages.png')
    blocks = {(0, 0, 0): ('farmerplus:banana_bunch', {'stage': '3', 'facing': 'north'})}
    sheet([(name, render(blocks, 155, yaw, tilt)) for name, yaw, tilt in [('Side', 0, 0.12), ('Three-quarter', 160, 0.5), ('Above: circular hands', 90, 1.1)]], 3, 'banana-bunch-3d.png')
    cells = []
    for center in (100, 120, 140, 160):
        world = collect(DEFAULT_WORLD, (center - 5, center + 5, 95, 105, 199, 210))
        plant = {position: value for position, value in world.items() if value[0].startswith('farmerplus:')}
        if center == 100:
            records = []
            for position, (name, properties) in plant.items():
                state = json.loads((ASSETS / 'farmerplus/blockstates' / (name.split(':')[1] + '.json')).read_text(encoding='utf-8'))
                records.extend(dict(part, position=[position[0] - 100, position[1] - 200, position[2] - 100]) for part in variants_for(state, properties))
            (ROOT / 'build/art/banana-preview-blocks.json').write_text(json.dumps(records), encoding='utf-8')
        if plant:
            cells.append(('Server feature at %d 200 100' % center, render(plant, 90, 200, 0.3)))
    sheet(cells, 2, 'banana-generated-plants.png')
    directions = [('north', 0, -1), ('north_east', 1, -1), ('east', 1, 0), ('south_east', 1, 1), ('south', 0, 1), ('south_west', -1, 1), ('west', -1, 0), ('north_west', -1, -1)]
    cells = []
    for age in ('young', 'mature'):
        for name, delta_x, delta_z in directions:
            blocks = {(0, 0, 0): ('farmerplus:banana_stem', {'segment': 'crown', 'fruited': 'false'})}
            diagonal = delta_x != 0 and delta_z != 0
            for step in range(2 if diagonal else 3):
                blocks[(delta_x * (step + 1), 0, delta_z * (step + 1))] = ('farmerplus:banana_leaf', {'age': age, 'direction': name, 'segment': str(2 if diagonal and step else step)})
            cells.append((age + ' ' + name, render(blocks, 60, 200, 0.4)))
    sheet(cells, 4, 'banana-leaf-directions.png')


if __name__ == '__main__':
    main()
