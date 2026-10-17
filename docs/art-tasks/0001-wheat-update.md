# Art task 0001 — Wheat update

**English** | [Português](0001-wheat-update.pt-BR.md)

The files below currently contain **placeholder art**. Replace each one in place, keeping the exact path and name.

Base path: `common/src/main/resources/assets/farmerplus/`

## Item textures (16×16)

| File | Subject | Reference mood |
|---|---|---|
| `textures/item/flour.png` | A small heap of white flour, slightly warm off-white, soft shadow at the base | vanilla sugar / bone meal |
| `textures/item/dough.png` | A round ball of raw bread dough, pale beige, with a darker fold line | vanilla bread, but rounder and paler |
| `textures/item/wheat_porridge.png` | A wooden bowl filled with creamy porridge, a few visible wheat grains on top | vanilla mushroom stew / beetroot soup bowl |

## Wheat Sheaf block (Blockbench)

A bundle of harvested wheat stalks standing upright, tied around the middle with a twine band, ears of grain fanning out at the top. Think "harvest stook", not a hay bale.

| File | Content |
|---|---|
| `art/blockbench/wheat_sheaf.bbmodel` | Blockbench source (Java Block/Item) |
| `models/block/wheat_sheaf.json` | Exported model, ≤ 24 elements with solid 3D binding, parent-free with full `display` transforms |
| `textures/block/wheat_sheaf_side.png` | Stalk material; the twine band is separate geometry |
| `textures/block/wheat_sheaf_top.png` | Top view: grain ears / cut stalks |

Extra textures are allowed (e.g. `wheat_sheaf_ears.png`) if the model needs them.

The current direction is Realistic Vanilla+: native 32×32 pixel art, a narrow visible twine band, individual splayed stalks and fuller overlapping grain heads. All sheaf block textures use 32×32, including the added stalk fan and twine atlas.

The sheaf also has a native 16×16 `textures/item/wheat_sheaf.png` and `models/item/wheat_sheaf.json` for inventories. The existing `items/wheat_sheaf.json` selects that icon for `gui` and keeps the 3D block model in other contexts. The existing `textures/block/wheat_sheaf_bound_stalks.png` path is retained but contains clean stalks. The binding is actual geometry using `wheat_sheaf_twine.png`: a closed four-sided wrap, two open loops, a raised knot and two hanging ends. Eight plant cards, one compressed core and fifteen cord elements total twenty-four elements; this is the sheaf-specific allowance. Crop budgets stay unchanged.

## Vanilla wheat

Replace `minecraft:wheat` AGE 0–7 through `assets/minecraft/`, preserving vanilla mechanics and resource-pack priority. Each age has four distinct 32×32 botanical sprites combined into four model variants, each with four rotations. Crops use four staggered double-sided plant elements; AGE 6–7 add six outward-curved leaves at staggered heights, each with two connected model segments, totalling sixteen elements. Stalks and leaves stay green at AGE 0–4, turn yellow-green at AGE 5, olive/straw at AGE 6, and golden straw at AGE 7. Mature ears must read as narrow grain clusters with subtle awns. Keep leaves sparse and clean, with visible stalks and restrained basal foliage; fullness comes primarily from the ears and layered stems. AGE 4–7 gradually gain height; AGE 6 uses four upper heights (18/20/21/24) and mature AGE 7 uses 19/21/23/26. The tallest profile reaches about 1.69 blocks including its buried base. Save the six added height source projects as `wheat_stage6_variant1..3.bbmodel` and `wheat_stage7_variant1..3.bbmodel`; exported variant paths stay unchanged. The vanilla interaction outline stays unchanged, so harvest at the original lower block.

Update the wheat and seed items in place using native 16×16 pixel art. See [the visual report](../wheat-visuals.md) for paths, previews, verification and the standalone optional pack.

Current collision/outline box is 12×16×12 centred (`Block.column(12.0, 0.0, 16.0)` in `WheatSheafBlock`). If the final silhouette is clearly narrower or wider, update that value.

## Mod icon

| File | Content |
|---|---|
| `icon.png` | 512×512, pixel-art style: a golden wheat bundle over a tilled farmland block, clean background. Readable at 64×64. |

## Done when

- [ ] All files above replaced, same names.
- [ ] `./gradlew :neoforge:runClient` shows the items correctly in the Farmer+ creative tab, in hand and on the ground; the sheaf looks right placed in the world.
- [ ] No `farmerplus` model/texture warnings in the log.
