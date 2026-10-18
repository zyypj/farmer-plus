# Changelog

**English** | [Português](CHANGELOG.pt-BR.md)

## Unreleased

### Added
- Banana plant: a pseudostem with young, mature and dry hanging leaves, one bunch per stem (bud, flowering, green, ripe) harvested whole and carried on the shoulder (heavy), crafted into 8 bananas or stood on the ground to pick bananas one by one, die-back after fruiting with a follower sucker, clumps, and wild clumps in jungles.
- Avocado tree: a realistic broadleaf tree (orchard tree from one sapling, wild giant from 2×2 saplings and jungles) whose leaves flower and fruit repeatedly; avocados hang under the leaves as their own block with a hitbox and are picked with right-click.
- Slim avocado wood: the tree grows from connecting `avocado_trunk` (10 px) and `avocado_branch` (6 px) blocks instead of full logs; the trunk drops logs, branches drop sticks.
- Avocado wood set (logs, wood, stripped variants, planks, stairs, slab, fence, fence gate, door, trapdoor, pressure plate, button, sign, hanging sign, shelf, boat, boat with chest) mirroring every oak tag, recipe, fuel value and flammability.
- Strawberries: a perennial crop planted only on farmland, with seedling, leafy, flowering, green and ripe stages, right-click harvesting and runners that spread to neighbouring farmland.
- Strawberry trampling: bent, flattened and crushed plants with fallen berries; damaged plants yield fewer strawberries.
- Strawberry jam: craft a glass bottle with 1–3 strawberries, eat it one portion at a time, place it as decoration facing you and refill it with strawberries.
- Wild strawberries generating in plains, meadows and forests (`farmerplus:has_wild_strawberries` biome tag).
- Crop trampling: walking bends crops, sprinting or riding flattens them and repeated passes crush them into paths, with modelled bent, snapped and flattened stalks.
- Jumping or falling on crops flattens them instead of turning the farmland into dirt.
- Trampled crops recover over time; crushed mature wheat only drops seeds. Sneaking never tramples.
- `farmerplus:crop_trampling` and `farmerplus:mob_crop_trampling` game rules and the `farmerplus:tramples_crops` entity tag.

## 0.1.0 — Wheat update

### Added
- Flour, crafted from wheat.
- Dough, crafted from flour and a water bucket; bakes into bread in a furnace, smoker or campfire.
- Wheat Porridge, a bowl food that restores 7 hunger.
- Wheat Sheaf, a decorative block that reduces fall damage like a hay bale.
- `c:flours`, `c:flours/wheat`, `c:doughs`, `c:doughs/wheat` and `c:foods/soup` convention tags.
- Farmer+ creative tab.
- English and Brazilian Portuguese translations.
- Fabric, NeoForge and Forge support for Minecraft 26.3.
- Realistic Vanilla+ wheat visuals: original 16×16 art for all eight stages, four variations per stage, taller mature crops, redrawn wheat and seeds.
- 3D Wheat Sheaf model with a solid cord binding and a dedicated inventory icon.
- Optional standalone wheat resource pack (`./gradlew wheatVisualPack`).
- Final art for flour, dough, porridge and the mod icon.
