package com.zyypj.farmerplus.core.worldgen;

import com.mojang.serialization.MapCodec;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import com.zyypj.farmerplus.platform.Services;
import net.minecraft.core.registries.Registries;

public final class FeatureTypes {

    public static final RegistryEntry<MapCodec<BroadleafTreeFeature>> BROADLEAF_TREE =
            Services.REGISTRATION.register(Registries.FEATURE_TYPE, "broadleaf_tree", key -> BroadleafTreeFeature.CODEC);

    private FeatureTypes() {
    }

    public static void bootstrap() {
    }
}
