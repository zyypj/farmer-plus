package com.zyypj.farmerplus.content.strawberry;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.worldgen.BiomeFeature;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.levelgen.GenerationStep;

public final class StrawberryWorldgen {

    public static final BiomeFeature WILD_STRAWBERRIES = new BiomeFeature(
            TagKey.create(Registries.BIOME, FarmerPlus.id("has_wild_strawberries")),
            GenerationStep.Decoration.VEGETAL_DECORATION,
            ResourceKey.create(Registries.PLACED_FEATURE, FarmerPlus.id("patch_wild_strawberries"))
    );

    private StrawberryWorldgen() {
    }
}
