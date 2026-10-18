# Tarefa de arte 0006 — Bananeira

[English](0006-banana-plant.md) | **Português**

A jogabilidade está pronta ([docs/banana.pt-BR.md](../banana.pt-BR.md)). A arte provisória foi substituída **no mesmo lugar**, preservando todos os nomes existentes. Veja [o relatório visual](../banana-visuals.pt-BR.md) para prévias, geometria multipart dos frutos, verificações e o teste pendente a 20 blocos. Não rode o gerador original `art/banana_art.py` sobre a arte final.

Leia antes: [AGENTS.md](../../AGENTS.md), [art-pipeline.pt-BR.md](../art-pipeline.pt-BR.md). Texturas **16×16**, pixels duros, Vanilla+ realista. Use o servidor MCP do Blockbench para os modelos 3D e salve as fontes em `art/blockbench/<modelo>.bbmodel`.

Caminho base: `common/src/main/resources/assets/farmerplus/`

## Referência: a planta de verdade

- **Pseudocaule:** não é madeira — são bainhas de folhas bem enroladas. Verde-amarelado a verde médio, com bordas verticais compridas das bainhas, manchas irregulares marrom-escuras e marrom-arroxeadas (típicas da Prata/Nanica) e tiras de bainha seca e marrom se soltando perto da base.
- **Folhas:** remos enormes, 1,5–3 m × 0,4–0,9 m, verde médio brilhante em cima e mais claras embaixo, nervura central grossa e verde-amarelada clara, nervuras finas e paralelas saindo quase retas da nervura central até a borda. O vento **rasga o limbo ao longo das nervuras** em tiras, principalmente nas bordas. As folhas novas saem do topo como um "charuto" claro e enrolado, sobem e arqueiam conforme envelhecem. As folhas mortas ficam cor de palha e penduradas ao longo do caule.
- **Cacho:** pendurado na copa por um engaço verde e grosso; pencas de frutos em espiral em volta do engaço, com as bananas curvadas **para cima**; verdes e com quinas quando verdes, amarelas com algumas pintas marrons quando maduras, pontas escuras de flor seca. Abaixo das pencas, o engaço nu termina no **coração** (botão masculino): uma gota de brácteas roxo-vinho brilhantes com uma camada cerosa.
- **Filhote:** broto novo com folhas estreitas e em pé ("chifrinho"), muitas vezes com pintas marrom-avermelhadas.

## Texturas (`textures/block/`, 16×16)

| Arquivo | Conteúdo |
|---|---|
| `banana_stem.png` | Lateral do pseudocaule (bainhas verticais, manchas, tiras secas). Usada na coluna de 6 px |
| `banana_stem_top.png` | Pseudocaule cortado: anéis claros concêntricos das bainhas, centro creme |
| `banana_leaf.png` | Meio de um limbo, **nervura central vertical nas colunas 7–8**, ponta para a linha de cima; as metades esquerda e direita ocupam toda a largura; rasgos como pixels transparentes ao longo das nervuras |
| `banana_leaf_tip.png` | A mesma folha afinando até uma ponta na linha de **cima**; as linhas de baixo também são usadas, invertidas, para a base arredondada do limbo |
| `banana_leaf_dry.png` | Folha morta cor de palha, bem rasgada, afinando para a linha de **baixo** (ela fica pendurada) |
| `banana_heart.png` | Brácteas do coração, roxo-vinho com camada cerosa |
| `banana_fingers_green.png` | Bananas verdes lado a lado (frutos verticais, pontas escuras nas linhas 0 e 8) |
| `banana_fingers_ripe.png` | Bananas maduras amarelas, algumas pintas, pontas escuras |
| `banana_sapling.png` | Sprite em cruz de um filhote |

Itens (`textures/item/`): `banana.png` (uma banana madura), `banana_leaf.png` (uma folha inteira vista de cima).

## Modelos (`models/block/`, Blockbench)

Mantenha os nomes e os pontos de encaixe — o código coloca os blocos lado a lado e as peças precisam se juntar.

| Modelo | Regras |
|---|---|
| `banana_stem_base`, `banana_stem_middle`, `banana_stem_crown` | Coluna em **x/z 5–11** (6 px). A base pode alargar para 8 px embaixo; a copa termina com as bainhas das folhas e o charuto enrolado subindo acima do bloco. Os pecíolos encostam na coluna em z = 21 do bloco de folha vizinho, então não afine a coluna |
| `banana_leaf_<idade>_base`, `_blade`, `_tip` (`young`, `mature`) | Uma folha apontando para o **norte** a partir de um pseudocaule ao sul. A base começa no caule (z = 21, fora do bloco) e termina em z = 0; o segmento seguinte começa em z = 16 na mesma altura. As idades mudam só a pose: a nova sobe, a madura arqueia e cai |
| `banana_leaf_<idade>_diagonal_base`, `_diagonal_tip` | A mesma folha apontando para o **nordeste** (rotação de elemento `y = -45`): a base começa no centro do caule (−8, 24) e termina no canto do bloco (16, 0); a ponta vai do canto (0, 16) até além de (16, 0) |
| `banana_leaf_dry` | Uma folha morta pendurada ao lado do caule, do pecíolo (z = 21) até y ≈ −14 |
| `banana_bunch_bud`, `_flowering`, `_green`, `_ripe` | Caule ao **norte** (z < 0). Engaço saindo do caule no alto, pencas de mais ou menos y = 16 até 0, e o engaço nu com o coração roxo pendurados abaixo do bloco (até y ≈ −8). Só o coração em `bud`; duas pencas pequenas e um coração grande em `flowering`; quatro pencas grandes em `green` e `ripe` |

Limites: até 12 elementos por modelo, coordenadas entre −16 e 32, `ambientocclusion: false`. `python art/banana_art.py` reescreve esses modelos, então quando eles forem feitos à mão, pare de rodá-lo (ou tire a parte dos modelos) — ele nunca sobrescreve texturas.

## Cacho colhido

| Arquivo | Regras |
|---|---|
| `models/block/harvested_banana_bunch_stalk` | O cacho colhido fica **em pé** e é um multipart: este modelo (engaço dentro das pencas e o toquinho cortado em cima, por onde o jogador segura) mais as 8 peças `banana_bunch_ripe_hand_<penca>_<lado>`, que somem uma por uma de baixo para cima. O código solta cada banana do centro da peça, então se mudar as pencas, atualize `HAND_CENTERS` em `HarvestedBananaBunchBlock`. Gerado por `python art/banana_bunch_art.py` |
| `items/banana_bunch.json` e `models/item/banana_bunch_*.json` | Item composto (toquinho + 8 pencas). Ajuste o `display` (igual em todas as peças) no Blockbench: Ajuste o `display` no Blockbench: `thirdperson_righthand` precisa apoiar o cacho **no ombro direito** com o braço levantado (a pose do braço vem do código), `firstperson_righthand` mostra o cacho no ombro no canto superior direito da tela, `gui` mostra o cacho inteiro |

## Hitbox das folhas

A hitbox das folhas segue os modelos: `python art/banana_leaf_shapes.py` voxeliza cada variante de `banana_leaf` (células de 2 px, y de −16 a 32) em `common/src/main/resources/farmerplus/shapes/banana_leaf.json`, que o `BananaLeafBlock` carrega. **Rode de novo depois de qualquer mudança num modelo de folha ou em `blockstates/banana_leaf.json`.**

## Pronto quando

- [x] Todos os arquivos acima substituídos com os mesmos nomes; `./gradlew build` e `python art/validate_wheat_art.py` passam.
- [x] `python art/preview_world_models.py` (veja [docs/banana.pt-BR.md](../banana.pt-BR.md)) mostra as folhas conectadas, sem buracos nas emendas dos segmentos, nas 8 direções.
- [ ] No jogo, a 20 blocos de distância, a planta parece uma bananeira: pseudocaule verde-claro, folhas enormes e rasgadas, um cacho com coração roxo.
- [x] Cacho colhido em pé: engaço fibroso e cortado finalizado, oito peças maduras compartilhadas e `HAND_CENTERS` correspondentes; estados cheio e parciais renderizados de um mundo de teste salvo.
- [x] Display idêntico exportado pelo Blockbench para os nove modelos do item composto; escala 1,1 da terceira pessoa preservada e enquadramentos de GUI/chão/fixo revisados.
- [x] Folhas secas conectadas nas oito direções; hitboxes regeneradas após a alteração do modelo/blockstate diagonal.
- [ ] Conferir no Minecraft o cacho apoiado no ombro direito em F5 e o recorte parcial no canto superior direito em primeira pessoa.

Os testes de distância e de carregar no ombro permanecem pendentes: a captura existente não tem distância medida e o Computer Use foi interrompido com Escape, inclusive na inspeção retomada. Prévias do editor e carregamento de recursos não substituem essas conferências. Os frutos sólidos acrescentam vinte modelos de meia penca via multipart vanilla; cada modelo respeita o limite de 12 elementos, mas o cacho verde/maduro da planta soma 104 elementos e o cacho colhido finalizado soma 102. Consulte o relatório antes de revisar o desempenho.
