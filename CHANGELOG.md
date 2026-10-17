# Changelog

**English** | [Português](CHANGELOG.pt-BR.md)

## Unreleased

### Added
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
- Realistic Vanilla+ wheat visuals: original 32×32 art for all eight stages, four variations per stage, taller mature crops, redrawn wheat and seeds.
- 3D Wheat Sheaf model with a solid cord binding and a dedicated inventory icon.
- Optional standalone wheat resource pack (`./gradlew wheatVisualPack`).
- Final art for flour, dough, porridge and the mod icon.
