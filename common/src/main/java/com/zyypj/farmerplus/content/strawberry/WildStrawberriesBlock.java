package com.zyypj.farmerplus.content.strawberry;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

public class WildStrawberriesBlock extends StrawberryPlantBlock {

    private static final ResourceKey<LootTable> HARVEST_LOOT = ResourceKey.create(Registries.LOOT_TABLE, FarmerPlus.id("harvest/wild_strawberries"));
    private static final int WILD_GROWTH_CHANCE = 10;
    private static final VoxelShape[] SHAPES = {
            Block.column(3.5, -1.0, 0.5),
            Block.column(7.0, -1.0, 1.25),
            Block.column(8.0, -1.0, 3.75),
            Block.column(11.5, -1.0, 4.0),
            Block.column(12.0, -1.0, 4.0)
    };

    public WildStrawberriesBlock(BlockBehaviour.Properties properties) {
        super(properties);
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
        return state.is(BlockTags.SUPPORTS_VEGETATION) && !state.is(BlockTags.SUPPORTS_CROPS);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPES[state.getValue(AGE)];
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
