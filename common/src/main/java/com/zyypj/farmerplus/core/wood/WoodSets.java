package com.zyypj.farmerplus.core.wood;

import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.Direction;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.DoubleHighBlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.FenceBlock;
import net.minecraft.world.level.block.FenceGateBlock;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.BlockSetType;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;
import net.minecraft.world.level.block.state.properties.WoodType;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProvider;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProviders;

public final class WoodSets {

    private static final int BUTTON_PRESS_TICKS = 30;

    private WoodSets() {
    }

    public static WoodSet register(String name, MapColor woodColor, MapColor barkColor) {
        List<RegistryEntry<? extends Item>> items = new ArrayList<>();

        RegistryEntry<RotatedPillarBlock> strippedLog = FarmerRegistries.block("stripped_" + name + "_log", RotatedPillarBlock::new,
                () -> logProperties(woodColor, woodColor));
        RegistryEntry<RotatedPillarBlock> strippedWood = FarmerRegistries.block("stripped_" + name + "_wood", RotatedPillarBlock::new,
                () -> logProperties(woodColor, woodColor));
        RegistryEntry<StrippableLogBlock> log = FarmerRegistries.block(name + "_log",
                properties -> new StrippableLogBlock(strippedLog, properties), () -> logProperties(woodColor, barkColor));
        RegistryEntry<StrippableLogBlock> wood = FarmerRegistries.block(name + "_wood",
                properties -> new StrippableLogBlock(strippedWood, properties), () -> logProperties(barkColor, barkColor));
        RegistryEntry<Block> planks = FarmerRegistries.block(name + "_planks", Block::new,
                () -> woodProperties(woodColor).strength(2.0F, 3.0F).sound(SoundType.WOOD));
        RegistryEntry<WoodStairBlock> stairs = FarmerRegistries.block(name + "_stairs",
                properties -> new WoodStairBlock(planks.get().defaultBlockState(), properties),
                () -> BlockBehaviour.Properties.ofLegacyCopy(planks.get()));
        RegistryEntry<SlabBlock> slab = FarmerRegistries.block(name + "_slab", SlabBlock::new,
                () -> BlockBehaviour.Properties.ofLegacyCopy(planks.get()));
        RegistryEntry<FenceBlock> fence = FarmerRegistries.block(name + "_fence", FenceBlock::new,
                () -> woodProperties(woodColor).strength(2.0F, 3.0F).sound(SoundType.WOOD));
        RegistryEntry<FenceGateBlock> fenceGate = FarmerRegistries.block(name + "_fence_gate",
                properties -> new FenceGateBlock(WoodType.OAK, properties),
                () -> woodProperties(woodColor).forceSolidOn().strength(2.0F, 3.0F));
        RegistryEntry<WoodDoorBlock> door = FarmerRegistries.block(name + "_door",
                properties -> new WoodDoorBlock(BlockSetType.OAK, properties),
                () -> woodProperties(woodColor).strength(3.0F).noOcclusion().pushReaction(PushReaction.POPPED));
        RegistryEntry<WoodTrapDoorBlock> trapdoor = FarmerRegistries.block(name + "_trapdoor",
                properties -> new WoodTrapDoorBlock(BlockSetType.OAK, properties),
                () -> woodProperties(woodColor).strength(3.0F).noOcclusion().isValidSpawn((state, level, pos, type) -> false));
        RegistryEntry<WoodPressurePlateBlock> pressurePlate = FarmerRegistries.block(name + "_pressure_plate",
                properties -> new WoodPressurePlateBlock(BlockSetType.OAK, properties),
                () -> woodProperties(woodColor).forceSolidOn().noCollision().strength(0.5F).pushReaction(PushReaction.POPPED));
        RegistryEntry<WoodButtonBlock> button = FarmerRegistries.block(name + "_button",
                properties -> new WoodButtonBlock(BlockSetType.OAK, BUTTON_PRESS_TICKS, properties),
                () -> BlockBehaviour.Properties.of().noCollision().strength(0.5F).pushReaction(PushReaction.POPPED));

        items.add(item(log, ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));
        items.add(item(wood, ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));
        items.add(item(strippedLog, ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));
        items.add(item(strippedWood, ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));
        items.add(item(planks, ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));
        items.add(item(stairs, ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));
        items.add(item(slab, ContextIntProviders.COOKING_TIME_WOOD_SLABS));
        items.add(item(fence, ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));
        items.add(item(fenceGate, ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));
        items.add(FarmerRegistries.blockItem(door, DoubleHighBlockItem::new,
                () -> new Item.Properties().cookingFuel(ContextIntProviders.COOKING_TIME_WOOD_ITEMS_LARGE)));
        items.add(item(trapdoor, ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));
        items.add(item(pressurePlate, ContextIntProviders.COOKING_TIME_WOOD_BLOCKS));
        items.add(item(button, ContextIntProviders.COOKING_TIME_WOOD_ITEMS_EXTRA_SMALL));

        Flammability.register(planks, 5, 20);
        Flammability.register(slab, 5, 20);
        Flammability.register(stairs, 5, 20);
        Flammability.register(fence, 5, 20);
        Flammability.register(fenceGate, 5, 20);
        Flammability.register(log, 5, 5);
        Flammability.register(wood, 5, 5);
        Flammability.register(strippedLog, 5, 5);
        Flammability.register(strippedWood, 5, 5);

        return new WoodSet(name, log, wood, strippedLog, strippedWood, planks, stairs, slab, fence, fenceGate,
                door, trapdoor, pressurePlate, button, List.copyOf(items));
    }

    private static RegistryEntry<BlockItem> item(RegistryEntry<? extends Block> block, ResourceKey<ContextIntProvider> burnTime) {
        return FarmerRegistries.blockItem(block, () -> new Item.Properties().cookingFuel(burnTime));
    }

    private static BlockBehaviour.Properties woodProperties(MapColor color) {
        return BlockBehaviour.Properties.of()
                .mapColor(color)
                .instrument(NoteBlockInstrument.BASS)
                .ignitedByLava();
    }

    private static BlockBehaviour.Properties logProperties(MapColor topColor, MapColor sideColor) {
        return BlockBehaviour.Properties.of()
                .mapColor(state -> state.getValue(RotatedPillarBlock.AXIS) == Direction.Axis.Y ? topColor : sideColor)
                .instrument(NoteBlockInstrument.BASS)
                .strength(2.0F)
                .sound(SoundType.WOOD)
                .ignitedByLava();
    }
}
