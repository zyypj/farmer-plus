# Pipeline de arte

[English](art-pipeline.md) | **Português**

A arte do Farmer+ segue **Vanilla+ realista**: pixel art reconhecível como Minecraft, com anatomia vegetal, proporções, camadas e sombreamento de materiais mais convincentes. Os detalhes precisam melhorar a silhueta e funcionar no campo inteiro, no inventário e à distância normal de jogo.

## Regras de estilo

- **32×32 pixels** para a reformulação do trigo e todos os recursos existentes relacionados a ele: os oito estágios e sprites alternativos, trigo, sementes, farinha, massa, mingau e todas as texturas do feixe. Desenhe diretamente na grade 32×32; não apenas amplie a arte antiga de 16×16. Outros conteúdos continuam em 16×16 até sua tarefa de arte definir outra resolução. O ícone permanece em 512×512.
- **PNG, RGBA, 8 bits.** Fundo transparente nos itens. Sem pixels semitransparentes, exceto materiais tipo vidro.
- **Sem anti-aliasing, degradês contínuos, desfoque ou texturas fotográficas.** Use grupos de pixels definidos e sombreamento em degraus. Amplie as prévias pelo vizinho mais próximo.
- **Paleta limitada.** Em geral, 5–8 tons por material, com verdes, palha, ocres e cremes naturais. Evite pontilhado aleatório e contraste excessivo entre caules vizinhos.
- **Anatomia vegetal.** O trigo tem caules afunilados, com sombra longitudinal suave e nós discretos de um pixel e espigas estreitas e alongadas, compostas por pequenos grupos alternados de grãos e poucas barbas curtas conectadas. Deixe o caule visível entre espiga e folhagem. Evite hastes grossas e retas, anéis transversais repetidos e faixas claras nos nós que lembrem bambu. Use poucas folhas longas e estreitas arqueadas na base e no meio. O estágio maduro tem uma lâmina basal discreta em cada sprite e seis folhas modeladas por bloco, variando em altura e comprimento e arqueadas para fora. Mantenha o material limpo, sem grades de folhas sobrepostas. Prenda as folhas aos caules externos, abaixo das espigas, e alinhe os UVs dos dois lados e das duas metades de cada curva. Evite espigas grossas de milho, folhas superiores envolvendo as espigas, panículas de sorgo e silhuetas lisas de taboa. Os brotos partem do solo e as espigas continuam ligadas aos caules.
- **Grandes grupos de pixels em vez de detalhe HD.** A grade 32×32 dá espaço para formas e massas mais fortes, sem buscar uma retexturização fina no estilo Faithful. Evite hastes de um fio de pixel, aristas isoladas, contornos de grãos ruidosos e aparência de capim seco pontudo. A silhueta e a densidade central do trigo maduro têm prioridade sobre marcas botânicas minúsculas.
- **Cor no amadurecimento.** Mantenha AGE 0–4 verdes, introduza verde-amarelado em AGE 5, misture oliva e palha em AGE 6 e deixe caules, folhas e espigas AGE 7 em tons de palha dourada. Use paletas por estágio e sombras em pixels definidos; não acrescente faixas transversais nem engrosse os caules para mostrar maturidade.
- **Campos naturais.** Varie a altura das espigas e a direção das folhas com poucas rotações determinísticas e sprites alternativos. Mantenha as bases no solo e espaços entre as folhas. O volume vem dos vários caules e planos sobrepostos, sem formar paredes sólidas de vegetação.
- **Variação e altura do trigo.** Cada estágio tem quatro sprites desenhados separadamente e quatro combinações de modelo, cada uma com quatro rotações espaciais. AGE 4–7 ultrapassam um bloco gradualmente; AGE 6 usa Y superior 18/20/21/24 e AGE 7 maduro usa 19/21/23/26. As quatro combinações de modelo existentes também fornecem esses perfis de altura, com seleção estável por posição e pesos iguais. Os encaixes das folhas acompanham os caules e cada curva mantém seu ângulo original. Preserve o contorno de interação vanilla e faça a colheita pelo bloco inferior. A altura visual não cria um bloco superior nem outro registro de plantação.
- **Luz vindo de cima à esquerda**, como no vanilla: brilho no canto superior esquerdo, tom mais escuro no inferior direito.
- **Silhuetas de itens** têm contorno de 1 pixel mais escuro no lado sombreado, igual às comidas vanilla.
- **Nunca copie nem decalque texturas da Mojang.** Use-as só como referência visual.

## Pastas

| O quê | Onde | Vai no jar |
|---|---|---|
| Texturas de item | `common/src/main/resources/assets/farmerplus/textures/item/<id>.png` | sim |
| Texturas de bloco | `common/src/main/resources/assets/farmerplus/textures/block/<id>[_parte].png` | sim |
| Substituições do trigo vanilla | `common/src/main/resources/assets/minecraft/{blockstates,models,items,textures}/…` | sim |
| Modelos de bloco (exportados) | `common/src/main/resources/assets/farmerplus/models/block/<id>.json` | sim |
| Ícone do mod | `common/src/main/resources/assets/farmerplus/icon.png` (quadrado, 128×128 ou 512×512) | sim |
| Projetos do Blockbench | `art/blockbench/<id>.bbmodel` | não |
| Arquivos de trabalho/camadas | `art/textures/…` | não |

## Fluxo no Blockbench

1. Crie o projeto como **Java Block/Item**.
   Configure a resolução em **32×32** nos modelos de trigo. Os UVs de modelos Minecraft continuam na escala 0–16; o Blockbench converte os pixels da textura. Preserve uma escala coerente de UV, sem comprimir uma textura inteira nas faces de caules estreitos.
2. Mantenha o modelo dentro da grade 0–16 do bloco sempre que possível (o máximo do vanilla é −16…32).
3. Rotação de elementos: só em um eixo e só −45, −22,5, 0, 22,5 ou 45 graus.
4. Mantenha leve: **no máximo 12 elementos** por modelo de bloco, com **limite de 16 para o trigo AGE 6–7** e **limite de 24 para o feixe com amarração 3D sólida**. A plantação usa **quatro planos desencontrados com duas faces**. AGE 6–7 acrescentam seis folhas modeladas, cada uma formada por dois planos conectados que sobem e depois descem, totalizando **dezesseis elementos**. Essas superfícies pontuais criam profundidade sem repetir folhas em cada haste nem acrescentar geometria a cada espiga. O feixe usa oito planos de caules/espigas em camadas, um núcleo de caules comprimidos e quinze elementos sólidos de corda: quatro trechos unidos ao redor do feixe, oito segmentos formando duas voltas vazadas, um nó e duas pontas penduradas. Os quatro volumes centrais de espigas anteriores foram retirados, mantendo o total em vinte e quatro elementos e noventa e seis faces. A corda passa pelos quatro lados e encosta no núcleo; o nó conecta a volta externa, os laços e as pontas. Retire a corda pintada dos atlas dos caules para não duplicar a amarração. Use o atlas original de barbante em 32×32 na geometria da corda. O ícone próprio de inventário em 32×32 é selecionado por `minecraft:display_context` vanilla; os demais contextos mantêm o modelo 3D do bloco. Sem renderizador próprio, block entity ou atualização estética por tick.
5. Dê às texturas exatamente o nome final do recurso (ex.: `wheat_sheaf_side`) e use o namespace `farmerplus`, para o JSON exportado apontar para `farmerplus:block/<nome>`.
6. Configure os transforms de **Display** para `gui`, `ground`, `fixed`, `thirdperson_righthand` e `firstperson_righthand`, para o item ficar certo no inventário e na mão.
7. Salve o projeto-fonte em `art/blockbench/<id>.bbmodel`.
8. Exporte o **Block/Item Model** para `models/block/<id>.json` e as texturas para `textures/block/`.
9. Se a silhueta de um bloco mudar, atualize o `VoxelShape` na classe do bloco para o contorno e a colisão baterem.
   Preserve o contorno, a colisão, o crescimento e as interações da plantação vanilla. A substituição visual não registra uma segunda plantação de trigo.

## Conectando o Blockbench a um agente de IA (MCP)

O repositório já vem com `.codex/config.toml`, que aponta o Codex para o servidor MCP do Blockbench.

1. Instale o Blockbench (desktop): <https://www.blockbench.net/downloads>
2. No Blockbench: **File → Plugins → Load Plugin from URL** e cole
   `https://jasonjgardner.github.io/blockbench-mcp-plugin/mcp.js`
3. Deixe o Blockbench aberto. O servidor escuta em `http://localhost:3000/bb-mcp`.
4. O Codex lê `.codex/config.toml` em projetos confiáveis. Para adicionar de forma global:
   ```bash
   codex mcp add blockbench --url http://localhost:3000/bb-mcp
   ```
5. Reinicie o Codex e rode `/mcp` para confirmar que o `blockbench` está conectado.

O plugin consegue executar JavaScript dentro do Blockbench (`risky_eval`). Deixe o servidor preso ao `localhost`.

## Conferindo o resultado

```bash
./gradlew :neoforge:runClient
```

Abra a aba criativa **Farmer+** e confira cada item no inventário, na mão, jogado no chão e colocado (no caso de blocos). O log não pode ter avisos de textura ou modelo do `farmerplus`.

Inspecione AGE 0–7 em ordem e um campo maduro grande. Compare o feixe de frente, de lado e de cima. Execute `./gradlew build` e `python art/validate_wheat_art.py` para conferir dimensões e alpha dos PNGs, limites de UV, dependências, texturas incorporadas nos projetos Blockbench e recursos idênticos nos jars Fabric, NeoForge e Forge.

Consulte [o relatório visual do trigo](wheat-visuals.pt-BR.md) para a cadeia de substituição, o pacote independente opcional, as etapas de reprodução e as limitações dos testes. A prioridade dos resource packs continua sob controle do jogador.
