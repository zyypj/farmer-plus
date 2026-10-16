# Updating Minecraft and loaders

**English** | [Português](updating.pt-BR.md)

All versions live in one file: `gradle.properties`.

## A loader released a new build (same Minecraft version)

1. Find the newest version:
   - Fabric API / Loader: <https://fabricmc.net/develop/>
   - NeoForge: <https://projects.neoforged.net/neoforged/neoforge>
   - Forge: <https://files.minecraftforge.net/net/minecraftforge/forge/>
2. Update `fabric_version`, `fabric_loader_version`, `neoforge_version` or `forge_version`.
3. `./gradlew build`, then start a dev server on the updated loader.
4. Bump the patch version (`0.1.0` → `0.1.1`) and add a changelog entry.

## A new Minecraft version

1. Create a maintenance branch for the old version: `git switch -c mc/26.3 && git push -u origin mc/26.3`.
2. On `main`, update `minecraft_version`, `minecraft_version_range`, `neo_form_version`, every loader version and, if needed, the Gradle plugin versions in `build.gradle`.
3. Check `pack.mcmeta` `min_format`/`max_format` against the new data pack format.
4. Fix compile errors in `common` first, then in each loader.
5. Re-check the JSON formats of recipes, item models and loot tables against the vanilla jar in `common/build/moddev/artifacts/`.
6. Build, run a client on one loader and servers on the others, then bump the minor version.

## Branches

| Branch | Purpose |
|---|---|
| `main` | Latest supported Minecraft version |
| `mc/<version>` | Bug-fix maintenance for an older Minecraft version |
