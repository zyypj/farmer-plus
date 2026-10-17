package com.zyypj.farmerplus.neoforge;

import com.zyypj.farmerplus.FarmerPlus;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;

@Mod(FarmerPlus.MOD_ID)
public final class FarmerPlusNeoForge {

    public FarmerPlusNeoForge(IEventBus modBus) {
        FarmerPlus.init();
        NeoForgeRegistrationPlatform.bind(modBus);
        modBus.addListener(FMLCommonSetupEvent.class, event -> event.enqueueWork(FarmerPlus::commonSetup));
    }
}
