async function exportWheatArt(root, selectedNames) {
    const fs = require('fs');
    const names = selectedNames || Array.from({length: 8}, (_, i) => 'wheat_stage' + i).concat([6, 7].flatMap(age => [1, 2, 3].map(v => 'wheat_stage' + age + '_variant' + v)), 'wheat_sheaf');
    const results = [];
    for (const name of names) {
        newProject(Formats.java_block);
        Project.name = name;
        const destination = root + '/common/src/main/resources/assets/farmerplus/models/block/' + name + '.json';
        const input = JSON.parse(fs.readFileSync(root + '/art/model-inputs/' + name + '.json', 'utf8'));
        Undo.initEdit({elements: [], textures: [], outliner: true});
        Codecs.java_block.parse(input, destination, {resolve_parent: false});
        for (const texture of Texture.all) {
            const name = texture.name;
            const path = root + '/common/src/main/resources/assets/farmerplus/textures/block/' + name;
            texture.fromDataURL('data:image/png;base64,' + fs.readFileSync(path).toString('base64'));
            texture.name = name;
            texture.namespace = 'farmerplus';
            texture.folder = 'block';
            texture.path = path;
            texture.saved = true;
        }
        Project.java_block_version = '26.3';
        await new Promise(resolve => setTimeout(resolve, 150));
        Undo.finishEdit('Refine Detailed Vanilla+ ' + name);
        Canvas.updateAll();
        const errors = Texture.all.filter(texture => texture.error).map(texture => texture.name);
        if (errors.length) throw Error(errors.join(', '));
        fs.mkdirSync(root + '/art/blockbench', {recursive: true});
        fs.mkdirSync(root + '/build/art/previews', {recursive: true});
        fs.mkdirSync(require('path').dirname(destination), {recursive: true});
        Project.save_path = root + '/art/blockbench/' + name + '.bbmodel';
        Project.export_path = destination;
        fs.writeFileSync(Project.save_path, JSON.stringify(JSON.parse(Codecs.project.compile({absolute_paths: false})), null, 2) + '\n');
        fs.writeFileSync(destination, JSON.stringify(JSON.parse(Codecs.java_block.compile({cube_name: true})), null, 2) + '\n');
        Project.saved = true;
        if (Dialog.open) Dialog.open.hide();
        Preview.selected.camera.position.set(-30, 24, -30);
        Preview.selected.controls.target.set(0, 8, 0);
        Preview.selected.controls.update();
        Canvas.updateAll();
        await new Promise(resolve => setTimeout(resolve, 50));
        await Promise.race([new Promise(resolve => Preview.selected.screenshot({width: 480, height: 480}, data => {
            fs.writeFileSync(root + '/build/art/previews/' + name + '-blockbench.png', Buffer.from(data.split(',')[1], 'base64'));
            resolve();
        })), new Promise((resolve, reject) => setTimeout(() => reject(Error('Preview timeout: ' + name)), 4000))]);
        results.push({name, elements: Cube.all.length, textures: Texture.all.length});
    }
    return results;
}
