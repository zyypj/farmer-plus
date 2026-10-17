# Avocado tree

**English** | [Português](avocado.pt-BR.md)

A full-size fruit tree with a complete, vanilla-compatible wood set. Wild avocado trees grow in jungles; their leaves flower, set fruit and ripen again and again.

## The tree

- **Size:** 10–15 blocks tall with a broad, rounded crown built from branching limbs (`minecraft:fancy_trunk_placer` + `minecraft:fancy_foliage_placer`, radius 3), close to a real 9–12 m avocado tree.
- **Sapling:** grows like a vanilla sapling but at half the speed (≈1 in 14 random ticks per stage, light 9+). It needs room for the whole crown.
- **Wild trees:** sparse jungle, jungle and bamboo jungle (`farmerplus:has_avocado_trees`), about one tree every six chunks.
- The tree is pure data: `data/farmerplus/worldgen/feature/avocado_tree.json`. Tweak the trunk and foliage there.

## Fruiting

Only **natural** leaves (placed by the tree, not by players) bear fruit, and only those with **air below** and on a sparse pattern, so a mature tree carries a realistic handful of avocados (about 5% of its leaves).

| Stage | `fruit` | Looks like | Next stage |
|---|---|---|---|
| Leaves | 0 | Plain leaves | Flowers (≈1 in 24 random ticks) |
| Flowering | 1 | Small yellow-green flowers under the leaves | Green fruit (≈1 in 8) |
| Unripe | 2 | Small green avocados hanging | Ripe (≈1 in 10) |
| Ripe | 3 | Large dark avocados hanging | Falls on its own (≈1 in 40) |

- **Pick:** right-click ripe leaves to get an avocado; the leaves start a new cycle, so a tree fruits many times.
- **Breaking** ripe leaves also drops the avocado. Leaves drop saplings (5%) and **sticks** like oak leaves; shears or Silk Touch give the leaves block.
- Avocado: 4 hunger, 0.6 saturation; villagers eat it; compostable.

## Wood set

`avocado_log`, `avocado_wood`, `stripped_avocado_log`, `stripped_avocado_wood`, `avocado_planks`, `avocado_stairs`, `avocado_slab`, `avocado_fence`, `avocado_fence_gate`, `avocado_door`, `avocado_trapdoor`, `avocado_pressure_plate`, `avocado_button`, `avocado_leaves`, `avocado_sapling`.

The set mirrors oak everywhere it matters:

- **Tags:** every vanilla tag that lists an oak block lists the avocado equivalent (`minecraft:logs_that_burn`, `minecraft:planks`, `minecraft:wooden_*`, `minecraft:fence_gates`, `minecraft:leaves`, `minecraft:saplings`, …). Planks therefore work in **every** wooden recipe — crafting tables, sticks, chests, tools, barrels — and logs work in campfires, charcoal and so on.
- **Recipes and loot:** same as oak (planks from `#farmerplus:avocado_logs`, wood, stairs, slabs, fences, gates, doors, trapdoors, plates, buttons).
- **Stripping:** right-click a log or wood with any axe (`#minecraft:axes`). The log handles it itself, so no shared vanilla file is overridden.
- **Fuel:** same burn times as oak through the `minecraft:cooking_fuel` item component.
- **Fire:** same flammability as oak. Fabric and Forge use the vanilla fire table (`FireBlockAccessor`), NeoForge uses its data map (`data/neoforge/data_maps/block/flammable.json`).

Signs, hanging signs, boats and shelves are not included yet.

## Reusing the wood set

`WoodSets.register(name, woodColor, barkColor)` registers the 13 wood blocks and items. `python tools/wood_set.py <name>` generates their blockstates, models, item definitions, loot tables, recipes, recipe unlocks and tag entries from the vanilla oak templates. Leaves, sapling, tree feature and textures are per tree.

## Art

Textures are placeholders; see [art task 0005](art-tasks/0005-avocado-tree.md).
