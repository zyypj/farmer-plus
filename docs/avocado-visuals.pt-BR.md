# Arte do abacateiro e do trigo esmagado

[English](avocado-visuals.md) | **Português**

As tarefas de arte 0005 e 0002 substituem as imagens provisórias nos mesmos caminhos. Vinte e seis imagens do abacateiro e doze sprites de trigo esmagado agora usam desenhos originais com pixels duros. Texturas de blocos e itens são 16×16. Os atlas das entidades dos barcos e as telas de placas mantêm as dimensões do layout vanilla, conforme a tarefa 0005.

## Árvore e madeira

A casca marrom-acinzentada tem fissuras curtas e irregulares e pequenas placas. Cortes de tora e madeira descascada mostram madeira creme levemente rosada. Tábuas, porta, alçapão vazado, placas, prateleira e barcos compartilham essa paleta quente. As folhas usam grupos grandes e alongados de verde-escuro, com pequenos espaços transparentes e nervuras claras; a muda tem cinco folhas grandes. A casca dos frutos verdes é lisa, enquanto os maduros têm sombras verde-escuras/arroxeadas e pequenos realces rugosos. O item tem silhueta de pera e cabinho curto.

![Texturas nativas da árvore e da madeira](images/avocado-textures.png)

![Texturas adicionais de madeira e layouts nativos das entidades](images/avocado-wood-extras.png)

## Modelos pendurados

O blockstate multipart das folhas e todos os nomes de recursos foram preservados. Cada sobreposição é um modelo Java Block/Item exportado pelo servidor MCP do Blockbench, salvo em `art/blockbench/avocado_leaves_<estágio>.bbmodel` com um atlas 16×16 embutido.

| Sobreposição | Elementos | Limites verticais após rotação | Arranjo |
|---|---:|---|---|
| `avocado_leaves_flowers` | 8 | −3,30…0 | Dois pequenos cachos ramificados com cabos e flores sólidos |
| `avocado_leaves_unripe` | 8 | −4,94…0 | Uma pera verde menor, sete partes conectadas no corpo e um cabo |
| `avocado_leaves_ripe` | 8 | −6,08…0 | Uma pera escura maior, sete partes conectadas no corpo e um cabo |

Um fruto por sobreposição permite modelar gradualmente o pescoço fino, a barriga larga embaixo e a base menor arredondada dentro do limite de oito elementos. As partes compartilham uma leve inclinação e alturas contínuas de UV nas laterais. Isso substitui a sugestão inicial de duas frutas em caixas da tarefa, preservando sua opção de um fruto e o limite de desempenho. Todos os vértices rotacionados ficam dentro de X/Z=0…16 e Y=−8…0. O estágio de floração continua mostrando flores.

![Comparação nativa do Blockbench abaixo das folhas](images/avocado-canopy-front.png)

## Trigo esmagado

As doze texturas AGE 2–7, base e alternate, foram desenhadas com arranjos diferentes de caules partidos. Tocos curtos quebrados ocupam as linhas inferiores. Caules dobrados, pontas de folhas rasgadas, espigas incompletas e grãos maduros soltos passam de verdes machucados para palha opaca e empoeirada. Os sprites não contêm terra nem lama. A cobertura dos pixels nativos em 16×16 fica em cerca de 14–27%, deixando aproximadamente 73–86% de cada sprite aberto; as prévias do campo ajudaram a evitar um tapete sólido quando os quatro planos do modelo se sobrepõem.

Os 48 modelos de trigo pisoteado e a geometria do blockstate continuam iguais. `art/trampled_wheat.py` agora delega os pixels esmagados AGE 2–7 a `art/crushed_pixels.py`, portanto regenerar os modelos preserva a arte final. As imagens AGE 0–1 não foram alteradas.

![Os doze sprites esmagados](images/crushed-wheat-textures.png)

![Renderização offline dos modelos de trigo distribuídos](images/trampled-wheat.png)

## Reprodução e verificações

1. Rode `python art/avocado_pixels.py` e `python art/avocado_wood_pixels.py` para gerar as texturas e entradas dos modelos do abacateiro.
2. Com o Blockbench aberto, execute `exportAvocado(root)` de `art/export_avocado.js` pelo MCP. As fontes nativas e os JSONs finais são salvos juntos.
3. Rode `python art/crushed_pixels.py`. O gerador do pisoteio também usa essa função de desenho ao reconstruir.
4. `previewAvocado(root)` em `art/preview_avocado.js` renderiza a comparação das folhas pelo MCP; `python art/preview_trampled_wheat.py` renderiza offline os modelos distribuídos do trigo pisoteado.
5. Rode `./gradlew build` e `python art/validate_wheat_art.py`.

O build e o validador passaram. As verificações incluem igualdade das texturas nativas embutidas, todos os vértices rotacionados dos abacates, limites de elementos, transparência/variação do trigo esmagado e bytes atuais dos recursos nos jars dos três loaders. O relatório da exportação MCP fica em `build/art/validation/avocado-blockbench.json`.

A imagem das copas é uma renderização do Blockbench e o campo de trigo é uma renderização offline dos modelos. A inspeção manual de uma árvore crescida e do pisoteio repetido em sobrevivência dentro do Minecraft ainda está pendente; o relatório `build/art/validation/avocado-crushed-resource-load.json` registra separadamente o carregamento no NeoForge.
