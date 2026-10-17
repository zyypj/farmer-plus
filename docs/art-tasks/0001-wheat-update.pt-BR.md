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
| `models/block/wheat_sheaf.json` | Modelo exportado, ≤ 24 elementos com amarração 3D sólida, com todos os transforms de `display` |
| `textures/block/wheat_sheaf_side.png` | Material dos talos; a faixa de barbante é geometria separada |
| `textures/block/wheat_sheaf_top.png` | Vista de cima: espigas / talos cortados |

Pode criar texturas extras (ex.: `wheat_sheaf_ears.png`) se o modelo precisar.

A direção atual é Vanilla+ realista: pixel art desenhada em 32×32, faixa fina de barbante visível, talos individuais abertos na base e espigas mais cheias e sobrepostas. Todas as texturas de bloco do feixe usam 32×32, incluindo o leque de talos e o atlas de barbante adicionados.

O feixe também tem `textures/item/wheat_sheaf.png` nativo em 16×16 e `models/item/wheat_sheaf.json` para o inventário. A definição existente `items/wheat_sheaf.json` escolhe o ícone em `gui` e conserva o modelo de bloco 3D nos demais contextos. O caminho existente `textures/block/wheat_sheaf_bound_stalks.png` foi preservado, mas agora contém caules limpos. A amarração usa geometria com `wheat_sheaf_twine.png`: uma volta fechada pelos quatro lados, duas alças vazadas, nó em relevo e duas pontas penduradas. Oito planos de plantas, um núcleo comprimido e quinze elementos de corda totalizam vinte e quatro elementos, limite específico do feixe. Os limites da plantação continuam iguais.

## Trigo vanilla

Substitua `minecraft:wheat` AGE 0–7 por `assets/minecraft/`, preservando as mecânicas vanilla e a prioridade dos resource packs. Cada estágio tem quatro sprites botânicos distintos em 32×32, combinados em quatro variantes de modelo, cada uma com quatro rotações. A plantação usa quatro elementos desencontrados com duas faces; AGE 6–7 acrescentam seis folhas curvas para fora, em alturas variadas, cada uma com dois segmentos conectados, totalizando dezesseis elementos. Caules e folhas ficam verdes em AGE 0–4, verde-amarelados em AGE 5, oliva/palha em AGE 6 e palha dourada em AGE 7. As espigas maduras precisam ser estreitas, com grãos agrupados e barbas discretas. Mantenha poucas folhas limpas, caules visíveis e folhagem basal discreta; o volume vem principalmente das espigas e das hastes em camadas. AGE 4–7 ganham altura gradualmente; AGE 6 usa quatro alturas superiores (18/20/21/24) e AGE 7 maduro usa 19/21/23/26. O maior perfil chega a cerca de 1,69 bloco incluindo a base enterrada. Salve os seis projetos adicionais de altura como `wheat_stage6_variant1..3.bbmodel` e `wheat_stage7_variant1..3.bbmodel`; os caminhos exportados das variantes permanecem iguais. O contorno de interação vanilla permanece igual: colha pelo bloco inferior original.

Atualize os itens de trigo e sementes nos mesmos caminhos, usando pixel art nativa em 16×16. Consulte [o relatório visual](../wheat-visuals.pt-BR.md) para caminhos, prévias, verificação e o pacote independente opcional.

A caixa de colisão/contorno atual é 12×16×12 centralizada (`Block.column(12.0, 0.0, 16.0)` em `WheatSheafBlock`). Se a silhueta final ficar claramente mais fina ou mais larga, atualize esse valor.

## Ícone do mod

| Arquivo | Conteúdo |
|---|---|
| `icon.png` | 512×512, estilo pixel art: um feixe de trigo dourado sobre um bloco de terra arada, fundo limpo. Legível em 64×64. |

## Pronto quando

- [ ] Todos os arquivos acima substituídos, com os mesmos nomes.
- [ ] `./gradlew :neoforge:runClient` mostra os itens certinhos na aba criativa Farmer+, na mão e no chão; o feixe fica bonito colocado no mundo.
- [ ] Nenhum aviso de modelo/textura do `farmerplus` no log.
