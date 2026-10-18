package com.zyypj.farmerplus.content.avocado;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.ScheduledTickAccess;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.BonemealSource;
import net.minecraft.world.level.block.BonemealableBlock;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

public class AvocadoFruitBlock extends Block implements BonemealableBlock {

    public static final int FLOWERING = 0;
    public static final int UNRIPE = 1;
    public static final int RIPE = 2;
    public static final IntegerProperty STAGE = IntegerProperty.create("stage", FLOWERING, RIPE);

    private static final ResourceKey<LootTable> HARVEST_LOOT = ResourceKey.create(Registries.LOOT_TABLE, FarmerPlus.id("harvest/avocado_fruit"));
    private static final int[] GROWTH_CHANCE = {8, 10};
    private static final VoxelShape[] SHAPES = {
            Block.box(3.0, 12.0, 4.0, 13.0, 16.0, 11.0),
            Block.box(6.0, 9.5, 5.5, 10.5, 16.0, 10.5),
            Block.box(5.5, 8.0, 5.0, 11.5, 16.0, 11.0)
    };

    public AvocadoFruitBlock(BlockBehaviour.Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(STAGE, FLOWERING));
    }

    public static boolean isRipe(BlockState state) {
        return state.getValue(STAGE) == RIPE;
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPES[state.getValue(STAGE)];
    }

    @Override
    protected boolean isRandomlyTicking(BlockState state) {
        return !isRipe(state);
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        int stage = state.getValue(STAGE);
        if (stage < RIPE && random.nextInt(GROWTH_CHANCE[stage]) == 0) {
            level.setBlock(pos, state.setValue(STAGE, stage + 1), Block.UPDATE_CLIENTS);
        }
    }

    @Override
    protected boolean canSurvive(BlockState state, LevelReader level, BlockPos pos) {
        return level.getBlockState(pos.above()).is(AvocadoBlocks.AVOCADO_LEAVES.get());
    }

    @Override
    protected BlockState updateShape(BlockState state, LevelReader level, ScheduledTickAccess ticks, BlockPos pos, Direction directionToNeighbour,
            BlockPos neighbourPos, BlockState neighbourState, RandomSource random) {
        if (directionToNeighbour == Direction.UP && !canSurvive(state, level, pos)) {
            return Blocks.AIR.defaultBlockState();
        }
        return super.updateShape(state, level, ticks, pos, directionToNeighbour, neighbourPos, neighbourState, random);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hitResult) {
        if (!isRipe(state)) {
            return super.useWithoutItem(state, level, pos, player, hitResult);
        }
        if (level instanceof ServerLevel serverLevel) {
            Block.dropFromBlockInteractLootTable(serverLevel, HARVEST_LOOT, pos, state, null, null, player,
                    (dropLevel, stack) -> Block.popResource(dropLevel, pos, stack));
            float pitch = 0.8F + serverLevel.getRandom().nextFloat() * 0.4F;
            serverLevel.playSound(null, pos, SoundEvents.CAVE_VINES_PICK_BERRIES, SoundSource.BLOCKS, 1.0F, pitch);
            BlockState picked = Blocks.AIR.defaultBlockState();
            serverLevel.setBlock(pos, picked, Block.UPDATE_ALL);
            serverLevel.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(player, picked));
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    protected ItemStack getCloneItemStack(LevelReader level, BlockPos pos, BlockState state, boolean includeData) {
        return new ItemStack(AvocadoItems.AVOCADO.get());
    }

    @Override
    public boolean isValidBonemealTarget(LevelReader level, BlockPos pos, BlockState state, BonemealSource source) {
        return !isRipe(state);
    }

    @Override
    public boolean isBonemealSuccess(Level level, RandomSource random, BlockPos pos, BlockState state, BonemealSource source) {
        return true;
    }

    @Override
    public void performBonemeal(ServerLevel level, RandomSource random, BlockPos pos, BlockState state, BonemealSource source) {
        level.setBlock(pos, state.setValue(STAGE, state.getValue(STAGE) + 1), Block.UPDATE_CLIENTS);
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(STAGE);
    }
}
