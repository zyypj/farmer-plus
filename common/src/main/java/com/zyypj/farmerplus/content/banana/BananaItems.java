package com.zyypj.farmerplus.content.banana;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.component.ItemAttributeModifiers;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProviders;

public final class BananaItems {

    private static final double CARRY_SLOWNESS = -0.3;

    public static final RegistryEntry<Item> BANANA = FarmerRegistries.item("banana",
            () -> new Item.Properties()
                    .food(BananaFoods.BANANA)
                    .villagerFood(3)
                    .compostable(ContextIntProviders.COMPOSTABLE_MEDIUM));

    public static final RegistryEntry<BlockItem> BANANA_BUNCH = FarmerRegistries.namedBlockItem("banana_bunch", BananaBlocks.HARVESTED_BANANA_BUNCH,
            () -> new Item.Properties()
                    .stacksTo(1)
                    .attributes(ItemAttributeModifiers.builder()
                            .add(Attributes.MOVEMENT_SPEED, new AttributeModifier(FarmerPlus.id("heavy_banana_bunch"), CARRY_SLOWNESS,
                                    AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL), EquipmentSlotGroup.HAND)
                            .build()));

    public static final RegistryEntry<BlockItem> BANANA_SAPLING = FarmerRegistries.blockItem(BananaBlocks.BANANA_SAPLING,
            () -> new Item.Properties().compostable(ContextIntProviders.COMPOSTABLE_LOW));

    public static final RegistryEntry<BlockItem> BANANA_LEAF = FarmerRegistries.blockItem(BananaBlocks.BANANA_LEAF,
            () -> new Item.Properties().compostable(ContextIntProviders.COMPOSTABLE_LOW));

    private BananaItems() {
    }

    static void bootstrap() {
    }
}
