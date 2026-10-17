package com.zyypj.farmerplus.content.avocado;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.worldgen.BiomeFeature;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.levelgen.GenerationStep;

public final class AvocadoWorldgen {

    public static final BiomeFeature WILD_AVOCADO_TREES = new BiomeFeature(
            TagKey.create(Registries.BIOME, FarmerPlus.id("has_avocado_trees")),
            GenerationStep.Decoration.VEGETAL_DECORATION,
            ResourceKey.create(Registries.PLACED_FEATURE, FarmerPlus.id("wild_avocado_trees"))
    );

    private AvocadoWorldgen() {
    }
}
