# Tarefa de arte 0005 — Abacateiro e madeira

[English](0005-avocado-tree.md) | **Português**

A jogabilidade está pronta ([docs/avocado.pt-BR.md](../avocado.pt-BR.md)). Todas as texturas abaixo são provisórias; substitua no mesmo lugar, mantendo todos os nomes. Regras: [art-pipeline.pt-BR.md](../art-pipeline.pt-BR.md) — **16×16**, pixels duros, Vanilla+ realista. Use o servidor MCP do Blockbench para os modelos 3D dos frutos.

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

## Modelos dos frutos (Blockbench, melhoria opcional)

`models/block/avocado_leaves_flowers.json`, `avocado_leaves_unripe.json` e `avocado_leaves_ripe.json` são sobreposições desenhadas **embaixo** de um bloco de folhas (o blockstate é multipart, `fruit` 1–3). Hoje usam caixas simples. Refaça como abacates em formato de pera (2–3 cubos cada: pescoço fino, corpo largo) pendurados 3–6 px abaixo das folhas num cabinho curto, 1–2 frutos por bloco, no máximo 8 elementos por modelo. Mantenha tudo entre y = −8 e y = 0 e dentro de x/z 0–16.

## Pronto quando

- [ ] Todas as texturas acima substituídas com os mesmos nomes.
- [ ] `./gradlew build` e `python art/validate_wheat_art.py` passam.
- [ ] No jogo: uma árvore crescida parece um abacateiro (madeira clara por dentro, casca cinza, copa escura e brilhante) e os frutos maduros aparecem do chão.
