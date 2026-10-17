package com.zyypj.farmerplus.core.wood;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.registry.BlockEntityBlocks;
import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.core.Direction;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.dispenser.BoatDispenseItemBehavior;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.vehicle.boat.Boat;
import net.minecraft.world.entity.vehicle.boat.ChestBoat;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.BoatItem;
import net.minecraft.world.item.DoubleHighBlockItem;
import net.minecraft.world.item.HangingSignItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.StandingAndWallBlockItem;
import net.minecraft.world.item.component.ItemContainerContents;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.CeilingHangingSignBlock;
import net.minecraft.world.level.block.DispenserBlock;
import net.minecraft.world.level.block.FenceBlock;
import net.minecraft.world.level.block.FenceGateBlock;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.ShelfBlock;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.StandingSignBlock;
import net.minecraft.world.level.block.WallHangingSignBlock;
import net.minecraft.world.level.block.WallSignBlock;
import net.minecraft.world.level.block.entity.BlockEntityTypes;
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
    private static final int SIGN_STACK_SIZE = 16;
    private static final float BOAT_WIDTH = 1.375F;
    private static final float BOAT_HEIGHT = 0.5625F;
    private static final int BOAT_TRACKING_RANGE = 10;
    private static final List<WoodSet> ALL = new ArrayList<>();

    private WoodSets() {
    }

    public static List<WoodSet> all() {
        return List.copyOf(ALL);
    }

    public static WoodSet register(String name, MapColor woodColor, MapColor barkColor) {
        List<RegistryEntry<? extends Item>> items = new ArrayList<>();
        BlockSetType setType = new BlockSetType(FarmerPlus.MOD_ID + "/" + name);
        WoodType woodType = new WoodType(FarmerPlus.MOD_ID + "/" + name, setType);

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
                properties -> new FenceGateBlock(woodType, properties),
                () -> woodProperties(woodColor).forceSolidOn().strength(2.0F, 3.0F));
        RegistryEntry<WoodDoorBlock> door = FarmerRegistries.block(name + "_door",
                properties -> new WoodDoorBlock(setType, properties),
                () -> woodProperties(woodColor).strength(3.0F).noOcclusion().pushReaction(PushReaction.POPPED));
        RegistryEntry<WoodTrapDoorBlock> trapdoor = FarmerRegistries.block(name + "_trapdoor",
                properties -> new WoodTrapDoorBlock(setType, properties),
                () -> woodProperties(woodColor).strength(3.0F).noOcclusion().isValidSpawn((state, level, pos, type) -> false));
        RegistryEntry<WoodPressurePlateBlock> pressurePlate = FarmerRegistries.block(name + "_pressure_plate",
                properties -> new WoodPressurePlateBlock(setType, properties),
                () -> woodProperties(woodColor).forceSolidOn().noCollision().strength(0.5F).pushReaction(PushReaction.POPPED));
        RegistryEntry<WoodButtonBlock> button = FarmerRegistries.block(name + "_button",
                properties -> new WoodButtonBlock(setType, BUTTON_PRESS_TICKS, properties),
                () -> BlockBehaviour.Properties.of().noCollision().strength(0.5F).pushReaction(PushReaction.POPPED));
        RegistryEntry<StandingSignBlock> sign = FarmerRegistries.block(name + "_sign",
                properties -> new StandingSignBlock(woodType, properties), () -> signProperties(woodColor));
        RegistryEntry<WallSignBlock> wallSign = FarmerRegistries.block(name + "_wall_sign",
                properties -> new WallSignBlock(woodType, properties), () -> wallVariant(sign, signProperties(woodColor)));
        RegistryEntry<CeilingHangingSignBlock> hangingSign = FarmerRegistries.block(name + "_hanging_sign",
                properties -> new CeilingHangingSignBlock(woodType, properties), () -> signProperties(woodColor));
        RegistryEntry<WallHangingSignBlock> wallHangingSign = FarmerRegistries.block(name + "_wall_hanging_sign",
                properties -> new WallHangingSignBlock(woodType, properties), () -> wallVariant(hangingSign, signProperties(woodColor)));
        RegistryEntry<ShelfBlock> shelf = FarmerRegistries.block(name + "_shelf", ShelfBlock::new,
                () -> woodProperties(woodColor).sound(SoundType.SHELF).strength(2.0F, 3.0F));

        RegistryEntry<EntityType<Boat>> boat = FarmerRegistries.entityType(name + "_boat",
                boatType((type, level) -> new Boat(type, level, item(name + "_boat"))));
        RegistryEntry<EntityType<ChestBoat>> chestBoat = FarmerRegistries.entityType(name + "_chest_boat",
                boatType((type, level) -> new ChestBoat(type, level, item(name + "_chest_boat"))));

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
        items.add(FarmerRegistries.blockItem(sign,
                (block, properties) -> new StandingAndWallBlockItem(block, wallSign.get(), Direction.DOWN, properties),
                () -> new Item.Properties().cookingFuel(ContextIntProviders.COOKING_TIME_WOOD_ITEMS_LARGE).stacksTo(SIGN_STACK_SIZE).signText()));
        items.add(FarmerRegistries.blockItem(hangingSign,
                (block, properties) -> new HangingSignItem(block, wallHangingSign.get(), properties),
                () -> new Item.Properties().cookingFuel(ContextIntProviders.COOKING_TIME_HANGING_SIGNS).stacksTo(SIGN_STACK_SIZE).signText()));
        items.add(FarmerRegistries.blockItem(shelf,
                () -> new Item.Properties().component(DataComponents.CONTAINER, ItemContainerContents.EMPTY)
                        .cookingFuel(ContextIntProviders.COOKING_TIME_WOOD_BLOCKS)));
        RegistryEntry<BoatItem> boatItem = FarmerRegistries.item(name + "_boat", properties -> new BoatItem(boat.get(), properties),
                WoodSets::boatProperties);
        RegistryEntry<BoatItem> chestBoatItem = FarmerRegistries.item(name + "_chest_boat", properties -> new BoatItem(chestBoat.get(), properties),
                WoodSets::boatProperties);
        items.add(boatItem);
        items.add(chestBoatItem);

        Flammability.register(planks, 5, 20);
        Flammability.register(slab, 5, 20);
        Flammability.register(stairs, 5, 20);
        Flammability.register(fence, 5, 20);
        Flammability.register(fenceGate, 5, 20);
        Flammability.register(log, 5, 5);
        Flammability.register(wood, 5, 5);
        Flammability.register(strippedLog, 5, 5);
        Flammability.register(strippedWood, 5, 5);
        Flammability.register(shelf, 30, 20);

        BlockEntityBlocks.add(() -> BlockEntityTypes.SIGN, sign, wallSign);
        BlockEntityBlocks.add(() -> BlockEntityTypes.HANGING_SIGN, hangingSign, wallHangingSign);
        BlockEntityBlocks.add(() -> BlockEntityTypes.SHELF, shelf);

        WoodSet set = new WoodSet(name, woodType, setType, log, wood, strippedLog, strippedWood, planks, stairs, slab, fence, fenceGate,
                door, trapdoor, pressurePlate, button, sign, wallSign, hangingSign, wallHangingSign, shelf,
                boat, chestBoat, boatItem, chestBoatItem, List.copyOf(items));
        ALL.add(set);
        return set;
    }

    public static void registerDispenserBehaviors() {
        ALL.forEach(set -> {
            DispenserBlock.registerBehavior(set.boatItem().get(), new BoatDispenseItemBehavior(set.boat().get()));
            DispenserBlock.registerBehavior(set.chestBoatItem().get(), new BoatDispenseItemBehavior(set.chestBoat().get()));
        });
    }

    private static Supplier<Item> item(String name) {
        return () -> BuiltInRegistries.ITEM.getValue(FarmerPlus.id(name));
    }

    private static <T extends Entity> EntityType.Builder<T> boatType(EntityType.EntityFactory<T> factory) {
        return EntityType.Builder.of(factory, MobCategory.MISC)
                .noLootTable()
                .sized(BOAT_WIDTH, BOAT_HEIGHT)
                .eyeHeight(BOAT_HEIGHT)
                .clientTrackingRange(BOAT_TRACKING_RANGE);
    }

    private static Item.Properties boatProperties() {
        return new Item.Properties().cookingFuel(ContextIntProviders.COOKING_TIME_BOATS).stacksTo(1);
    }

    private static RegistryEntry<BlockItem> item(RegistryEntry<? extends Block> block, ResourceKey<ContextIntProvider> burnTime) {
        return FarmerRegistries.blockItem(block, () -> new Item.Properties().cookingFuel(burnTime));
    }

    private static BlockBehaviour.Properties wallVariant(RegistryEntry<? extends Block> standing, BlockBehaviour.Properties properties) {
        return properties.overrideLootTable(standing.get().getLootTable()).overrideDescription(standing.get().getDescriptionId());
    }

    private static BlockBehaviour.Properties signProperties(MapColor color) {
        return woodProperties(color).forceSolidOn().noCollision().strength(1.0F);
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
