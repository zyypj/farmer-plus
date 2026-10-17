# Tarefa de arte 0005 — Abacateiro e madeira

[English](0005-avocado-tree.md) | **Português**

A jogabilidade está pronta ([docs/avocado.pt-BR.md](../avocado.pt-BR.md)). As texturas abaixo eram provisórias; substitua no mesmo lugar, mantendo todos os nomes. Regras: [art-pipeline.pt-BR.md](../art-pipeline.pt-BR.md) — **16×16**, pixels duros, Vanilla+ realista. Use o servidor MCP do Blockbench para os modelos 3D dos frutos.

Caminho base: `common/src/main/resources/assets/farmerplus/`

## Referência: o abacateiro de verdade

- **Casca:** marrom-acinzentada, com fissuras finas formando placas irregulares, um pouco áspera; nunca tão escura quanto o carvalho-escuro.
- **Madeira:** clara, amarelo-creme a bege-rosado, veio fino e uniforme, com poucos nós.
- **Folhas:** elípticas, coriáceas, verde-escuro brilhante em cima, mais claras embaixo, 10–25 cm, concentradas nas pontas dos galhos; a copa é densa e escura.
- **Flores:** minúsculas, amarelo-esverdeadas, em cachos soltos nas pontas dos galhos.
- **Fruto:** formato de pera, pendurado sozinho ou em pares num cabinho grosso. Verde: verde vivo e liso. Maduro (tipo Hass): verde-escuro a roxo-quase-preto, casca rugosa.

## Texturas (`textures/block/`, 16×16)

| Arquivo | Conteúdo |
|---|---|
| `avocado_log.png` | Lateral da casca, fissuras verticais, marrom-acinzentado |
| `avocado_log_top.png` | Corte: anel de casca em volta de anéis creme-claros |
| `stripped_avocado_log.png`, `stripped_avocado_log_top.png` | Descascada: madeira clara com veio fino / anéis de crescimento |
| `avocado_planks.png` | Tábuas creme-claras, veio fino, emendas visíveis como no vanilla |
| `avocado_door_top.png`, `avocado_door_bottom.png` | Porta com uma janelinha em cima; use transparência nas aberturas |
| `avocado_trapdoor.png` | Alçapão com uma pequena treliça |
| `avocado_leaves.png` | Folhas alongadas verde-escuro brilhante, densas, com algumas faces de baixo mais claras; alpha binário com pequenos buracos |
| `avocado_sapling.png` | Caule jovem com 4–5 folhas grandes e alongadas |
| `avocado_flowers.png` | Atlas dos cachinhos de flores pendurados embaixo das folhas |
| `avocado_fruit_unripe.png` | Atlas: casca verde viva e lisa (corpo) + faixa do cabinho |
| `avocado_fruit_ripe.png` | Atlas: casca verde-escura/roxa rugosa (corpo) + faixa do cabinho |

Texturas de item (`textures/item/`): `avocado.png` (abacate maduro, formato de pera, cabinho), `avocado_door.png`.

## Placas, prateleira e botes

Texturas de bloco e item continuam **16×16** (os moldes vanilla de placa e prateleira mapeiam os UVs no sprite inteiro). Texturas de entidade e de tela mantêm o tamanho do layout vanilla, porque o modelo do bote e as telas de placa leem regiões fixas; desenhe arte própria sobre esse layout (`python art/validate_wheat_art.py` confere os tamanhos).

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| `textures/block/avocado_sign.png` | 16×16 | Atlas da placa (`template_sign`): faces da tábua e haste, tábuas claras de abacateiro |
| `textures/block/avocado_hanging_sign.png` | 16×16 | Atlas da placa suspensa (`template_hanging_sign`): tábua e barra de madeira descascada, região das correntes no canto superior direito com vãos transparentes |
| `textures/block/avocado_shelf.png` | 16×16 | Atlas da prateleira (`template_shelf_*`): tábuas claras, fundo e bordas mais escuros |
| `textures/item/avocado_sign.png`, `avocado_hanging_sign.png` | 16×16 | Ícones de inventário |
| `textures/item/avocado_boat.png`, `avocado_chest_boat.png` | 16×16 | Ícones de inventário: casco de tábuas claras (+ baú) |
| `textures/entity/boat/avocado.png` | 128×64 | Entidade do bote, layout de UV do bote vanilla |
| `textures/entity/chest_boat/avocado.png` | 128×128 | Entidade do bote com baú, layout de UV do bote com baú vanilla |
| `assets/minecraft/textures/gui/signs/farmerplus/avocado.png` | 24×26 | Tela de edição da placa: tábua em cima, haste embaixo |
| `assets/minecraft/textures/gui/hanging_signs/farmerplus/avocado.png` | 16×16 | Tela de edição da placa suspensa |

Os dois arquivos de `gui` ficam em `assets/minecraft/` porque o vanilla monta esses caminhos a partir do nome do tipo de madeira (`farmerplus/avocado`).


## Modelos do tronco e dos galhos (Blockbench, melhoria opcional)

A árvore é feita de dois blocos que se conectam, gerados por `python art/avocado_branches.py` como caixas simples que reaproveitam `avocado_log.png` (casca) e `avocado_log_top.png` (pontas cortadas):

| Bloco | Largura | Modelos (`models/block/`) |
|---|---|---|
| `avocado_trunk` | 10 px | `avocado_trunk_core.json`, `avocado_trunk_arm.json`, `avocado_trunk_inventory.json` |
| `avocado_branch` | 6 px | `avocado_branch_core.json`, `avocado_branch_arm.json`, `avocado_branch_inventory.json` |

O blockstate é multipart: `*_core` sempre aparece e `*_arm` (apontando para o norte, de z = 0 até o núcleo) é girado para cada lado conectado. Pode adicionar detalhes de casca (um nó, um leve alargamento onde o braço encontra o núcleo) no Blockbench, mas mantenha cada braço dentro da caixa, o núcleo centralizado e os nomes dos arquivos; rodar o script de novo sobrescreve os modelos, então pare de usá-lo quando eles forem feitos à mão.

## Modelos dos frutos (Blockbench, melhoria opcional)

`models/block/avocado_leaves_flowers.json`, `avocado_leaves_unripe.json` e `avocado_leaves_ripe.json` são sobreposições desenhadas **embaixo** de um bloco de folhas (o blockstate é multipart, `fruit` 1–3). Hoje usam caixas simples. Refaça como abacates em formato de pera (2–3 cubos cada: pescoço fino, corpo largo) pendurados 3–6 px abaixo das folhas num cabinho curto, 1–2 frutos por bloco, no máximo 8 elementos por modelo. Mantenha tudo entre y = −8 e y = 0 e dentro de x/z 0–16.

## Pronto quando

- [x] Todas as texturas acima substituídas com os mesmos nomes.
- [x] `./gradlew build` e `python art/validate_wheat_art.py` passam.
- [ ] No jogo: tronco e galhos se conectam sem buracos e parecem madeira fina, não toras.
- [ ] No jogo: uma árvore crescida parece um abacateiro (madeira clara por dentro, casca cinza, copa escura e brilhante) e os frutos maduros aparecem do chão.

Veja [o relatório da arte](../avocado-visuals.pt-BR.md) para fontes, prévias, geometria final e limites da verificação.
