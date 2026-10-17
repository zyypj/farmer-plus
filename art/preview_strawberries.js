async function previewStrawberries(root) {
    const fs = require('fs');
    const names = JSON.parse(fs.readFileSync(root + '/build/art/strawberry-models.json', 'utf8'));
    const projects = Object.fromEntries(names.map(name => [name, ModelProject.all.filter(p => p.name === name && p.save_path).at(-1)]));
    const sources = {};
    for (const name of names) {
        projects[name].select();
        Canvas.updateAll();
        sources[name] = Project.model_3d;
    }
    projects.strawberry_plant_stage4.select();
    const original = Project.model_3d, preview = Preview.selected;
    const previous = {position: preview.camera.position.clone(), target: preview.controls.target.clone(), ortho: preview.isOrtho};
    const field = new THREE.Group();
    const soilMaterials = [new THREE.MeshBasicMaterial({color: 0x60432d}), new THREE.MeshBasicMaterial({color: 0x765038}), new THREE.MeshBasicMaterial({color: 0x4d382a})];
    const soilGeometry = new THREE.BoxGeometry(15.9, .6, 15.9);
    try {
        for (let x = 0; x < 9; x++) for (let z = 0; z < 9; z++) {
            const age = z < 5 ? z : 4;
            const variant = (x * 7 + z * 3) % 4;
            const name = 'strawberry_plant_stage' + age + (variant ? '_variant' + variant : '');
            const model = sources[name].clone(true);
            model.position.set(-8, 0, -8);
            model.visible = true;
            model.traverse(object => { if (object.type === 'LineSegments') object.visible = false; });
            const pivot = new THREE.Group();
            pivot.position.set((x - 4) * 16, 0, (z - 4) * 16);
            pivot.rotation.y = (x + z * 3) % 4 * Math.PI / 2;
            pivot.add(model);
            field.add(pivot);
            const soil = new THREE.Mesh(soilGeometry, soilMaterials[(x + z) % 3]);
            soil.position.set(pivot.position.x, -1.32, pivot.position.z);
            field.add(soil);
        }
        scene.add(field);
        original.visible = false;
        preview.setProjectionMode(false);
        for (const [name, position, target] of [
            ['strawberry-field-overview', [-125, 105, -145], [0, 0, 0]],
            ['strawberry-field-5-blocks', [0, 25, 145], [0, 2, 45]],
            ['strawberry-field-20-blocks', [0, 25, 385], [0, 2, 45]]
        ]) {
            preview.camera.position.set(...position);
            preview.controls.target.set(...target);
            preview.controls.update();
            preview.render();
            await new Promise(resolve => setTimeout(resolve, 100));
            await new Promise(resolve => preview.screenshot({width: 1200, height: 780, crop: false}, data => {
                fs.writeFileSync(root + '/build/art/previews/' + name + '.png', Buffer.from(data.split(',')[1], 'base64'));
                resolve();
            }));
        }
        return {renderer: 'Blockbench', positions: 81, cultivatedAges: 5, variantsPerAge: 4, cameraDistancesApproximate: true, manualMinecraftFieldInspection: false};
    } finally {
        scene.remove(field);
        original.visible = true;
        preview.setProjectionMode(previous.ortho);
        preview.camera.position.copy(previous.position);
        preview.controls.target.copy(previous.target);
        preview.controls.update();
        soilGeometry.dispose();
        soilMaterials.forEach(m => m.dispose());
    }
}
