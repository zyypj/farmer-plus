package com.zyypj.farmerplus.content.avocado;

import com.zyypj.farmerplus.core.module.FarmerModule;
import com.zyypj.farmerplus.core.worldgen.BiomeFeatures;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.world.level.ItemLike;

public final class AvocadoModule implements FarmerModule {

    @Override
    public String id() {
        return "avocado";
    }

    @Override
    public void register() {
        AvocadoBlocks.bootstrap();
        AvocadoItems.bootstrap();
        BiomeFeatures.add(AvocadoWorldgen.WILD_AVOCADO_TREES);
    }

    @Override
    public List<ItemLike> creativeTabItems() {
        List<ItemLike> items = new ArrayList<>();
        items.add(AvocadoItems.AVOCADO.get());
        items.add(AvocadoItems.AVOCADO_SAPLING.get());
        items.add(AvocadoItems.AVOCADO_LEAVES.get());
        items.addAll(AvocadoBlocks.WOOD.creativeTabItems());
        return items;
    }
}
