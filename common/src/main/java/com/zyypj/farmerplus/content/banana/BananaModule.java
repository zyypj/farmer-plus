package com.zyypj.farmerplus.content.banana;

import com.zyypj.farmerplus.core.module.FarmerModule;
import com.zyypj.farmerplus.core.worldgen.BiomeFeatures;
import java.util.List;
import net.minecraft.world.level.ItemLike;

public final class BananaModule implements FarmerModule {

    @Override
    public String id() {
        return "banana";
    }

    @Override
    public void register() {
        BananaBlocks.bootstrap();
        BananaItems.bootstrap();
        BiomeFeatures.add(BananaWorldgen.WILD_BANANA_CLUMPS);
    }

    @Override
    public List<ItemLike> creativeTabItems() {
        return List.of(BananaItems.BANANA.get(), BananaItems.BANANA_BUNCH.get(), BananaItems.BANANA_SAPLING.get(), BananaItems.BANANA_LEAF.get());
    }
}
