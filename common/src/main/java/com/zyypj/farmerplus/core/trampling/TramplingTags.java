package com.zyypj.farmerplus.core.trampling;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraft.core.registries.Registries;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.EntityType;

public final class TramplingTags {

    public static final TagKey<EntityType<?>> TRAMPLES_CROPS = TagKey.create(Registries.ENTITY_TYPE, FarmerPlus.id("tramples_crops"));

    private TramplingTags() {
    }
}
