package com.zyypj.farmerplus.content.banana;

import com.mojang.serialization.MapCodec;
import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import com.zyypj.farmerplus.core.worldgen.BiomeFeature;
import com.zyypj.farmerplus.platform.Services;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.levelgen.GenerationStep;

public final class BananaWorldgen {

    public static final RegistryEntry<MapCodec<BananaPlantFeature>> BANANA_PLANT_TYPE =
            Services.REGISTRATION.register(Registries.FEATURE_TYPE, "banana_plant", key -> BananaPlantFeature.CODEC);

    public static final BiomeFeature WILD_BANANA_CLUMPS = new BiomeFeature(
            TagKey.create(Registries.BIOME, FarmerPlus.id("has_banana_plants")),
            GenerationStep.Decoration.VEGETAL_DECORATION,
            ResourceKey.create(Registries.PLACED_FEATURE, FarmerPlus.id("wild_banana_clumps"))
    );

    private BananaWorldgen() {
    }
}
