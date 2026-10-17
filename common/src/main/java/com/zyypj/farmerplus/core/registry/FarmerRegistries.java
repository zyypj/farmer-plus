package com.zyypj.farmerplus.core.registry;

import com.zyypj.farmerplus.platform.Services;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.function.Supplier;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;

public final class FarmerRegistries {

    private FarmerRegistries() {
    }

    public static RegistryEntry<Item> item(String name, Supplier<Item.Properties> properties) {
        return item(name, Item::new, properties);
    }

    public static <T extends Item> RegistryEntry<T> item(String name, Function<Item.Properties, T> factory, Supplier<Item.Properties> properties) {
        return Services.REGISTRATION.register(Registries.ITEM, name, key -> factory.apply(properties.get().setId(key)));
    }

    public static <T extends Entity> RegistryEntry<EntityType<T>> entityType(String name, EntityType.Builder<T> builder) {
        return Services.REGISTRATION.register(Registries.ENTITY_TYPE, name, builder::build);
    }

    public static <T extends Block> RegistryEntry<T> block(String name, Function<BlockBehaviour.Properties, T> factory, Supplier<BlockBehaviour.Properties> properties) {
        return Services.REGISTRATION.register(Registries.BLOCK, name, key -> factory.apply(properties.get().setId(key)));
    }

    public static RegistryEntry<BlockItem> blockItem(RegistryEntry<? extends Block> block, Supplier<Item.Properties> properties) {
        return blockItem(block, BlockItem::new, properties);
    }

    public static RegistryEntry<BlockItem> namedBlockItem(String name, RegistryEntry<? extends Block> block, Supplier<Item.Properties> properties) {
        return Services.REGISTRATION.register(Registries.ITEM, name, key -> {
            BlockItem item = new BlockItem(block.get(), properties.get().useItemDescriptionPrefix().setId(key));
            item.registerBlocks(Item.BY_BLOCK, item);
            return item;
        });
    }

    public static <T extends BlockItem> RegistryEntry<T> blockItem(RegistryEntry<? extends Block> block, BiFunction<Block, Item.Properties, T> factory, Supplier<Item.Properties> properties) {
        String name = block.id().getPath();
        return Services.REGISTRATION.register(Registries.ITEM, name, key -> {
            T item = factory.apply(block.get(), properties.get().useBlockDescriptionPrefix().setId(key));
            item.registerBlocks(Item.BY_BLOCK, item);
            return item;
        });
    }
}
