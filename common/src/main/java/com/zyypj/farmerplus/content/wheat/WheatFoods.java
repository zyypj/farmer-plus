package com.zyypj.farmerplus.content.wheat;

import net.minecraft.world.food.FoodProperties;

public final class WheatFoods {

    public static final FoodProperties WHEAT_PORRIDGE = new FoodProperties.Builder()
            .nutrition(7)
            .saturationModifier(0.6F)
            .build();

    private WheatFoods() {
    }
}
