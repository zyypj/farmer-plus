async function previewBananaLeaves(root) {
    const fs = require('fs');
    const previous = Project;
    const records = JSON.parse(fs.readFileSync(root + '/build/art/banana-preview-blocks.json', 'utf8'));
    const projects = [];
    const models = new Map();
    const field = new THREE.Group();
    for (const identifier of [...new Set(records.map(record => record.model))]) {
        newProject(Formats.java_block);
        Project.java_block_version = '26.3';
        Project.name = 'Banana preview ' + identifier.split('/').at(-1);
        const path = root + '/common/src/main/resources/assets/farmerplus/models/' + identifier.split(':')[1] + '.json';
        Undo.initEdit({elements: [], textures: [], outliner: true});
        Codecs.java_block.parse(JSON.parse(fs.readFileSync(path, 'utf8')), path, {resolve_parent: false});
        Project.java_block_version = '26.3';
        for (const texture of Texture.all) {
            texture.fromDataURL('data:image/png;base64,' + fs.readFileSync(root + '/common/src/main/resources/assets/farmerplus/textures/block/' + texture.name).toString('base64'));
        }
        await Promise.all(Texture.all.map(texture => texture.img.decode()));
        Undo.finishEdit('Inspect revised banana foliage');
        Canvas.updateAll();
        models.set(identifier, Project.model_3d.clone(true));
        Project.saved = true;
        projects.push(Project);
    }
    for (const record of records) {
        const block = models.get(record.model).clone(true);
        block.visible = true;
        block.position.set(-8, -8, -8);
        block.traverse(object => {
            if (object.type === 'LineSegments') object.visible = false;
        });
        const pivot = new THREE.Group();
        pivot.position.set(record.position[0] * 16 + 8, record.position[1] * 16 + 8, record.position[2] * 16 + 8);
        pivot.rotation.y = -(record.y || 0) * Math.PI / 180;
        pivot.add(block);
        field.add(pivot);
    }
    scene.add(field);
    const preview = Preview.selected;
    const camera = preview.camera.position.clone();
    const target = preview.controls.target.clone();
    const active = Project.model_3d;
    active.visible = false;
    try {
        for (const [name, position] of [['banana-leaves-blockbench', [110, 86, 145]], ['banana-leaves-underside', [-110, 22, 140]]]) {
            preview.camera.position.set(...position);
            preview.controls.target.set(8, 38, 8);
            preview.controls.update();
            preview.render();
            await new Promise(resolve => setTimeout(resolve, 120));
            await new Promise(resolve => preview.screenshot({width: 1000, height: 780, crop: false}, data => {
                fs.writeFileSync(root + '/docs/images/' + name + '.png', Buffer.from(data.split(',')[1], 'base64'));
                resolve();
            }));
        }
        return {renderer: 'Blockbench 5.2.2', blocks: records.length, images: ['banana-leaves-blockbench.png', 'banana-leaves-underside.png']};
    } finally {
        scene.remove(field);
        active.visible = true;
        preview.camera.position.copy(camera);
        preview.controls.target.copy(target);
        preview.controls.update();
        for (const project of projects) await project.close();
        previous.select();
    }
}
