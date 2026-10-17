package com.zyypj.farmerplus.core.wood;

import com.zyypj.farmerplus.core.registry.RegistryEntry;
import java.util.List;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.FenceBlock;
import net.minecraft.world.level.block.FenceGateBlock;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.SlabBlock;

public record WoodSet(
        String name,
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
        List<RegistryEntry<? extends Item>> items
) {

    public List<ItemLike> creativeTabItems() {
        return items.stream().<ItemLike>map(RegistryEntry::get).toList();
    }
}
