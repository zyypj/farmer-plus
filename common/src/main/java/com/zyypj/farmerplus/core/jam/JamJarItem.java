package com.zyypj.farmerplus.core.jam;

import net.minecraft.core.component.DataComponents;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.component.Consumable;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;

public class JamJarItem extends BlockItem {

    public JamJarItem(Block block, Properties properties) {
        super(block, properties);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Player player = context.getPlayer();
        if (player != null && player.isSecondaryUseActive()) {
            return InteractionResult.PASS;
        }
        return super.useOn(context);
    }

    @Override
    public ItemStack finishUsingItem(ItemStack stack, Level level, LivingEntity entity) {
        Consumable consumable = stack.get(DataComponents.CONSUMABLE);
        if (consumable == null) {
            return stack;
        }

        consumable.onConsume(level, entity, stack.copyWithCount(1));
        if (entity.hasInfiniteMaterials()) {
            return stack;
        }

        int portions = JamJarBlock.portions(stack);
        ItemStack leftover = portions > 1
                ? JamJarBlock.withPortions(stack.copyWithCount(1), portions - 1)
                : new ItemStack(Items.GLASS_BOTTLE);
        if (stack.getCount() == 1) {
            return leftover;
        }

        stack.shrink(1);
        entity.handleExtraItemsCreatedOnUse(leftover);
        return stack;
    }
}
