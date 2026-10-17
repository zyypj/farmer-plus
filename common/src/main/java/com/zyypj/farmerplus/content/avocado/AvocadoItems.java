package com.zyypj.farmerplus.content.avocado;

import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProviders;

public final class AvocadoItems {

    public static final RegistryEntry<Item> AVOCADO = FarmerRegistries.item("avocado",
            () -> new Item.Properties()
                    .food(AvocadoFoods.AVOCADO)
                    .villagerFood(3)
                    .compostable(ContextIntProviders.COMPOSTABLE_MEDIUM));

    public static final RegistryEntry<BlockItem> AVOCADO_TRUNK = FarmerRegistries.blockItem(AvocadoBlocks.AVOCADO_TRUNK,
            () -> new Item.Properties().cookingFuel(ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));

    public static final RegistryEntry<BlockItem> AVOCADO_BRANCH = FarmerRegistries.blockItem(AvocadoBlocks.AVOCADO_BRANCH,
            () -> new Item.Properties().cookingFuel(ContextIntProviders.COOKING_TIME_WOOD_ITEMS_SMALL));

    public static final RegistryEntry<BlockItem> AVOCADO_LEAVES = FarmerRegistries.blockItem(AvocadoBlocks.AVOCADO_LEAVES,
            () -> new Item.Properties().compostable(ContextIntProviders.COMPOSTABLE_LOW));

    public static final RegistryEntry<BlockItem> AVOCADO_SAPLING = FarmerRegistries.blockItem(AvocadoBlocks.AVOCADO_SAPLING,
            () -> new Item.Properties()
                    .compostable(ContextIntProviders.COMPOSTABLE_LOW)
                    .cookingFuel(ContextIntProviders.COOKING_TIME_WOOD_ITEMS_SMALL));

    private AvocadoItems() {
    }

    static void bootstrap() {
    }
}
