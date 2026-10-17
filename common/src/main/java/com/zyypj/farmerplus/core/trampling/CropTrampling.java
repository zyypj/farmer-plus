package com.zyypj.farmerplus.core.trampling;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.CropBlock;
import net.minecraft.world.level.block.state.BlockState;

public final class CropTrampling {

    private static final int MIN_TRAMPLE_AGE = 2;
    private static final float HEAVY_ENTITY_WIDTH = 1.2F;
    private static final double MIN_HORIZONTAL_MOVEMENT_SQR = 1.0E-6;
    private static final int PARTICLE_COUNT = 6;
    private static final float SOUND_VOLUME = 0.4F;

    private CropTrampling() {
    }

    public static void onEntityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
        if (!(level instanceof ServerLevel serverLevel)
                || !entity.onGround()
                || entity.isSteppingCarefully()
                || !standsIn(entity, pos)
                || !enteredFromAnotherBlock(entity, pos)) {
            return;
        }

        TrampledCropBlock trampled = state.getBlock() instanceof TrampledCropBlock trampledCrop
                ? trampledCrop
                : TrampleableCrops.trampledFormOf(state.getBlock());
        if (trampled == null || !canTrample(serverLevel, entity)) {
            return;
        }

        BlockState trampledState = trample(state, trampled, force(entity), movementDirection(entity));
        if (trampledState != state) {
            serverLevel.setBlock(pos, trampledState, Block.UPDATE_CLIENTS);
            playEffects(serverLevel, pos, state);
        }
    }

    private static BlockState trample(BlockState state, TrampledCropBlock trampled, int force, Direction direction) {
        if (state.getBlock() instanceof TrampledCropBlock) {
            int flattening = Math.min(TrampledCropBlock.CRUSHED, TrampledCropBlock.flattening(state) + force);
            return state.setValue(TrampledCropBlock.FLATTENING, flattening);
        }

        int age = ((CropBlock) state.getBlock()).getAge(state);
        if (age < MIN_TRAMPLE_AGE) {
            return state;
        }
        return trampled.trampledState(age, Math.min(TrampledCropBlock.CRUSHED, force), direction);
    }

    private static boolean standsIn(Entity entity, BlockPos pos) {
        return Mth.floor(entity.getX()) == pos.getX() && Mth.floor(entity.getZ()) == pos.getZ();
    }

    private static boolean enteredFromAnotherBlock(Entity entity, BlockPos pos) {
        return Mth.floor(entity.xo) != pos.getX() || Mth.floor(entity.zo) != pos.getZ();
    }

    private static boolean canTrample(ServerLevel level, Entity entity) {
        if (entity instanceof Player player) {
            return !player.isCreative()
                    && !player.isSpectator()
                    && level.getGameRules().get(TramplingGameRules.PLAYERS_TRAMPLE_CROPS.get());
        }
        return entity.is(TramplingTags.TRAMPLES_CROPS)
                && level.getGameRules().get(TramplingGameRules.MOBS_TRAMPLE_CROPS.get());
    }

    private static int force(Entity entity) {
        int force = 1;
        if (entity.isSprinting()) {
            force++;
        }
        if (entity.getBbWidth() >= HEAVY_ENTITY_WIDTH) {
            force++;
        }
        return force;
    }

    private static Direction movementDirection(Entity entity) {
        double dx = entity.getX() - entity.xo;
        double dz = entity.getZ() - entity.zo;
        if (dx * dx + dz * dz < MIN_HORIZONTAL_MOVEMENT_SQR) {
            return entity.getDirection();
        }
        return Direction.getApproximateNearest(dx, 0.0, dz);
    }

    private static void playEffects(ServerLevel level, BlockPos pos, BlockState state) {
        float pitch = 0.8F + level.getRandom().nextFloat() * 0.4F;
        level.playSound(null, pos, SoundEvents.CROP_BREAK, SoundSource.BLOCKS, SOUND_VOLUME, pitch);
        level.sendParticles(new BlockParticleOption(ParticleTypes.BLOCK, state),
                pos.getX() + 0.5, pos.getY() + 0.2, pos.getZ() + 0.5,
                PARTICLE_COUNT, 0.25, 0.05, 0.25, 0.0);
    }
}
