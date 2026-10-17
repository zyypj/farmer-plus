package com.zyypj.farmerplus.content.strawberry;

import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProviders;

public final class StrawberryItems {

    public static final RegistryEntry<BlockItem> STRAWBERRY = FarmerRegistries.namedBlockItem("strawberry", StrawberryBlocks.STRAWBERRY_PLANT,
            () -> new Item.Properties()
                    .food(StrawberryFoods.STRAWBERRY)
                    .villagerFood(2)
                    .compostable(ContextIntProviders.COMPOSTABLE_LOW));

    private StrawberryItems() {
    }

    static void bootstrap() {
    }
}
