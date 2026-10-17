package com.zyypj.farmerplus.neoforge;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.client.BoatRendering;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

@Mod(value = FarmerPlus.MOD_ID, dist = Dist.CLIENT)
public final class FarmerPlusNeoForgeClient {

    public FarmerPlusNeoForgeClient(IEventBus modBus) {
        modBus.addListener(EntityRenderersEvent.RegisterLayerDefinitions.class, event ->
                BoatRendering.registerLayerDefinitions(event::registerLayerDefinition));
        modBus.addListener(EntityRenderersEvent.RegisterRenderers.class, event ->
                BoatRendering.registerRenderers(event::registerEntityRenderer));
    }
}
