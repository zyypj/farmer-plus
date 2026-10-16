# Contribuindo com o Farmer+

[English](CONTRIBUTING.md) | **Português**

Obrigado pela ajuda! O Farmer+ quer parecer vanilla e não custar nada em desempenho. Leia [docs/architecture.pt-BR.md](docs/architecture.pt-BR.md) antes de abrir um pull request.

## Antes de começar

- Abra uma issue descrevendo a plantação, comida ou mecânica que você quer adicionar. Explique por que combina com o vanilla.
- Requisitos: JDK 25 e Git. O Gradle vem pelo wrapper.

## Fluxo

1. Faça um fork e crie um branch: `feat/tomato`, `fix/sheaf-shape`, `docs/readme`.
2. Faça a mudança seguindo as regras de arquitetura e estilo.
3. Adicione todo nome novo **nos dois** arquivos, `en_us.json` e `pt_br.json`.
4. Rode `./gradlew build` e teste num cliente de dev em pelo menos um loader.
5. Abra o pull request com título em [Conventional Commits](https://www.conventionalcommits.org/pt-br/), ex.: `feat(wheat): add wheat sheaf`.

## Escopos de commit

`build`, `core`, `platform`, `fabric`, `neoforge`, `forge`, `docs`, `art` e um por módulo de conteúdo (`wheat`, …).

## Checklist do pull request

- [ ] Compila em todos os loaders (`./gradlew build`)
- [ ] Nenhum mixin, handler de tick ou reflexão novo (ou justificativa no PR)
- [ ] Traduções em inglês e português
- [ ] Receitas têm advancement de desbloqueio
- [ ] Blocos têm loot table e a tag `mineable` correta
- [ ] Arte segue [docs/art-pipeline.pt-BR.md](docs/art-pipeline.pt-BR.md)
- [ ] Changelog atualizado (nos dois idiomas)
