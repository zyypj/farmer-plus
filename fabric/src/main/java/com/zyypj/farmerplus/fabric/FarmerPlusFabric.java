package com.zyypj.farmerplus.fabric;

import com.zyypj.farmerplus.FarmerPlus;
import net.fabricmc.api.ModInitializer;

public final class FarmerPlusFabric implements ModInitializer {

    @Override
    public void onInitialize() {
        FarmerPlus.init();
        FabricWorldgen.register();
    }
}
