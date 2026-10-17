package com.zyypj.farmerplus.fabric;

import com.zyypj.farmerplus.client.BoatRendering;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry;

public final class FarmerPlusFabricClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        BoatRendering.registerLayerDefinitions((layer, definition) -> ModelLayerRegistry.registerModelLayer(layer, definition::get));
        BoatRendering.registerRenderers(EntityRendererRegistry::register);
    }
}
