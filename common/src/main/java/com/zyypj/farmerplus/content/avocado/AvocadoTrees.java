package com.zyypj.farmerplus.content.avocado;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.util.random.WeightedList;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.levelgen.feature.Feature;

public final class AvocadoTrees {

    public static final ResourceKey<Feature> AVOCADO_TREE = ResourceKey.create(Registries.FEATURE, FarmerPlus.id("avocado_tree"));

    public static final TreeGrower GROWER = new TreeGrower(
            FarmerPlus.MOD_ID + "_avocado",
            WeightedList.of(AVOCADO_TREE),
            WeightedList.of(),
            WeightedList.of(),
            AVOCADO_TREE
    );

    private AvocadoTrees() {
    }
}
