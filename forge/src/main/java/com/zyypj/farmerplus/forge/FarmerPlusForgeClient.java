package com.zyypj.farmerplus.forge;

import com.zyypj.farmerplus.client.BoatRendering;
import net.minecraftforge.client.event.EntityRenderersEvent;

final class FarmerPlusForgeClient {

    private FarmerPlusForgeClient() {
    }

    static void register() {
        EntityRenderersEvent.RegisterLayerDefinitions.BUS.addListener(event ->
                BoatRendering.registerLayerDefinitions(event::registerLayerDefinition));
        EntityRenderersEvent.RegisterRenderers.BUS.addListener(event ->
                BoatRendering.registerRenderers(event::registerEntityRenderer));
    }
}
