async function exportStrawberryJam(root) {
    const fs = require('fs');
    const records = [];
    for (let level = 1; level <= 3; level++) {
        const name = 'strawberry_jam_' + level;
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
        Undo.finishEdit('Create country preserve jar ' + level + '/3');
        Canvas.updateAll();
        const result = JSON.parse(Codecs.java_block.compile({cube_name: true}));
        if (result.elements.length !== 12) throw Error('Jar element budget changed');
        if (!Object.values(result.textures).some(texture => texture?.force_translucent)) throw Error('Lost glass translucency');
        fs.mkdirSync(root + '/art/blockbench', {recursive: true});
        fs.mkdirSync(root + '/build/art/previews', {recursive: true});
        Project.save_path = root + '/art/blockbench/' + name + '.bbmodel';
        Project.export_path = destination;
        fs.writeFileSync(Project.save_path, JSON.stringify(JSON.parse(Codecs.project.compile({absolute_paths: false})), null, 2) + '\n');
        fs.writeFileSync(destination, JSON.stringify(result, null, 2) + '\n');
        Project.saved = true;
        if (Dialog.open) Dialog.open.hide();
        for (const texture of Texture.all) {
            const material = texture.getMaterial();
            material.transparent = texture.force_translucent;
            material.depthWrite = !texture.force_translucent;
            material.needsUpdate = true;
        }
        for (const cube of Cube.all) cube.mesh.renderOrder = cube.name.startsWith('glass_') || cube.name === 'rounded_glass_foot' ? 2 : 0;
        Preview.selected.camera.position.set(-17, 14, -25);
        Preview.selected.controls.target.set(0, 3.5, 0);
        Preview.selected.controls.update();
        Canvas.updateAll();
        await new Promise(resolve => setTimeout(resolve, 80));
        await new Promise(resolve => Preview.selected.screenshot({width: 520, height: 440}, data => {
            fs.writeFileSync(root + '/build/art/previews/' + name + '.png', Buffer.from(data.split(',')[1], 'base64'));
            resolve();
        }));
        if (level === 3) {
            const mode = BarItems.view_mode.value;
            BarItems.view_mode.set('solid');
            BarItems.view_mode.onChange();
            for (const cube of Cube.all) if (!['gingham_cap', 'raised_twine_wrap'].includes(cube.name) && !cube.name.startsWith('cloth_drape_')) cube.mesh.visible = false;
            Preview.selected.controls.target.set(0, 7.1, 0);
            Preview.selected.camera.position.set(-14, 15, -19);
            Preview.selected.controls.update();
            await new Promise(resolve => setTimeout(resolve, 100));
            await new Promise(resolve => Preview.selected.screenshot({width: 650, height: 440}, data => {
                fs.writeFileSync(root + '/build/art/previews/strawberry-jam-lid-geometry.png', Buffer.from(data.split(',')[1], 'base64'));
                resolve();
            }));
            BarItems.view_mode.set(mode);
            BarItems.view_mode.onChange();
            Canvas.updateAll();
        }
        records.push({name, elements: Cube.all.length, faces: result.elements.reduce((count, cube) => count + Object.keys(cube.faces).length, 0), textures: Texture.all.length});
        const active = Project;
        for (const old of ModelProject.all.filter(project => project !== active && project.name === name && project.saved && project.save_path === active.save_path)) await old.close();
        active.select();
    }
    fs.mkdirSync(root + '/build/art/validation', {recursive: true});
    fs.writeFileSync(root + '/build/art/validation/strawberry-jam-blockbench.json', JSON.stringify({blockbench: Blockbench.version, transport: 'MCP localhost:3000/bb-mcp', records}, null, 2) + '\n');
    return records;
}
