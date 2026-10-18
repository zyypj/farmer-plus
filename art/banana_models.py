import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = 'farmerplus:block/'
MODELS = {}
JOINS = {}


def face(texture, uv=(0, 0, 16, 16)):
    return {'texture': '#' + texture, 'uv': list(uv)}


def box(name, start, end, texture, uv=(0, 0, 16, 16), rotation=None):
    element = {'name': name, 'from': start, 'to': end,
               'faces': {side: face(texture, uv) for side in ('north', 'south', 'east', 'west', 'up', 'down')}}
    if rotation:
        element['rotation'] = rotation
    return element


def rotation(origin, x=0, y=0, z=0):
    return {'origin': origin, 'x': x, 'y': y, 'z': z}


def model(name, textures, elements):
    MODELS[name] = {'ambientocclusion': False, 'textures': dict(textures, particle=next(iter(textures.values()))), 'elements': elements}


def leaf_rotation(pivot, tilt, yaw, fold):
    tilt, yaw, fold = map(math.radians, (tilt, yaw, fold))
    cos_tilt, sin_tilt = math.cos(tilt), math.sin(tilt)
    cos_yaw, sin_yaw = math.cos(yaw), math.sin(yaw)
    cos_fold, sin_fold = math.cos(fold), math.sin(fold)
    return rotation(pivot,
                    x=math.degrees(math.atan2(sin_yaw * sin_fold + cos_yaw * sin_tilt * cos_fold, cos_yaw * cos_tilt)),
                    y=math.degrees(math.asin(sin_yaw * cos_fold - cos_yaw * sin_tilt * sin_fold)),
                    z=math.degrees(math.atan2(cos_tilt * sin_fold, cos_yaw * cos_fold + sin_yaw * sin_tilt * sin_fold)))


def leaf_panel(name, start, end, width, texture, uv, yaw=0, fold=12):
    length = math.dist(start, end)
    tilt = math.degrees(math.atan2(end[1] - start[1], math.hypot(end[0] - start[0], start[2] - end[2])))
    pivot = list(start)
    elements = []
    for side, low, high, roll in [('left', -width / 2, 0, fold), ('right', 0, width / 2, -fold)]:
        half_uv = (uv[0], uv[1], 8, uv[3]) if side == 'left' else (8, uv[1], uv[2], uv[3])
        panel = box(name + '_' + side, [start[0] + low, start[1] - 0.5, start[2] - length - 0.65],
                    [start[0] + high, start[1] + 0.05, start[2] + 0.65], texture, half_uv,
                    leaf_rotation(pivot, tilt, yaw, roll))
        panel['faces'] = {'up': face(texture, half_uv), 'down': face(texture, (half_uv[0], half_uv[3], half_uv[2], half_uv[1])),
                          'north': face(texture, (half_uv[2], min(15, half_uv[1]), half_uv[0], min(16, half_uv[1] + 1))),
                          'south': face(texture, (half_uv[0], max(0, half_uv[3] - 1), half_uv[2], max(1, half_uv[3])))}
        elements.append(panel)
    elements.append(leaf_rib(name + '_midrib', start, end, yaw))
    return elements


def leaf_rib(name, start, end, yaw=0):
    length = math.dist(start, end)
    tilt = math.degrees(math.atan2(end[1] - start[1], math.hypot(end[0] - start[0], start[2] - end[2])))
    return box(name, [start[0] - 0.28, start[1] - 0.28, start[2] - length],
               [start[0] + 0.28, start[1] + 0.12, start[2]], 'leaf', (7, 0, 9, 1), rotation(list(start), x=tilt, y=yaw))


def blade_sections(prefix, points, texture, rows, yaw=0):
    elements = []
    for index, (start, end) in enumerate(zip(points, points[1:])):
        elements += leaf_panel(prefix + '_' + str(index), start, end, 16, texture, (0, rows[index + 1], 16, rows[index]), yaw)
    return elements


def leaves():
    textures = {'leaf': NS + 'banana_leaf', 'tip': NS + 'banana_leaf_tip'}
    for age, heights in [('young', (10, 16, 22, 24, 21, 16)), ('mature', (10, 13, 15, 13, 8, 0))]:
        root, shoulder, seam, bend, tip_bend, tip_end = heights
        petiole = leaf_rib('petiole', (8, root, 21), (8, shoulder, 13))
        base = [petiole] + blade_sections('blade_base', [(8, shoulder, 13), (8, seam - 1.5, 6), (8, seam, 0)], 'tip', [2, 9, 16])
        blade = blade_sections('blade', [(8, seam, 16), (8, max(seam, bend) + 1, 8), (8, bend, 0)], 'leaf', [16, 8, 0])
        tip = blade_sections('tip', [(8, bend, 16), (8, tip_bend, 8), (8, tip_end, 0)], 'tip', [16, 8, 0])
        for segment, elements in [('base', base), ('blade', blade), ('tip', tip)]:
            model('banana_leaf_' + age + '_' + segment, textures, elements)
        JOINS[age] = {'base': [8, seam, 0], 'blade_start': [8, seam, 16], 'blade_end': [8, bend, 0], 'tip': [8, bend, 16]}
        diagonal_root = [-8, root, 24]
        diagonal_shoulder = [-8 + 8 / math.sqrt(2), shoulder, 24 - 8 / math.sqrt(2)]
        diagonal_seam = [16, seam, 0]
        elements = [leaf_rib('diagonal_petiole', diagonal_root, diagonal_shoulder, -45)]
        diagonal_mid = [(diagonal_shoulder[0] + 16) / 2, seam - 1.5, diagonal_shoulder[2] / 2]
        elements += blade_sections('diagonal_blade_base', [diagonal_shoulder, diagonal_mid, diagonal_seam], 'tip', [2, 9, 16], -45)
        model('banana_leaf_' + age + '_diagonal_base', textures, elements)
        elements = blade_sections('diagonal_blade', [(0, seam, 16), (6, max(seam, bend) + 1, 10), (12, bend, 4)], 'leaf', [16, 8, 0], -45)
        elements += blade_sections('diagonal_tip', [(12, bend, 4), (16, tip_bend, 0), (20, tip_end, -4)], 'tip', [16, 8, 0], -45)
        model('banana_leaf_' + age + '_diagonal_tip', textures, elements)
    dry = box('hanging_torn_blade', [2, -14, 14.5], [14, 8, 14.5], 'dry', rotation=rotation([8, 8, 14.5], x=-8))
    dry['faces'] = {'north': face('dry'), 'south': face('dry')}
    petiole = box('dry_petiole', [7.4, 7.6, 14], [8.6, 8.6, 21], 'dry', (7, 0, 9, 7))
    model('banana_leaf_dry', {'dry': NS + 'banana_leaf_dry'}, [petiole, dry])
    diagonal_petiole = box('dry_diagonal_petiole', [-8.6, 7.6, 17], [-7.4, 8.6, 24], 'dry', (7, 0, 9, 7), rotation([-8, 8, 24], y=-45))
    offset = 6.5 / math.sqrt(2)
    origin = [-8 + offset, 8, 24 - offset]
    diagonal_blade = box('dry_diagonal_hanging_blade', [origin[0] - 6, -14, origin[2]], [origin[0] + 6, 8, origin[2]], 'dry', rotation=rotation(origin, x=-8, y=-45))
    diagonal_blade['faces'] = {'north': face('dry'), 'south': face('dry')}
    model('banana_leaf_dry_diagonal', {'dry': NS + 'banana_leaf_dry'}, [diagonal_petiole, diagonal_blade])


def stems():
    textures = {'stem': NS + 'banana_stem', 'cut': NS + 'banana_stem_top', 'leaf': NS + 'banana_leaf', 'dry': NS + 'banana_leaf_dry'}
    column = box('overlapping_sheaths', [5, 0, 5], [11, 16, 11], 'stem')
    for side in ('up', 'down'):
        column['faces'][side] = face('cut')
    model('banana_stem_middle', textures, [column])
    model('banana_stem_base', textures, [column, box('basal_sheaths', [4, 0, 4], [12, 3, 12], 'stem', (0, 12, 16, 16)),
          box('peeling_sheath_west', [4.3, 1, 5.5], [5, 11, 8], 'dry', (6, 0, 10, 16), rotation([5, 11, 8], z=-9)),
          box('peeling_sheath_front', [8, 0.5, 10.9], [10, 8, 11.25], 'dry', (7, 0, 9, 16), rotation([9, 8, 11], x=-13))])
    elements = [column]
    for name, start, end, tilt in [('north', [5.5, 10, 4.5], [10.5, 17, 5.1], -20), ('south', [5.5, 10, 10.9], [10.5, 17, 11.5], 20)]:
        elements.append(box('open_sheath_' + name, start, end, 'stem', (3, 0, 10, 8), rotation([8, 10, 8], x=tilt)))
    elements += [box('rolled_cigar', [7, 14, 7], [9, 28, 9], 'leaf', (7, 0, 9, 16), rotation([8, 14, 8], x=6, z=-5)),
                 box('cigar_tip', [7.5, 27, 7.5], [8.5, 31, 8.5], 'leaf', (7, 0, 8, 5), rotation([8, 14, 8], x=6, z=-5))]
    model('banana_stem_crown', textures, elements)


def bunches():
    textures = {'stem': NS + 'banana_stem', 'heart': NS + 'banana_heart'}
    for stage in ('bud', 'flowering', 'green', 'ripe'):
        flowering = stage == 'flowering'
        bud = stage == 'bud'
        heart_top = 6 if bud else -1 if flowering else -3
        elements = [box('peduncle_from_stem', [7, 14, -5], [9, 16, 9], 'stem', (7, 0, 9, 16)),
                    box('exposed_rachis', [7.5, heart_top, 8], [8.5, 15, 9], 'stem', (7, 0, 9, 16))]
        size = 4.8 if bud or flowering else 3.6
        height = 7 if bud or flowering else 5
        for layer, factor in enumerate((0.72, 1, 0.92, 0.73, 0.46, 0.18)):
            half_width = size * factor / 2
            top = heart_top - layer * height / 6
            bottom = heart_top - (layer + 1) * height / 6
            elements.append(box('male_bud_bract_%d' % layer, [8 - half_width, bottom, 8.5 - half_width], [8 + half_width, top, 8.5 + half_width],
                                'heart', (0, layer * 2, 16, layer * 2 + 4), rotation([8, top, 8.5], y=45)))
        model('banana_bunch_' + stage, dict(textures, **({} if bud else {'fingers': NS + 'banana_fingers_' + ('ripe' if stage == 'ripe' else 'green')})), elements)
        if not bud:
            for tier, top in enumerate((12, 8) if flowering else (16, 12, 8, 4)):
                size = (0.65 if flowering else 1) * (1 - tier * 0.045)
                for half in range(2):
                    fingers = []
                    for finger in range(half * 4, half * 4 + 4):
                        yaw = finger * 45 + tier * 22.5
                        radians = math.radians(yaw)
                        profile = [(0.6, -4.5), (2.4, -4.1), (4.1, -2.4), (4.7, 0)]
                        for section, ((radius, height), (end_radius, end_height)) in enumerate(zip(profile, profile[1:])):
                            start = [8 + math.sin(radians) * radius * size, top + height * size, 8.5 + math.cos(radians) * radius * size]
                            length = math.hypot(end_radius - radius, end_height - height) * size
                            tilt = -math.degrees(math.atan2(end_height - height, end_radius - radius))
                            width = (0.6 if section == 2 else 0.72) * size
                            element = box('hand_%d_finger_%d_curve_%d' % (tier, finger, section),
                                          [start[0] - width, start[1] - width, start[2] - 0.12],
                                          [start[0] + width, start[1] + width, start[2] + length + 0.12],
                                          'fingers', (4, 2, 7, 7), rotation(start, x=tilt, y=yaw if yaw <= 180 else yaw - 360))
                            if section == 0:
                                element['faces']['north'] = face('fingers', (4, 0, 7, 1))
                            fingers.append(element)
                    model('banana_bunch_%s_hand_%d_%d' % (stage, tier, half),
                          {'fingers': NS + 'banana_fingers_' + ('ripe' if stage == 'ripe' else 'green')}, fingers)


def bunch_blockstate():
    parts = []
    for facing, yaw in [('north', 0), ('east', 90), ('south', 180), ('west', 270)]:
        for stage, name in enumerate(('bud', 'flowering', 'green', 'ripe')):
            names = ['banana_bunch_' + name]
            if stage:
                names += ['banana_bunch_%s_hand_%d_%d' % (name, tier, half) for tier in range(2 if stage == 1 else 4) for half in range(2)]
            for identifier in names:
                part = {'model': NS + identifier}
                if yaw:
                    part['y'] = yaw
                parts.append({'when': {'facing': facing, 'stage': str(stage)}, 'apply': part})
    return {'multipart': parts}


def main():
    leaves()
    stems()
    bunches()
    folder = ROOT / 'art/model-inputs'
    folder.mkdir(parents=True, exist_ok=True)
    for name, data in MODELS.items():
        assert len(data['elements']) <= 12, name
        for element in data['elements']:
            assert all(-16 <= coordinate <= 32 for key in ('from', 'to') for coordinate in element[key]), (name, element)
        (folder / (name + '.json')).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    target = ROOT / 'build/art'
    target.mkdir(parents=True, exist_ok=True)
    (target / 'banana-models.json').write_text(json.dumps(list(MODELS)), encoding='utf-8')
    (target / 'banana-joins.json').write_text(json.dumps(JOINS, indent=2), encoding='utf-8')
    destination = ROOT / 'common/src/main/resources/assets/farmerplus/blockstates/banana_bunch.json'
    destination.write_text(json.dumps(bunch_blockstate(), indent=2) + '\n', encoding='utf-8')
    print(len(MODELS), 'model inputs; export through art/export_banana.js in Blockbench MCP')


if __name__ == '__main__':
    main()
