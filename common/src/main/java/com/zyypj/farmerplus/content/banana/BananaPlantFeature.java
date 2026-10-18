package com.zyypj.farmerplus.content.banana;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.util.valueproviders.IntProvider;
import net.minecraft.util.valueproviders.IntProviders;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.TreeFeature;

public record BananaPlantFeature(
        IntProvider height,
        IntProvider leaves,
        IntProvider suckers,
        float bunchChance
) implements Feature {

    public static final MapCodec<BananaPlantFeature> CODEC = RecordCodecBuilder.mapCodec(instance -> instance.group(
            IntProviders.codec(2, 8).fieldOf("height").forGetter(BananaPlantFeature::height),
            IntProviders.codec(2, 16).fieldOf("leaves").forGetter(BananaPlantFeature::leaves),
            IntProviders.codec(0, 6).fieldOf("suckers").forGetter(BananaPlantFeature::suckers),
            Codec.floatRange(0.0F, 1.0F).optionalFieldOf("bunch_chance", 0.0F).forGetter(BananaPlantFeature::bunchChance)
    ).apply(instance, BananaPlantFeature::new));

    private static final int SET_BLOCK_FLAGS = 18;
    private static final int SPIRAL_STEP = 3;
    private static final int LOWER_TIER_OFFSET = 5;
    private static final int SUCKER_RADIUS = 2;
    private static final int SUCKER_ATTEMPTS = 4;
    private static final int MIN_HEIGHT = 2;
    private static final int MAX_DRY_LEAVES = 2;

    @Override
    public MapCodec<? extends Feature> codec() {
        return CODEC;
    }

    @Override
    public boolean place(WorldGenLevel level, ChunkGenerator chunkGenerator, RandomSource random, BlockPos origin) {
        if (!placePlant(level, random, origin, height.sample(random), leaves.sample(random), random.nextFloat() < bunchChance)) {
            return false;
        }
        int count = suckers.sample(random);
        for (int i = 0; i < count; i++) {
            placeSucker(level, random, origin);
        }
        return true;
    }

    private boolean placePlant(WorldGenLevel level, RandomSource random, BlockPos origin, int stemHeight, int leafCount, boolean withBunch) {
        if (!level.getBlockState(origin.below()).is(BlockTags.SUPPORTS_VEGETATION) || origin.getY() + stemHeight + 2 > level.getMaxY()) {
            return false;
        }
        for (int y = 0; y < stemHeight; y++) {
            if (!TreeFeature.validTreePos(level, origin.above(y))) {
                return false;
            }
        }

        BlockState stem = BananaBlocks.BANANA_STEM.get().defaultBlockState();
        for (int y = 0; y < stemHeight; y++) {
            BananaStemBlock.Segment segment = y == 0 ? BananaStemBlock.Segment.BASE
                    : y == stemHeight - 1 ? BananaStemBlock.Segment.CROWN : BananaStemBlock.Segment.MIDDLE;
            level.setBlock(origin.above(y), stem.setValue(BananaStemBlock.SEGMENT, segment), SET_BLOCK_FLAGS);
        }

        BlockPos crown = origin.above(stemHeight - 1);
        Direction bunchSide = Direction.Plane.HORIZONTAL.getRandomDirection(random);
        LeafDirection reserved = LeafDirection.of(bunchSide);
        int start = random.nextInt(8);
        int upper = (leafCount + 1) / 2;
        for (int i = 0; i < leafCount; i++) {
            boolean lower = i >= upper;
            int index = lower ? start + LOWER_TIER_OFFSET + SPIRAL_STEP * (i - upper) : start + SPIRAL_STEP * i;
            LeafDirection direction = LeafDirection.values()[Math.floorMod(index, 8)];
            if (lower && (direction == reserved || stemHeight < MIN_HEIGHT + 1)) {
                continue;
            }
            placeLeaf(level, lower ? crown.below() : crown, direction, lower ? LeafAge.MATURE : LeafAge.YOUNG);
        }

        if (stemHeight > MIN_HEIGHT + 1) {
            int dryLeaves = random.nextInt(MAX_DRY_LEAVES + 1);
            Direction side = bunchSide;
            for (int i = 0; i < dryLeaves; i++) {
                side = side.getClockWise();
                BlockPos pos = crown.below(2).relative(side);
                if (TreeFeature.validTreePos(level, pos)) {
                    level.setBlock(pos, BananaLeafBlock.of(LeafDirection.of(side), 0, LeafAge.DRY), SET_BLOCK_FLAGS);
                }
            }
        }

        if (withBunch && stemHeight > MIN_HEIGHT) {
            BlockPos bunchPos = crown.below().relative(bunchSide);
            if (level.isEmptyBlock(bunchPos)) {
                level.setBlock(bunchPos, BananaBlocks.BANANA_BUNCH.get().defaultBlockState()
                        .setValue(BananaBunchBlock.FACING, bunchSide.getOpposite())
                        .setValue(BananaBunchBlock.STAGE, random.nextIntBetweenInclusive(BananaBunchBlock.FLOWERING, BananaBunchBlock.RIPE)), SET_BLOCK_FLAGS);
            }
        }
        return true;
    }

    private static void placeLeaf(WorldGenLevel level, BlockPos attach, LeafDirection direction, LeafAge age) {
        for (int step = 0; step < direction.length(); step++) {
            BlockPos pos = direction.offset(attach, step + 1);
            if (!TreeFeature.validTreePos(level, pos)) {
                return;
            }
            level.setBlock(pos, BananaLeafBlock.of(direction, step, age), SET_BLOCK_FLAGS);
        }
    }

    private void placeSucker(WorldGenLevel level, RandomSource random, BlockPos origin) {
        for (int attempt = 0; attempt < SUCKER_ATTEMPTS; attempt++) {
            int dx = random.nextIntBetweenInclusive(-SUCKER_RADIUS, SUCKER_RADIUS);
            int dz = random.nextIntBetweenInclusive(-SUCKER_RADIUS, SUCKER_RADIUS);
            if (Math.max(Math.abs(dx), Math.abs(dz)) < SUCKER_RADIUS) {
                continue;
            }
            for (int dy = 1; dy >= -1; dy--) {
                BlockPos pos = origin.offset(dx, dy, dz);
                if (!level.isEmptyBlock(pos) || !level.getBlockState(pos.below()).is(BlockTags.SUPPORTS_VEGETATION)) {
                    continue;
                }
                if (random.nextBoolean()) {
                    level.setBlock(pos, BananaBlocks.BANANA_SAPLING.get().defaultBlockState(), SET_BLOCK_FLAGS);
                } else {
                    placePlant(level, random, pos, Math.max(MIN_HEIGHT + 1, height.sample(random) - 1), Math.max(2, leaves.sample(random) - 2), false);
                }
                return;
            }
        }
    }
}
