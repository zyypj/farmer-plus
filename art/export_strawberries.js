async function exportStrawberries(root, selected, previews = true) {
    const fs = require('fs');
    const names = selected || JSON.parse(fs.readFileSync(root + '/build/art/strawberry-models.json', 'utf8'));
    const records = [];
    for (const name of names) {
        newProject(Formats.java_block);
        Project.name = name;
        Project.java_block_version = '26.3';
        const destination = root + '/common/src/main/resources/assets/farmerplus/models/block/' + name + '.json';
        const input = JSON.parse(fs.readFileSync(root + '/art/model-inputs/' + name + '.json', 'utf8'));
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
        Undo.finishEdit('Model Vanilla+ strawberry ' + name);
        Canvas.updateAll();
        if (Texture.all.some(t => t.error)) throw Error('Texture error: ' + name);
        const result = JSON.parse(Codecs.java_block.compile({cube_name: true}));
        if (result.elements.length !== input.elements.length) throw Error('Element loss: ' + name);
        for (let i = 0; i < input.elements.length; i++) {
            const expected = input.elements[i].rotation;
            if (!expected) continue;
            const actual = result.elements[i].rotation || {};
            if (actual.axis) actual[actual.axis] = actual.angle;
            for (const axis of ['x', 'y', 'z']) if (Math.abs((actual[axis] || 0) - expected[axis]) > .001) throw Error('Euler loss: ' + name + ':' + i + ':' + axis + ':' + JSON.stringify(actual));
        }
        fs.mkdirSync(root + '/art/blockbench', {recursive: true});
        fs.mkdirSync(root + '/build/art/previews', {recursive: true});
        Project.save_path = root + '/art/blockbench/' + name + '.bbmodel';
        Project.export_path = destination;
        fs.writeFileSync(Project.save_path, JSON.stringify(JSON.parse(Codecs.project.compile({absolute_paths: false})), null, 2) + '\n');
        fs.writeFileSync(destination, JSON.stringify(result, null, 2) + '\n');
        Project.saved = true;
        if (Dialog.open) Dialog.open.hide();
        Preview.selected.camera.position.set(-25, 22, -30);
        Preview.selected.controls.target.set(0, 1.5, 0);
        Preview.selected.controls.update();
        Canvas.updateAll();
        if (previews && !name.includes('_variant')) await Promise.race([new Promise(resolve => Preview.selected.screenshot({width: 480, height: 360}, data => {
            fs.writeFileSync(root + '/build/art/previews/' + name + '.png', Buffer.from(data.split(',')[1], 'base64'));
            resolve();
        })), new Promise((resolve, reject) => setTimeout(() => reject(Error('Preview timeout ' + name)), 4000))]);
        records.push({name, elements: Cube.all.length, faces: result.elements.reduce((n, c) => n + Object.keys(c.faces).length, 0), textures: Texture.all.length});
        const active = Project;
        for (const old of ModelProject.all.filter(project => project !== active && project.name === name && project.saved && project.save_path === active.save_path)) await old.close();
        active.select();
    }
    fs.mkdirSync(root + '/build/art/validation', {recursive: true});
    fs.writeFileSync(root + '/build/art/validation/strawberry-blockbench-export.json', JSON.stringify({blockbench: Blockbench.version, transport: 'MCP HTTP localhost:3000/bb-mcp', records}, null, 2) + '\n');
    return records;
}
