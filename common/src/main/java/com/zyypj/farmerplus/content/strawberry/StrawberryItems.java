package com.zyypj.farmerplus.content.strawberry;

import com.zyypj.farmerplus.core.jam.JamJarBlock;
import com.zyypj.farmerplus.core.jam.JamJarItem;
import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.component.BlockItemStateProperties;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProviders;

public final class StrawberryItems {

    public static final RegistryEntry<BlockItem> STRAWBERRY = FarmerRegistries.namedBlockItem("strawberry", StrawberryBlocks.STRAWBERRY_PLANT,
            () -> new Item.Properties()
                    .food(StrawberryFoods.STRAWBERRY)
                    .villagerFood(2)
                    .compostable(ContextIntProviders.COMPOSTABLE_LOW));

    public static final RegistryEntry<JamJarItem> STRAWBERRY_JAM = FarmerRegistries.blockItem(StrawberryBlocks.STRAWBERRY_JAM, JamJarItem::new,
            () -> new Item.Properties()
                    .stacksTo(16)
                    .food(StrawberryFoods.STRAWBERRY_JAM_PORTION)
                    .component(DataComponents.BLOCK_STATE, BlockItemStateProperties.EMPTY.with(JamJarBlock.PORTIONS, JamJarBlock.MAX_PORTIONS)));

    private StrawberryItems() {
    }

    static void bootstrap() {
    }
}
