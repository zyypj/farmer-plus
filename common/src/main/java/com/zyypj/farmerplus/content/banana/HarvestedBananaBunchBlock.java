package com.zyypj.farmerplus.content.banana;

import java.util.Map;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ItemParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.ScheduledTickAccess;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

public class HarvestedBananaBunchBlock extends Block {

    public static final int MAX_BANANAS = 8;
    public static final EnumProperty<Direction> FACING = BlockStateProperties.HORIZONTAL_FACING;
    public static final IntegerProperty BANANAS = IntegerProperty.create("bananas", 1, MAX_BANANAS);

    private static final Map<Direction, VoxelShape> SHAPES = Shapes.rotateHorizontal(Block.box(3.0, 0.0, 3.0, 13.0, 16.0, 14.0));
    private static final double[][] HAND_CENTERS = {
            {9.84, 13.08, 9.26}, {6.16, 13.08, 7.74},
            {9.90, 9.21, 8.50}, {6.10, 9.21, 8.50},
            {9.68, 5.35, 7.81}, {6.32, 5.35, 9.19},
            {9.22, 1.48, 7.28}, {6.78, 1.48, 9.72}
    };
    private static final double TOSS_SPEED = 0.08;

    public HarvestedBananaBunchBlock(BlockBehaviour.Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH).setValue(BANANAS, MAX_BANANAS));
    }

    public static Vec3 fingerPosition(BlockPos pos, Direction facing, int index) {
        double x = HAND_CENTERS[index][0];
        double z = HAND_CENTERS[index][2];
        double rotatedX = switch (facing) {
            case SOUTH -> 16.0 - x;
            case EAST -> 16.0 - z;
            case WEST -> z;
            default -> x;
        };
        double rotatedZ = switch (facing) {
            case SOUTH -> 16.0 - z;
            case EAST -> x;
            case WEST -> 16.0 - x;
            default -> z;
        };
        return new Vec3(pos.getX() + rotatedX / 16.0, pos.getY() + HAND_CENTERS[index][1] / 16.0, pos.getZ() + rotatedZ / 16.0);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPES.get(state.getValue(FACING));
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        return defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
    }

    @Override
    protected boolean canSurvive(BlockState state, LevelReader level, BlockPos pos) {
        return level.getBlockState(pos.below()).isFaceSturdy(level, pos.below(), Direction.UP);
    }

    @Override
    protected BlockState updateShape(BlockState state, LevelReader level, ScheduledTickAccess ticks, BlockPos pos, Direction directionToNeighbour,
            BlockPos neighbourPos, BlockState neighbourState, RandomSource random) {
        if (directionToNeighbour == Direction.DOWN && !canSurvive(state, level, pos)) {
            ticks.scheduleTick(pos, this, 1);
        }
        return state;
    }

    @Override
    protected void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (!canSurvive(state, level, pos)) {
            level.destroyBlock(pos, true);
        }
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hitResult) {
        if (level instanceof ServerLevel serverLevel) {
            int bananas = state.getValue(BANANAS);
            Vec3 finger = fingerPosition(pos, state.getValue(FACING), bananas - 1);
            ItemStack banana = new ItemStack(BananaItems.BANANA.get());
            ItemEntity drop = new ItemEntity(serverLevel, finger.x, finger.y, finger.z, banana);
            drop.setDeltaMovement(player.position().subtract(finger).normalize().scale(TOSS_SPEED).add(0.0, TOSS_SPEED, 0.0));
            drop.setDefaultPickUpDelay();
            serverLevel.addFreshEntity(drop);
            serverLevel.sendParticles(new ItemParticleOption(ParticleTypes.ITEM, BananaItems.BANANA.get()), finger.x, finger.y, finger.z, 6, 0.08, 0.05, 0.08, 0.02);
            float pitch = 0.9F + serverLevel.getRandom().nextFloat() * 0.3F;
            serverLevel.playSound(null, pos, SoundEvents.SWEET_BERRY_BUSH_PICK_BERRIES, SoundSource.BLOCKS, 1.0F, pitch);
            BlockState remaining = bananas > 1 ? state.setValue(BANANAS, bananas - 1) : Blocks.AIR.defaultBlockState();
            serverLevel.setBlock(pos, remaining, Block.UPDATE_ALL);
            serverLevel.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(player, remaining));
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    protected BlockState rotate(BlockState state, Rotation rotation) {
        return state.setValue(FACING, rotation.rotate(state.getValue(FACING)));
    }

    @Override
    protected BlockState mirror(BlockState state, Mirror mirror) {
        return state.rotate(mirror.getRotation(state.getValue(FACING)));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING, BANANAS);
    }
}
