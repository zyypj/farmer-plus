# Bananeira

[English](banana.md) | **Português**

A bananeira não é uma árvore. É uma erva gigante: o que parece um tronco é um **pseudocaule** de bainhas de folhas bem enroladas, cada pé dá fruto **uma vez só** e depois morre, e a planta continua viva pelos **filhotes** que o rizoma subterrâneo vai soltando. O Farmer+ monta a planta exatamente assim.

![Bananeira com cacho maduro](images/banana-plant.png) ![Touceira silvestre](images/banana-clump.png)

*Renderizações de plantas geradas pelo jogo e lidas do mundo salvo (`python art/preview_world_models.py`).*

## Planta real → jogo

| | Planta real | No jogo |
|---|---|---|
| Altura até a copa | 2,5–3 m (Nanica, Prata-Anã); 4–8 m silvestre | 3–4 blocos (pomar), 4–6 blocos (silvestre) |
| Pseudocaule | 22–30 cm de largura, um pouco mais largo na base | Coluna de 6 px com base de 8 px |
| Folhas | 12–18 vivas, limbo de 1,5–3 m × 0,4–0,9 m, pecíolo de 0,6 m | 8–10 folhas, cada uma com uns 3 blocos de comprimento e 13 px de largura |
| Copa | Folhas novas sobem do topo, as mais velhas arqueiam e as mortas ficam penduradas marrons no caule | Camada nova mais em pé, camada madura arqueada e 0–2 folhas secas penduradas |
| Cacho | Um por pé, 8–12 pencas, 20–25 kg, pendurado embaixo da copa com o coração roxo | Um bloco de cacho embaixo da copa, com pencas e coração roxo |
| Ciclo | Floresce ~6 meses após o plantio, amadurece ~4,5 meses depois e um filho seguidor substitui o pé | Cerca de uma hora de jogo do filhote ao cacho maduro, depois um filho seguidor |

Fontes: [ProMusa — morfologia da bananeira](https://www.promusa.org/Morphology+of+banana+plant), [ensaios da Embrapa com Prata-Anã e outras cultivares](https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/653602/1/Avaliacao-de-cultivares-e-hibridos-de-bananeira-no-reconcavo-baiano..pdf), [CIRAD — cultivares Cavendish](https://revues.cirad.fr/index.php/fruits/article/download/35482/36857/40496), [Kew POWO — *Musa acuminata* subsp. *microcarpa*](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:60457966-2/general-information), [*Musa acuminata* na Wikipedia](https://en.wikipedia.org/wiki/Musa_acuminata).

## Blocos

| Bloco | O que é |
|---|---|
| `banana_sapling` (Muda de Bananeira) | Um filhote novo. Cresce e vira planta (≈1 a cada 8 random ticks por estágio, luz 9+). Dropa a si mesmo. |
| `banana_stem` (Pseudocaule) | Descobre o próprio `segment`: `base` (pé mais largo), `middle` e `crown` (bainhas das folhas e a folha enrolada, o "charuto"). Precisa de chão de terra ou de outro pseudocaule embaixo; cortar derruba tudo o que estiver em cima. Dropa linha um terço das vezes — fibra de bananeira. |
| `banana_leaf` | Uma folha gigante feita de segmentos: `direction` (8 direções), `segment` (`0` pecíolo e começo do limbo, `1` limbo, `2` ponta caída; folhas diagonais usam `0` e `2`) e `age` (`young`, `mature`, `dry`). Tirar um segmento derruba o resto da folha, e cortar o pseudocaule derruba todas as folhas dele. Sem colisão. Só tesoura ou Toque Suave guardam o bloco. |
| `banana_bunch` | Fica pendurado ao lado do pseudocaule, embaixo da copa. `stage`: `0` coração roxo, `1` florescendo com pencas pequenas, `2` cacho verde, `3` maduro. |

## Ciclo de vida

1. **Filhote → planta.** O filhote vira uma planta com uma camada de folhas novas mais em pé, uma camada madura arqueada e, nas plantas mais altas, algumas folhas secas penduradas no pseudocaule.
2. **Florada.** A copa solta um cacho (≈1 a cada 20 random ticks) ao lado do pseudocaule, logo abaixo da copa, em qualquer lado livre.
3. **Fruto.** O cacho passa por coração → flor → verde → maduro (≈1 em 6 por estágio; farinha de osso avança um estágio). O cacho maduro fica até ser colhido.
4. **Colheita.** Botão direito num cacho maduro dá **6–10 bananas**. Quebrar um cacho maduro também dá as bananas; estágios anteriores não dão nada.
5. **Morte do pé.** Depois que o cacho sai (colhido, quebrado ou perdido), o pé está gasto: nunca mais floresce, logo tomba (≈1 a cada 6 random ticks) e um **filho seguidor** nasce no mesmo lugar.
6. **Touceiras.** Uma planta viva também solta filhotes novos a até 2 blocos (≈1 a cada 40 random ticks), até 4 pés e filhotes por touceira.

Com o `random_tick_speed` padrão, um filhote vira uma planta com cacho maduro em cerca de uma hora.

## Banana

4 de fome, 0,4 de saturação; aldeões comem; dá para compostar.

## Plantas silvestres

Touceiras com uma planta alta e mais 2–4 filhotes ou plantas novas nascem em selvas, selvas esparsas e selvas de bambu (`farmerplus:has_banana_plants`), cerca de uma touceira a cada quatro chunks; um terço delas já vem com cacho.

## Ajuste

`data/farmerplus/worldgen/feature/banana_plant.json` (crescimento a partir do filhote) e `wild_banana_clump.json` usam a feature `farmerplus:banana_plant` (`content/banana/BananaPlantFeature`):

| Campo | Significado |
|---|---|
| `height` | Altura do pseudocaule em blocos (2–8) |
| `leaves` | Número de folhas vivas (2–16), divididas entre a camada nova e a madura |
| `suckers` | Filhotes ou plantas novas extras em volta (0–6) |
| `bunch_chance` | Chance de a planta já vir com cacho (0–1) |

## Arte

Modelos e texturas provisórias vêm de `python art/banana_art.py`; texturas que já existem nunca são sobrescritas. A lista de arte é a [tarefa de arte 0006](art-tasks/0006-banana-plant.pt-BR.md).
