package com.zyypj.farmerplus.core.wood;

import com.zyypj.farmerplus.core.registry.RegistryEntry;
import com.zyypj.farmerplus.mixin.FireBlockAccessor;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;

public final class Flammability {

    private static final List<Entry> ENTRIES = new ArrayList<>();

    private Flammability() {
    }

    public static void register(RegistryEntry<? extends Block> block, int igniteOdds, int burnOdds) {
        ENTRIES.add(new Entry(block, igniteOdds, burnOdds));
    }

    public static void apply() {
        FireBlockAccessor fire = (FireBlockAccessor) Blocks.FIRE;
        ENTRIES.forEach(entry -> fire.farmerplus$setFlammable(entry.block().get(), entry.igniteOdds(), entry.burnOdds()));
    }

    private record Entry(RegistryEntry<? extends Block> block, int igniteOdds, int burnOdds) {
    }
}
