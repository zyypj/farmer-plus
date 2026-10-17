package com.zyypj.farmerplus;

import com.zyypj.farmerplus.core.FarmerCreativeTab;
import com.zyypj.farmerplus.core.module.FarmerModules;
import com.zyypj.farmerplus.core.trampling.TramplingGameRules;
import net.minecraft.resources.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class FarmerPlus {

    public static final String MOD_ID = "farmerplus";
    public static final String MOD_NAME = "Farmer+";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_NAME);

    private static boolean initialized;

    private FarmerPlus() {
    }

    public static void init() {
        if (initialized) {
            return;
        }
        initialized = true;

        TramplingGameRules.bootstrap();
        FarmerModules.registerAll();
        FarmerCreativeTab.register();
        LOGGER.info("{} loaded {} content modules", MOD_NAME, FarmerModules.all().size());
    }

    public static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(MOD_ID, path);
    }
}
