package com.zyypj.farmerplus.content.strawberry;

import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.jam.JamJarBlock;
import com.zyypj.farmerplus.core.registry.RegistryEntry;

public final class StrawberryBlocks {

    public static final RegistryEntry<StrawberryPlantBlock> STRAWBERRY_PLANT = FarmerRegistries.block("strawberry_plant",
            StrawberryPlantBlock::new, StrawberryPlantBlock::plantProperties);

    public static final RegistryEntry<WildStrawberriesBlock> WILD_STRAWBERRIES = FarmerRegistries.block("wild_strawberries",
            WildStrawberriesBlock::new, StrawberryPlantBlock::plantProperties);

    public static final RegistryEntry<JamJarBlock> STRAWBERRY_JAM = FarmerRegistries.block("strawberry_jam",
            properties -> new JamJarBlock(() -> StrawberryItems.STRAWBERRY.get(), properties), JamJarBlock::jarProperties);

    private StrawberryBlocks() {
    }

    static void bootstrap() {
    }
}
