package com.zyypj.farmerplus.content.banana;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.pathfinder.PathComputationType;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

public class BananaLeafBlock extends Block {

    public static final int BASE = 0;
    public static final int BLADE = 1;
    public static final int TIP = 2;
    public static final EnumProperty<LeafDirection> DIRECTION = EnumProperty.create("direction", LeafDirection.class);
    public static final IntegerProperty SEGMENT = IntegerProperty.create("segment", BASE, TIP);
    public static final EnumProperty<LeafAge> AGE = EnumProperty.create("age", LeafAge.class);

    private static final VoxelShape[] SHAPES = {
            Block.box(0.0, 8.0, 0.0, 16.0, 16.0, 16.0),
            Block.box(0.0, 11.0, 0.0, 16.0, 16.0, 16.0),
            Block.box(0.0, 2.0, 0.0, 16.0, 15.0, 16.0)
    };
    private static final VoxelShape DRY_SHAPE = Block.box(2.0, 0.0, 2.0, 14.0, 12.0, 14.0);

    public BananaLeafBlock(BlockBehaviour.Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(DIRECTION, LeafDirection.NORTH).setValue(SEGMENT, BASE).setValue(AGE, LeafAge.MATURE));
    }

    public static boolean isSegment(BlockState state, LeafDirection direction, int segment) {
        return state.getBlock() instanceof BananaLeafBlock && state.getValue(DIRECTION) == direction && state.getValue(SEGMENT) == segment;
    }

    public static BlockState of(LeafDirection direction, int step, LeafAge age) {
        return BananaBlocks.BANANA_LEAF.get().defaultBlockState()
                .setValue(DIRECTION, direction)
                .setValue(SEGMENT, direction.segmentAt(step))
                .setValue(AGE, age);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return state.getValue(AGE) == LeafAge.DRY ? DRY_SHAPE : SHAPES[state.getValue(SEGMENT)];
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        LeafDirection direction = LeafDirection.fromYaw(context.getRotation());
        BlockState behind = context.getLevel().getBlockState(direction.offset(context.getClickedPos(), -1));
        int step = 0;
        if (behind.getBlock() instanceof BananaLeafBlock && behind.getValue(DIRECTION) == direction) {
            step = Math.min(behind.getValue(SEGMENT) + 1, direction.length() - 1);
        }
        return of(direction, step, LeafAge.MATURE);
    }

    @Override
    protected void affectNeighborsAfterRemoval(BlockState state, ServerLevel level, BlockPos pos, boolean movedByPiston) {
        LeafDirection direction = state.getValue(DIRECTION);
        BlockPos next = direction.offset(pos, 1);
        BlockState outer = level.getBlockState(next);
        if (outer.getBlock() instanceof BananaLeafBlock && outer.getValue(DIRECTION) == direction && outer.getValue(SEGMENT) > state.getValue(SEGMENT)) {
            level.destroyBlock(next, true);
        }
    }

    @Override
    protected BlockState rotate(BlockState state, Rotation rotation) {
        return state.setValue(DIRECTION, state.getValue(DIRECTION).rotate(rotation));
    }

    @Override
    protected boolean propagatesSkylightDown(BlockState state) {
        return true;
    }

    @Override
    protected boolean isPathfindable(BlockState state, PathComputationType type) {
        return type == PathComputationType.AIR;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(DIRECTION, SEGMENT, AGE);
    }
}
