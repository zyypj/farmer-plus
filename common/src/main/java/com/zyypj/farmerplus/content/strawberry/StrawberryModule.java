package com.zyypj.farmerplus.content.strawberry;

import com.zyypj.farmerplus.core.module.FarmerModule;
import com.zyypj.farmerplus.core.worldgen.BiomeFeatures;
import java.util.List;
import net.minecraft.world.level.ItemLike;

public final class StrawberryModule implements FarmerModule {

    @Override
    public String id() {
        return "strawberry";
    }

    @Override
    public void register() {
        StrawberryBlocks.bootstrap();
        StrawberryItems.bootstrap();
        BiomeFeatures.add(StrawberryWorldgen.WILD_STRAWBERRIES);
    }

    @Override
    public List<ItemLike> creativeTabItems() {
        return List.of(StrawberryItems.STRAWBERRY.get());
    }
}
