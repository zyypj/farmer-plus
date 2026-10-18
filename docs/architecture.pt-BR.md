# Arquitetura

[English](architecture.md) | **Português**

## Estrutura do projeto

```
farmer+/
├── common/      Código compartilhado e todos os assets/dados. Compilado contra o vanilla puro.
├── fabric/      Entrypoint do Fabric + implementação Fabric das interfaces de plataforma.
├── neoforge/    Entrypoint do NeoForge + implementação NeoForge.
├── forge/       Entrypoint do Forge + implementação Forge.
├── build-logic/ Convenções de Gradle compartilhadas entre os subprojetos.
├── art/         Arte-fonte (arquivos .bbmodel do Blockbench, texturas em camadas). Nunca vai no jar.
└── docs/        Documentação (inglês + português).
```

Regra geral: **se pode ficar no `common`, fica no `common`.** As pastas de loader só têm o código que a API daquele loader obriga.

## Camadas

```
content/<feature>      O que o mod adiciona (trigo, tomate, solos, …)
        │ usa
core/                  Peças reutilizáveis: módulos, registros, aba criativa
        │ chama
platform/              Interfaces que cada loader implementa
        │ implementadas por
fabric/ neoforge/ forge/
```

### `core/module`

Cada funcionalidade é um **módulo** que implementa `FarmerModule`:

```java
public interface FarmerModule {
    String id();
    void register();
    List<ItemLike> creativeTabItems();
}
```

Os módulos ficam listados, na ordem de exibição, em `FarmerModules`. Desligar uma funcionalidade é uma linha, e um módulo nunca acessa as classes de outro.

### `core/registry`

`FarmerRegistries` encapsula o registro com o mesmo formato que o vanilla usa em `Items` e `Blocks`:

```java
FarmerRegistries.item("flour", () -> new Item.Properties().compostable(...));
FarmerRegistries.block("wheat_sheaf", WheatSheafBlock::new, () -> BlockBehaviour.Properties.of()...);
FarmerRegistries.blockItem(WheatBlocks.WHEAT_SHEAF, Item.Properties::new);
```

Toda chamada devolve um `RegistryEntry<T>`, um `Supplier<T>` preguiçoso que pode ficar num campo `static final`. Só chame `.get()` depois que o registro terminou (dentro da lógica do jogo, nunca em inicializadores estáticos de outro conteúdo).

### `platform`

`RegistrationPlatform` é o único contrato que um loader precisa cumprir. Ele é encontrado via `java.util.ServiceLoader`:

| Loader | Implementação | Estratégia |
|---|---|---|
| Fabric | `FabricRegistrationPlatform` | Registra direto nos registros nativos |
| NeoForge | `NeoForgeRegistrationPlatform` | Um `DeferredRegister` por registro, ligado ao mod bus |
| Forge | `ForgeRegistrationPlatform` | Um `DeferredRegister` por registro, ligado ao mod bus group |

O entrypoint de cada loader chama `FarmerPlus.init()`, liga os deferred registers no NeoForge/Forge e entrega as listas compartilhadas à API do loader: `BlockEntityBlocks` (blocos válidos extras para tipos de block entity vanilla) e, no cliente, `client/BoatRendering` (camadas de modelo e renderers dos botes). Código só de cliente em `common` fica no pacote `client` e só é alcançado pelos entrypoints de cliente.

## Regras de desempenho

O Farmer+ precisa ser invisível no profiler.

1. **Sem mixins**, a não ser que não exista alternativa por dados ou API — e nunca em caminhos quentes (render, tick, pathfinding). Todo mixin fica em `common/…/mixin`, é listado em `farmerplus.mixins.json` e tem o motivo documentado. Lista atual: `CropBlockMixin` — a única forma de reagir a entidades andando pelas plantações vanilla; `FarmlandBlockMixin` — mantém a terra arada e amassa a planta quando algo cai em cima ([pisoteio](trampling.pt-BR.md)); `FireBlockAccessor` — um invoker usado uma vez na inicialização para dar à madeira do Farmer+ a inflamabilidade do vanilla ([abacateiro](avocado.pt-BR.md#conjunto-de-madeira)); `BlockEntityTypeAccessor` — usado uma vez no common setup do Forge para adicionar as placas e prateleiras do Farmer+ aos tipos de block entity vanilla, porque o Forge não tem API para isso (Fabric e NeoForge usam suas APIs) ([abacateiro](avocado.pt-BR.md#placas-prateleira-e-botes)).
2. **Sem handlers de tick.** Use random ticks de bloco, scheduled ticks ou mecânicas vanilla.
3. **Dados antes de código.** Compostagem, combustível, comida, comida de aldeão, ferramentas e loot são componentes de dados ou JSON do vanilla — use-os.
4. **Sem reflexão, sem varredura de classpath em runtime, sem biblioteca de config** para coisas que um data pack já resolve.
5. **Shapes estáticos.** `VoxelShape`s são calculados uma vez em campos `static final`.

## Sistemas

| Sistema | Pacote | Docs |
|---|---|---|
| Pisoteio de plantações | `core/trampling` | [trampling.pt-BR.md](trampling.pt-BR.md) |
| Features de bioma (worldgen) | `core/worldgen` | [strawberries.pt-BR.md](strawberries.pt-BR.md#compatibilidade-com-modpacks) |
| Morangos | `content/strawberry` | [strawberries.pt-BR.md](strawberries.pt-BR.md) |
| Conjuntos de madeira e galhos conectáveis | `core/wood`, `client/BoatRendering`, `tools/wood_set.py`, `art/avocado_branches.py` | [avocado.pt-BR.md](avocado.pt-BR.md#reaproveitando-o-conjunto-de-madeira) |
| Abacateiro | `content/avocado` | [avocado.pt-BR.md](avocado.pt-BR.md) |
| Bananeira | `content/banana`, `art/banana_art.py` | [banana.pt-BR.md](banana.pt-BR.md) |
| Gerador de árvore de folha larga | `core/worldgen/BroadleafTreeFeature` | [avocado.pt-BR.md](avocado.pt-BR.md#a-árvore) |

## Adicionando uma plantação nova (checklist)

1. Crie `content/<planta>/` com `<Planta>Module`, `<Planta>Blocks`, `<Planta>Items` e, se precisar, `<Planta>Foods`.
2. Registre o módulo em `FarmerModules`.
3. Adicione os assets em `common/src/main/resources/assets/farmerplus/`:
   - `blockstates/<id>.json`, `models/block/…`, `models/item/…`, `items/<id>.json`
   - texturas em `textures/block` e `textures/item` (veja [art-pipeline.pt-BR.md](art-pipeline.pt-BR.md))
   - traduções em **ambos** `lang/en_us.json` e `lang/pt_br.json`
4. Adicione os dados em `common/src/main/resources/data/`:
   - `farmerplus/recipe/…` mais o desbloqueio em `farmerplus/advancement/recipes/<categoria>/…`
   - `farmerplus/loot_table/blocks/…` para todo bloco
   - tags de ferramenta (`minecraft:mineable/*`) e tags de convenção `c:` para ingredientes compartilhados
5. `./gradlew build`, depois abra um cliente de dev em pelo menos um loader e um servidor de dev nos outros dois.

## Nomenclatura

| O quê | Convenção | Exemplo |
|---|---|---|
| Id de registro | `snake_case` | `wheat_porridge` |
| Classe de módulo | `<Feature>Module` | `WheatModule` |
| Classes de entradas | `<Feature>Blocks`, `<Feature>Items`, `<Feature>Foods` | `WheatItems.FLOUR` |
| Classes de bloco | `<Nome>Block` | `WheatSheafBlock` |
| Classes de loader | `<Loader><Papel>` | `NeoForgeRegistrationPlatform` |

## Estilo de código

- Java 25, indentação de 4 espaços, imports em vez de nomes totalmente qualificados.
- Sem comentários: nomes e métodos pequenos explicam o código.
- Constantes em vez de números mágicos (`FALL_DAMAGE_MULTIPLIER`).
- Classes são `final`, exceto as feitas para serem estendidas (blocos e itens).
