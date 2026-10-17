# Art pipeline

**English** | [Português](art-pipeline.pt-BR.md)

Farmer+ uses **Realistic Vanilla+**: recognizable Minecraft pixel art with more believable plant anatomy, proportions, layering and material shading. Detail must improve the silhouette and read well in a whole field, in inventories and at normal gameplay distance.

## Style rules

- **Native texture grids:** wheat crop and sheaf block textures use **32×32 pixels**; all item icons use **16×16 pixels**, including wheat, seeds, flour, dough, porridge, sheaf and strawberry. Strawberry task 0003 block atlases also use 16×16. Draw directly on the target grid with deliberate pixel clusters; simplify small markings when authoring 16×16 art. Other content defaults to 16×16 until its art task specifies otherwise. The mod icon remains 512×512.
- **PNG, RGBA, 8-bit.** Transparent background for items. No semi-transparent pixels except glass-like materials.
- **No anti-aliasing, continuous gradients, blur or photographic textures.** Use hard pixel clusters and deliberate stepped shading. Preview enlarged sprites with nearest-neighbour sampling.
- **Limited palette.** Usually 5–8 shades per material, with natural green, straw, ochre and cream tones. Avoid noisy single-pixel dithering and excessive contrast between adjacent stalks.
- **Botanical structure.** Wheat has tapered stalks with soft lengthwise shading and discreet single-pixel nodes and narrow elongated ears made of small alternating grain clusters, with a few short connected awns. Leave visible stalk between the head and foliage. Avoid thick straight culms, repeated transverse rings and bright node bands that resemble bamboo. Use a few long narrow leaves arching from the base and middle. Mature crops have one discreet basal blade in each plant sprite and six modelled leaves per block, staggered in height and length and arching outward. Keep their material clean and avoid overlapping leaf grids. Attach leaves to the outer culms, keep them below the ears, and align the upper/lower UVs and both halves of each bend. Avoid thick cob-like heads, upper leaves wrapping the ears, sorghum panicles and smooth cattail silhouettes. Sprouts begin at the soil; heads stay connected to stalks.
- **Large pixel clusters over HD detail.** The 32×32 grid is room for stronger forms and material masses, not a Faithful-style thin retexture. Avoid hairline stems, isolated awns, noisy kernel outlines and a dry spiky-grass appearance. The mature silhouette and centre density take priority over tiny botanical marks.
- **Maturity colour.** Keep AGE 0–4 green, introduce yellow-green at AGE 5, use a mixed olive/straw palette at AGE 6, and make AGE 7 stalks, leaves and ears golden straw. Use separate age palettes and hard pixel shading; do not add transverse bands or thicken the stems to show maturity.
- **Natural fields.** Stagger ear height, vary leaf direction and use a small number of deterministic model rotations and alternate sprites. Keep plant bases grounded and leave gaps through the foliage. Fullness comes from several stalks and layered planes, not solid walls of leaves.
- **Wheat variation and height.** Each growth age has four separately authored sprites and four model combinations, with four spatial rotations each. AGE 4–7 gradually extend above one block; AGE 6 uses upper Y=18/20/21/24 and mature AGE 7 uses Y=19/21/23/26. The existing four model combinations also provide these height profiles, with equally weighted position-stable selection. Leaf attachments move with their stalks and each bend keeps its original angle. Preserve the original vanilla interaction outline and harvest from the lower block. Visual height does not create an upper crop block or another registry entry.
- **Top-left lighting**, like vanilla: highlights on the top-left, darkest shade on the bottom-right.
- **Item silhouettes** have a 1-pixel darker outline on the shaded side, matching vanilla food items.
- **Never copy or trace Mojang textures.** Use them only as visual reference.

## Folders

| What | Where | Shipped in jar |
|---|---|---|
| Item textures | `common/src/main/resources/assets/farmerplus/textures/item/<id>.png` | yes |
| Block textures | `common/src/main/resources/assets/farmerplus/textures/block/<id>[_part].png` | yes |
| Vanilla wheat overrides | `common/src/main/resources/assets/minecraft/{blockstates,models,items,textures}/…` | yes |
| Block models (exported) | `common/src/main/resources/assets/farmerplus/models/block/<id>.json` | yes |
| Mod icon | `common/src/main/resources/assets/farmerplus/icon.png` (square, 128×128 or 512×512) | yes |
| Blockbench projects | `art/blockbench/<id>.bbmodel` | no |
| Layered/working files | `art/textures/…` | no |

## Blockbench workflow

1. Create the project as **Java Block/Item**.
   Set texture resolution to **32×32** for wheat models. Minecraft model UVs still use 0–16; Blockbench handles the conversion from texture pixels. Keep UV scale consistent so narrow stalk faces do not compress a full texture onto each side.
2. Keep the model inside the 0–16 block grid when possible (vanilla max is −16…32).
3. Element rotations: Minecraft 26.3 accepts any angle on one axis (`axis` + `angle`) or Euler rotations (`x`, `y`, `z`, applied X → Y → Z). Prefer the simplest rotation that reads well.
4. Keep it cheap: **at most 12 elements** per block model, with a **16-element allowance for AGE 6–7 wheat** and a **24-element allowance for the sheaf with a solid 3D binding**. Wheat crops use **four staggered double-sided plant planes**. AGE 6–7 add six modelled leaves, each built from two connected planes bending up then down, for **sixteen elements total**. These restrained leaf surfaces create depth without repeating foliage on every stalk or adding geometry to every grain head. The sheaf uses eight layered stalk/head planes, one compressed stalk core and fifteen solid cord elements: four joined wrap sections, eight segments forming two open loops, one knot and two hanging ends. The four former ear-core volumes are removed to keep the total at twenty-four elements and ninety-six faces. The cord wraps all four sides and intersects the stalk core; the knot joins the wrap, loops and ends. Remove painted cord from the stalk atlases so the binding appears once. Use the original 32×32 twine atlas for the geometric cord. Its dedicated 16×16 inventory icon is selected through vanilla `minecraft:display_context`; other item contexts retain the 3D block model. No custom renderer, block entity or visual tick handler.
   Strawberry models use the task 0003 budgets: cultivated ages 0–4 allow 8/12/16/20/20 elements; wild models allow 12. A berry uses three solid cuboids with raised shoulders and a corner-oriented Euler tip. Reuse a thin branching stalk plane for a pair of berries where needed to keep the mature model at twenty elements. Keep different red shades and sizes in one plant. Start each crown at Y=-1 and compare selection shapes with every exported arrangement.
5. Name textures exactly as the final resource id (e.g. `wheat_sheaf_side`), and set the texture namespace to `farmerplus` so the exported JSON points at `farmerplus:block/<name>`.
6. Set **Display** transforms for `gui`, `ground`, `fixed`, `thirdperson_righthand` and `firstperson_righthand` so the item looks right in inventories and hands.
7. Save the source as `art/blockbench/<id>.bbmodel`.
8. Export **Block/Item Model** to `models/block/<id>.json` and the textures to `textures/block/`.
9. If the silhouette of a block changes, update the `VoxelShape` in its block class so the outline and collision match.
   Preserve the vanilla crop's outline, collision, growth and interactions. A visual override does not register a second wheat crop.

## Connecting Blockbench to an AI agent (MCP)

The repository ships `.codex/config.toml`, which points Codex at the Blockbench MCP server.

1. Install Blockbench (desktop): <https://www.blockbench.net/downloads>
2. In Blockbench: **File → Plugins → Load Plugin from URL** and paste
   `https://jasonjgardner.github.io/blockbench-mcp-plugin/mcp.js`
3. Keep Blockbench open. The server listens on `http://localhost:3000/bb-mcp`.
4. Codex picks up `.codex/config.toml` for trusted projects. To add it globally instead:
   ```bash
   codex mcp add blockbench --url http://localhost:3000/bb-mcp
   ```
5. Restart Codex and run `/mcp` to confirm `blockbench` is connected.

The plugin can run JavaScript inside Blockbench (`risky_eval`). Leave the server bound to `localhost`.

## Checking your work

```bash
./gradlew :neoforge:runClient
```

Open the **Farmer+** creative tab and check every item in the inventory, in hand, dropped on the ground and placed (for blocks). The log must contain no `farmerplus` texture or model warnings.

Inspect AGE 0–7 in order and a large mature field. Compare the sheaf from the front, side and above. Run `./gradlew build` and `python art/validate_wheat_art.py` to check PNG dimensions/alpha, UV bounds, model dependencies, embedded Blockbench textures and identical assets in Fabric, NeoForge and Forge jars.

See [the wheat visual report](wheat-visuals.md) for the resource-pack override chain, optional standalone pack, reproduction steps and test limitations. Resource-pack priority remains under the player's control.
