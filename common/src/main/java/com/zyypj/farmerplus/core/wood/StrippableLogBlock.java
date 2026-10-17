package com.zyypj.farmerplus.core.wood;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.phys.BlockHitResult;

public class StrippableLogBlock extends RotatedPillarBlock {

    private final Supplier<? extends Block> stripped;

    public StrippableLogBlock(Supplier<? extends Block> stripped, BlockBehaviour.Properties properties) {
        super(properties);
        this.stripped = stripped;
    }

    @Override
    protected InteractionResult useItemOn(ItemStack itemStack, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hitResult) {
        if (!itemStack.is(ItemTags.AXES)) {
            return super.useItemOn(itemStack, state, level, pos, player, hand, hitResult);
        }

        if (level instanceof ServerLevel serverLevel) {
            BlockState strippedState = stripped.get().defaultBlockState().setValue(AXIS, state.getValue(AXIS));
            serverLevel.setBlock(pos, strippedState, Block.UPDATE_ALL_IMMEDIATE);
            serverLevel.playSound(null, pos, SoundEvents.AXE_STRIP.value(), SoundSource.BLOCKS, 1.0F, 1.0F);
            serverLevel.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(player, strippedState));
            itemStack.hurtAndBreak(1, player, hand);
        }
        return InteractionResult.SUCCESS;
    }
}
