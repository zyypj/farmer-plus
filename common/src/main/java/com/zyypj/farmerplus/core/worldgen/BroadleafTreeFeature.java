package com.zyypj.farmerplus.core.worldgen;

import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.util.valueproviders.IntProvider;
import net.minecraft.util.valueproviders.IntProviders;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.TreeFeature;
import net.minecraft.world.phys.Vec3;

public record BroadleafTreeFeature(
        BlockState trunk,
        BlockState leader,
        BlockState branch,
        BlockState leaves,
        IntProvider height,
        IntProvider trunkHeight,
        IntProvider limbs,
        IntProvider crownRadius
) implements Feature {

    public static final MapCodec<BroadleafTreeFeature> CODEC = RecordCodecBuilder.mapCodec(instance -> instance.group(
            BlockState.CODEC.fieldOf("trunk").forGetter(BroadleafTreeFeature::trunk),
            BlockState.CODEC.fieldOf("leader").forGetter(BroadleafTreeFeature::leader),
            BlockState.CODEC.fieldOf("branch").forGetter(BroadleafTreeFeature::branch),
            BlockState.CODEC.fieldOf("leaves").forGetter(BroadleafTreeFeature::leaves),
            IntProviders.codec(6, 40).fieldOf("height").forGetter(BroadleafTreeFeature::height),
            IntProviders.codec(1, 12).fieldOf("trunk_height").forGetter(BroadleafTreeFeature::trunkHeight),
            IntProviders.codec(2, 8).fieldOf("limbs").forGetter(BroadleafTreeFeature::limbs),
            IntProviders.codec(3, 10).fieldOf("crown_radius").forGetter(BroadleafTreeFeature::crownRadius)
    ).apply(instance, BroadleafTreeFeature::new));

    private static final int SET_BLOCK_FLAGS = 19;
    private static final int MAX_LEAF_DISTANCE = 6;
    private static final double LEADER_HEIGHT = 0.82;
    private static final double LIMB_REACH_MIN = 0.55;
    private static final double LIMB_REACH_MAX = 0.72;
    private static final double LIMB_RISE_MIN = 0.5;
    private static final double LIMB_RISE_MAX = 0.85;
    private static final double LIMB_ANGLE_JITTER = 0.45;
    private static final double SIDE_BRANCH_AT = 0.55;
    private static final double SIDE_BRANCH_TURN = 0.75;
    private static final double SKIRT_BRANCH_AT = 0.3;
    private static final double SKIRT_REACH = 0.42;
    private static final double BLOB_RADIUS_MIN = 2.9;
    private static final double BLOB_RADIUS_MAX = 3.8;
    private static final double BLOB_FLATTENING = 0.72;
    private static final double SKIRT_BLOB_RADIUS = 2.6;
    private static final double EDGE_NOISE = 0.18;

    @Override
    public MapCodec<? extends Feature> codec() {
        return CODEC;
    }

    @Override
    public boolean place(WorldGenLevel level, ChunkGenerator chunkGenerator, RandomSource random, BlockPos origin) {
        int treeHeight = height.sample(random);
        int clearTrunk = Math.min(trunkHeight.sample(random), treeHeight / 2);
        if (origin.getY() <= level.getMinY() || origin.getY() + treeHeight + 4 > level.getMaxY()) {
            return false;
        }

        Map<BlockPos, BlockState> logs = new HashMap<>();
        List<Crown> crowns = new ArrayList<>();
        Vec3 base = Vec3.atBottomCenterOf(origin);

        for (int y = 0; y <= clearTrunk; y++) {
            logs.put(origin.above(y), oriented(trunk, Direction.Axis.Y));
        }

        Vec3 split = base.add(0.0, clearTrunk, 0.0);
        Vec3 leaderTop = base.add(random.nextDouble() - 0.5, treeHeight * LEADER_HEIGHT, random.nextDouble() - 0.5);
        addLimb(logs, leader, split, leaderTop);
        crowns.add(new Crown(leaderTop, radius(random) + 0.4));

        int radius = crownRadius.sample(random);
        int limbCount = limbs.sample(random);
        double startAngle = random.nextDouble() * Math.PI * 2.0;
        for (int i = 0; i < limbCount; i++) {
            double angle = startAngle + i * Math.PI * 2.0 / limbCount + (random.nextDouble() - 0.5) * LIMB_ANGLE_JITTER;
            Vec3 direction = new Vec3(Math.cos(angle), 0.0, Math.sin(angle));
            Vec3 start = split.add(0.0, -(i % 2), 0.0);
            double reach = radius * Mth.lerp(random.nextDouble(), LIMB_REACH_MIN, LIMB_REACH_MAX);
            double rise = (treeHeight * LEADER_HEIGHT - clearTrunk) * Mth.lerp(random.nextDouble(), LIMB_RISE_MIN, LIMB_RISE_MAX);
            Vec3 tip = start.add(direction.scale(reach)).add(0.0, rise, 0.0);
            addLimb(logs, branch, start, tip);
            crowns.add(new Crown(tip, radius(random)));

            Vec3 fork = start.lerp(tip, SIDE_BRANCH_AT);
            double sideAngle = angle + (random.nextBoolean() ? SIDE_BRANCH_TURN : -SIDE_BRANCH_TURN);
            Vec3 sideTip = fork.add(new Vec3(Math.cos(sideAngle), 0.0, Math.sin(sideAngle)).scale(2.0 + random.nextInt(2))).add(0.0, 1.0 + random.nextInt(2), 0.0);
            addLimb(logs, branch, fork, sideTip);
            crowns.add(new Crown(sideTip, radius(random) - 0.3));

            Vec3 skirtStart = start.lerp(tip, SKIRT_BRANCH_AT);
            Vec3 skirtTip = skirtStart.add(direction.scale(radius * SKIRT_REACH)).add(0.0, -0.5, 0.0);
            addLimb(logs, branch, skirtStart, skirtTip);
            crowns.add(new Crown(skirtTip, SKIRT_BLOB_RADIUS));
        }

        if (!trunkIsFree(level, origin, clearTrunk)) {
            return false;
        }

        Set<BlockPos> foliage = new LinkedHashSet<>();
        for (Crown crown : crowns) {
            addCrown(foliage, logs, crown, random);
        }

        List<BlockPos> placed = new ArrayList<>();
        logs.forEach((pos, state) -> {
            if (TreeFeature.validTreePos(level, pos) || pos.getY() <= origin.getY() + clearTrunk) {
                level.setBlock(pos, state, SET_BLOCK_FLAGS);
                placed.add(pos);
            }
        });
        for (BlockPos pos : placed) {
            level.setBlock(pos, Block.updateFromNeighbourShapes(level.getBlockState(pos), level, pos), SET_BLOCK_FLAGS);
        }
        placeLeaves(level, logs.keySet(), foliage);
        return true;
    }

    private static void addLimb(Map<BlockPos, BlockState> logs, BlockState wood, Vec3 from, Vec3 to) {
        Vec3 delta = to.subtract(from);
        int steps = Math.max(1, (int) Math.ceil(Math.max(Math.abs(delta.x), Math.max(Math.abs(delta.y), Math.abs(delta.z)))));
        BlockState state = oriented(wood, axisOf(delta));
        BlockPos previous = BlockPos.containing(from);
        logs.putIfAbsent(previous, state);
        for (int step = 1; step <= steps; step++) {
            BlockPos next = BlockPos.containing(from.add(delta.scale(step / (double) steps)));
            BlockPos.MutableBlockPos cursor = previous.mutable();
            for (Direction.Axis axis : Direction.Axis.values()) {
                int offset = next.get(axis) - cursor.get(axis);
                while (offset != 0) {
                    cursor.move(Direction.fromAxisAndDirection(axis, offset > 0 ? Direction.AxisDirection.POSITIVE : Direction.AxisDirection.NEGATIVE));
                    logs.putIfAbsent(cursor.immutable(), state);
                    offset -= Integer.signum(offset);
                }
            }
            previous = next;
        }
    }

    private static BlockState oriented(BlockState state, Direction.Axis axis) {
        return state.hasProperty(RotatedPillarBlock.AXIS) ? state.setValue(RotatedPillarBlock.AXIS, axis) : state;
    }

    private static Direction.Axis axisOf(Vec3 delta) {
        double x = Math.abs(delta.x);
        double y = Math.abs(delta.y);
        double z = Math.abs(delta.z);
        if (y >= x && y >= z) {
            return Direction.Axis.Y;
        }
        return x >= z ? Direction.Axis.X : Direction.Axis.Z;
    }

    private double radius(RandomSource random) {
        return Mth.lerp(random.nextDouble(), BLOB_RADIUS_MIN, BLOB_RADIUS_MAX);
    }

    private static void addCrown(Set<BlockPos> foliage, Map<BlockPos, BlockState> logs, Crown crown, RandomSource random) {
        double horizontal = crown.radius();
        double vertical = crown.radius() * BLOB_FLATTENING;
        int reach = (int) Math.ceil(horizontal);
        BlockPos center = BlockPos.containing(crown.center());
        for (int dx = -reach; dx <= reach; dx++) {
            for (int dy = -reach; dy <= reach; dy++) {
                for (int dz = -reach; dz <= reach; dz++) {
                    double distance = (dx * dx + dz * dz) / (horizontal * horizontal) + (dy * dy) / (vertical * vertical);
                    if (distance <= 1.0 - random.nextDouble() * EDGE_NOISE) {
                        BlockPos pos = center.offset(dx, dy, dz);
                        if (!logs.containsKey(pos)) {
                            foliage.add(pos);
                        }
                    }
                }
            }
        }
    }

    private static boolean trunkIsFree(WorldGenLevel level, BlockPos origin, int clearTrunk) {
        for (int y = 1; y <= clearTrunk; y++) {
            BlockPos pos = origin.above(y);
            if (!TreeFeature.validTreePos(level, pos)) {
                return false;
            }
        }
        return true;
    }

    private void placeLeaves(WorldGenLevel level, Set<BlockPos> logs, Set<BlockPos> foliage) {
        Map<BlockPos, Integer> distances = new HashMap<>();
        Deque<BlockPos> queue = new ArrayDeque<>();
        for (BlockPos pos : logs) {
            distances.put(pos, 0);
            queue.add(pos);
        }
        while (!queue.isEmpty()) {
            BlockPos pos = queue.poll();
            int distance = distances.get(pos);
            if (distance >= MAX_LEAF_DISTANCE) {
                continue;
            }
            for (Direction direction : Direction.values()) {
                BlockPos next = pos.relative(direction);
                if (foliage.contains(next) && !distances.containsKey(next)) {
                    distances.put(next, distance + 1);
                    queue.add(next);
                }
            }
        }
        for (BlockPos pos : foliage) {
            Integer distance = distances.get(pos);
            if (distance != null && TreeFeature.validTreePos(level, pos)) {
                level.setBlock(pos, leaves.setValue(BlockStateProperties.DISTANCE, distance), SET_BLOCK_FLAGS);
            }
        }
    }

    private record Crown(Vec3 center, double radius) {
    }
}
