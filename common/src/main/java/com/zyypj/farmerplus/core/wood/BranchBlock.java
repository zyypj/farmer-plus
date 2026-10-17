package com.zyypj.farmerplus.core.wood;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.ScheduledTickAccess;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.PipeBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.pathfinder.PathComputationType;

public class BranchBlock extends PipeBlock {

    public BranchBlock(float size, BlockBehaviour.Properties properties) {
        super(size, properties);
        registerDefaultState(stateDefinition.any()
                .setValue(NORTH, false)
                .setValue(EAST, false)
                .setValue(SOUTH, false)
                .setValue(WEST, false)
                .setValue(UP, false)
                .setValue(DOWN, false));
    }

    public static BlockState withConnections(BlockGetter level, BlockPos pos, BlockState state) {
        for (Direction direction : Direction.values()) {
            BlockPos neighbourPos = pos.relative(direction);
            state = state.setValue(PROPERTY_BY_DIRECTION.get(direction), connectsTo(level, neighbourPos, level.getBlockState(neighbourPos), direction));
        }
        return state;
    }

    private static boolean connectsTo(BlockGetter level, BlockPos neighbourPos, BlockState neighbour, Direction direction) {
        if (neighbour.getBlock() instanceof BranchBlock || neighbour.is(BlockTags.LOGS)) {
            return true;
        }
        return direction == Direction.DOWN && neighbour.isFaceSturdy(level, neighbourPos, Direction.UP);
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        return withConnections(context.getLevel(), context.getClickedPos(), defaultBlockState());
    }

    @Override
    protected BlockState updateShape(BlockState state, LevelReader level, ScheduledTickAccess ticks, BlockPos pos, Direction directionToNeighbour,
            BlockPos neighbourPos, BlockState neighbourState, RandomSource random) {
        return state.setValue(PROPERTY_BY_DIRECTION.get(directionToNeighbour), connectsTo(level, neighbourPos, neighbourState, directionToNeighbour));
    }

    @Override
    protected boolean propagatesSkylightDown(BlockState state) {
        return true;
    }

    @Override
    protected boolean isPathfindable(BlockState state, PathComputationType type) {
        return false;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(NORTH, EAST, SOUTH, WEST, UP, DOWN);
    }
}
