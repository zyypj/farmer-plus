package com.zyypj.farmerplus.core.wood;

import net.minecraft.world.level.block.ButtonBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.BlockSetType;

public class WoodButtonBlock extends ButtonBlock {

    public WoodButtonBlock(BlockSetType type, int ticksToStayPressed, BlockBehaviour.Properties properties) {
        super(type, ticksToStayPressed, properties);
    }
}
