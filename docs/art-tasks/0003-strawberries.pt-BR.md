# Tarefa de arte 0003 — Morangos (modelos 3D)

[English](0003-strawberries.md) | **Português**

A jogabilidade está pronta ([docs/strawberries.pt-BR.md](../strawberries.pt-BR.md)). Hoje a planta aparece como planos em cruz provisórios. Crie **modelos 3D de verdade no Blockbench**: uma roseta baixa de morangueiro com folhas trifoliadas, flores brancas e morangos pendurados para fora da planta, como um campo de morangos cultivados em canteiros.

Leia antes: [AGENTS.md](../../AGENTS.md), [art-pipeline.pt-BR.md](../art-pipeline.pt-BR.md). Use o servidor MCP do Blockbench.

Caminho base: `common/src/main/resources/assets/farmerplus/`

## Referência: como é um morangueiro de verdade

- Uma **coroa** no nível do solo; tudo nasce dela. Sem caule lenhoso visível.
- **Folhas trifoliadas**: cada folha tem três folíolos ovais com **bordas serrilhadas** num pecíolo (cabinho) de 2–5 px. Folíolos verde vivo/médio em cima, mais claros por baixo, com nervura central visível. As folhas abrem em leque e arqueiam; a planta madura chega a ~6–7 px de altura e quase a largura toda do bloco.
- **Flores**: cinco pétalas brancas arredondadas em volta de um centro amarelo-esverdeado, ~3 px, em hastes finas que sobem um pouco acima ou entre as folhas.
- **Morangos** pendurados em hastes finas arqueadas que **caem para fora da borda** da planta, muitas vezes encostando ou deitando perto do solo. Formato de cone/coração, mais largo em cima, com o **cálice** verde (estrela de sépalas) no topo e pequenas **sementes (aquênios)** amarelas na superfície.
  - Verde: verde-claro → esbranquiçado, pequeno.
  - Maduro: vermelho brilhante, um pouco mais escuro embaixo/no lado da sombra, maior.
- Folhas velhas perto da base podem ser mais escuras; uma ou duas folhas levemente amareladas dão realismo.

## Estilo

Vanilla+ realista, igual ao trigo: pixel art reconhecível como Minecraft, pixels duros, sem anti-aliasing, paleta limitada, luz vindo de cima à esquerda. **Texturas 16×16.** Nunca decalque texturas da Mojang.

## Modelos a criar

| Idade | Modelo | Precisa mostrar | Limite de elementos |
|---|---|---|---|
| 0 | `models/block/strawberry_plant_stage0.json` | Coroa pequena, 2–3 folhas novas | ≤ 8 |
| 1 | `models/block/strawberry_plant_stage1.json` | Roseta cheia, 5–7 folhas arqueadas para fora | ≤ 12 |
| 2 | `models/block/strawberry_plant_stage2.json` | Roseta + 3–5 flores brancas | ≤ 16 |
| 3 | `models/block/strawberry_plant_stage3.json` | Roseta + 3–5 morangos pequenos verdes/brancos, 1 flor restante | ≤ 20 |
| 4 | `models/block/strawberry_plant_stage4.json` | Roseta + 4–6 morangos vermelhos maduros caindo pela borda | ≤ 20 |

Para **cada** idade crie também três variações, `strawberry_plant_stage<idade>_variant1..3.json` (arranjo de folhas e posição dos morangos diferentes — não só trocar textura), e atualize `blockstates/strawberry_plant.json` para que cada idade escolha um dos 4 modelos com 4 rotações `y` (16 alternativas com o mesmo peso, como `blockstates/wheat.json` em `assets/minecraft`).

**Morangos silvestres** (`blockstates/wild_strawberries.json`): menores, mais ralos e mais baixos que o cultivado, com menos morangos e menores (2–3 quando maduro). Crie `models/block/wild_strawberries_stage<idade>.json` (+ `_variant1`), limite de 12 elementos, e aponte o blockstate silvestre para eles.

### Regras de geometria

- Coordenadas do bloco: a superfície da terra arada fica em **y = −1**, então a coroa começa em y = −1 para encostar no solo (como nos modelos do trigo).
- **Os morangos são cubos de verdade**, não sprites chapados: ~2 × 2,5 × 2 px (maduro) e ~1,5 × 2 × 1,5 px (verde), com sementes pintadas em todos os lados e o cálice no topo. Ficam pendurados em hastes finas e **fora da roseta de folhas**, parcialmente para fora da borda do bloco (x/z podem passar um pouco de 0–16, até −2…18).
- **Folhas** são planos finos com duas faces (ou cubos de 0,1 px) inclinados com rotação. O 26.3 aceita qualquer ângulo e rotação Euler `x`/`y`/`z` — use para cada folíolo inclinar e arquear naturalmente. Junte uma folha trifoliada num plano texturizado quando possível para economizar elementos.
- Mantenha a planta **baixa**: altura máxima de ~7 px acima do solo na idade 4. Se a silhueta final ficar bem mais alta ou mais baixa, atualize `SHAPES` em `content/strawberry/StrawberryPlantBlock.java` (um `Block.column(...)` por idade).
- Use `"ambientocclusion": false`, `"shade_direction_override": "up"` nas folhas como no trigo, e dê uma textura `particle` a todo modelo.

### Texturas (16×16, `textures/block/`)

| Arquivo | Conteúdo |
|---|---|
| `strawberry_leaf.png` | Atlas de folhas trifoliadas: 2–3 formatos (nova, madura, levemente amarelada), bordas serrilhadas, nervura central, tons de cima e de baixo |
| `strawberry_flower.png` | Flor vista de cima + de lado, cinco pétalas brancas, centro amarelo |
| `strawberry_fruit.png` | Atlas das faces dos cubos dos morangos: vermelho maduro com sementes, verde/branco com sementes, cálice no topo |
| `strawberry_stem.png` | Tiras finas de pecíolo / haste do fruto, base da coroa |

Pode criar texturas extras se precisar. Apague as provisórias `strawberry_plant_stage0..4.png` quando nada mais referenciar elas.

### Item

| Arquivo | Conteúdo |
|---|---|
| `textures/item/strawberry.png` | Morango maduro 16×16: formato de coração, vermelho brilhante com sementes amarelas, cálice verde e cabinho curto, contorno 1 px mais escuro no lado da sombra |

## Salvar e exportar

- Fontes do Blockbench: `art/blockbench/strawberry_plant_stage<idade>[_variantN].bbmodel` e `art/blockbench/wild_strawberries_stage<idade>[_variant1].bbmodel`.
- Exporte modelos Java Block/Item para os caminhos acima, com texturas referenciadas como `farmerplus:block/<nome>`.

## Pronto quando

- [x] 5 idades × 4 variações do cultivado, 5 idades × 2 do silvestre, blockstates atualizados.
- [x] Textura do item substituída.
- [x] Limites de elementos respeitados; morangos em 3D pendurados pela borda; nenhuma peça flutuando.
- [x] `./gradlew build` passa e `./gradlew :neoforge:runClient` não mostra avisos de modelo/textura do `farmerplus`.
- [ ] No jogo: um campo 9×9 de terra arada com todas as idades parece um morangal de verdade a 5 e a 20 blocos de distância; os morangos maduros aparecem claramente na altura dos olhos.

Implementação e verificação atuais: [relatório visual](../strawberry-visuals.pt-BR.md). A conferência manual final do campo 9×9 no jogo permanece aberta.
