# Art task 0004 — Strawberry jam jar

**English** | [Português](0004-strawberry-jam.pt-BR.md)

Gameplay is done ([docs/strawberries.md](../strawberries.md#strawberry-jam)). The jar currently uses placeholder boxes. Build a **real 3D Blockbench jar** that can sit on a table as decoration and visibly fills with 1, 2 or 3 portions.

Read first: [AGENTS.md](../../AGENTS.md), [art-pipeline.md](../art-pipeline.md). Use the Blockbench MCP server. Strawberry art uses **16×16** textures (see `art/strawberry_pixels.py`).

Base path: `common/src/main/resources/assets/farmerplus/`

## Look

A small country-style preserve jar:
- **Glass body**: short and round-shouldered, slightly wider than tall, clear glass with a subtle blue-green tint on the edges and one vertical highlight. Glass pixels may be semi-transparent (the only allowed exception).
- **Jam inside**: deep glossy red with darker seeds and a few lighter fruit pieces, visible through the glass. The jam surface is slightly uneven.
- **Lid**: a metal lid covered by a **red-and-white gingham cloth** tied with a thin string, the cloth edges hanging a little over the rim.
- **Label** (front, follows `facing`): a small cream label with a tiny strawberry drawing. No text.

## Fill levels

| `portions` | Jam height inside | Notes |
|---|---|---|
| 1 | about one third | Visible empty glass above the jam, a smear of jam on the inner wall |
| 2 | about two thirds | |
| 3 | full, just under the lid | |

## Files

| File | Content |
|---|---|
| `models/block/strawberry_jam_1.json` … `_3.json` | The jar for each level, built so the label faces **north** (the blockstate rotates it) |
| `textures/block/strawberry_jam_glass.png` | Glass atlas (sides, top rim, highlight) |
| `textures/block/strawberry_jam_fill.png` | Jam atlas (side seen through glass, top surface) |
| `textures/block/strawberry_jam_lid.png` | Gingham cloth, string and metal rim |
| `textures/block/strawberry_jam_label.png` | Label (optional, may live in another atlas) |
| `textures/item/strawberry_jam_1.png` … `_3.png` | 16×16 inventory icons for each level, same jar seen from the front |
| `art/blockbench/strawberry_jam_<level>.bbmodel` | Blockbench sources |

Keep the block and item paths above — the item definition `items/strawberry_jam.json` already selects the icon by `portions`, and the blockstate already maps `portions` × `facing`.

## Rules

- Footprint about 6×6 px, height about 8 px including the lid; centred in the block, resting on y = 0. If the final size is clearly different, update `SHAPE` in `core/jam/JamJarBlock.java`.
- **≤ 12 elements** per level. The jam is its own cuboid inside the glass so its height changes per level; render glass faces with the jam behind them.
- `"ambientocclusion": false`, a `particle` texture on every model, `display` transforms so the jar looks right on the ground, in hand and in item frames.

## Done when

- [x] Three block models, item icons and textures replaced; Blockbench sources saved.
- [x] `./gradlew build` and `python art/validate_wheat_art.py` pass.
- [ ] In game: three jars on a table (1, 2 and 3 portions) clearly read as the same jar filling up, from the front and from above.

See [the visual report](../strawberry-jam-visuals.md) for sources, 3D item contexts and verification.
