package com.zyypj.farmerplus.content.avocado;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ColorParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.ParticleUtils;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.TintedParticleLeavesBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;

public class AvocadoLeavesBlock extends TintedParticleLeavesBlock {

    private static final float LEAF_PARTICLE_CHANCE = 0.01F;
    private static final int MAX_FRUITING_DISTANCE = 5;
    private static final int FRUITING_SPACING = 3;
    private static final int FLOWERING_CHANCE = 24;
    private static final ColorParticleOption FALLING_LEAF = ColorParticleOption.create(ParticleTypes.TINTED_LEAVES, 0.3F, 0.52F, 0.31F);

    public AvocadoLeavesBlock(BlockBehaviour.Properties properties) {
        super(LEAF_PARTICLE_CHANCE, properties);
    }

    @Override
    protected void spawnFallingLeavesParticle(Level level, BlockPos pos, RandomSource random) {
        ParticleUtils.spawnParticleBelow(level, pos, random, FALLING_LEAF);
    }

    @Override
    protected boolean isRandomlyTicking(BlockState state) {
        return super.isRandomlyTicking(state) || !state.getValue(PERSISTENT);
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        super.randomTick(state, level, pos, random);
        if (level.getBlockState(pos).is(this) && canBearFruit(state, level, pos) && random.nextInt(FLOWERING_CHANCE) == 0) {
            level.setBlock(pos.below(), AvocadoBlocks.AVOCADO_FRUIT.get().defaultBlockState(), Block.UPDATE_ALL);
        }
    }

    private static boolean canBearFruit(BlockState state, ServerLevel level, BlockPos pos) {
        return !state.getValue(PERSISTENT)
                && state.getValue(DISTANCE) <= MAX_FRUITING_DISTANCE
                && Math.floorMod(pos.getX() * 7 + pos.getY() * 13 + pos.getZ() * 5, FRUITING_SPACING) == 0
                && level.isEmptyBlock(pos.below());
    }
}
