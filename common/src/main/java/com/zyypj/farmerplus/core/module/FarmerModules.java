package com.zyypj.farmerplus.core.module;

import com.zyypj.farmerplus.content.strawberry.StrawberryModule;
import com.zyypj.farmerplus.content.wheat.WheatModule;
import java.util.List;

public final class FarmerModules {

    private static final List<FarmerModule> MODULES = List.of(
            new WheatModule(),
            new StrawberryModule()
    );

    private FarmerModules() {
    }

    public static List<FarmerModule> all() {
        return MODULES;
    }

    public static void registerAll() {
        MODULES.forEach(FarmerModule::register);
    }
}
