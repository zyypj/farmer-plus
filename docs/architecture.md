# Architecture

**English** | [Português](architecture.pt-BR.md)

## Project layout

```
farmer+/
├── common/      Shared code and every asset/data file. Compiled against plain vanilla.
├── fabric/      Fabric entrypoint + Fabric implementation of the platform interfaces.
├── neoforge/    NeoForge entrypoint + NeoForge implementation.
├── forge/       Forge entrypoint + Forge implementation.
├── build-logic/ Gradle conventions shared by all subprojects.
├── art/         Source art (Blockbench .bbmodel files, layered textures). Never shipped.
└── docs/        Documentation (English + Portuguese).
```

Rule of thumb: **if it can live in `common`, it lives in `common`.** Loader folders only contain the code that a specific loader API forces on us.

## Layers

```
content/<feature>      What the mod adds (wheat, tomato, soils, …)
        │ uses
core/                  Reusable building blocks: modules, registries, creative tab
        │ calls
platform/              Interfaces that each loader implements
        │ implemented by
fabric/ neoforge/ forge/
```

### `core/module`

Every feature is a **module** that implements `FarmerModule`:

```java
public interface FarmerModule {
    String id();
    void register();
    List<ItemLike> creativeTabItems();
}
```

Modules are listed, in display order, in `FarmerModules`. Turning a feature off is one line, and features never reach into each other's classes.

### `core/registry`

`FarmerRegistries` wraps registration with the same shape vanilla uses in `Items` and `Blocks`:

```java
FarmerRegistries.item("flour", () -> new Item.Properties().compostable(...));
FarmerRegistries.block("wheat_sheaf", WheatSheafBlock::new, () -> BlockBehaviour.Properties.of()...);
FarmerRegistries.blockItem(WheatBlocks.WHEAT_SHEAF, Item.Properties::new);
```

Every call returns a `RegistryEntry<T>`, a lazy `Supplier<T>` that is safe to hold in a `static final` field. Call `.get()` only after registration has finished (inside game logic, never in static initialisers of other content).

### `platform`

`RegistrationPlatform` is the only contract a loader must fulfil. It is discovered through `java.util.ServiceLoader`:

| Loader | Implementation | Strategy |
|---|---|---|
| Fabric | `FabricRegistrationPlatform` | Registers immediately into the built-in registries |
| NeoForge | `NeoForgeRegistrationPlatform` | One `DeferredRegister` per registry, bound to the mod bus |
| Forge | `ForgeRegistrationPlatform` | One `DeferredRegister` per registry, bound to the mod bus group |

Each loader entrypoint does exactly two things: call `FarmerPlus.init()` and, on NeoForge/Forge, bind the deferred registers.

## Performance rules

Farmer+ must stay invisible on a profiler.

1. **No mixins** unless there is no data-driven or API alternative, and never in hot paths (rendering, ticking, pathfinding). Every mixin lives in `common/…/mixin`, is listed in `farmerplus.mixins.json` and is documented with its reason. Current list: `CropBlockMixin` — the only way to react to entities walking through vanilla crops; `FarmlandBlockMixin` — keeps farmland and flattens the crop when something lands on it ([trampling](trampling.md)); `FireBlockAccessor` — an invoker used once at startup to give Farmer+ wood vanilla flammability ([avocado](avocado.md#wood-set)).
2. **No tick handlers.** Use block random ticks, scheduled ticks or vanilla mechanics instead.
3. **Prefer data over code.** Composting, fuel, food, villager food, tool behaviour and loot are vanilla data components or JSON — use them.
4. **No reflection, no runtime classpath scanning, no config libraries** for things a data pack can already express.
5. **Static shapes.** `VoxelShape`s are computed once in `static final` fields.

## Systems

| System | Package | Docs |
|---|---|---|
| Crop trampling | `core/trampling` | [trampling.md](trampling.md) |
| Biome features (worldgen) | `core/worldgen` | [strawberries.md](strawberries.md#modpack-compatibility) |
| Strawberries | `content/strawberry` | [strawberries.md](strawberries.md) |
| Wood sets | `core/wood`, `tools/wood_set.py` | [avocado.md](avocado.md#reusing-the-wood-set) |
| Avocado tree | `content/avocado` | [avocado.md](avocado.md) |

## Adding a new crop (checklist)

1. Create `content/<crop>/` with `<Crop>Module`, `<Crop>Blocks`, `<Crop>Items` and, if needed, `<Crop>Foods`.
2. Register the module in `FarmerModules`.
3. Add assets in `common/src/main/resources/assets/farmerplus/`:
   - `blockstates/<id>.json`, `models/block/…`, `models/item/…`, `items/<id>.json`
   - textures under `textures/block` and `textures/item` (see [art-pipeline.md](art-pipeline.md))
   - translations in **both** `lang/en_us.json` and `lang/pt_br.json`
4. Add data in `common/src/main/resources/data/`:
   - `farmerplus/recipe/…` plus a matching `farmerplus/advancement/recipes/<category>/…` unlock
   - `farmerplus/loot_table/blocks/…` for every block
   - tool tags (`minecraft:mineable/*`) and `c:` convention tags for shared ingredients
5. `./gradlew build`, then start a dev client on at least one loader and a dev server on the other two.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Registry id | `snake_case` | `wheat_porridge` |
| Module class | `<Feature>Module` | `WheatModule` |
| Holder classes | `<Feature>Blocks`, `<Feature>Items`, `<Feature>Foods` | `WheatItems.FLOUR` |
| Block classes | `<Name>Block` | `WheatSheafBlock` |
| Loader classes | `<Loader><Role>` | `NeoForgeRegistrationPlatform` |

## Code style

- Java 25, 4-space indentation, imports instead of fully-qualified names.
- No comments: names and small methods carry the meaning.
- Constants instead of magic numbers (`FALL_DAMAGE_MULTIPLIER`).
- Classes are `final` unless they are meant to be extended (blocks and items are).
