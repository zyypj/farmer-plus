package com.zyypj.farmerplus.forge;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(FarmerPlus.MOD_ID)
public final class FarmerPlusForge {

    public FarmerPlusForge(FMLJavaModLoadingContext context) {
        FarmerPlus.init();
        ForgeRegistrationPlatform.bind(context.getModBusGroup());
        FMLCommonSetupEvent.getBus(context.getModBusGroup()).addListener(event -> event.enqueueWork(FarmerPlus::commonSetup));
    }
}
