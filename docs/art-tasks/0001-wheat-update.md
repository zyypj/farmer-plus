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
| `models/block/wheat_sheaf.json` | Exported model, ≤ 12 elements, parent-free with full `display` transforms |
| `textures/block/wheat_sheaf_side.png` | Stalks seen from the side, with the twine band |
| `textures/block/wheat_sheaf_top.png` | Top view: grain ears / cut stalks |

Extra textures are allowed (e.g. `wheat_sheaf_ears.png`) if the model needs them.

Current collision/outline box is 12×16×12 centred (`Block.column(12.0, 0.0, 16.0)` in `WheatSheafBlock`). If the final silhouette is clearly narrower or wider, update that value.

## Mod icon

| File | Content |
|---|---|
| `icon.png` | 512×512, pixel-art style: a golden wheat bundle over a tilled farmland block, clean background. Readable at 64×64. |

## Done when

- [ ] All files above replaced, same names.
- [ ] `./gradlew :neoforge:runClient` shows the items correctly in the Farmer+ creative tab, in hand and on the ground; the sheaf looks right placed in the world.
- [ ] No `farmerplus` model/texture warnings in the log.
