# Art task 0006 — Banana plant

**English** | [Português](0006-banana-plant.pt-BR.md)

Gameplay is done ([docs/banana.md](../banana.md)). The placeholder art has been replaced **in place**, preserving every existing name. See [the visual report](../banana-visuals.md) for previews, multipart fruit geometry, verification and the pending 20-block check. Do not rerun the original `art/banana_art.py` generator over the final art.

Read first: [AGENTS.md](../../AGENTS.md), [art-pipeline.md](../art-pipeline.md). **16×16** textures, hard pixels, Realistic Vanilla+. Use the Blockbench MCP server for the 3D models and save sources as `art/blockbench/<model>.bbmodel`.

Base path: `common/src/main/resources/assets/farmerplus/`

## Reference: the real plant

- **Pseudostem:** not wood — tightly rolled leaf sheaths. Yellow-green to mid green with long vertical sheath edges, irregular blackish-brown and purple-brown blotches (typical of Prata/Cavendish), strips of dry brown sheath peeling off near the base.
- **Leaves:** enormous paddles, 1.5–3 m × 0.4–0.9 m, glossy mid green on top, paler underneath, a thick pale yellow-green midrib, fine parallel veins running almost straight out from the midrib to the edge. Wind **tears the blade along the veins** into strips, mostly near the edges. Young leaves come out of the top as a pale rolled "cigar", rise, and arch over as they age. Dead leaves turn straw-brown and hang down along the stem.
- **Bunch:** hangs from the crown on a thick green stalk; hands of fingers in a spiral around the stalk, fingers curving **up**; green and ridged when unripe, yellow with a few brown sugar spots when ripe, dark dried flower tips. Below the hands, a bare stalk ends in the **male bud** ("heart"): a teardrop of glossy deep maroon-purple bracts with a waxy bloom.
- **Sucker:** a young shoot with narrow upright "sword" leaves, often with red-brown spots.

## Textures (`textures/block/`, 16×16)

| File | Content |
|---|---|
| `banana_stem.png` | Pseudostem side (vertical sheaths, blotches, dry strips). Used on the 6 px column |
| `banana_stem_top.png` | Cut pseudostem: concentric pale sheath rings, cream centre |
| `banana_leaf.png` | Middle of a blade, **midrib vertical in columns 7–8**, tip towards the top row; left/right halves fill the whole width; torn slits as transparent pixels along the veins |
| `banana_leaf_tip.png` | Same leaf narrowing to a point at the **top** row; the lower rows are also used, flipped, for the rounded blade base |
| `banana_leaf_dry.png` | Dead straw-brown leaf, heavily torn, narrowing towards the **bottom** row (it hangs) |
| `banana_heart.png` | Male bud bracts, deep maroon-purple with waxy bloom |
| `banana_fingers_green.png` | Unripe fingers seen side by side (vertical fingers, dark tips on rows 0 and 8) |
| `banana_fingers_ripe.png` | Ripe yellow fingers, a few sugar spots, dark tips |
| `banana_sapling.png` | Cross sprite of a sucker |

Items (`textures/item/`): `banana.png` (a single ripe banana), `banana_leaf.png` (a whole leaf seen flat).

## Models (`models/block/`, Blockbench)

Keep the names and the attachment points — the code places blocks next to each other and the pieces must join.

| Model | Rules |
|---|---|
| `banana_stem_base`, `banana_stem_middle`, `banana_stem_crown` | Column **x/z 5–11** (6 px). The base may flare to 8 px at the bottom; the crown ends with leaf sheaths and the rolled cigar leaf rising above the block. Leaf petioles touch the column at z = 21 of the neighbouring leaf block, so do not make the column thinner |
| `banana_leaf_<age>_base`, `_blade`, `_tip` (`young`, `mature`) | A leaf pointing **north** from a stem to the south. The base starts at the stem (z = 21, beyond the block) and ends at z = 0; the next segment starts at z = 16 at the same height. Ages differ only in pose: young rises, mature arches and droops |
| `banana_leaf_<age>_diagonal_base`, `_diagonal_tip` | The same leaf pointing **north-east** (`y = -45` element rotation): the base starts at the stem centre (−8, 24) and ends at the block corner (16, 0); the tip runs from corner (0, 16) to beyond (16, 0) |
| `banana_leaf_dry` | A dead leaf hanging down the stem side, from the petiole (z = 21) down to y ≈ −14 |
| `banana_bunch_bud`, `_flowering`, `_green`, `_ripe` | Stem to the **north** (z < 0). Stalk from the stem at the top, hands from about y = 16 down to 0, the bare stalk and the purple bud hanging below the block (down to y ≈ −8). Bud only for `bud`; two small hands plus a big bud for `flowering`; four big hands for `green` and `ripe` |

Limits: ≤ 12 elements per model, coordinates between −16 and 32, `ambientocclusion: false`. `python art/banana_art.py` rewrites these models, so once they are hand-made, stop running it (or delete the model part) — it never overwrites textures.

## Harvested bunch

| File | Rules |
|---|---|
| `models/block/harvested_banana_bunch_stalk` | The harvested bunch stands **upright** as a multipart: this model (the rachis inside the hands and the short cut stub on top that the player holds) plus the 8 `banana_bunch_ripe_hand_<tier>_<half>` pieces, which disappear one by one from the bottom up. The code pops each banana from the centre of its piece, so if the hands change, update `HAND_CENTERS` in `HarvestedBananaBunchBlock`. Generated by `python art/banana_bunch_art.py` |
| `items/banana_bunch.json` and `models/item/banana_bunch_*.json` | A composite item (stub + 8 hands). Tune the `display` (the same in every piece) in Blockbench: `thirdperson_righthand` must rest the bunch **on the right shoulder** while the arm is raised (the arm pose comes from code), `firstperson_righthand` shows it on the shoulder at the top-right of the screen, `gui` shows the whole bunch |

## Leaf hitboxes

Leaf hitboxes follow the leaf models: `python art/banana_leaf_shapes.py` voxelizes every `banana_leaf` variant (2 px cells, y from −16 to 32) into `common/src/main/resources/farmerplus/shapes/banana_leaf.json`, which `BananaLeafBlock` loads. **Run it again after any change to a leaf model or to `blockstates/banana_leaf.json`.**

## Done when

- [x] All files above replaced with the same names; `./gradlew build` and `python art/validate_wheat_art.py` pass.
- [x] `python art/preview_world_models.py` (see [docs/banana.md](../banana.md)) shows connected leaves with no gaps at the segment joins, in all 8 directions.
- [ ] In game, from 20 blocks away the plant reads as a banana: pale green pseudostem, huge torn leaves, a bunch with a purple bud.

The last item remains pending: the in-game screenshot has no measured camera distance and desktop inspection was stopped by the user. Solid individual fruit adds twenty half-hand models through vanilla multipart; each model respects the 12-element limit, while the assembled green/ripe bunch totals 104 elements. See the report before reviewing performance.
