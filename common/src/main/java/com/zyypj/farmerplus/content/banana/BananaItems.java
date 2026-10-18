package com.zyypj.farmerplus.content.banana;

import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProviders;

public final class BananaItems {

    public static final RegistryEntry<Item> BANANA = FarmerRegistries.item("banana",
            () -> new Item.Properties()
                    .food(BananaFoods.BANANA)
                    .villagerFood(3)
                    .compostable(ContextIntProviders.COMPOSTABLE_MEDIUM));

    public static final RegistryEntry<BlockItem> BANANA_SAPLING = FarmerRegistries.blockItem(BananaBlocks.BANANA_SAPLING,
            () -> new Item.Properties().compostable(ContextIntProviders.COMPOSTABLE_LOW));

    public static final RegistryEntry<BlockItem> BANANA_LEAF = FarmerRegistries.blockItem(BananaBlocks.BANANA_LEAF,
            () -> new Item.Properties().compostable(ContextIntProviders.COMPOSTABLE_LOW));

    private BananaItems() {
    }

    static void bootstrap() {
    }
}
