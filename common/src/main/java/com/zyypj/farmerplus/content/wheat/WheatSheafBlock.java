package com.zyypj.farmerplus.content.wheat;

import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

public class WheatSheafBlock extends Block {

    private static final VoxelShape SHAPE = Block.column(12.0, 0.0, 16.0);
    private static final float FALL_DAMAGE_MULTIPLIER = 0.2F;

    public WheatSheafBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPE;
    }

    @Override
    public void fallOn(Level level, BlockState state, BlockPos pos, Entity entity, double fallDistance) {
        entity.causeFallDamage(fallDistance, FALL_DAMAGE_MULTIPLIER, level.damageSources().fall());
    }
}
