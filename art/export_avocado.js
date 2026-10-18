async function exportAvocado(root) {
    const fs = require('fs');
    const records = [];
    for (const stage of ['flowers', 'unripe', 'ripe']) {
        const name = 'avocado_fruit_' + (stage === 'flowers' ? 'flowering' : stage);
        const destination = root + '/common/src/main/resources/assets/farmerplus/models/block/' + name + '.json';
        const input = JSON.parse(fs.readFileSync(root + '/art/model-inputs/avocado_leaves_' + stage + '.json', 'utf8'));
        for (const element of input.elements) {
            element.from[1] += 16;
            element.to[1] += 16;
            if (element.rotation) element.rotation.origin[1] += 16;
        }
        newProject(Formats.java_block);
        Project.name = name;
        Project.java_block_version = '26.3';
        Undo.initEdit({elements: [], textures: [], outliner: true});
        Codecs.java_block.parse(input, destination, {resolve_parent: false});
        Project.java_block_version = '26.3';
        Project.ambientocclusion = false;
        for (const texture of Texture.all) {
            const filename = texture.name;
            const path = root + '/common/src/main/resources/assets/farmerplus/textures/block/' + filename;
            texture.fromDataURL('data:image/png;base64,' + fs.readFileSync(path).toString('base64'));
            texture.name = filename;
            texture.namespace = 'farmerplus';
            texture.folder = 'block';
            texture.path = path;
            texture.saved = true;
        }
        await Promise.all(Texture.all.map(texture => texture.img.decode()));
        Undo.finishEdit('Model hanging avocado ' + stage);
        Canvas.updateAll();
        const result = JSON.parse(Codecs.java_block.compile({cube_name: true}));
        if (result.elements.length !== 8) throw Error('Avocado element budget changed');
        const min = [Infinity, Infinity, Infinity], max = [-Infinity, -Infinity, -Infinity];
        for (const cube of Cube.all) {
            for (const x of [cube.from[0], cube.to[0]]) for (const y of [cube.from[1], cube.to[1]]) for (const z of [cube.from[2], cube.to[2]]) {
                const vertex = new THREE.Vector3(x, y, z);
                const origin = new THREE.Vector3(...cube.origin);
                const euler = new THREE.Euler(...cube.rotation.map(angle => angle * Math.PI / 180), 'ZYX');
                vertex.sub(origin).applyEuler(euler).add(origin);
                vertex.toArray().forEach((value, axis) => {min[axis] = Math.min(min[axis], value); max[axis] = Math.max(max[axis], value);});
            }
        }
        if (min[1] < 8 || max[1] > 16 || min[0] < 0 || min[2] < 0 || max[0] > 16 || max[2] > 16) throw Error('Avocado outside hanging fruit limits');
        Project.save_path = root + '/art/blockbench/' + name + '.bbmodel';
        Project.export_path = destination;
        fs.writeFileSync(Project.save_path, JSON.stringify(JSON.parse(Codecs.project.compile({absolute_paths: false})), null, 2) + '\n');
        fs.writeFileSync(destination, JSON.stringify(result, null, 2) + '\n');
        Project.saved = true;
        if (Dialog.open) Dialog.open.hide();
        Preview.selected.camera.position.set(-19, 23, -25);
        Preview.selected.controls.target.set(0, 13.2, 0);
        Preview.selected.controls.update();
        Canvas.updateAll();
        await new Promise(resolve => setTimeout(resolve, 120));
        await new Promise(resolve => Preview.selected.screenshot({width: 600, height: 460}, data => {
            fs.writeFileSync(root + '/build/art/previews/' + name + '.png', Buffer.from(data.split(',')[1], 'base64'));
            resolve();
        }));
        records.push({name, elements: Cube.all.length, faces: result.elements.reduce((n, cube) => n + Object.keys(cube.faces).length, 0), min, max, textures: Texture.all.length});
        const active = Project;
        for (const old of ModelProject.all.filter(project => project !== active && project.name === name && project.saved && project.save_path === active.save_path)) await old.close();
        active.select();
    }
    const hashes = {};
    const crypto = require('crypto');
    for (const record of records) for (const path of ['art/blockbench/' + record.name + '.bbmodel', 'common/src/main/resources/assets/farmerplus/models/block/' + record.name + '.json']) hashes[path] = crypto.createHash('sha256').update(fs.readFileSync(root + '/' + path)).digest('hex');
    fs.mkdirSync(root + '/build/art/validation', {recursive: true});
    fs.writeFileSync(root + '/build/art/validation/avocado-blockbench.json', JSON.stringify({blockbench: Blockbench.version, transport: 'MCP HTTP localhost:3000/bb-mcp', records, hashes}, null, 2) + '\n');
    return records;
}
