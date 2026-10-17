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
- **Featherweight.** Two tiny mixins, no per-tick logic, no reflection. Content is registered once at startup and behaviour is driven by vanilla data components, tags and JSON data. Each loader jar is about 160 KB, almost all of it 32×32 art and block models.
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

Wheat itself gets a **Realistic Vanilla+ visual overhaul**: original 32×32 art for all eight growth stages, four natural variations per stage, taller mature crops and redrawn wheat and seeds. Mechanics stay vanilla. The visuals are also available as a standalone resource pack (`./gradlew wheatVisualPack`). See [docs/wheat-visuals.md](docs/wheat-visuals.md).

![Wheat stages and items](docs/images/wheat-textures.png)

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
| Updating Minecraft and loaders | [docs/updating.md](docs/updating.md) | [docs/updating.pt-BR.md](docs/updating.pt-BR.md) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) | [CONTRIBUTING.pt-BR.md](CONTRIBUTING.pt-BR.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) | [CHANGELOG.pt-BR.md](CHANGELOG.pt-BR.md) |

## Languages

English (`en_us`) and Brazilian Portuguese (`pt_br`). Every new name must be added to both files in `common/src/main/resources/assets/farmerplus/lang/`.

## License

Code and assets are released under the [MIT License](LICENSE).
