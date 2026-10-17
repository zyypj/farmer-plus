package com.zyypj.farmerplus.fabric;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.registry.BlockEntityBlocks;
import net.fabricmc.api.ModInitializer;

public final class FarmerPlusFabric implements ModInitializer {

    @Override
    public void onInitialize() {
        FarmerPlus.init();
        BlockEntityBlocks.forEach((type, blocks) -> blocks.forEach(type::addValidBlock));
        FabricWorldgen.register();
        FarmerPlus.commonSetup();
    }
}
