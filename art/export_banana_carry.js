async function finishBananaCarry(root) {
    const fs = require('fs');
    const name = 'harvested_banana_bunch_stalk';
    const destination = root + '/common/src/main/resources/assets/farmerplus/models/block/' + name + '.json';
    const input = JSON.parse(fs.readFileSync(root + '/art/model-inputs/' + name + '.json', 'utf8'));
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
    Undo.finishEdit('Finish fibrous cut banana stalk');
    Canvas.updateAll();
    Project.save_path = root + '/art/blockbench/' + name + '.bbmodel';
    fs.writeFileSync(Project.save_path, Codecs.project.compile({absolute_paths: false}) + '\n');
    fs.writeFileSync(destination, Codecs.java_block.compile({cube_name: true}) + '\n');
    Project.saved = true;
    const display = JSON.parse(fs.readFileSync(root + '/build/art/banana-carry-display.json', 'utf8'));
    Modes.options.display.select();
    Undo.initEdit({display_slots: Object.keys(display)});
    for (const [slot, value] of Object.entries(display)) {
        if (!Project.display_settings[slot]) Project.display_settings[slot] = new DisplaySlot(slot);
        Project.display_settings[slot].extend(value);
    }
    DisplayMode.loadGUI();
    Undo.finishEdit('Refine complete bunch display at original shoulder scale');
    const exported = JSON.parse(Codecs.java_block.compile());
    const finalDisplay = exported.display;
    if (finalDisplay.thirdperson_righthand.scale.some(value => value !== 1.1)) throw Error('Shoulder scale changed');
    const paths = fs.readdirSync(root + '/common/src/main/resources/assets/farmerplus/models/item').filter(path => path.startsWith('banana_bunch_') && path.endsWith('.json'));
    if (paths.length !== 9) throw Error('Expected nine composite item models');
    for (const path of paths) {
        const filename = root + '/common/src/main/resources/assets/farmerplus/models/item/' + path;
        const item = JSON.parse(fs.readFileSync(filename, 'utf8'));
        item.display = finalDisplay;
        fs.writeFileSync(filename, JSON.stringify(item, null, 2) + '\n');
    }
    fs.writeFileSync(Project.save_path, Codecs.project.compile({absolute_paths: false}) + '\n');
    Project.saved = true;
    fs.writeFileSync(root + '/build/art/validation/banana-carry-blockbench.json', JSON.stringify({blockbench: Blockbench.version, displayEditor: true, source: Project.save_path, coreElements: Cube.all.length, itemModels: paths, display: finalDisplay}, null, 2) + '\n');
    return {coreElements: Cube.all.length, itemModels: paths.length, display: finalDisplay};
}
