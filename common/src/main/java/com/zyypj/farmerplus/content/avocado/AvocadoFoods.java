package com.zyypj.farmerplus.content.avocado;

import net.minecraft.world.food.FoodProperties;

public final class AvocadoFoods {

    public static final FoodProperties AVOCADO = new FoodProperties.Builder()
            .nutrition(4)
            .saturationModifier(0.6F)
            .build();

    private AvocadoFoods() {
    }
}
