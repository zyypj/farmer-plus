package com.zyypj.farmerplus.content.banana;

import net.minecraft.world.food.FoodProperties;

public final class BananaFoods {

    public static final FoodProperties BANANA = new FoodProperties.Builder()
            .nutrition(4)
            .saturationModifier(0.4F)
            .build();

    private BananaFoods() {
    }
}
