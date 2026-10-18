package com.zyypj.farmerplus.content.banana;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.util.random.WeightedList;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.levelgen.feature.Feature;

public final class BananaPlants {

    public static final ResourceKey<Feature> BANANA_PLANT = ResourceKey.create(Registries.FEATURE, FarmerPlus.id("banana_plant"));
    public static final TreeGrower GROWER = new TreeGrower(
            FarmerPlus.MOD_ID + "_banana",
            WeightedList.of(BANANA_PLANT),
            WeightedList.of(),
            WeightedList.of(),
            BANANA_PLANT
    );

    private BananaPlants() {
    }
}
