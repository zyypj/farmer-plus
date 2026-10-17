package com.zyypj.farmerplus.core.wood;

import com.zyypj.farmerplus.core.registry.RegistryEntry;
import java.util.List;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.vehicle.boat.Boat;
import net.minecraft.world.entity.vehicle.boat.ChestBoat;
import net.minecraft.world.item.BoatItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.CeilingHangingSignBlock;
import net.minecraft.world.level.block.FenceBlock;
import net.minecraft.world.level.block.FenceGateBlock;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.ShelfBlock;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.StandingSignBlock;
import net.minecraft.world.level.block.WallHangingSignBlock;
import net.minecraft.world.level.block.WallSignBlock;
import net.minecraft.world.level.block.state.properties.BlockSetType;
import net.minecraft.world.level.block.state.properties.WoodType;

public record WoodSet(
        String name,
        WoodType woodType,
        BlockSetType setType,
        RegistryEntry<StrippableLogBlock> log,
        RegistryEntry<StrippableLogBlock> wood,
        RegistryEntry<RotatedPillarBlock> strippedLog,
        RegistryEntry<RotatedPillarBlock> strippedWood,
        RegistryEntry<Block> planks,
        RegistryEntry<WoodStairBlock> stairs,
        RegistryEntry<SlabBlock> slab,
        RegistryEntry<FenceBlock> fence,
        RegistryEntry<FenceGateBlock> fenceGate,
        RegistryEntry<WoodDoorBlock> door,
        RegistryEntry<WoodTrapDoorBlock> trapdoor,
        RegistryEntry<WoodPressurePlateBlock> pressurePlate,
        RegistryEntry<WoodButtonBlock> button,
        RegistryEntry<StandingSignBlock> sign,
        RegistryEntry<WallSignBlock> wallSign,
        RegistryEntry<CeilingHangingSignBlock> hangingSign,
        RegistryEntry<WallHangingSignBlock> wallHangingSign,
        RegistryEntry<ShelfBlock> shelf,
        RegistryEntry<EntityType<Boat>> boat,
        RegistryEntry<EntityType<ChestBoat>> chestBoat,
        RegistryEntry<BoatItem> boatItem,
        RegistryEntry<BoatItem> chestBoatItem,
        List<RegistryEntry<? extends Item>> items
) {

    public List<ItemLike> creativeTabItems() {
        return items.stream().<ItemLike>map(RegistryEntry::get).toList();
    }
}
