# Tarefa de arte 0006 — Bananeira

[English](0006-banana-plant.md) | **Português**

A jogabilidade está pronta ([docs/banana.pt-BR.md](../banana.pt-BR.md)). Tudo abaixo usa pixels provisórios e caixas simples geradas por `python art/banana_art.py`. Substitua a arte **no mesmo lugar**, mantendo todos os nomes de arquivo, para a planta parecer uma bananeira (*Musa*) de verdade de longe e de perto.

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

## Pronto quando

- [ ] Todos os arquivos acima substituídos com os mesmos nomes; `./gradlew build` e `python art/validate_wheat_art.py` passam.
- [ ] `python art/preview_world_models.py` (veja [docs/banana.pt-BR.md](../banana.pt-BR.md)) mostra as folhas conectadas, sem buracos nas emendas dos segmentos, nas 8 direções.
- [ ] No jogo, a 20 blocos de distância, a planta parece uma bananeira: pseudocaule verde-claro, folhas enormes e rasgadas, um cacho com coração roxo.
