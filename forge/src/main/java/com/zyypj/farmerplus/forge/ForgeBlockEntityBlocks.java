package com.zyypj.farmerplus.forge;

import com.zyypj.farmerplus.core.registry.BlockEntityBlocks;
import com.zyypj.farmerplus.mixin.BlockEntityTypeAccessor;
import java.util.HashSet;
import java.util.Set;
import net.minecraft.world.level.block.Block;

final class ForgeBlockEntityBlocks {

    private ForgeBlockEntityBlocks() {
    }

    static void apply() {
        BlockEntityBlocks.forEach((type, blocks) -> {
            BlockEntityTypeAccessor accessor = (BlockEntityTypeAccessor) type;
            Set<Block> validBlocks = new HashSet<>(accessor.farmerplus$getValidBlocks());
            validBlocks.addAll(blocks);
            accessor.farmerplus$setValidBlocks(Set.copyOf(validBlocks));
        });
    }
}
