async function previewWheatField(root, singleRow = false) {
    const fs = require('fs');
    const project = ModelProject.all.filter(p => p.name === 'wheat_stage7' && p.save_path).at(-1);
    const sources = [0, 1, 2, 3].map(variation => {
        const name = 'wheat_stage7' + (variation ? '_variant' + variation : '');
        ModelProject.all.filter(p => p.name === name && p.save_path).at(-1).select();
        return {model: Project.model_3d, upperY: Cube.all[0].to[1], materials: Texture.all.map(t => t.getMaterial())};
    });
    project.select();
    const preview = Preview.selected;
    const previousPosition = preview.camera.position.clone();
    const previousTarget = preview.controls.target.clone();
    const original = Project.model_3d;
    const field = new THREE.Group();
    const materials = sources.flatMap(source => source.materials);
    const size = singleRow ? 4 : 12;
    const rows = singleRow ? 1 : size;
    const screenshot = 'build/art/previews/' + (singleRow ? 'wheat-height-variants.png' : 'mature-field-blockbench.png');
    try {
        for (let x = 0; x < size; x++) {
            for (let z = 0; z < rows; z++) {
                const seed = (Math.imul(x + 1, 73856093) ^ Math.imul(z + 1, 19349663)) >>> 0;
                const variation = singleRow ? [1, 3, 0, 2][x] : (seed >>> 4) % 4;
                const tile = sources[variation].model.clone(true);
                tile.visible = true;
                tile.position.set(-8, 0, -8);
                tile.traverse(mesh => {
                    if (mesh.type === 'LineSegments') mesh.visible = false;
                });
                const pivot = new THREE.Group();
                pivot.position.set((x - (size - 1) / 2) * (singleRow ? 28 : 16), 0, (z - (rows - 1) / 2) * 16);
                pivot.rotation.y = singleRow ? 0 : seed % 4 * Math.PI / 2;
                pivot.add(tile);
                field.add(pivot);
            }
        }
        const soil = new THREE.Mesh(new THREE.PlaneGeometry(singleRow ? 112 : size * 16, rows * 16), new THREE.MeshBasicMaterial({color: 0x63503a, side: THREE.DoubleSide}));
        soil.rotation.x = -Math.PI / 2;
        soil.position.y = -1.05;
        field.add(soil);
        scene.add(field);
        original.visible = false;
        preview.camera.position.set(...(singleRow ? [0, 30, -125] : [-180, 118, -190]));
        preview.controls.target.set(0, singleRow ? 9 : 7, 0);
        preview.controls.update();
        preview.render();
        await new Promise(resolve => setTimeout(resolve, 100));
        await new Promise(resolve => preview.screenshot({width: singleRow ? 1280 : 1200, height: singleRow ? 500 : 780}, data => {
            fs.writeFileSync(root + '/' + screenshot, Buffer.from(data.split(',')[1], 'base64'));
            resolve();
        }));
        return {cropPositions: size * rows, elementsPerCrop: Cube.all.length, botanicalVariants: 4, modelUpperY: sources.map(s => s.upperY), renderer: 'Blockbench', screenshot};
    } finally {
        scene.remove(field);
        original.visible = true;
        preview.camera.position.copy(previousPosition);
        preview.controls.target.copy(previousTarget);
        preview.controls.update();
        field.traverse(mesh => {
            if (mesh.type === 'Mesh' && !materials.includes(mesh.material)) {
                mesh.geometry.dispose();
                mesh.material.dispose();
            }
        });
    }
}
