package com.zyypj.farmerplus.core.module;

import java.util.List;
import net.minecraft.world.level.ItemLike;

public interface FarmerModule {

    String id();

    void register();

    List<ItemLike> creativeTabItems();
}
