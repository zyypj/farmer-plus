package com.zyypj.farmerplus.content.wheat;

import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProviders;

public final class WheatItems {

    public static final RegistryEntry<Item> FLOUR = FarmerRegistries.item("flour",
            () -> new Item.Properties().compostable(ContextIntProviders.COMPOSTABLE_LOW_MEDIUM));

    public static final RegistryEntry<Item> DOUGH = FarmerRegistries.item("dough",
            () -> new Item.Properties().compostable(ContextIntProviders.COMPOSTABLE_MEDIUM));

    public static final RegistryEntry<Item> WHEAT_PORRIDGE = FarmerRegistries.item("wheat_porridge",
            () -> new Item.Properties().stacksTo(1).food(WheatFoods.WHEAT_PORRIDGE).usingConvertsTo(Items.BOWL));

    public static final RegistryEntry<BlockItem> WHEAT_SHEAF = FarmerRegistries.blockItem(WheatBlocks.WHEAT_SHEAF,
            () -> new Item.Properties().compostable(ContextIntProviders.COMPOSTABLE_MEDIUM_HIGH));

    private WheatItems() {
    }

    static void bootstrap() {
    }
}
