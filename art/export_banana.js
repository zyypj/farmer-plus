async function exportBanana(root, selected) {
    const fs = require('fs');
    const names = selected || JSON.parse(fs.readFileSync(root + '/build/art/banana-models.json', 'utf8'));
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
        Undo.finishEdit('Author Musa ' + name);
        Canvas.updateAll();
        const result = JSON.parse(Codecs.java_block.compile({cube_name: true}));
        if (result.elements.length !== input.elements.length || result.elements.length > 12) throw Error('Element budget: ' + name);
        for (let index = 0; index < input.elements.length; index++) {
            const expected = input.elements[index].rotation;
            if (!expected) continue;
            const actual = result.elements[index].rotation || {};
            if (actual.axis) actual[actual.axis] = actual.angle;
            for (const axis of ['x', 'y', 'z']) if (Math.abs((actual[axis] || 0) - expected[axis]) > .001) throw Error('Euler loss: ' + name);
        }
        Project.save_path = root + '/art/blockbench/' + name + '.bbmodel';
        Project.export_path = destination;
        fs.writeFileSync(Project.save_path, JSON.stringify(JSON.parse(Codecs.project.compile({absolute_paths: false})), null, 2) + '\n');
        fs.writeFileSync(destination, JSON.stringify(result, null, 2) + '\n');
        Project.saved = true;
        records.push({name, elements: result.elements.length, textures: Texture.all.length});
        if (Dialog.open) Dialog.open.hide();
        if (name !== names[names.length - 1]) await Project.close();
    }
    fs.mkdirSync(root + '/build/art/validation', {recursive: true});
    fs.writeFileSync(root + '/build/art/validation/banana-blockbench.json', JSON.stringify({blockbench: Blockbench.version, transport: 'MCP localhost:3000/bb-mcp', records}, null, 2) + '\n');
    return records;
}
