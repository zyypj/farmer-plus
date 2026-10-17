# Art task 0002 — Trampled wheat

**English** | [Português](0002-trampled-wheat.pt-BR.md)

Trampled wheat already has final **geometry** (see [docs/trampling.md](../trampling.md)). *Bent* and *flattened* crops reuse the standing stage sprites. Only the **crushed** stage needs its own art: the files below are generated placeholders (darkened copies of the standing sprites). Replace them in place.

Base path: `common/src/main/resources/assets/farmerplus/textures/block/`

## Textures (16×16, same rules as [art-pipeline.md](../art-pipeline.md))

| File | Content |
|---|---|
| `wheat_stage2_crushed.png` … `wheat_stage7_crushed.png` | Side view of stalks that were stepped on: snapped culms with sharp kinks, split and frayed stems, bruised darker green (young) or dull dusty straw (mature), a few leaves torn |
| `wheat_stage2_alternate_crushed.png` … `wheat_stage7_alternate_crushed.png` | A second, different layout of the same, for variation |

Ages 0–1 are never crushed in game; their `_crushed` files can stay as they are.

### How the sprite is used

The sprite is mapped onto planes that lie almost flat on the farmland, with the **bottom 1–2 px** used as a short upright stub and **everything above it lying on the ground**, ears pointing away from the stub. Draw it as a normal upright side view (like the standing sprites); the model does the laying down.

- Keep the bottom edge as cut/snapped stubs, not roots.
- Mature (AGE 6–7): ears flattened and partly broken off, some loose kernels near the ears, colour duller and dustier than standing wheat.
- Keep transparency binary (0 or 255) and leave real gaps so farmland shows through — a solid mat looks like a carpet.
- Avoid mud or dirt colours inside the sprite; the farmland underneath supplies that.

## Done when

- [ ] 12 textures replaced (ages 2–7, base and alternate), same names.
- [ ] `python art/validate_wheat_art.py` passes.
- [ ] In a survival world, sprint through mature wheat several times: the crushed path reads as broken stalks pressed into the soil, not as a texture glitch.
