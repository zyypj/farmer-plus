# Strawberry jam visuals

**English** | [Português](strawberry-jam-visuals.pt-BR.md)

The three portion levels use original native 16×16 pixel art and editable Java Block/Item projects made through Blockbench MCP. Each model has twelve elements and fifty-one faces. Geometry, textures, ids and the existing portion/facing state mapping are shared across loaders.

![Three real jar models on a table, rendered in Blockbench](images/strawberry-jam-table-front.png)

## Geometry and materials

Four pairs of glass faces form an eight-sided body resting at Y=0, with bottom faces integrated into the same elements. The glass stays six units wide; the cloth flares to about seven units. Overall height stays eight units, so `JamJarBlock.SHAPE` remains `Block.column(6.0, 0.0, 8.0)`.

One solid jam volume fits inside the glass bevels. Its height increases from about one third to two thirds and full. Pixel clusters make its surface slightly uneven. Deep red shading, sparse darker seeds and brighter fruit pieces stay behind the glass. A small smear sits on a bevel above the lowest fill.

The gingham cap is a thin top with four solid cloth panels attached to its four edges. Each panel has thickness and rotates outward at a different angle, producing a connected flared skirt. The isolated corner flap and box-shaped hem were removed. The raised twine band encircles all four sides and is 0.5 model units thick vertically, 2.5 times its previous thickness. The north-facing cream label is a single masked face just outside the glass and has a strawberry drawing without text.

Glass is the only texture with partial alpha. Minecraft 26.3's texture object `{"sprite": "farmerplus:block/strawberry_jam_glass", "force_translucent": true}` keeps it in the translucent material path while jam, cloth and label stay opaque or cut out. No renderer, block entity, tick handler or new registry entry is needed. The Blockbench export script configures preview material depth order after saving; this is an editor preview adjustment.

![Untextured lid geometry](images/strawberry-jam-lid-geometry.png)

![View from above in Blockbench](images/strawberry-jam-table-above.png)

## Item contexts

`items/strawberry_jam.json` still selects the portion level using `minecraft:block_state`. Each level then uses `minecraft:display_context`: GUI selects its 16×16 icon, while hand, dropped, fixed and other contexts use the corresponding real 3D block model. Display transforms are saved in all three projects and exported JSON files.

![Three native inventory icons](images/strawberry-jam-icons.png)

## Sources and reproduction

- `art/strawberry_jam.py`: original pixel authoring, model inputs, inventory icons and context definitions.
- `art/model-inputs/strawberry_jam_1.json` through `_3.json`: geometry inputs.
- `art/blockbench/strawberry_jam_1.bbmodel` through `_3.bbmodel`: editable projects with four embedded 16×16 atlases each.
- `art/export_strawberry_jam.js`: `exportStrawberryJam(root)` imports and exports through Blockbench MCP.
- `art/preview_strawberry_jam.js`: `previewStrawberryJam(root)` builds a temporary table scene and renders front, above and rear views.

Run `python art/strawberry_jam.py`, export through MCP, then run `./gradlew build` and `python art/validate_wheat_art.py`. The validator checks references, budgets, portable embedded textures, real fill heights, north-facing labels, context selection and identical packaged assets for all three loaders.

## Verification

Build and the art validator passed. NeoForge loaded the current resources and created the block and item atlases without Farmer+ model or texture warnings. Runtime byte comparisons and hashes are in `build/art/validation/strawberry-jam-resource-load.json`.

The table images are Blockbench renders. A manual inspection of three placed jars inside Minecraft is still pending; resource loading alone does not establish that visual acceptance check.
