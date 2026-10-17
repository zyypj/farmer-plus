# Morangos

[English](strawberries.md) | **Português**

O morango funciona como um arbusto de frutas — você colhe e a planta continua produzindo — mas é **plantado como plantação, só em terra arada**. Na natureza existe um parente menor, o **morango silvestre**, que nasce na grama e dá os primeiros morangos.

## Começando

1. Encontre **morangos silvestres** em planícies, planícies de girassóis, campinas, florestas, florestas floridas, florestas de bétulas e florestas salpicadas.
2. Clique com o botão direito numa moita madura para colher 1–2 morangos (ou quebre para obter o mesmo).
3. Plante um morango em **terra arada**. Ele não pode ser plantado em grama nem em terra comum.

## Crescimento

| Idade | Estágio | Observações |
|---|---|---|
| 0 | Muda | Coroa pequena com poucas folhas |
| 1 | Folhagem | Roseta cheia de folhas trifoliadas |
| 2 | Florindo | Flores brancas de cinco pétalas |
| 3 | Fruto verde | Morangos verdes; não dá para colher |
| 4 | Maduro | Morangos vermelhos; clique com o botão direito para colher |

- Precisa de luz 9+. Cresce mais rápido em terra arada **molhada** (≈1 a cada 5 random ticks) do que em terra arada seca (≈1 a cada 8).
- **Colher** (botão direito numa planta madura) dá 2–4 morangos e a planta volta para *florindo*, produzindo de novo.
- **Quebrar** devolve a planta (1 morango), mais 1–3 se estiver madura (Fortuna funciona).
- **Estolões:** enquanto floresce ou frutifica, a planta às vezes solta um estolão que enraíza num bloco de **terra arada vazia** ao lado, como os morangos de verdade. Caminhos, grama e terra comum bloqueiam o espalhamento.
- Farinha de osso avança um estágio.
- Comer um morango recupera 2 de fome. Aldeões podem comer; dá para compostar.

## Morangos silvestres

Os silvestres nascem em grama/terra, nunca em terra arada, crescem devagar (≈1 a cada 10 random ticks), não se espalham e dão 1–2 morangos. Eles existem para o jogador começar a fazenda sem receitas nem trocas novas.

## Compatibilidade com modpacks

- A planta cultivada aceita qualquer bloco da tag `minecraft:supports_crops`, então terras aradas de outros mods que entrem nessa tag funcionam.
- Os morangos estão em `c:foods/berry` e `c:foods/fruit`.
- A geração silvestre é controlada pela tag de bioma `farmerplus:has_wild_strawberries` (data packs podem adicionar ou remover biomas) e pela placed feature `farmerplus:patch_wild_strawberries`.

| Loader | Como os silvestres entram nos biomas |
|---|---|
| NeoForge | `data/farmerplus/neoforge/biome_modifier/wild_strawberries.json` |
| Forge | `data/farmerplus/forge/biome_modifier/wild_strawberries.json` |
| Fabric | `FabricWorldgen`, que lê `BiomeFeatures` do código comum |

Ao adicionar uma feature de bioma nova, registre em `BiomeFeatures` (Fabric) **e** crie os arquivos de biome modifier equivalentes do NeoForge e do Forge.

## Desempenho

Sem handlers de tick nem mixins. As plantas usam random ticks do vanilla só até amadurecer; plantas maduras param de receber tick. Os drops da colheita vêm de loot tables em dados (`harvest/strawberry_plant`, `harvest/wild_strawberries`).

## Arte

Os modelos atuais são provisórios (planos em cruz). Os modelos 3D de verdade estão descritos na [tarefa de arte 0003](art-tasks/0003-strawberries.pt-BR.md).
