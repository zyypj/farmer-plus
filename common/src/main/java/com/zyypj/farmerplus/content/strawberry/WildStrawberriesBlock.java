package com.zyypj.farmerplus.content.strawberry;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.loot.LootTable;

public class WildStrawberriesBlock extends StrawberryPlantBlock {

    private static final ResourceKey<LootTable> HARVEST_LOOT = ResourceKey.create(Registries.LOOT_TABLE, FarmerPlus.id("harvest/wild_strawberries"));
    private static final int WILD_GROWTH_CHANCE = 10;

    public WildStrawberriesBlock(BlockBehaviour.Properties properties) {
        super(properties);
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
        return state.is(BlockTags.SUPPORTS_VEGETATION) && !state.is(BlockTags.SUPPORTS_CROPS);
    }

    @Override
    protected int growthChance(ServerLevel level, BlockPos pos) {
        return WILD_GROWTH_CHANCE;
    }

    @Override
    protected boolean spreadsRunners() {
        return false;
    }

    @Override
    protected ResourceKey<LootTable> harvestLootTable() {
        return HARVEST_LOOT;
    }
}
