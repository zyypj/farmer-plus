package com.zyypj.farmerplus.core.trampling;

import com.zyypj.farmerplus.core.registry.RegistryEntry;
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.world.level.block.Block;

public final class TrampleableCrops {

    private static final List<RegistryEntry<? extends TrampledCropBlock>> ENTRIES = new ArrayList<>();
    private static Map<Block, TrampledCropBlock> byStandingCrop;

    private TrampleableCrops() {
    }

    public static void register(RegistryEntry<? extends TrampledCropBlock> trampledCrop) {
        ENTRIES.add(trampledCrop);
        byStandingCrop = null;
    }

    public static TrampledCropBlock trampledFormOf(Block standingCrop) {
        Map<Block, TrampledCropBlock> lookup = byStandingCrop;
        if (lookup == null) {
            lookup = buildLookup();
            byStandingCrop = lookup;
        }
        return lookup.get(standingCrop);
    }

    private static Map<Block, TrampledCropBlock> buildLookup() {
        Map<Block, TrampledCropBlock> lookup = new IdentityHashMap<>();
        for (RegistryEntry<? extends TrampledCropBlock> entry : ENTRIES) {
            TrampledCropBlock trampled = entry.get();
            lookup.put(trampled.standingCrop(), trampled);
        }
        return lookup;
    }
}
