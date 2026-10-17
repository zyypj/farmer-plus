# Tarefa de arte 0002 — Trigo amassado

[English](0002-trampled-wheat.md) | **Português**

O trigo amassado já tem a **geometria** final (veja [docs/trampling.pt-BR.md](../trampling.pt-BR.md)). As plantas *entortadas* e *deitadas* reaproveitam os sprites dos estágios em pé. Só o estágio **esmagado** precisa de arte própria: os arquivos abaixo são provisórios gerados automaticamente (cópias escurecidas dos sprites em pé). Substitua no mesmo lugar.

Caminho base: `common/src/main/resources/assets/farmerplus/textures/block/`

## Texturas (32×32, mesmas regras de [art-pipeline.pt-BR.md](../art-pipeline.pt-BR.md))

| Arquivo | Conteúdo |
|---|---|
| `wheat_stage2_crushed.png` … `wheat_stage7_crushed.png` | Vista lateral de caules que foram pisados: hastes quebradas com dobras secas, caules rachados e desfiados, verde machucado mais escuro (jovem) ou palha opaca e empoeirada (maduro), algumas folhas rasgadas |
| `wheat_stage2_alternate_crushed.png` … `wheat_stage7_alternate_crushed.png` | Um segundo layout diferente do mesmo, para variação |

As idades 0–1 nunca são esmagadas no jogo; os `_crushed` delas podem ficar como estão.

### Como o sprite é usado

O sprite é aplicado em planos quase deitados sobre a terra arada: os **1–2 px de baixo** viram um toco curto em pé e **todo o resto fica deitado no chão**, com as espigas apontando para longe do toco. Desenhe como uma vista lateral normal em pé (igual aos sprites em pé); o modelo é que deita.

- A borda de baixo deve ser de tocos cortados/quebrados, não raízes.
- Maduro (AGE 6–7): espigas achatadas e parcialmente arrancadas, alguns grãos soltos perto das espigas, cor mais opaca e empoeirada que o trigo em pé.
- Transparência binária (0 ou 255) e com buracos de verdade para a terra aparecer — um tapete sólido fica com cara de carpete.
- Evite cores de lama/terra dentro do sprite; a terra arada embaixo já faz esse papel.

## Pronto quando

- [ ] 12 texturas substituídas (idades 2–7, base e alternate), com os mesmos nomes.
- [ ] `python art/validate_wheat_art.py` passa.
- [ ] Num mundo sobrevivência, corra várias vezes pelo trigo maduro: o caminho esmagado precisa parecer caules quebrados prensados no solo, não um erro de textura.
