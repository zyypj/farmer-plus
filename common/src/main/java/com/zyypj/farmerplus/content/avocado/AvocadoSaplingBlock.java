package com.zyypj.farmerplus.content.avocado;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.SaplingBlock;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;

public class AvocadoSaplingBlock extends SaplingBlock {

    private static final int MIN_GROWTH_BRIGHTNESS = 9;
    private static final int GROWTH_CHANCE = 14;

    public AvocadoSaplingBlock(TreeGrower treeGrower, BlockBehaviour.Properties properties) {
        super(treeGrower, properties);
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (level.getMaxLocalRawBrightness(pos.above()) >= MIN_GROWTH_BRIGHTNESS && random.nextInt(GROWTH_CHANCE) == 0) {
            advanceTree(level, pos, state, random);
        }
    }
}
