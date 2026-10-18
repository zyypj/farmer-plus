# Avocado and crushed wheat art

**English** | [Português](avocado-visuals.pt-BR.md)

Art tasks 0005 and 0002 replace the provisional images in place. Twenty-six avocado images and twelve crushed wheat sprites now use original hard-pixel artwork. Block and item textures are 16×16. Boat entity atlases and sign screens keep their required vanilla layout dimensions, as specified by task 0005.

## Tree and wood

Grey-brown bark has short irregular fissures and small plates. Cut ends and stripped logs expose creamy, slightly pink wood. Planks, door, lattice trapdoor, signs, shelf and boats share that warm palette. Leaves use original native 16×16 lanceolate clusters with softer dark-green shading, subtle central veins, restrained waxy highlights and irregular transparent gaps. Reduced edge contrast and varied directions keep the crown dense and compatible with vanilla; the sapling shares the new leaf palette. Unripe skins are smooth green, while ripe skins have dark green/purple shadows and sparse pebbled highlights. The fruit item has a pear silhouette and a short stalk.

![Native tree and wood textures](images/avocado-textures.png)

![Additional wood textures and native entity layouts](images/avocado-wood-extras.png)

## Inventory icon refinement

The boat and chest-boat sprites use an original diagonal view, a readable recessed hull, shorter integrated oars and a shaded chest. Sign and hanging-sign icons have stronger board depth, wood grain and clearer supports; the door icon has four window panes and two lower panels matching the block design. All five icons retain the creamy avocado palette, native 16×16 pixels and existing paths. Vanilla sprites were viewed only as style references.

![Refined wood item icons](images/avocado-items-refined.png)

Run `python art/avocado_wood_pixels.py --items-only` to regenerate these five icons and their preview without rewriting block textures or entity atlases.

## Hanging models

The hanging fruit block uses the flowering, unripe and ripe models below. Each is a Java Block/Item model exported through the Blockbench MCP server, saved in `art/blockbench/avocado_fruit_<stage>.bbmodel` with an embedded 16×16 atlas. Models occupy the upper half of the separate fruit block, with their stalks reaching the leaves above.

| Overlay | Elements | Vertical bounds after rotation | Arrangement |
|---|---:|---|---|
| `avocado_fruit_flowering` | 8 | 12.70…16 | Two small branching panicles with solid stalks and florets |
| `avocado_fruit_unripe` | 8 | 9.82…16 | One smaller green pear, seven connected body sections and one stalk |
| `avocado_fruit_ripe` | 8 | 8.34…16 | One larger dark pear, seven connected body sections and one stalk |

One fruit per model leaves room for a gradual narrow neck, broad lower belly and smaller rounded base within the eight-element budget. Both fruit stages are now 65% wider and their body sections are 30% taller than the first export; the stalk is thicker too, improving visibility below a full leaf block. The sections share a slight lean and continuous side UV heights. This replaces the task's initial two-fruit box suggestion while retaining its permitted one-fruit arrangement and performance limit. Every rotated vertex stays within X/Z=0…16 and Y=8…16 in the fruit block, equivalent to Y=−8…0 relative to the leaves above. Flowers remain flowers rather than prematurely showing fruit.

![Native Blockbench comparison below leaf blocks](images/avocado-canopy-front.png)

## Crushed wheat

All twelve AGE 2–7 base/alternate textures were drawn as distinct broken stalk arrangements. Short snapped stubs occupy the bottom rows. Kinked culms, torn leaf ends, partial ears and loose mature kernels use bruised greens transitioning to dusty, muted straw. No soil or mud is painted into the sprites. Native 16×16 pixel coverage is about 14–27%, keeping roughly 73–86% of each sprite open; field previews were used to avoid a solid carpet after the four model planes overlap.

The existing 48 trampled models and blockstate geometry are unchanged. `art/trampled_wheat.py` now delegates AGE 2–7 crushed pixels to `art/crushed_pixels.py`, so regenerating the models preserves the final art. AGE 0–1 images are unchanged.

![The twelve crushed sprites](images/crushed-wheat-textures.png)

![Offline render of the shipped wheat models](images/trampled-wheat.png)

## Reproduction and checks

1. Run `python art/avocado_pixels.py` and `python art/avocado_wood_pixels.py` for the avocado textures and model inputs.
2. With Blockbench open, call `exportAvocado(root)` from `art/export_avocado.js` through MCP. The native sources and final exported JSON are saved together.
3. Run `python art/crushed_pixels.py`. The trampling generator also uses this authoring function when rebuilding.
4. `previewAvocado(root)` in `art/preview_avocado.js` renders the leaf overlay comparison through MCP; `python art/preview_trampled_wheat.py` renders the shipped trampled models offline.
5. Run `./gradlew build` and `python art/validate_wheat_art.py`.

Build and the validator passed. Checks include native embedded texture equality, all rotated avocado vertices, element budgets, crushed transparency/variation and current asset bytes in all three loader jars. The MCP export report is `build/art/validation/avocado-blockbench.json`.

The canopy image is a Blockbench render and the wheat field is an offline model render. The latest enlarged-fruit build passed 19,188 validator checks, and NeoForge loaded the current models and textures without Farmer+ model or texture warnings; resource hashes and atlas loading are recorded in `build/art/validation/avocado-canopy-resource-load.json`. Manual inspection of a grown tree and repeated survival trampling inside Minecraft remains pending.
