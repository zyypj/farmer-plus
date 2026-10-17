# Strawberry visual models

**English** | [Português](strawberry-visuals.pt-BR.md)

Art task 0003 replaces the placeholder cross models with thirty native Blockbench Java Block/Item projects: five cultivated ages with four different arrangements each, and five wild ages with two arrangements each. Cultivated blockstates have sixteen equally weighted alternatives per age; wild blockstates have eight. Arrangements change petiole angles, heights, leaf lengths, berry positions, sizes and material colours.

| Age | Cultivated elements | Wild elements | Contents |
|---|---:|---:|---|
| 0 | 7 | 5 | Low crown and young trifoliate leaves |
| 1 | 11 | 7 | Larger leaf rosette with connected arch segments |
| 2 | 15 | 9 | Three cultivated flowers, two wild flowers |
| 3 | 20 | 12 | Three cultivated or two wild green/white berries, one flower |
| 4 | 20 | 11 | Four cultivated or two smaller wild ripe berries |

Each berry has three solid cuboids: two independently tilted shoulders and a corner-oriented tip. Composed Euler rotations give the tip a low vertex in three dimensions, rather than a flat bottom. The calyx is painted across the upper faces; yellow achenes and stepped highlights appear on the sides. There are fresh red, rose red and deeper red materials, and four size factors. Unripe fruit uses green, cream and nearly white palettes. Shared branching peduncle planes keep the mature model within twenty elements. Leaves use hard serrated silhouettes, central and lateral veins, and a paler underside. No custom renderer, block entity or visual ticking was introduced.

The crown is only 0.38 model units thick, with an irregular transparent silhouette, from Y=-1 to -0.62. Petioles start inside it at Y=-0.65. Mature berries remain above Y=0.25, clearing both farmland at Y=-1 and neighbouring full-height soil at Y=0. All thirty arrangements are checked. The old square stalk base and five unused placeholder stage textures are removed.

All eleven block atlases and the strawberry item sprite are original 32×32 RGBA pixel art with binary alpha. Textures are authored with explicit pixel polygons and paths in `art/strawberries.py`. Three leaf palettes and a separate underside atlas preserve the same silhouette; fruit colour atlases vary the material without replacing the geometric layout variations. The item is a red heart-shaped berry with seeds, calyx and a short stalk. Existing registry identifiers and item/model paths are preserved.

## Sources and reproduction

Sources are `art/blockbench/strawberry_plant_stage<age>[_variantN].bbmodel` and `art/blockbench/wild_strawberries_stage<age>[_variant1].bbmodel`. Each embeds its 32×32 textures. Every final model is imported, saved and exported through Blockbench 5.2.2 and its MCP plugin. The compiler's exported Euler rotations are compared to the input; a one-axis rotation may be serialized as `axis`/`angle` without changing the result.

1. Run `python art/strawberries.py` to author textures, geometry inputs and blockstates.
2. Through the connected Blockbench MCP `risky_eval`, load `art/export_strawberries.js` and execute `await exportStrawberries(root)`, with the absolute repository root. `previews=false` skips screenshots without skipping native save/export.
3. Run `python art/validate_strawberries.py`. If geometry changes, compare the reported selection dimensions with the static Java arrays before rebuilding.
4. Run `./gradlew build` and `python art/validate_wheat_art.py`; the latter includes the strawberry checks.
5. Run `./gradlew :neoforge:runClient` and inspect models and the log.

`art/blockbench_mcp.py` is a small local MCP HTTP client for the configured `http://localhost:3000/bb-mcp` transport when the named MCP tool is not exposed. It still calls the actual MCP `risky_eval` tool in Blockbench; it does not generate fake native project files.

`art/validate_strawberries.py` checks all model budgets, distinct arrangements, blockstate weights/rotations, six-faced fruit volumes, independently tilted shoulders, solid-piece intersection using separating axes, stalk-to-calyx attachment, soil clearance, model bounds, exact embedded texture pixels and static selection shapes. Its current hashes and model measurements are in `build/art/validation/strawberries.json`. MCP export records are in `build/art/validation/strawberry-blockbench-export.json`.

## Selection shapes

`StrawberryPlantBlock.SHAPES` was changed. The lower ages are smaller and lower than the placeholders, and fruiting plants extend past the original fourteen-unit outline. All shapes begin at Y=-1. Wild strawberries now override the selection shape with their own smaller five-entry array instead of inheriting the cultivated sizes. These are static selection outlines, not new collision or growth mechanics. Restart the client to load Java shape changes; F3+T only reloads assets.

## Verification and limits

`art/preview_strawberries.js` renders an 81-position field with all stages and arrangements through Blockbench. It also renders standing-height views from approximately five and twenty blocks from the near edge. These are **Blockbench renders, not Minecraft screenshots**. The agent did not manually inspect the final 9×9 field at both distances in Minecraft, and no gameplay FPS benchmark was performed. That manual acceptance check remains open.

![Cultivated and wild growth stages](images/strawberry-stages.png)

![An 81-position field rendered in Blockbench](images/strawberry-field-overview.png)
