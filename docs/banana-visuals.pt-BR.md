# Visual da bananeira

[English](banana-visuals.md) | **Português**

Os arquivos provisórios da tarefa 0006 foram substituídos no mesmo lugar. As doze texturas da bananeira são grades de pixels desenhadas manualmente, em RGBA 16×16 e alfa binário. Os quarenta modelos Java de blocos, incluindo o engaço colhido e a folha seca diagonal, têm fontes `.bbmodel` portáteis com texturas embutidas exportadas pelo Blockbench 5.2.2 via MCP local. Os ids, nomes de modelos existentes e caminhos de texturas foram preservados.

![Bananeira no jogo, captura fornecida durante a revisão](images/banana-in-game.png)

O usuário forneceu esta captura durante a primeira revisão. Ela é anterior à revisão das folhas largas e dobradas descrita abaixo. A distância da câmera não foi informada; ela não comprova a verificação específica a 20 blocos.

## Refinamento das folhas após a revisão

A prancha de inspiração orienta a silhueta larga de remo e a curvatura da nervura, sem reproduzir seus detalhes pintados. O limbo vivo passou de 13 para 16 pixels de modelo de largura, cerca de 23% a mais. O pecíolo ficou mais curto, o começo arredondado do limbo se aproxima da copa e o afinamento se concentra no final da folha. Seis trechos longitudinais formam o arco. As duas metades caem 12° a partir da nervura elevada, criando uma dobra suave e superfícies visíveis por baixo. Os grupos de pixels verdes têm brilho mais suave, nervuras menos contrastadas e rasgos assimétricos nas margens.

Cada metade tem uma seção fina de 0,55 pixel e avança 0,65 pixel além dos encaixes nominais. As UVs das faces de fechamento acompanham o afinamento, evitando pixels verdes soltos fora da ponta. Os pontos da nervura continuam coincidentes; as superfícies dobradas se sobrepõem nas curvas, sem exigir que bordas com inclinações diferentes ocupem a mesma linha. O validador amostra as duas metades em cada curva interna e emenda de blocos, nas oito direções. Os segmentos cardinais têm 7/6/6 elementos; os diagonais têm 7/12. Todos respeitam o limite por modelo. Os painéis diagonais dobrados usam rotações Euler compostas para manter a nervura montada exatamente na direção nordeste; a nervura preserva Y=-45°.

![Mesma planta salva e mesma escala de câmera antes e depois da revisão](images/banana-leaves-comparison.png)
![Folhas revisadas renderizadas no Blockbench](images/banana-leaves-blockbench.png)
![Folhas revisadas vistas por baixo no Blockbench](images/banana-leaves-underside.png)

Estas são prévias dos modelos, não novas capturas do Minecraft. A geometria dos frutos não foi alterada nesta revisão das folhas.

## Anatomia e geometria

- O pseudocaule verde-amarelado mantém a coluna de 6 pixels em x/z 5–11, a base de 8 pixels, manchas marrons nas bainhas, tiras secas, bainhas abertas na copa e o charuto claro enrolado.
- As folhas novas sobem e as maduras caem. Cada segmento parte dos pontos reais de encaixe; o comprimento antes da rotação compensa a inclinação. As nervuras cardinais e diagonais coincidem exatamente, enquanto as superfícies dobradas se sobrepõem em toda a largura.
- A nervura permanece nas colunas 7–8. Os rasgos entram pelas bordas acompanhando as nervuras; a textura da ponta afina para cima e a folha morta afina para baixo. O filhote tem três folhas estreitas em pé.
- Cada banana tem volume sólido: três cuboides sobrepostos e inclinados formam a curva ascendente. Oito frutos circundam o engaço por penca, com orientação alternada entre as pencas. A extremidade escura fica voltada para dentro, junto ao engaço, conforme solicitado na revisão. A extremidade externa usa a cor do fruto.
- O botão não tem frutos; a floração tem duas pencas menores; os estágios verde e maduro têm quatro pencas completas. O engaço nu continua até um coração vinho, afilado em degraus.

![Cacho sólido visto de três ângulos](images/banana-bunch-3d.png)
![Os quatro estágios do cacho](images/banana-bunch-stages.png)
![Texturas manuais ampliadas por vizinho mais próximo](images/banana-textures.png)

## Cacho colhido e display no ombro

O cacho colhido em pé reutiliza as mesmas oito meias pencas maduras. A geometria e as posições delas não foram alteradas. `validate_banana_carry.py` compara os oito centros geométricos com `HAND_CENTERS`; as coordenadas arredondadas do Java continuam correspondendo, sem necessidade de mudança no código. As 32 combinações de orientação/quantidade mantêm o núcleo e exatamente as peças restantes, retiradas de baixo para cima.

O engaço passou a ter seis elementos: eixo estreito dentro dos frutos, região de pegada reforçada, pequeno colar e duas fibras se soltando. O topo permanece em Y=19,5, preservando o encaixe da mão. Uma tampa chanfrada usa a textura original de corte claro e concêntrico em toda a face superior. O novo atlas original `banana_bunch_stalk.png` usa sete cores escolhidas manualmente para as fibras longitudinais, sem alterar a textura do pseudocaule da planta. O cacho colhido cheio soma 102 elementos nas nove partes.

![Cacho colhido em pé, de oito até uma peça restante](images/banana-harvested-stages.png)
![Oito estados realmente colocados e lidos do mundo de teste Fabric salvo](images/banana-harvested-world.png)

Os nove arquivos `models/item/banana_bunch_*.json` receberam o mesmo display exportado pelo editor de display do Blockbench. Após a captura em F5 fornecida pelo usuário abaixo, a rotação da terceira pessoa foi refinada para `[57,0,156]`, com translação `[3.08642,3.5033,7.33115]`, preservando a escala `[1.1,1.1,1.1]`. O cacho gira em torno do centro do toquinho segurado, em (8;17,75;8,5): o encaixe original na mão se desloca menos de 0,001 pixel de modelo. Isso baixa o corpo dos frutos e o afasta lateralmente da cabeça sem mudar o tamanho. O cálculo segue a ordem XYZ do quaternion de `ItemTransform` no Minecraft 26.3, conferida na classe local do jogo. A posição existente em primeira pessoa foi preservada. A translação vertical da GUI foi refinada para -1,25; no chão, ficou em 3,2, acompanhando a base reduzida; no modo fixo, há rotação de 15° em Y. O item completo de nove partes foi montado no Blockbench para as prévias de GUI/chão/fixo, sem avaliar apenas o toquinho isolado.

![Captura de revisão em F5 do usuário, anterior ao ajuste em torno da pegada](images/banana-shoulder-review.png)

Essa imagem mostrou sobreposição com a cabeça e motivou o ajuste final da inclinação; ela não representa aprovação desse ajuste. Ainda é necessária uma nova captura em F5 e a inspeção em primeira pessoa.

![Item composto inteiro no editor de display da GUI](images/banana-display-gui.png)
![Referência do display no chão](images/banana-display-ground.png)
![Referência do display fixo](images/banana-display-fixed.png)

Estas prévias conferem o enquadramento no editor. Elas não comprovam o braço levantado pelo código, o contato com o ombro em F5 nem o recorte na primeira pessoa; essas verificações no jogo permanecem pendentes porque o Computer Use foi interrompido com Escape, inclusive após o pedido posterior para continuar.

## Encaixe seco diagonal e hitboxes

A revisão encontrou estados secos diagonais reutilizando o modelo cardinal, deixando o pecíolo afastado do caule. O novo `banana_leaf_dry_diagonal` preserva os nomes existentes e coloca a raiz no centro do caule vizinho (-8,24), com rotação local de -45° em Y. Apenas as doze variantes secas diagonais (quatro direções × três segmentos) selecionam esse modelo adicional. As folhas vivas e as peças do cacho mantêm suas posições.

`python art/banana_leaf_shapes.py` foi executado novamente após a exportação e a mudança do blockstate. O arquivo gerado agora tem 48 formas únicas e 72 mapeamentos de estado, incluindo as quatro diagonais secas. A prancha de direções cobre young, mature e dry nas oito direções.

![Folhas secas nas oito direções colocadas no mundo de teste](images/banana-dry-world.png)

## Custo da geometria do cacho na planta

Os frutos sólidos usam composição aditiva `multipart` dos blockstates vanilla. Cada meia penca é um modelo Java separado com 12 elementos; os modelos originais dos cachos ficam como núcleo do pedúnculo, engaço e coração. Foram acrescentados vinte arquivos de modelos de pencas e suas fontes Blockbench. Nenhum nome existente foi removido ou renomeado. Não há renderizador próprio, entidade de bloco ou processamento por tick de renderização.

| Estágio | Núcleo | Partes adicionais | Total de elementos por cacho colocado |
|---|---:|---:|---:|
| Botão | 8 | 0 | 8 |
| Floração | 8 | 4 × 12 | 56 |
| Verde | 8 | 8 × 12 | 104 |
| Maduro | 8 | 8 × 12 | 104 |

O limite de doze elementos é atendido **por modelo**, e não pelo cacho montado. O aumento de geometria em relação ao provisório é significativo e precisa ser considerado na revisão. Pomares densos não foram medidos. Usar apenas o modelo do núcleo remove os frutos; preserve o blockstate multipart ao integrar os arquivos.

## Referências e procedência

- [ProMusa: morfologia da bananeira](https://www.promusa.org/Morphology+of+banana+plant): bainhas sobrepostas, anatomia do limbo e da nervura, rasgos, charuto, filhotes de folhas estreitas, pencas e coração. Consultado em 18 de outubro de 2026.
- [Kew POWO: Musa acuminata subsp. microcarpa](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:60457966-2/general-information): identidade e contexto botânico. Consultado em 18 de outubro de 2026.
- O estudo abaixo foi criado com a ferramenta integrada de geração de imagem para explorar paleta e formas. É uma ilustração por IA, não uma fotografia botânica nem uma fonte de pixels das texturas. Nenhum pixel gerado foi reduzido, decalcado ou colado nos atlas distribuídos; `art/banana_pixels.py` contém cada pixel escolhido manualmente.
- As prévias dos modelos são renderizações próprias dos arquivos do repositório. A captura do jogo foi fornecida pelo usuário. Não são redistribuídas fotografias botânicas de terceiros nem texturas da Mojang.

![Estudo conceitual gerado, não usado como textura](images/banana-reference-study.png)

O prompt usado na ferramenta integrada pediu uma prancha botânica de Musa Prata/Nanica para orientar um artista de pixel art 16×16, com pseudocaule verde-amarelado manchado, bainhas secas, folhas largas rasgadas, nervura clara, charuto, filhote de folhas estreitas e cachos verdes e maduros com quatro pencas curvadas para cima e coração vinho. Pediu fundo marfim, luz superior esquerda, amostras de verde natural, ocre, creme e vinho, sem texturas da Mojang, sprites ou capturas de jogo. O texto do prompt está registrado na [versão inglesa](banana-visuals.md#references-and-provenance).

## Reprodução

1. Execute `python art/banana_pixels.py` para gravar os onze atlas manuais e a prancha ampliada por vizinho mais próximo.
2. Execute `python art/banana_models.py` para preparar as 38 entradas de geometria e o blockstate multipart dos cachos.
3. Com o Blockbench aberto, chame `exportBanana(root)` de `art/export_banana.js` pelo MCP. Isso salva as fontes editáveis e os modelos Java, verificando ângulos Euler e quantidades de elementos.
4. Execute `./gradlew build`, `python art/validate_wheat_art.py` e `python art/validate_banana_art.py`.
5. No mundo de testes existente do servidor Fabric, use `gamerule minecraft:random_tick_speed 0`. Coloque plataformas de grama em y=199 ao redor de (100,100), (120,100), (140,100) e (160,100). Execute `place feature farmerplus:banana_plant X 200 100` nos três primeiros locais e `place feature farmerplus:wild_banana_clump 160 200 100`. Salve com `save-all flush`.
6. Execute `python art/preview_banana.py` para regenerar as pranchas de estágios, ângulos, direções e mundo salvo. A prancha das direções é uma montagem controlada; a das plantas geradas lê os blocos reais salvos pelo servidor. Isso também prepara a lista de blocos usada por `previewBananaLeaves(root)` em `art/preview_banana_blockbench.js`; chame essa função pelo MCP para as prévias por GPU acima.
7. O exemplo original também funciona: `python art/preview_world_models.py --box 35 45 35 45 199 207 --scale 34 --yaw 200 --tilt 0.3 --out docs/images/banana-plant.png`.

**Não execute `python art/banana_art.py`: ele sobrescreveria os modelos finais e o blockstate multipart.**

Para reproduzir o acabamento do cacho colhido, execute `python art/finish_banana_bunch.py` e chame `finishBananaCarry(root)` de `art/export_banana_carry.js` pelo MCP. O helper escreve as entradas de arte; o Blockbench grava o engaço final e sua fonte, além de sincronizar o display dos nove modelos de item. `previewBananaCarry(root)`, em `art/preview_banana_carry.js`, gera as prévias do editor. Se precisar executar `art/banana_bunch_art.py` para regenerar o blockstate colhido ou o item composto, reaplique esse acabamento depois: o gerador restaura o engaço provisório e os valores padrão de display.

Para as folhas secas diagonais, execute `python art/finish_banana_dry.py`, exporte `banana_leaf_dry_diagonal` com `exportBanana(root, ['banana_leaf_dry_diagonal'])` e rode `python art/banana_leaf_shapes.py`. Regenere sempre as formas após mudar qualquer modelo de folha ou o blockstate das folhas. Execute também `python art/validate_banana_carry.py`, além dos validadores existentes.

![Plantas geradas pela feature no servidor](images/banana-generated-plants.png)
![Folhas young, mature e dry nas oito direções](images/banana-leaf-directions.png)

## Verificações e limites

Em 18 de outubro de 2026, o build da arte final passou. `validate_wheat_art.py` passou em 24.557 verificações, sem erros; `validate_banana_art.py` passou em 3.588, sem erros; `validate_banana_carry.py` passou em 95, sem erros. As verificações cobrem alfa binário, RGBA 16×16, coordenadas, UVs, pixels embutidos nas fontes, as dezesseis combinações de estágio/orientação dos cachos na planta, as 32 combinações de orientação/quantidade do cacho colhido, displays compartilhados, pegada preservada, encaixes secos e arquivos idênticos nos jars Fabric, NeoForge e Forge. As plantas do mundo salvo contêm folhas vivas nas oito direções. Oitenta verificações de curvas internas e emendas conferem os pontos das nervuras e 640 amostras de sobreposição das superfícies dobradas. A maior diferença entre nervuras é de aproximadamente 0,0000065 pixel de modelo. As prévias do Blockbench foram inspecionadas por cima e por baixo.

A instância de `:neoforge:runClient` da arte final carregou os atlas de blocos e itens sem avisos de modelo/textura do Farmer+ (`build/banana-final-client.log`). O controle de tela foi interrompido antes da inspeção solicitada em F5/primeira pessoa. A conexão local ao servidor rejeitou inicialmente o jogador de teste pela whitelist; essa identidade foi adicionada, e um mundo local foi aberto em seguida por interação do usuário. Isso não comprova o alinhamento no ombro. O último ajuste do display em torno da pegada foi validado numericamente e exportado no Blockbench depois dessa execução; sua verificação visual no jogo continua pendente. Os avisos independentes dizem respeito ao loot do trigo pisoteado, datapacks de teste ausentes, contadores do Windows e tags de itens sem tradução. Uma disputa inicial na cópia de recursos entre build e servidor simultâneos foi resolvida executando o build final em sequência, após parar o servidor dedicado.

O usuário interrompeu o Computer Use com Escape durante a inspeção visual adicional; não foram enviados outros comandos de interface. A captura fornecida registra a planta nova no jogo, mas a verificação à distância exata de 20 blocos permanece **pendente**. As prévias por software usam iluminação simplificada e não descartam faces traseiras pela GPU; não comprovam a iluminação do jogo, todos os ângulos nem desempenho em pomares. As interações de colheita e tempos de crescimento não foram retestados. Nenhum commit foi criado.
