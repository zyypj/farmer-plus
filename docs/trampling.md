# Crop trampling

**English** | [Português](trampling.pt-BR.md)

Walking through a field leaves a mark. Crops bend, fall over and, if you keep using the same route, get crushed into a real path. This is geometry, not a texture swap: the stalks are modelled tilted, kinked at the base and lying on the ground in the direction you walked.

![Trampled wheat stages and a crushed path through a field](images/trampled-wheat.png)

*Offline render of the shipped block models (`python art/preview_trampled_wheat.py`), not an in-game screenshot.*

## Stages

| Flattening | Name | What it looks like | Recovers? | Mature drops |
|---|---|---|---|---|
| — | Standing | Vanilla crop | — | 1 wheat + seeds (vanilla) |
| 1 | Bent | Whole stalks leaning 30–47° | Stands back up (≈1 in 3 random ticks) | 1 wheat + seeds (vanilla) |
| 2 | Flattened | Stalks snapped near the base, lying at 70–80° | Young crops rise to *bent* (≈1 in 6); mature stay down | 50% wheat, else 1 seed |
| 3 | Crushed | Short stubs, stalks pressed flat, darker | Never — harvest and replant | 1 seed |

Crops at age 0–1 are too small to be damaged. A bent or flattened crop stops growing until it stands back up. Bone meal only works on *bent* crops.

## What tramples

| Entity | Rule |
|---|---|
| Players | Survival and adventure only. Sneaking never tramples. |
| Mobs | Only types in the `farmerplus:tramples_crops` entity tag (livestock, horses, camels, llamas, goats, sniffers, hoglins, ravagers, bears, pandas). |

Each time an entity **enters** a crop block it applies force:

| Condition | Force |
|---|---|
| Walking | +1 |
| Sprinting | +1 |
| Wide body (≥ 1.2 blocks, e.g. horses, camels) | +1 |

**Jumping or falling** onto a crop no longer turns the farmland into dirt and destroys the plant, as vanilla does: the farmland is kept and the crop is flattened instead (force 2, +1 for falls of 3+ blocks, +1 for wide bodies). Crops without a trampled form yet (e.g. carrots) keep vanilla behaviour.

A walk turns a standing crop *bent*; a sprint or a horse flattens it at once; repeated passes crush it. The stalks fall in the direction of movement, so paths read naturally.

## Configuration

Game rules (per world):

```text
/gamerule farmerplus:crop_trampling true|false
/gamerule farmerplus:mob_crop_trampling true|false
```

Add or remove mobs with a data pack overriding `data/farmerplus/tags/entity_type/tramples_crops.json`.

## Performance

- Two mixins. `CropBlockMixin` hooks `CropBlock#entityInside`, which Minecraft only calls while an entity overlaps a crop; it exits after a few field reads unless the entity just stepped into a new block. `FarmlandBlockMixin` hooks `FarmlandBlock#turnToBaseBlock`, which only runs when something lands hard on farmland.
- No tick handlers, no block entities, no per-entity state. Progress lives in the block state.
- Recovery uses vanilla random ticks, and only *bent* or young *flattened* crops tick at all. Crushed paths and mature flattened crops cost nothing.
- Rendering is plain baked block models: 6–8 elements per model, fewer than the mature standing wheat (16).

## Other plants

Any block can be trampled by implementing `Trampleable#trample(state, force, direction)` and calling `CropTrampling.onEntityInside` from its own `entityInside` — no mixin needed for Farmer+ blocks. Strawberries do this with a `flattening` property (0–3) on the plant itself; see [strawberries.md](strawberries.md#trampling).

## Adding trampling to another vanilla crop

1. Register a `TrampledCropBlock` that points at the standing crop:
   ```java
   public static final RegistryEntry<TrampledCropBlock> TRAMPLED_CARROTS = FarmerRegistries.block("trampled_carrots",
           properties -> new TrampledCropBlock(() -> (CropBlock) Blocks.CARROTS, properties),
           TrampledCropBlock::cropProperties);
   ```
2. In the module's `register()`: `TrampleableCrops.register(TRAMPLED_CARROTS);`
3. Add its blockstate/models (see `art/trampled_wheat.py`), loot table, translations and the `minecraft:crops`, `minecraft:maintains_farmland` and `minecraft:washed_away_by_fluids` tags.

## Models

`art/trampled_wheat.py` generates `blockstates/trampled_wheat.json`, 48 models (`trampled_wheat_stage<age>_<flattening>` plus a texture-swapped `_variant1`) and final native 16×16 AGE 0–7 `wheat_stage<age>[_alternate]_crushed.png` textures through `art/crushed_pixels.py`. The unused AGE 0–1 crushed sprites also use separately authored 16×16 stubs. All 48 models retain their original geometry and 0–16 UV coordinates. See [the wheat art report](wheat-visuals.md). Models are authored falling north and rotated by the blockstate for the other directions. Minecraft 26.3 accepts any rotation angle and Euler `x`/`y`/`z` rotations, which the bent and fallen stalks rely on.

```bash
python art/trampled_wheat.py
```
