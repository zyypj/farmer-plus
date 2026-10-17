package com.zyypj.farmerplus.fabric;

import com.zyypj.farmerplus.core.worldgen.BiomeFeatures;
import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;

final class FabricWorldgen {

    private FabricWorldgen() {
    }

    static void register() {
        BiomeFeatures.all().forEach(feature ->
                BiomeModifications.addFeature(BiomeSelectors.tag(feature.biomes()), feature.step(), feature.feature()));
    }
}
