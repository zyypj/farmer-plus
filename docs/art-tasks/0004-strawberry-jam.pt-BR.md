# Tarefa de arte 0004 — Pote de geleia de morango

[English](0004-strawberry-jam.md) | **Português**

A jogabilidade está pronta ([docs/strawberries.pt-BR.md](../strawberries.pt-BR.md#geleia-de-morango)). Hoje o pote usa caixas provisórias. Crie um **pote 3D de verdade no Blockbench**, que fique bonito como decoração em cima de uma mesa e encha visivelmente com 1, 2 ou 3 porções.

Leia antes: [AGENTS.md](../../AGENTS.md), [art-pipeline.pt-BR.md](../art-pipeline.pt-BR.md). Use o servidor MCP do Blockbench. A arte de morango usa texturas **16×16** (veja `art/strawberry_pixels.py`).

Caminho base: `common/src/main/resources/assets/farmerplus/`

## Visual

Um potinho de geleia caseira, estilo fazenda:
- **Corpo de vidro**: baixo e com ombros arredondados, um pouco mais largo que alto, vidro transparente com leve tom verde-azulado nas bordas e um reflexo vertical. Pixels de vidro podem ser semitransparentes (única exceção permitida).
- **Geleia dentro**: vermelho escuro brilhante com sementes mais escuras e alguns pedaços de fruta mais claros, visível através do vidro. A superfície da geleia é levemente irregular.
- **Tampa**: tampa de metal coberta por um **tecido xadrez vermelho e branco** amarrado com um barbante fino, com as pontas do tecido caindo um pouco sobre a borda.
- **Rótulo** (frente, segue o `facing`): um rótulo creme pequeno com o desenho de um morango. Sem texto.

## Níveis

| `portions` | Altura da geleia | Observações |
|---|---|---|
| 1 | cerca de um terço | Vidro vazio visível acima, um pouco de geleia escorrida na parede interna |
| 2 | cerca de dois terços | |
| 3 | cheio, logo abaixo da tampa | |

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `models/block/strawberry_jam_1.json` … `_3.json` | O pote de cada nível, com o rótulo virado para o **norte** (o blockstate gira) |
| `textures/block/strawberry_jam_glass.png` | Atlas do vidro (laterais, borda de cima, reflexo) |
| `textures/block/strawberry_jam_fill.png` | Atlas da geleia (lateral vista pelo vidro, superfície) |
| `textures/block/strawberry_jam_lid.png` | Tecido xadrez, barbante e aro de metal |
| `textures/block/strawberry_jam_label.png` | Rótulo (opcional, pode ficar em outro atlas) |
| `textures/item/strawberry_jam_1.png` … `_3.png` | Ícones 16×16 de inventário para cada nível, o mesmo pote visto de frente |
| `art/blockbench/strawberry_jam_<nível>.bbmodel` | Fontes do Blockbench |

Mantenha esses caminhos — a definição de item `items/strawberry_jam.json` já escolhe o ícone por `portions`, e o blockstate já mapeia `portions` × `facing`.

## Regras

- Base de uns 6×6 px e altura de uns 8 px com a tampa; centralizado no bloco, apoiado em y = 0. Se o tamanho final ficar bem diferente, atualize `SHAPE` em `core/jam/JamJarBlock.java`.
- **≤ 12 elementos** por nível. A geleia é um cubo próprio dentro do vidro, para a altura mudar por nível; as faces do vidro ficam na frente da geleia.
- `"ambientocclusion": false`, textura `particle` em todo modelo, transforms de `display` para o pote ficar certo no chão, na mão e na moldura.

## Pronto quando

- [x] Três modelos de bloco, ícones de item e texturas substituídos; fontes do Blockbench salvas.
- [x] `./gradlew build` e `python art/validate_wheat_art.py` passam.
- [ ] No jogo: três potes numa mesa (1, 2 e 3 porções) parecem claramente o mesmo pote enchendo, de frente e de cima.

Veja [o relatório visual](../strawberry-jam-visuals.pt-BR.md) para fontes, contextos 3D do item e verificação.
