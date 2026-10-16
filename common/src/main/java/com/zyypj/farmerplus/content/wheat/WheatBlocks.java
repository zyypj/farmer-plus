package com.zyypj.farmerplus.content.wheat;

import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;
import net.minecraft.world.level.material.MapColor;

public final class WheatBlocks {

    public static final RegistryEntry<WheatSheafBlock> WHEAT_SHEAF = FarmerRegistries.block("wheat_sheaf", WheatSheafBlock::new,
            () -> BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_YELLOW)
                    .instrument(NoteBlockInstrument.BANJO)
                    .strength(0.5F)
                    .sound(SoundType.GRASS)
                    .noOcclusion()
                    .ignitedByLava());

    private WheatBlocks() {
    }

    static void bootstrap() {
    }
}
