# Farmer+

**English** | [Português](README.pt-BR.md)

A vanilla-friendly overhaul of Minecraft farming. Farmer+ adds crops, foods, ingredients and soils that feel like they always belonged in the game — no farm simulator, no menus to learn, just a deeper version of what you already know.

| | |
|---|---|
| Minecraft | 26.3 |
| Loaders | Fabric, NeoForge, Forge |
| Java | 25 |
| Side | Client and server |
| License | MIT |

## Design goals

- **Vanilla first.** Every addition must look, sound and behave like something Mojang could ship. Recipes, textures and progression follow vanilla conventions.
- **Featherweight.** Three tiny mixins, no per-tick logic, no reflection. Content is registered once at startup and behaviour is driven by vanilla data components, tags and JSON data. Each loader jar is about 160 KB, almost all of it 16×16 art and block models.
- **Modpack friendly.** Ingredients use the shared `c:` convention tags (`c:flours/wheat`, `c:doughs/wheat`, …), so flour or dough from other mods works in Farmer+ recipes and vice versa.
- **Every loader.** One shared codebase ships to Fabric, NeoForge and Forge, and is updated whenever Minecraft or a loader releases a new version.

## Content

### Wheat update (0.1.0)

| Item | How to get it | Notes |
|---|---|---|
| Flour | 1 wheat (crafting) | Accepted wherever `c:flours/wheat` is used |
| Dough | 3 flour + water bucket → 3 dough | Bake in a furnace, smoker or campfire to get bread |
| Wheat Porridge | 2 wheat + sugar + milk bucket + bowl | Restores 7 hunger, returns the bowl |
| Wheat Sheaf | 4 wheat around 1 string | Decorative block, cuts fall damage by 80% like a hay bale, mined fastest with a hoe, compostable |

Vanilla bread (3 wheat) is untouched — dough is an alternative path that rewards cooking.

Wheat itself gets a **Realistic Vanilla+ visual overhaul**: original 16×16 art for all eight growth stages, four natural variations per stage, taller mature crops and redrawn wheat and seeds. Mechanics stay vanilla. The visuals are also available as a standalone resource pack (`./gradlew wheatVisualPack`). See [docs/wheat-visuals.md](docs/wheat-visuals.md).

![Wheat stages and items](docs/images/wheat-textures.png)

### Strawberries

A new perennial crop. Find **wild strawberries** in plains, meadows and forests, then plant the berries on **farmland** (only farmland). Plants flower, set green fruit and ripen; right-click to pick 2–4 strawberries and the plant flowers again. Healthy plants send runners onto neighbouring empty farmland, trampled plants lose part of their harvest, and strawberries become **jam**: a glass bottle with 1–3 strawberries fills a jar you can eat a portion at a time or place as decoration. See [docs/strawberries.md](docs/strawberries.md).

### Avocado tree

A full-size fruit tree modelled on real avocados — a dense rounded crown 10–13 blocks tall, or a 16–20 block wild giant from 2×2 saplings — that grows wild in jungles. Its leaves flower, set green fruit and ripen into avocados you pick with a right-click — again and again. It comes with a complete wood set (logs, wood, stripped variants, planks, stairs, slabs, fences, gates, doors, trapdoors, plates, buttons, signs, hanging signs, shelves, boats and chest boats) that works in every vanilla wooden recipe. See [docs/avocado.md](docs/avocado.md).

### Banana plant

A banana built like the real giant herb: a slim pseudostem, huge leaves that tear and arch (young, mature and dry hanging ones), and one bunch per stem that hangs under the crown with its purple bud. Harvest the whole heavy bunch and carry it on your shoulder, then craft it into 8 bananas or stand it on the ground and pull bananas off one by one; the spent stem then dies back and a follower sucker takes its place, so plants spread into clumps. Wild clumps grow in jungles. See [docs/banana.md](docs/banana.md).

### Crop trampling

Walking through crops bends them, sprinting or riding flattens them, and paths you keep using get crushed into the soil — real tilted and snapped stalk geometry that falls in the direction you moved. Bent crops recover over time; crushed ones yield only seeds. Jumping on crops flattens them instead of destroying them and the farmland. Sneak to walk carefully. Toggle with `/gamerule farmerplus:crop_trampling` and `/gamerule farmerplus:mob_crop_trampling`. See [docs/trampling.md](docs/trampling.md).

## Installing

1. Install the loader of your choice for Minecraft 26.3.
2. Fabric only: also install [Fabric API](https://modrinth.com/mod/fabric-api).
3. Drop the matching `farmerplus-<loader>-26.3-<version>.jar` into your `mods` folder.

## Building from source

```bash
./gradlew build
```

Jars are written to `fabric/build/libs`, `neoforge/build/libs` and `forge/build/libs`.

Run a development client:

```bash
./gradlew :neoforge:runClient
```

The same task exists for `:fabric` and `:forge`.

## Documentation

| Topic | English | Português |
|---|---|---|
| Architecture and adding content | [docs/architecture.md](docs/architecture.md) | [docs/architecture.pt-BR.md](docs/architecture.pt-BR.md) |
| Art pipeline (textures, Blockbench) | [docs/art-pipeline.md](docs/art-pipeline.md) | [docs/art-pipeline.pt-BR.md](docs/art-pipeline.pt-BR.md) |
| Wheat visuals | [docs/wheat-visuals.md](docs/wheat-visuals.md) | [docs/wheat-visuals.pt-BR.md](docs/wheat-visuals.pt-BR.md) |
| Crop trampling | [docs/trampling.md](docs/trampling.md) | [docs/trampling.pt-BR.md](docs/trampling.pt-BR.md) |
| Strawberries | [docs/strawberries.md](docs/strawberries.md) | [docs/strawberries.pt-BR.md](docs/strawberries.pt-BR.md) |
| Avocado tree and wood | [docs/avocado.md](docs/avocado.md) | [docs/avocado.pt-BR.md](docs/avocado.pt-BR.md) |
| Banana plant | [docs/banana.md](docs/banana.md) | [docs/banana.pt-BR.md](docs/banana.pt-BR.md) |
| Updating Minecraft and loaders | [docs/updating.md](docs/updating.md) | [docs/updating.pt-BR.md](docs/updating.pt-BR.md) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) | [CONTRIBUTING.pt-BR.md](CONTRIBUTING.pt-BR.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) | [CHANGELOG.pt-BR.md](CHANGELOG.pt-BR.md) |

## Languages

English (`en_us`) and Brazilian Portuguese (`pt_br`). Every new name must be added to both files in `common/src/main/resources/assets/farmerplus/lang/`.

## License

Code and assets are released under the [MIT License](LICENSE).
