package com.zyypj.farmerplus.core.worldgen;

import net.minecraft.resources.ResourceKey;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.levelgen.placement.PlacedFeature;

public record BiomeFeature(TagKey<Biome> biomes, GenerationStep.Decoration step, ResourceKey<PlacedFeature> feature) {
}
