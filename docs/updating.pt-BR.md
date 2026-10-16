# Atualizando Minecraft e loaders

[English](updating.md) | **Português**

Todas as versões ficam em um único arquivo: `gradle.properties`.

## Um loader lançou build nova (mesma versão do Minecraft)

1. Encontre a versão mais recente:
   - Fabric API / Loader: <https://fabricmc.net/develop/>
   - NeoForge: <https://projects.neoforged.net/neoforged/neoforge>
   - Forge: <https://files.minecraftforge.net/net/minecraftforge/forge/>
2. Atualize `fabric_version`, `fabric_loader_version`, `neoforge_version` ou `forge_version`.
3. `./gradlew build` e suba um servidor de dev no loader atualizado.
4. Suba a versão de patch (`0.1.0` → `0.1.1`) e registre no changelog.

## Versão nova do Minecraft

1. Crie um branch de manutenção para a versão antiga: `git switch -c mc/26.3 && git push -u origin mc/26.3`.
2. No `main`, atualize `minecraft_version`, `minecraft_version_range`, `neo_form_version`, a versão de cada loader e, se precisar, as versões dos plugins Gradle em `build.gradle`.
3. Confira `min_format`/`max_format` do `pack.mcmeta` com o novo formato de data pack.
4. Corrija os erros de compilação primeiro no `common`, depois em cada loader.
5. Revalide os formatos JSON de receitas, modelos de item e loot tables com o jar vanilla em `common/build/moddev/artifacts/`.
6. Compile, rode um cliente em um loader e servidores nos outros, e suba a versão minor.

## Branches

| Branch | Uso |
|---|---|
| `main` | Versão mais recente do Minecraft suportada |
| `mc/<versão>` | Manutenção de bugs para uma versão antiga do Minecraft |
