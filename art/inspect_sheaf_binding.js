function inspectSheafBinding(root) {
    const fs = require('fs'), crypto = require('crypto');
    if (Project.name !== 'wheat_sheaf') throw Error('Open wheat_sheaf before inspecting the binding');
    const vector = value => new THREE.Vector3(...value);
    const makeBox = cube => {
        cube.mesh.updateWorldMatrix(true, false);
        const centre = vector(cube.from.map((v, i) => (v + cube.to[i]) / 2));
        const origin = vector(cube.origin);
        const rotation = new THREE.Quaternion().setFromEuler(new THREE.Euler(...cube.rotation.map(v => v * Math.PI / 180), 'ZYX'));
        centre.sub(origin).applyQuaternion(rotation).add(origin);
        return {name: cube.name, centre, axes: [new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 1, 0), new THREE.Vector3(0, 0, 1)].map(axis => axis.applyQuaternion(rotation)), half: cube.from.map((v, i) => (cube.to[i] - v) / 2)};
    };
    const boxes = Cube.all.filter(cube => cube.name.startsWith('binding_') || cube.name.startsWith('bow_')).map(makeBox);
    const overlap = (a, b) => {
        const delta = b.centre.clone().sub(a.centre);
        const axes = a.axes.concat(b.axes, a.axes.flatMap(x => b.axes.map(y => x.clone().cross(y))));
        return axes.every(axis => {
            if (axis.lengthSq() < 1e-12) return true;
            axis.normalize();
            const radius = box => box.axes.reduce((sum, direction, i) => sum + Math.abs(direction.dot(axis)) * box.half[i], 0);
            return Math.abs(delta.dot(axis)) <= radius(a) + radius(b) + 1e-6;
        });
    };
    const graph = Object.fromEntries(boxes.map(a => [a.name, boxes.filter(b => a !== b && overlap(a, b)).map(b => b.name)]));
    const visit = names => {
        const seen = new Set(), pending = [names[0]];
        while (pending.length) {
            const name = pending.pop();
            if (seen.has(name)) continue;
            seen.add(name);
            pending.push(...graph[name].filter(next => names.includes(next)));
        }
        return seen.size === names.length;
    };
    const band = boxes.filter(b => /^binding_(front|right|back|left)$/.test(b.name));
    const waist = makeBox(Cube.all.find(cube => cube.name === 'compressed_stalk_waist'));
    const centreInsideBand = band.every(box => {
        const dx = Math.abs(box.centre.x - 8), dz = Math.abs(box.centre.z - 8);
        return Math.max(dx, dz) > 2 && Math.min(dx, dz) < 0.01;
    });
    const apertures = [['left', [6.4, 7.05, 5.4]], ['right', [9.7, 7.05, 5.3]]].map(([side, point]) => {
        const pieces = boxes.filter(box => box.name.startsWith('bow_' + side + '_'));
        const inside = box => box.axes.every((axis, i) => Math.abs(vector(point).sub(box.centre).dot(axis)) < box.half[i] - 1e-6);
        return {side, fourConnectedSegments: pieces.length === 4 && visit(pieces.map(b => b.name)), openingIsEmpty: pieces.every(box => !inside(box))};
    });
    const bounds = new THREE.Box3();
    for (const cube of Cube.all) bounds.union(new THREE.Box3().setFromObject(cube.mesh));
    bounds.translate(new THREE.Vector3(8, 0, 8));
    const hashes = {};
    for (const path of ['art/blockbench/wheat_sheaf.bbmodel', 'common/src/main/resources/assets/farmerplus/models/block/wheat_sheaf.json', ...Texture.all.map(t => 'common/src/main/resources/assets/farmerplus/textures/block/' + t.name)]) hashes[path] = crypto.createHash('sha256').update(fs.readFileSync(root + '/' + path)).digest('hex');
    const report = {renderer: 'Blockbench', elements: Cube.all.length, faces: Cube.all.reduce((n, c) => n + Object.values(c.faces).filter(f => f.texture !== null).length, 0), solidCordElements: boxes.length, allCordPartsConnected: visit(boxes.map(b => b.name)), bandClosed: band.length === 4 && band.every(b => graph[b.name].filter(n => band.some(other => other.name === n)).length === 2) && visit(band.map(b => b.name)), waistInsideBand: centreInsideBand, waistTouchesEveryWrapSection: band.every(box => overlap(box, waist)), apertures, graph, bounds: {min: bounds.min.toArray(), max: bounds.max.toArray()}, assetHashes: hashes, manualMinecraftVisualInspection: false};
    if (!report.allCordPartsConnected || !report.bandClosed || !report.waistInsideBand || !report.waistTouchesEveryWrapSection || apertures.some(a => !a.fourConnectedSegments || !a.openingIsEmpty)) throw Error(JSON.stringify(report));
    fs.mkdirSync(root + '/build/art/validation', {recursive: true});
    fs.writeFileSync(root + '/build/art/validation/sheaf-redesign.json', JSON.stringify(report, null, 2) + '\n');
    return report;
}
