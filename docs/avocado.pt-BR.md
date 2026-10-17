# Abacateiro

[English](avocado.md) | **Português**

Uma árvore frutífera em tamanho real, com um conjunto completo de madeira compatível com o vanilla. Abacateiros silvestres crescem nas selvas; suas folhas florescem, dão fruto e amadurecem várias e várias vezes.

## A árvore

- **Tamanho:** 10–15 blocos de altura, com copa larga e arredondada formada por galhos (`minecraft:fancy_trunk_placer` + `minecraft:fancy_foliage_placer`, raio 3), próxima de um abacateiro real de 9–12 m.
- **Muda:** cresce como uma muda vanilla, mas na metade da velocidade (≈1 a cada 14 random ticks por estágio, luz 9+). Precisa de espaço para a copa inteira.
- **Árvores silvestres:** selva esparsa, selva e selva de bambu (`farmerplus:has_avocado_trees`), cerca de uma árvore a cada seis chunks.
- A árvore é feita só de dados: `data/farmerplus/worldgen/feature/avocado_tree.json`. Ajuste tronco e copa por lá.

## Frutificação

Só folhas **naturais** (colocadas pela árvore, não pelo jogador) dão fruto, e só as que têm **ar embaixo** e seguem um padrão espaçado, então uma árvore madura carrega uma quantidade realista de abacates (cerca de 5% das folhas).

| Estágio | `fruit` | Aparência | Próximo estágio |
|---|---|---|---|
| Folhas | 0 | Folhas comuns | Flores (≈1 a cada 24 random ticks) |
| Florindo | 1 | Florzinhas amarelo-esverdeadas embaixo das folhas | Fruto verde (≈1 em 8) |
| Verde | 2 | Abacates pequenos e verdes pendurados | Maduro (≈1 em 10) |
| Maduro | 3 | Abacates grandes e escuros pendurados | Cai sozinho (≈1 em 40) |

- **Colher:** botão direito nas folhas com fruto maduro dá um abacate; as folhas começam um novo ciclo, então a árvore frutifica muitas vezes.
- **Quebrar** folhas maduras também dá o abacate. As folhas dão mudas (5%) e **gravetos** como as de carvalho; tesoura ou Toque de Seda dão o bloco de folhas.
- Abacate: 4 de fome, 0,6 de saturação; aldeões comem; dá para compostar.

## Conjunto de madeira

`avocado_log`, `avocado_wood`, `stripped_avocado_log`, `stripped_avocado_wood`, `avocado_planks`, `avocado_stairs`, `avocado_slab`, `avocado_fence`, `avocado_fence_gate`, `avocado_door`, `avocado_trapdoor`, `avocado_pressure_plate`, `avocado_button`, `avocado_leaves`, `avocado_sapling`.

O conjunto espelha o carvalho em tudo que importa:

- **Tags:** toda tag vanilla que lista um bloco de carvalho lista o equivalente de abacateiro (`minecraft:logs_that_burn`, `minecraft:planks`, `minecraft:wooden_*`, `minecraft:fence_gates`, `minecraft:leaves`, `minecraft:saplings`, …). Por isso as tábuas funcionam em **todas** as receitas de madeira — bancada, gravetos, baú, ferramentas, barril — e as toras funcionam em fogueira, carvão vegetal etc.
- **Receitas e loot:** iguais às do carvalho (tábuas a partir de `#farmerplus:avocado_logs`, madeira, escadas, lajes, cercas, portões, portas, alçapões, placas e botões).
- **Descascar:** botão direito numa tora ou madeira com qualquer machado (`#minecraft:axes`). A própria tora cuida disso, sem sobrescrever nenhum arquivo compartilhado do vanilla.
- **Combustível:** mesmos tempos de queima do carvalho, pelo componente de item `minecraft:cooking_fuel`.
- **Fogo:** mesma inflamabilidade do carvalho. Fabric e Forge usam a tabela de fogo do vanilla (`FireBlockAccessor`); o NeoForge usa o data map dele (`data/neoforge/data_maps/block/flammable.json`).

Placas, placas penduradas, barcos e prateleiras ainda não estão incluídos.

## Reaproveitando o conjunto de madeira

`WoodSets.register(nome, corDaMadeira, corDaCasca)` registra os 13 blocos e itens de madeira. `python tools/wood_set.py <nome>` gera blockstates, modelos, definições de item, loot tables, receitas, desbloqueios de receita e entradas de tag a partir dos moldes do carvalho vanilla. Folhas, muda, feature da árvore e texturas são próprias de cada árvore.

## Arte

As texturas são provisórias; veja a [tarefa de arte 0005](art-tasks/0005-avocado-tree.pt-BR.md).
