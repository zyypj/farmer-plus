# Art task 0005 — Avocado tree and wood

**English** | [Português](0005-avocado-tree.pt-BR.md)

Gameplay is done ([docs/avocado.md](../avocado.md)). All textures below are placeholders; replace them in place, keeping every file name. Rules: [art-pipeline.md](../art-pipeline.md) — **16×16**, hard pixels, Realistic Vanilla+. Use the Blockbench MCP server for the 3D fruit models.

Base path: `common/src/main/resources/assets/farmerplus/`

## Reference: the real avocado tree

- **Bark:** grey-brown, finely fissured into small irregular plates, a little rough; never as dark as dark oak.
- **Wood:** pale, creamy yellow to light pinkish-tan, fine and even grain with few knots.
- **Leaves:** elliptical, leathery, glossy dark green on top, paler underneath, 10–25 cm long, crowded at branch tips; the canopy is dense and dark.
- **Flowers:** tiny, pale yellow-green, in loose clusters at branch tips.
- **Fruit:** pear-shaped, hanging singly or in pairs on a thick stalk. Unripe: bright, smooth green. Ripe (Hass style): dark green to purplish-black, pebbly skin.

## Textures (`textures/block/`, 16×16)

| File | Content |
|---|---|
| `avocado_log.png` | Bark side, vertical fissures, grey-brown |
| `avocado_log_top.png` | Cut end: bark ring around pale creamy rings |
| `stripped_avocado_log.png`, `stripped_avocado_log_top.png` | Stripped: pale wood with fine grain / growth rings |
| `avocado_planks.png` | Pale creamy-tan planks, fine grain, readable plank seams like vanilla |
| `avocado_door_top.png`, `avocado_door_bottom.png` | Door with a simple window on top; use transparency for the glass gaps |
| `avocado_trapdoor.png` | Trapdoor with a small lattice |
| `avocado_leaves.png` | Dense glossy dark-green elongated leaves with a few lighter undersides; binary alpha with small gaps |
| `avocado_sapling.png` | Young stem with 4–5 large elongated leaves |
| `avocado_flowers.png` | Atlas for the flower clusters hanging under the leaves |
| `avocado_fruit_unripe.png` | Atlas: bright green smooth skin (body) + stalk strip |
| `avocado_fruit_ripe.png` | Atlas: dark green/purple pebbly skin (body) + stalk strip |

Item textures (`textures/item/`): `avocado.png` (ripe avocado, pear shape, stalk), `avocado_door.png`.

## Fruit models (Blockbench, optional upgrade)

`models/block/avocado_leaves_flowers.json`, `avocado_leaves_unripe.json` and `avocado_leaves_ripe.json` are overlays drawn **under** a leaves block (the blockstate is multipart, `fruit` 1–3). They currently use simple boxes. Rebuild them as pear-shaped avocados (2–3 cuboids each: narrow neck, wide body) hanging 3–6 px below the leaves on a short stalk, 1–2 fruits per block, ≤ 8 elements per model. Keep everything between y = −8 and y = 0 and inside x/z 0–16.

## Done when

- [ ] All textures above replaced with the same names.
- [ ] `./gradlew build` and `python art/validate_wheat_art.py` pass.
- [ ] In game: a grown tree reads as an avocado tree (pale wood inside, grey bark, dark glossy crown) and ripe fruit is visible from the ground.
