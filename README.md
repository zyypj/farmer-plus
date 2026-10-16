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
- **Featherweight.** No mixins, no per-tick logic, no reflection. Content is registered once at startup and behaviour is driven by vanilla data components, tags and JSON data. Each loader jar is under 40 KB of code and data.
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
| Updating Minecraft and loaders | [docs/updating.md](docs/updating.md) | [docs/updating.pt-BR.md](docs/updating.pt-BR.md) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) | [CONTRIBUTING.pt-BR.md](CONTRIBUTING.pt-BR.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) | [CHANGELOG.pt-BR.md](CHANGELOG.pt-BR.md) |

## Languages

English (`en_us`) and Brazilian Portuguese (`pt_br`). Every new name must be added to both files in `common/src/main/resources/assets/farmerplus/lang/`.

## License

Code and assets are released under the [MIT License](LICENSE).
