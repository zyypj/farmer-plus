# Pisoteio de plantações

[English](trampling.md) | **Português**

Andar por uma plantação deixa marca. As plantas entortam, tombam e, se você continuar usando o mesmo trajeto, são esmagadas até virar um caminho de verdade. Isso é geometria, não troca de textura: os caules são modelados inclinados, quebrados na base e deitados no chão na direção em que você andou.

![Estágios do trigo amassado e um caminho esmagado atravessando o campo](images/trampled-wheat.png)

*Renderização fora do jogo dos modelos do mod (`python art/preview_trampled_wheat.py`), não é captura de tela do jogo.*

## Estágios

| Achatamento | Nome | Aparência | Se recupera? | Drops do trigo maduro |
|---|---|---|---|---|
| — | Em pé | Plantação vanilla | — | 1 trigo + sementes (vanilla) |
| 1 | Entortado | Caules inteiros inclinados 30–47° | Levanta de novo (≈1 a cada 3 random ticks) | 1 trigo + sementes (vanilla) |
| 2 | Deitado | Caules quebrados perto da base, deitados a 70–80° | Plantas jovens voltam a *entortado* (≈1 em 6); maduras ficam no chão | 50% trigo, senão 1 semente |
| 3 | Esmagado | Tocos curtos, caules prensados no chão, mais escuros | Nunca — colha e replante | 1 semente |

Plantas com idade 0–1 são pequenas demais para serem danificadas. Uma planta entortada ou deitada para de crescer até se levantar. Farinha de osso só funciona em plantas *entortadas*.

## O que amassa

| Entidade | Regra |
|---|---|
| Jogadores | Só no sobrevivência e aventura. Agachado nunca amassa. |
| Criaturas | Só os tipos da tag de entidade `farmerplus:tramples_crops` (gado, cavalos, camelos, lhamas, cabras, farejadores, hoglins, devastadores, ursos, pandas). |

Cada vez que uma entidade **entra** num bloco de plantação ela aplica força:

| Condição | Força |
|---|---|
| Andando | +1 |
| Correndo | +1 |
| Corpo largo (≥ 1,2 bloco, ex.: cavalos, camelos) | +1 |

**Pular ou cair** em cima da plantação não transforma mais a terra arada em terra comum nem destrói a planta, como no vanilla: a terra arada é mantida e a planta é amassada (força 2, +1 em quedas de 3+ blocos, +1 para corpos largos). Plantações que ainda não têm forma amassada (ex.: cenoura) mantêm o comportamento vanilla.

Uma caminhada deixa a planta *entortada*; uma corrida ou um cavalo já deita na hora; passadas repetidas esmagam. Os caules caem na direção do movimento, então os caminhos ficam naturais.

## Configuração

Game rules (por mundo):

```text
/gamerule farmerplus:crop_trampling true|false
/gamerule farmerplus:mob_crop_trampling true|false
```

Adicione ou remova criaturas com um data pack que sobrescreva `data/farmerplus/tags/entity_type/tramples_crops.json`.

## Desempenho

- Dois mixins. `CropBlockMixin` entra em `CropBlock#entityInside`, que o Minecraft só chama enquanto uma entidade encosta numa plantação; ele sai depois de ler poucos campos, a não ser que a entidade tenha acabado de entrar num bloco novo. `FarmlandBlockMixin` entra em `FarmlandBlock#turnToBaseBlock`, que só roda quando algo cai com força na terra arada.
- Sem handlers de tick, sem block entities, sem estado por entidade. O progresso fica no próprio estado do bloco.
- A recuperação usa os random ticks do vanilla, e só plantas *entortadas* ou *deitadas* jovens recebem tick. Caminhos esmagados e plantas maduras deitadas não custam nada.
- A renderização é feita com modelos de bloco comuns: 6–8 elementos por modelo, menos que o trigo maduro em pé (16).

## Outras plantas

Qualquer bloco pode ser pisoteado implementando `Trampleable#trample(state, force, direction)` e chamando `CropTrampling.onEntityInside` no seu próprio `entityInside` — blocos do Farmer+ não precisam de mixin. O morango faz isso com uma propriedade `flattening` (0–3) na própria planta; veja [strawberries.pt-BR.md](strawberries.pt-BR.md#pisoteio).

## Adicionando pisoteio a outra plantação vanilla

1. Registre um `TrampledCropBlock` apontando para a plantação em pé:
   ```java
   public static final RegistryEntry<TrampledCropBlock> TRAMPLED_CARROTS = FarmerRegistries.block("trampled_carrots",
           properties -> new TrampledCropBlock(() -> (CropBlock) Blocks.CARROTS, properties),
           TrampledCropBlock::cropProperties);
   ```
2. No `register()` do módulo: `TrampleableCrops.register(TRAMPLED_CARROTS);`
3. Adicione blockstate/modelos (veja `art/trampled_wheat.py`), loot table, traduções e as tags `minecraft:crops`, `minecraft:maintains_farmland` e `minecraft:washed_away_by_fluids`.

## Modelos

`art/trampled_wheat.py` gera `blockstates/trampled_wheat.json`, 48 modelos (`trampled_wheat_stage<idade>_<achatamento>` mais um `_variant1` com as texturas trocadas) e as texturas finais AGE 2–7 `wheat_stage<idade>[_alternate]_crushed.png` por `art/crushed_pixels.py`. As imagens AGE 0–1 permanecem iguais. Os modelos são feitos caindo para o norte e o blockstate gira para as outras direções. O Minecraft 26.3 aceita qualquer ângulo de rotação e rotações Euler `x`/`y`/`z`, que os caules entortados e caídos usam.

```bash
python art/trampled_wheat.py
```

As texturas esmagadas AGE 2–7 agora são desenhadas em 16×16 por `art/crushed_pixels.py`, chamado pelo gerador; AGE 0–1 permanecem iguais. Veja [o relatório da arte](avocado-visuals.pt-BR.md).
