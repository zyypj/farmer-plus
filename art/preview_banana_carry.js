async function previewBananaCarry(root) {
    const fs = require('fs');
    const previous = Project;
    const asset = root + '/common/src/main/resources/assets/farmerplus/';
    const display = JSON.parse(fs.readFileSync(asset + 'models/item/banana_bunch_stalk.json', 'utf8')).display;
    const assembled = {ambientocclusion: false, textures: {}, elements: [], display};
    const names = ['harvested_banana_bunch_stalk'];
    for (let tier = 0; tier < 4; tier++) for (let half = 0; half < 2; half++) names.push('banana_bunch_ripe_hand_' + tier + '_' + half);
    for (const name of names) {
        const part = JSON.parse(fs.readFileSync(asset + 'models/block/' + name + '.json', 'utf8'));
        Object.assign(assembled.textures, part.textures);
        assembled.elements.push(...part.elements);
    }
    newProject(Formats.java_block);
    Project.name = 'Complete banana bunch display review';
    Project.java_block_version = '26.3';
    Undo.initEdit({elements: [], textures: [], outliner: true});
    Codecs.java_block.parse(assembled, root + '/build/art/banana-carry-preview.json', {resolve_parent: false});
    Project.java_block_version = '26.3';
    for (const texture of Texture.all) texture.fromDataURL('data:image/png;base64,' + fs.readFileSync(asset + 'textures/block/' + texture.name).toString('base64'));
    await Promise.all(Texture.all.map(texture => texture.img.decode()));
    Undo.finishEdit('Review all nine bunch components together');
    Canvas.updateAll();
    Modes.options.display.select();
    Undo.initEdit({display_slots: Object.keys(display)});
    for (const [slot, values] of Object.entries(display)) {
        if (!Project.display_settings[slot]) Project.display_settings[slot] = new DisplaySlot(slot);
        Project.display_settings[slot].extend(values);
    }
    Undo.finishEdit('Review identical composite transforms');
    const images = [];
    try {
        for (const slot of ['gui', 'ground', 'fixed']) {
            DisplayMode.load(slot);
            Canvas.updateAll();
            await new Promise(resolve => setTimeout(resolve, 160));
            await new Promise(resolve => Preview.selected.screenshot({width: 800, height: 650}, data => {
                const name = 'banana-display-' + slot + '.png';
                fs.writeFileSync(root + '/docs/images/' + name, Buffer.from(data.split(',')[1], 'base64'));
                images.push(name);
                resolve();
            }));
        }
        return {elements: assembled.elements.length, images};
    } finally {
        Project.saved = true;
        await Project.close();
        previous.select();
    }
}
