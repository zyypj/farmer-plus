package com.zyypj.farmerplus.neoforge;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.registry.BlockEntityBlocks;
import net.minecraft.world.level.block.Block;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.event.BlockEntityTypeAddBlocksEvent;

@Mod(FarmerPlus.MOD_ID)
public final class FarmerPlusNeoForge {

    public FarmerPlusNeoForge(IEventBus modBus) {
        FarmerPlus.init();
        NeoForgeRegistrationPlatform.bind(modBus);
        modBus.addListener(FMLCommonSetupEvent.class, event -> event.enqueueWork(FarmerPlus::commonSetup));
        modBus.addListener(BlockEntityTypeAddBlocksEvent.class, event ->
                BlockEntityBlocks.forEach((type, blocks) -> event.modify(type, blocks.toArray(Block[]::new))));
    }
}
