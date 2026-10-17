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
import net.minecraft.world.phys.Vec3;

public final class CropTrampling {

    private static final int MIN_TRAMPLE_AGE = 2;
    private static final float HEAVY_ENTITY_WIDTH = 1.2F;
    private static final double MIN_HORIZONTAL_MOVEMENT_SQR = 1.0E-6;
    private static final int PARTICLE_COUNT = 6;
    private static final float SOUND_VOLUME = 0.4F;
    private static final int LANDING_FORCE = 2;
    private static final double HIGH_FALL_DISTANCE = 3.0;

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

        TrampledCropBlock trampled = trampledFormOf(state);
        if (trampled != null && canTrample(serverLevel, entity)) {
            apply(serverLevel, pos, state, trampled, force(entity), movementDirection(entity));
        }
    }

    public static boolean cushionLanding(Level level, BlockPos cropPos, Entity entity) {
        if (!(level instanceof ServerLevel serverLevel)) {
            return false;
        }

        BlockState state = serverLevel.getBlockState(cropPos);
        TrampledCropBlock trampled = trampledFormOf(state);
        if (trampled == null) {
            return false;
        }
        if (canTrample(serverLevel, entity)) {
            apply(serverLevel, cropPos, state, trampled, landingForce(entity), movementDirection(entity));
        }
        return true;
    }

    private static TrampledCropBlock trampledFormOf(BlockState state) {
        return state.getBlock() instanceof TrampledCropBlock trampledCrop
                ? trampledCrop
                : TrampleableCrops.trampledFormOf(state.getBlock());
    }

    private static void apply(ServerLevel level, BlockPos pos, BlockState state, TrampledCropBlock trampled, int force, Direction direction) {
        BlockState trampledState = trample(state, trampled, force, direction);
        if (trampledState != state) {
            level.setBlock(pos, trampledState, Block.UPDATE_CLIENTS);
            playEffects(level, pos, state);
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
        Vec3 previous = previousPosition(entity);
        return Mth.floor(previous.x) != pos.getX() || Mth.floor(previous.z) != pos.getZ();
    }

    private static Vec3 previousPosition(Entity entity) {
        if (entity instanceof Player) {
            return entity.position().subtract(entity.getKnownMovement());
        }
        return new Vec3(entity.xo, entity.yo, entity.zo);
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

    private static int landingForce(Entity entity) {
        int force = LANDING_FORCE;
        if (entity.fallDistance >= HIGH_FALL_DISTANCE) {
            force++;
        }
        if (entity.getBbWidth() >= HEAVY_ENTITY_WIDTH) {
            force++;
        }
        return force;
    }

    private static Direction movementDirection(Entity entity) {
        Vec3 previous = previousPosition(entity);
        double dx = entity.getX() - previous.x;
        double dz = entity.getZ() - previous.z;
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
