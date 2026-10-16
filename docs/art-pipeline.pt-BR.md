# Pipeline de arte

[English](art-pipeline.md) | **Português**

A arte do Farmer+ precisa ser indistinguível do vanilla. Se o jogador não consegue dizer quais itens vieram do mod, a arte está certa.

## Regras de estilo

- **16×16 pixels** para toda textura de item e bloco. Sem HD, sem 32×32.
- **PNG, RGBA, 8 bits.** Fundo transparente nos itens. Sem pixels semitransparentes, exceto materiais tipo vidro.
- **Sem anti-aliasing, sem degradê, sem desfoque.** Só bordas de pixel duras.
- **Paleta limitada.** 4–7 tons por material, baseados em (não copiados de) materiais vanilla parecidos (trigo, pão, tigelas, feno).
- **Luz vindo de cima à esquerda**, como no vanilla: brilho no canto superior esquerdo, tom mais escuro no inferior direito.
- **Silhuetas de itens** têm contorno de 1 pixel mais escuro no lado sombreado, igual às comidas vanilla.
- **Nunca copie nem decalque texturas da Mojang.** Use-as só como referência visual.

## Pastas

| O quê | Onde | Vai no jar |
|---|---|---|
| Texturas de item | `common/src/main/resources/assets/farmerplus/textures/item/<id>.png` | sim |
| Texturas de bloco | `common/src/main/resources/assets/farmerplus/textures/block/<id>[_parte].png` | sim |
| Modelos de bloco (exportados) | `common/src/main/resources/assets/farmerplus/models/block/<id>.json` | sim |
| Ícone do mod | `common/src/main/resources/assets/farmerplus/icon.png` (quadrado, 128×128 ou 512×512) | sim |
| Projetos do Blockbench | `art/blockbench/<id>.bbmodel` | não |
| Arquivos de trabalho/camadas | `art/textures/…` | não |

## Fluxo no Blockbench

1. Crie o projeto como **Java Block/Item**.
2. Mantenha o modelo dentro da grade 0–16 do bloco sempre que possível (o máximo do vanilla é −16…32).
3. Rotação de elementos: só em um eixo e só −45, −22,5, 0, 22,5 ou 45 graus.
4. Mantenha leve: **no máximo 12 elementos** por modelo de bloco. Quanto menos, melhor.
5. Dê às texturas exatamente o nome final do recurso (ex.: `wheat_sheaf_side`) e use o namespace `farmerplus`, para o JSON exportado apontar para `farmerplus:block/<nome>`.
6. Configure os transforms de **Display** para `gui`, `ground`, `fixed`, `thirdperson_righthand` e `firstperson_righthand`, para o item ficar certo no inventário e na mão.
7. Salve o projeto-fonte em `art/blockbench/<id>.bbmodel`.
8. Exporte o **Block/Item Model** para `models/block/<id>.json` e as texturas para `textures/block/`.
9. Se a silhueta de um bloco mudar, atualize o `VoxelShape` na classe do bloco para o contorno e a colisão baterem.

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
