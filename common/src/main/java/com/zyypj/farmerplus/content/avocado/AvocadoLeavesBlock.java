package com.zyypj.farmerplus.content.avocado;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.TintedParticleLeavesBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.phys.BlockHitResult;

public class AvocadoLeavesBlock extends TintedParticleLeavesBlock {

    public static final int NO_FRUIT = 0;
    public static final int FLOWERING = 1;
    public static final int UNRIPE = 2;
    public static final int RIPE = 3;
    public static final IntegerProperty FRUIT = IntegerProperty.create("fruit", NO_FRUIT, RIPE);

    private static final ResourceKey<LootTable> HARVEST_LOOT = ResourceKey.create(Registries.LOOT_TABLE, FarmerPlus.id("harvest/avocado_leaves"));
    private static final float LEAF_PARTICLE_CHANCE = 0.01F;
    private static final int MAX_FRUITING_DISTANCE = 5;
    private static final int FRUITING_SPACING = 3;
    private static final int FLOWERING_CHANCE = 24;
    private static final int FRUIT_SET_CHANCE = 8;
    private static final int RIPENING_CHANCE = 10;
    private static final int FRUIT_FALL_CHANCE = 40;

    public AvocadoLeavesBlock(BlockBehaviour.Properties properties) {
        super(LEAF_PARTICLE_CHANCE, properties);
        registerDefaultState(defaultBlockState().setValue(FRUIT, NO_FRUIT));
    }

    public static boolean isRipe(BlockState state) {
        return state.getValue(FRUIT) == RIPE;
    }

    @Override
    protected boolean isRandomlyTicking(BlockState state) {
        return super.isRandomlyTicking(state) || !state.getValue(PERSISTENT);
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        super.randomTick(state, level, pos, random);
        if (!level.getBlockState(pos).is(this) || !canBearFruit(state, level, pos)) {
            return;
        }

        int fruit = state.getValue(FRUIT);
        if (fruit == NO_FRUIT && random.nextInt(FLOWERING_CHANCE) == 0) {
            setFruit(level, pos, state, FLOWERING);
        } else if (fruit == FLOWERING && random.nextInt(FRUIT_SET_CHANCE) == 0) {
            setFruit(level, pos, state, UNRIPE);
        } else if (fruit == UNRIPE && random.nextInt(RIPENING_CHANCE) == 0) {
            setFruit(level, pos, state, RIPE);
        } else if (fruit == RIPE && random.nextInt(FRUIT_FALL_CHANCE) == 0) {
            Block.popResource(level, pos.below(), new ItemStack(AvocadoItems.AVOCADO.get()));
            setFruit(level, pos, state, NO_FRUIT);
        }
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hitResult) {
        if (!isRipe(state)) {
            return super.useWithoutItem(state, level, pos, player, hitResult);
        }

        if (level instanceof ServerLevel serverLevel) {
            Block.dropFromBlockInteractLootTable(serverLevel, HARVEST_LOOT, pos, state, null, null, player,
                    (dropLevel, stack) -> Block.popResource(dropLevel, pos.below(), stack));
            float pitch = 0.8F + serverLevel.getRandom().nextFloat() * 0.4F;
            serverLevel.playSound(null, pos, SoundEvents.CAVE_VINES_PICK_BERRIES, SoundSource.BLOCKS, 1.0F, pitch);
            BlockState picked = state.setValue(FRUIT, NO_FRUIT);
            serverLevel.setBlock(pos, picked, Block.UPDATE_CLIENTS);
            serverLevel.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(player, picked));
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        super.createBlockStateDefinition(builder);
        builder.add(FRUIT);
    }

    private static boolean canBearFruit(BlockState state, ServerLevel level, BlockPos pos) {
        return !state.getValue(PERSISTENT)
                && state.getValue(DISTANCE) <= MAX_FRUITING_DISTANCE
                && Math.floorMod(pos.getX() * 7 + pos.getY() * 13 + pos.getZ() * 5, FRUITING_SPACING) == 0
                && level.isEmptyBlock(pos.below());
    }

    private static void setFruit(ServerLevel level, BlockPos pos, BlockState state, int fruit) {
        level.setBlock(pos, state.setValue(FRUIT, fruit), Block.UPDATE_CLIENTS);
    }
}
