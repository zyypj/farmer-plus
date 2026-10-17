async function previewStrawberryJam(root) {
    const fs = require('fs');
    const previous = Project;
    const inputs = [1, 2, 3].map(level => JSON.parse(fs.readFileSync(root + '/art/model-inputs/strawberry_jam_' + level + '.json', 'utf8')));
    const combined = {ambientocclusion: false, textures: inputs[0].textures, elements: []};
    inputs.forEach((input, index) => {
        const offset = (index - 1) * 11;
        for (const original of input.elements) {
            const cube = JSON.parse(JSON.stringify(original));
            cube.name = 'level' + (index + 1) + '_' + cube.name;
            cube.from[0] += offset;
            cube.to[0] += offset;
            if (cube.rotation) cube.rotation.origin[0] += offset;
            combined.elements.push(cube);
        }
    });
    newProject(Formats.java_block);
    Project.name = 'Strawberry jam table preview';
    Project.java_block_version = '26.3';
    Undo.initEdit({elements: [], textures: [], outliner: true});
    Codecs.java_block.parse(combined, root + '/art/model-inputs/jam-preview.json', {resolve_parent: false});
    for (const texture of Texture.all) {
        const path = root + '/common/src/main/resources/assets/farmerplus/textures/block/' + texture.name;
        texture.fromDataURL('data:image/png;base64,' + fs.readFileSync(path).toString('base64'));
    }
    await Promise.all(Texture.all.map(texture => texture.img.decode()));
    const canvas = document.createElement('canvas');
    canvas.width = canvas.height = 16;
    const context = canvas.getContext('2d');
    context.fillStyle = '#795338';
    context.fillRect(0, 0, 16, 16);
    context.fillStyle = '#65462f';
    for (const y of [3, 8, 13]) context.fillRect(0, y, 16, 1);
    const wood = new Texture({name: 'preview_table.png'}).fromDataURL(canvas.toDataURL()).add(false);
    await wood.img.decode();
    const table = new Cube({name: 'Preview table', from: [-10, -1, 2], to: [26, 0, 14]}).init();
    for (const face of Object.values(table.faces)) {
        face.texture = wood.uuid;
        face.uv = [0, 0, 16, 16];
    }
    Undo.finishEdit('Arrange three jam levels on a table');
    for (const texture of Texture.all) {
        const material = texture.getMaterial();
        material.transparent = texture.force_translucent;
        material.depthWrite = !texture.force_translucent;
        material.needsUpdate = true;
    }
    for (const cube of Cube.all) cube.mesh.renderOrder = cube.name.includes('glass_') ? 2 : 0;
    Canvas.updateAll();
    const preview = Preview.selected;
    try {
        preview.setProjectionMode(false);
        for (const [name, position, target] of [
            ['strawberry-jam-table-front', [-18, 15, -42], [0, 3.5, 0]],
            ['strawberry-jam-table-above', [-12, 32, -28], [0, 2.5, 0]],
            ['strawberry-jam-table-rear', [19, 14, 39], [0, 3.5, 0]],
        ]) {
            preview.camera.position.set(...position);
            preview.controls.target.set(...target);
            preview.controls.update();
            Canvas.updateAll();
            await new Promise(resolve => setTimeout(resolve, 150));
            await new Promise(resolve => preview.screenshot({width: 1100, height: 650}, data => {
                fs.writeFileSync(root + '/build/art/previews/' + name + '.png', Buffer.from(data.split(',')[1], 'base64'));
                resolve();
            }));
        }
        return {renderer: 'Blockbench', levels: 3, views: ['front', 'above', 'rear'], elementsPerJar: 12, manualMinecraftTableInspection: false};
    } finally {
        Project.saved = true;
        await Project.close();
        previous.select();
    }
}
