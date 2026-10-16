package com.zyypj.farmerplus.content.wheat;

import com.zyypj.farmerplus.core.module.FarmerModule;
import java.util.List;
import net.minecraft.world.level.ItemLike;

public final class WheatModule implements FarmerModule {

    @Override
    public String id() {
        return "wheat";
    }

    @Override
    public void register() {
        WheatBlocks.bootstrap();
        WheatItems.bootstrap();
    }

    @Override
    public List<ItemLike> creativeTabItems() {
        return List.of(
                WheatItems.FLOUR.get(),
                WheatItems.DOUGH.get(),
                WheatItems.WHEAT_PORRIDGE.get(),
                WheatItems.WHEAT_SHEAF.get()
        );
    }
}
