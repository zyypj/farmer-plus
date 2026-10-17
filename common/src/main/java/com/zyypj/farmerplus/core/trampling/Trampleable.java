package com.zyypj.farmerplus.core.trampling;

import net.minecraft.core.Direction;
import net.minecraft.world.level.block.state.BlockState;

public interface Trampleable {

    BlockState trample(BlockState state, int force, Direction direction);
}
