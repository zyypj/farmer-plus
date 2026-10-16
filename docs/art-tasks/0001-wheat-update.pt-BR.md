# Tarefa de arte 0001 — Atualização do trigo

[English](0001-wheat-update.md) | **Português**

Os arquivos abaixo hoje têm **arte provisória**. Substitua cada um no mesmo lugar, mantendo exatamente o caminho e o nome.

Caminho base: `common/src/main/resources/assets/farmerplus/`

## Texturas de item (16×16)

| Arquivo | O que é | Referência de clima |
|---|---|---|
| `textures/item/flour.png` | Um montinho de farinha branca, branco levemente quente, sombra suave na base | açúcar / farinha de osso vanilla |
| `textures/item/dough.png` | Uma bola de massa de pão crua, bege claro, com uma dobra mais escura | pão vanilla, só que mais redondo e claro |
| `textures/item/wheat_porridge.png` | Uma tigela de madeira com mingau cremoso e alguns grãos de trigo por cima | tigela do ensopado de cogumelo / sopa de beterraba |

## Bloco Feixe de Trigo (Blockbench)

Um feixe de talos de trigo colhidos, em pé, amarrado no meio com uma faixa de barbante, com as espigas abrindo em leque no topo. Pense em "feixe de colheita", não em fardo de feno.

| Arquivo | Conteúdo |
|---|---|
| `art/blockbench/wheat_sheaf.bbmodel` | Projeto-fonte do Blockbench (Java Block/Item) |
| `models/block/wheat_sheaf.json` | Modelo exportado, ≤ 12 elementos, com todos os transforms de `display` |
| `textures/block/wheat_sheaf_side.png` | Talos vistos de lado, com a faixa de barbante |
| `textures/block/wheat_sheaf_top.png` | Vista de cima: espigas / talos cortados |

Pode criar texturas extras (ex.: `wheat_sheaf_ears.png`) se o modelo precisar.

A caixa de colisão/contorno atual é 12×16×12 centralizada (`Block.column(12.0, 0.0, 16.0)` em `WheatSheafBlock`). Se a silhueta final ficar claramente mais fina ou mais larga, atualize esse valor.

## Ícone do mod

| Arquivo | Conteúdo |
|---|---|
| `icon.png` | 512×512, estilo pixel art: um feixe de trigo dourado sobre um bloco de terra arada, fundo limpo. Legível em 64×64. |

## Pronto quando

- [ ] Todos os arquivos acima substituídos, com os mesmos nomes.
- [ ] `./gradlew :neoforge:runClient` mostra os itens certinhos na aba criativa Farmer+, na mão e no chão; o feixe fica bonito colocado no mundo.
- [ ] Nenhum aviso de modelo/textura do `farmerplus` no log.
