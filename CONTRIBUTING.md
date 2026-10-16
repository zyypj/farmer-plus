# Contributing to Farmer+

**English** | [Português](CONTRIBUTING.pt-BR.md)

Thanks for helping! Farmer+ aims to feel like vanilla and to cost nothing at runtime. Please read [docs/architecture.md](docs/architecture.md) before opening a pull request.

## Before you start

- Open an issue describing the crop, food or mechanic you want to add. Explain why it fits vanilla.
- Requirements: JDK 25 and Git. Gradle is provided by the wrapper.

## Workflow

1. Fork and create a branch: `feat/tomato`, `fix/sheaf-shape`, `docs/readme`.
2. Make the change following the architecture and style rules.
3. Add every new name to **both** `en_us.json` and `pt_br.json`.
4. Run `./gradlew build` and test in a dev client on at least one loader.
5. Open a pull request using [Conventional Commits](https://www.conventionalcommits.org/) in the title, e.g. `feat(wheat): add wheat sheaf`.

## Commit scopes

`build`, `core`, `platform`, `fabric`, `neoforge`, `forge`, `docs`, `art`, and one per content module (`wheat`, …).

## Pull request checklist

- [ ] Builds on all loaders (`./gradlew build`)
- [ ] No new mixins, tick handlers or reflection (or a justification in the PR)
- [ ] Translations in English and Portuguese
- [ ] Recipes have a recipe-unlock advancement
- [ ] Blocks have a loot table and the right `mineable` tag
- [ ] Art follows [docs/art-pipeline.md](docs/art-pipeline.md)
- [ ] Changelog updated (both languages)
