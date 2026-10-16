package com.zyypj.farmerplus.forge;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(FarmerPlus.MOD_ID)
public final class FarmerPlusForge {

    public FarmerPlusForge(FMLJavaModLoadingContext context) {
        FarmerPlus.init();
        ForgeRegistrationPlatform.bind(context.getModBusGroup());
    }
}
