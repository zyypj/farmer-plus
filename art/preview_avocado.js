async function previewAvocado(root) {
    const fs = require('fs');
    const previous = Project;
    const input = {ambientocclusion: false, textures: {leaf: 'farmerplus:block/avocado_leaves', particle: 'farmerplus:block/avocado_leaves'}, elements: []};
    ['flowers', 'unripe', 'ripe'].forEach((stage, index) => {
        const source = JSON.parse(fs.readFileSync(root + '/art/model-inputs/avocado_leaves_' + stage + '.json', 'utf8'));
        const offset = (index - 1) * 16;
        input.textures[stage] = source.textures.fruit;
        for (const original of source.elements) {
            const element = JSON.parse(JSON.stringify(original));
            element.from[0] += offset;
            element.to[0] += offset;
            if (element.rotation) element.rotation.origin[0] += offset;
            for (const face of Object.values(element.faces)) face.texture = '#' + stage;
            input.elements.push(element);
        }
        input.elements.push({name: stage + '_leaf_block', from: [offset, 0, 0], to: [offset + 16, 16, 16], faces: Object.fromEntries(['north', 'south', 'east', 'west', 'up', 'down'].map(side => [side, {texture: '#leaf', uv: [0, 0, 16, 16]}]))});
    });
    newProject(Formats.java_block);
    Project.name = 'Avocado fruit stage preview';
    Project.java_block_version = '26.3';
    Undo.initEdit({elements: [], textures: [], outliner: true});
    Codecs.java_block.parse(input, root + '/build/art/avocado-preview.json', {resolve_parent: false});
    for (const texture of Texture.all) texture.fromDataURL('data:image/png;base64,' + fs.readFileSync(root + '/common/src/main/resources/assets/farmerplus/textures/block/' + texture.name).toString('base64'));
    await Promise.all(Texture.all.map(texture => texture.img.decode()));
    Undo.finishEdit('Preview avocado phenology below leaves');
    Canvas.updateAll();
    try {
        for (const [name, camera, target] of [
            ['avocado-canopy-front', [-20, 10, -60], [0, 3, 0]],
            ['avocado-canopy-below', [-20, -18, -50], [0, -1, 0]],
        ]) {
            Preview.selected.camera.position.set(...camera);
            Preview.selected.controls.target.set(...target);
            Preview.selected.controls.update();
            Canvas.updateAll();
            await new Promise(resolve => setTimeout(resolve, 100));
            await new Promise(resolve => Preview.selected.screenshot({width: 1200, height: 650}, data => {
                fs.writeFileSync(root + '/build/art/previews/' + name + '.png', Buffer.from(data.split(',')[1], 'base64'));
                resolve();
            }));
        }
        return {renderer: 'Blockbench', stages: 3, modelsUnchanged: true, manualMinecraftTreeInspection: false};
    } finally {
        Project.saved = true;
        await Project.close();
        previous.select();
    }
}
