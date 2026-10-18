package com.zyypj.farmerplus.core.worldgen;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.SaplingBlock;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;

public class GrowingSaplingBlock extends SaplingBlock {

    private static final int MIN_GROWTH_BRIGHTNESS = 9;

    private final int growthChance;

    public GrowingSaplingBlock(TreeGrower treeGrower, int growthChance, BlockBehaviour.Properties properties) {
        super(treeGrower, properties);
        this.growthChance = growthChance;
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (level.getMaxLocalRawBrightness(pos.above()) >= MIN_GROWTH_BRIGHTNESS && random.nextInt(growthChance) == 0) {
            advanceTree(level, pos, state, random);
        }
    }
}
