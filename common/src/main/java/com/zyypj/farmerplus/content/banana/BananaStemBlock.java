package com.zyypj.farmerplus.content.banana;

import java.util.Locale;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.util.StringRepresentable;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.ScheduledTickAccess;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.pathfinder.PathComputationType;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

public class BananaStemBlock extends Block {

    public static final EnumProperty<Segment> SEGMENT = EnumProperty.create("segment", Segment.class);
    public static final BooleanProperty FRUITED = BooleanProperty.create("fruited");

    private static final VoxelShape SHAPE = Block.column(6.0, 0.0, 16.0);
    private static final int FLOWERING_CHANCE = 20;
    private static final int SUCKER_CHANCE = 40;
    private static final int DIEBACK_CHANCE = 6;
    private static final int CLUMP_RADIUS = 2;
    private static final int MAX_CLUMP_SIZE = 4;

    public BananaStemBlock(BlockBehaviour.Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(SEGMENT, Segment.MIDDLE).setValue(FRUITED, false));
    }

    public static boolean isStem(BlockState state) {
        return state.getBlock() instanceof BananaStemBlock;
    }

    public static BlockState segmentFor(BlockState state, BlockGetter level, BlockPos pos) {
        boolean below = isStem(level.getBlockState(pos.below()));
        boolean above = isStem(level.getBlockState(pos.above()));
        Segment segment = !below ? Segment.BASE : above ? Segment.MIDDLE : Segment.CROWN;
        return state.setValue(SEGMENT, segment);
    }

    public static void markFruited(LevelAccessor level, BlockPos stemPos) {
        BlockPos.MutableBlockPos cursor = stemPos.mutable();
        if (!isStem(level.getBlockState(cursor))) {
            return;
        }
        while (isStem(level.getBlockState(cursor.above()))) {
            cursor.move(Direction.UP);
        }
        BlockState crown = level.getBlockState(cursor);
        if (!crown.getValue(FRUITED)) {
            level.setBlock(cursor, crown.setValue(FRUITED, true), Block.UPDATE_CLIENTS);
        }
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPE;
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        return segmentFor(defaultBlockState(), context.getLevel(), context.getClickedPos());
    }

    @Override
    protected boolean canSurvive(BlockState state, LevelReader level, BlockPos pos) {
        BlockState below = level.getBlockState(pos.below());
        return isStem(below) || below.is(BlockTags.SUPPORTS_VEGETATION);
    }

    @Override
    protected BlockState updateShape(BlockState state, LevelReader level, ScheduledTickAccess ticks, BlockPos pos, Direction directionToNeighbour,
            BlockPos neighbourPos, BlockState neighbourState, RandomSource random) {
        if (directionToNeighbour.getAxis() != Direction.Axis.Y) {
            return state;
        }
        if (directionToNeighbour == Direction.DOWN && !canSurvive(state, level, pos)) {
            ticks.scheduleTick(pos, this, 1);
        }
        return segmentFor(state, level, pos);
    }

    @Override
    protected void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (!canSurvive(state, level, pos)) {
            level.destroyBlock(pos, true);
        }
    }

    @Override
    protected void affectNeighborsAfterRemoval(BlockState state, ServerLevel level, BlockPos pos, boolean movedByPiston) {
        for (LeafDirection direction : LeafDirection.values()) {
            BlockPos leafPos = direction.offset(pos, 1);
            BlockState leaf = level.getBlockState(leafPos);
            if (BananaLeafBlock.isSegment(leaf, direction, 0)) {
                level.destroyBlock(leafPos, true);
            }
        }
    }

    @Override
    protected boolean isRandomlyTicking(BlockState state) {
        return state.getValue(SEGMENT) == Segment.CROWN;
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (state.getValue(FRUITED)) {
            if (random.nextInt(DIEBACK_CHANCE) == 0) {
                dieBack(level, pos);
            }
            return;
        }
        if (random.nextInt(FLOWERING_CHANCE) == 0) {
            flower(level, pos.below(), random);
        }
        if (random.nextInt(SUCKER_CHANCE) == 0) {
            sprout(level, base(level, pos), random);
        }
    }

    @Override
    protected ItemStack getCloneItemStack(LevelReader level, BlockPos pos, BlockState state, boolean includeData) {
        return new ItemStack(BananaItems.BANANA_SAPLING.get());
    }

    @Override
    protected boolean isPathfindable(BlockState state, PathComputationType type) {
        return false;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(SEGMENT, FRUITED);
    }

    private static void flower(ServerLevel level, BlockPos stemPos, RandomSource random) {
        if (!isStem(level.getBlockState(stemPos)) || hasBunch(level, stemPos)) {
            return;
        }
        Direction side = Direction.Plane.HORIZONTAL.getRandomDirection(random);
        for (int i = 0; i < 4; i++) {
            BlockPos bunchPos = stemPos.relative(side);
            if (level.isEmptyBlock(bunchPos)) {
                level.setBlock(bunchPos, BananaBlocks.BANANA_BUNCH.get().defaultBlockState()
                        .setValue(BlockStateProperties.HORIZONTAL_FACING, side.getOpposite()), Block.UPDATE_ALL);
                return;
            }
            side = side.getClockWise();
        }
    }

    private static boolean hasBunch(ServerLevel level, BlockPos stemPos) {
        for (Direction side : Direction.Plane.HORIZONTAL) {
            if (level.getBlockState(stemPos.relative(side)).is(BananaBlocks.BANANA_BUNCH.get())) {
                return true;
            }
        }
        return false;
    }

    private static BlockPos base(ServerLevel level, BlockPos pos) {
        BlockPos.MutableBlockPos cursor = pos.mutable();
        while (isStem(level.getBlockState(cursor.below()))) {
            cursor.move(Direction.DOWN);
        }
        return cursor.immutable();
    }

    private static void dieBack(ServerLevel level, BlockPos crown) {
        BlockPos base = base(level, crown);
        for (BlockPos cursor = crown; cursor.getY() >= base.getY(); cursor = cursor.below()) {
            level.destroyBlock(cursor, false);
        }
        BlockState follower = BananaBlocks.BANANA_SAPLING.get().defaultBlockState();
        if (level.isEmptyBlock(base) && follower.canSurvive(level, base)) {
            level.setBlock(base, follower, Block.UPDATE_ALL);
        }
    }

    private static void sprout(ServerLevel level, BlockPos base, RandomSource random) {
        BlockPos target = base.offset(random.nextIntBetweenInclusive(-CLUMP_RADIUS, CLUMP_RADIUS), random.nextIntBetweenInclusive(-1, 1),
                random.nextIntBetweenInclusive(-CLUMP_RADIUS, CLUMP_RADIUS));
        BlockState sucker = BananaBlocks.BANANA_SAPLING.get().defaultBlockState();
        if (!level.isEmptyBlock(target) || !sucker.canSurvive(level, target) || clumpSize(level, base) >= MAX_CLUMP_SIZE) {
            return;
        }
        level.setBlock(target, sucker, Block.UPDATE_ALL);
    }

    private static int clumpSize(ServerLevel level, BlockPos base) {
        int count = 0;
        for (BlockPos pos : BlockPos.betweenClosed(base.offset(-CLUMP_RADIUS, -1, -CLUMP_RADIUS), base.offset(CLUMP_RADIUS, 1, CLUMP_RADIUS))) {
            BlockState state = level.getBlockState(pos);
            if (state.is(BananaBlocks.BANANA_SAPLING.get()) || isStem(state) && state.getValue(SEGMENT) == Segment.BASE) {
                count++;
            }
        }
        return count;
    }

    public enum Segment implements StringRepresentable {
        BASE,
        MIDDLE,
        CROWN;

        @Override
        public String getSerializedName() {
            return name().toLowerCase(Locale.ROOT);
        }
    }
}
