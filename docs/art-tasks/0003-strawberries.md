# Art task 0003 — Strawberries (3D models)

**English** | [Português](0003-strawberries.pt-BR.md)

Gameplay is done ([docs/strawberries.md](../strawberries.md)). The plant currently renders as flat placeholder cross planes. Build **real 3D Blockbench models**: a low strawberry rosette with trifoliate leaves, white flowers and berries that hang over the edge of the plant, like a field of cultivated strawberries on raised rows.

Read first: [AGENTS.md](../../AGENTS.md), [art-pipeline.md](../art-pipeline.md). Use the Blockbench MCP server.

Base path: `common/src/main/resources/assets/farmerplus/`

## Reference: what a real strawberry plant looks like

- A **crown** at soil level; everything grows out of it. No visible woody stem.
- **Trifoliate leaves**: each leaf is three oval leaflets with **serrated edges** on one petiole (leaf stalk) 2–5 px long. Leaflets are bright/mid green on top, paler underneath, with a visible central vein. Leaves fan out and arch, mature plants reach ~6–7 px high and nearly the full block wide.
- **Flowers**: five rounded white petals around a yellow-green centre, ~3 px across, on thin stalks that rise slightly above or between the leaves.
- **Berries** hang from thin arching stalks and **droop over the edge** of the plant, often touching or lying near the soil. Cone/heart shaped, wider at the top, with a green **calyx** (star of small sepals) on top and small yellow **seeds (achenes)** on the surface.
  - Unripe: pale green → whitish, small.
  - Ripe: glossy red, a little darker at the bottom/shade side, larger.
- Older leaves near the base can be darker; one or two slightly yellowed leaves add realism.

## Style

Realistic Vanilla+, same as the wheat: recognisable Minecraft pixel art, hard pixels, no anti-aliasing, limited palette, top-left lighting. **Textures 32×32.** Never trace Mojang textures.

## Models to create

| Age | Model | Must show | Element budget |
|---|---|---|---|
| 0 | `models/block/strawberry_plant_stage0.json` | Tiny crown, 2–3 young leaves | ≤ 8 |
| 1 | `models/block/strawberry_plant_stage1.json` | Full rosette, 5–7 leaves arching outward | ≤ 12 |
| 2 | `models/block/strawberry_plant_stage2.json` | Rosette + 3–5 white flowers | ≤ 16 |
| 3 | `models/block/strawberry_plant_stage3.json` | Rosette + 3–5 small green/white berries, 1 leftover flower | ≤ 20 |
| 4 | `models/block/strawberry_plant_stage4.json` | Rosette + 4–6 ripe red berries drooping over the edge | ≤ 20 |

For **each** age also create three variations, `strawberry_plant_stage<age>_variant1..3.json` (different leaf arrangement and berry positions — not just a texture swap), and update `blockstates/strawberry_plant.json` so every age picks one of the 4 models with 4 `y` rotations (16 equally weighted alternatives, like `blockstates/wheat.json` in `assets/minecraft`).

**Wild strawberries** (`blockstates/wild_strawberries.json`): smaller, sparser and lower than the cultivated plant, with fewer and smaller berries (2–3 when ripe). Create `models/block/wild_strawberries_stage<age>.json` (+ `_variant1`), budget ≤ 12 elements, and point the wild blockstate at them.

### Geometry rules

- Block coordinates: the farmland surface is at **y = −1**, so the crown starts at y = −1 to touch the soil (like the wheat models).
- **Berries are real cuboids**, not flat sprites: ~2 × 2.5 × 2 px (ripe) and ~1.5 × 2 × 1.5 px (unripe), with seeds painted on all sides and the calyx on top. They hang from thin stalk planes and sit **outside the leaf rosette**, partly over the block edge (x/z may go slightly beyond 0–16, up to −2…18).
- **Leaves** are thin double-sided planes (or 0.1 px cuboids) angled with rotation. 26.3 accepts any angle and Euler `x`/`y`/`z` rotations — use them so each leaflet tilts and arches naturally. Group a trifoliate leaf into one textured plane when possible to save elements.
- Keep plants **low**: max height ~7 px above the soil for age 4. If the final silhouette is clearly taller or smaller, update `SHAPES` in `content/strawberry/StrawberryPlantBlock.java` (one `Block.column(...)` per age).
- Set `"ambientocclusion": false`, use `"shade_direction_override": "up"` on leaves like the wheat, give every model a `particle` texture.

### Textures (32×32, `textures/block/`)

| File | Content |
|---|---|
| `strawberry_leaf.png` | Trifoliate leaf atlas: 2–3 leaf shapes (young, mature, slightly yellow), serrated edges, central vein, top and underside tones |
| `strawberry_flower.png` | Flower top view + side view, five white petals, yellow centre |
| `strawberry_fruit.png` | Atlas for berry cuboid faces: ripe red with seeds, unripe green/white with seeds, calyx top |
| `strawberry_stem.png` | Thin petiole / fruit stalk strips, crown base |

Extra textures are fine if needed. Remove the placeholder `strawberry_plant_stage0..4.png` once nothing references them.

### Item

| File | Content |
|---|---|
| `textures/item/strawberry.png` | 32×32 ripe strawberry: heart-shaped, glossy red with yellow seeds, green calyx and short stalk, 1-px darker outline on the shaded side |

## Save and export

- Blockbench sources: `art/blockbench/strawberry_plant_stage<age>[_variantN].bbmodel` and `art/blockbench/wild_strawberries_stage<age>[_variant1].bbmodel`.
- Export Java Block/Item models to the paths above with textures referenced as `farmerplus:block/<name>`.

## Done when

- [x] 5 ages × 4 variations for the cultivated plant, 5 ages × 2 for wild, blockstates updated.
- [x] Item texture replaced.
- [x] Element budgets respected; berries are 3D and hang over the edge; no floating parts.
- [x] `./gradlew build` passes and `./gradlew :neoforge:runClient` shows no `farmerplus` model/texture warnings.
- [ ] In game: a 9×9 farmland field with all ages reads as a real strawberry field from 5 and 20 blocks away; ripe berries are clearly visible from standing height.

Implementation and current verification: [visual report](../strawberry-visuals.md). The final manual in-game 9×9 distance check remains open.
