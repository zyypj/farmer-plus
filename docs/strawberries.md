# Strawberries

**English** | [Português](strawberries.pt-BR.md)

Strawberries behave like a berry bush — pick the fruit and the plant keeps producing — but they are **planted like crops, only on farmland**. In the wild you find a smaller relative, **wild strawberries**, that grows on grass and gives you your first berries.

## Getting started

1. Find **wild strawberries** in plains, sunflower plains, meadows, forests, flower forests, birch forests and dappled forests.
2. Right-click a ripe patch to pick 1–2 strawberries (or break it for the same).
3. Plant a strawberry on **farmland**. It will not go on grass or dirt.

## Growth

| Age | Stage | Notes |
|---|---|---|
| 0 | Seedling | Small crown with a few leaves |
| 1 | Leafy | Full rosette of trifoliate leaves |
| 2 | Flowering | White five-petal flowers |
| 3 | Green fruit | Unripe berries; cannot be picked |
| 4 | Ripe | Red berries; right-click to pick |

- Needs light level 9+. Grows faster on **hydrated** farmland (≈1 in 5 random ticks) than on dry farmland (≈1 in 8).
- **Picking** (right-click a ripe plant) drops 2–4 strawberries and sends the plant back to *flowering*, so it fruits again.
- **Breaking** returns the plant (1 strawberry), plus 1–3 more if it was ripe (Fortune applies).
- **Runners:** while flowering or fruiting, a plant occasionally sends a runner that roots on an adjacent **empty farmland** block, just like real strawberries. Paths, grass and dirt stop them.
- Bone meal advances one stage.
- Eating a strawberry restores 2 hunger. Villagers can eat them; they are compostable.

## Wild strawberries

Wild strawberries grow on grass/dirt, never on farmland, grow slowly (≈1 in 10 random ticks), do not spread and yield 1–2 berries. They exist so players can start a farm without new recipes or trades.

## Modpack compatibility

- Cultivated plants accept any block in `minecraft:supports_crops`, so modded farmland that joins this tag works.
- Strawberries are in `c:foods/berry` and `c:foods/fruit`.
- Wild generation is controlled by the biome tag `farmerplus:has_wild_strawberries` (data packs can add or remove biomes) and the placed feature `farmerplus:patch_wild_strawberries`.

| Loader | How wild strawberries are added to biomes |
|---|---|
| NeoForge | `data/farmerplus/neoforge/biome_modifier/wild_strawberries.json` |
| Forge | `data/farmerplus/forge/biome_modifier/wild_strawberries.json` |
| Fabric | `FabricWorldgen`, which reads `BiomeFeatures` from common code |

When adding a new biome feature, register it in `BiomeFeatures` (Fabric) **and** add matching NeoForge and Forge biome modifier files.

## Performance

No tick handlers or mixins. Plants use vanilla random ticks only until they are ripe; ripe plants stop ticking. Harvest drops come from data-driven loot tables (`harvest/strawberry_plant`, `harvest/wild_strawberries`).

## Art

The five ages now use native 3D models with four cultivated and two wild arrangements each. See [the visual report](strawberry-visuals.md) for source projects, geometry, selection shapes and validation, and [art task 0003](art-tasks/0003-strawberries.md) for the acceptance checklist.
