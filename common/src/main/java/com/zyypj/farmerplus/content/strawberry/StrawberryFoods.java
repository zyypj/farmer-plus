package com.zyypj.farmerplus.content.strawberry;

import net.minecraft.world.food.FoodProperties;

public final class StrawberryFoods {

    public static final FoodProperties STRAWBERRY = new FoodProperties.Builder()
            .nutrition(2)
            .saturationModifier(0.3F)
            .build();

    private StrawberryFoods() {
    }
}
