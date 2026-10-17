package com.zyypj.farmerplus.content.avocado;

import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import com.zyypj.farmerplus.core.wood.Flammability;
import com.zyypj.farmerplus.core.wood.WoodSet;
import com.zyypj.farmerplus.core.wood.WoodSets;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;

public final class AvocadoBlocks {

    public static final WoodSet WOOD = WoodSets.register("avocado", MapColor.SAND, MapColor.COLOR_BROWN);

    public static final RegistryEntry<AvocadoLeavesBlock> AVOCADO_LEAVES = FarmerRegistries.block("avocado_leaves", AvocadoLeavesBlock::new,
            () -> BlockBehaviour.Properties.of()
                    .mapColor(MapColor.PLANT)
                    .strength(0.2F)
                    .randomTicks()
                    .sound(SoundType.GRASS)
                    .noOcclusion()
                    .isValidSpawn((state, level, pos, type) -> false)
                    .isSuffocating((state, level, pos) -> false)
                    .ignitedByLava()
                    .pushReaction(PushReaction.POPPED));

    public static final RegistryEntry<AvocadoSaplingBlock> AVOCADO_SAPLING = FarmerRegistries.block("avocado_sapling",
            properties -> new AvocadoSaplingBlock(AvocadoTrees.GROWER, properties),
            () -> BlockBehaviour.Properties.of()
                    .mapColor(MapColor.PLANT)
                    .noCollision()
                    .randomTicks()
                    .instabreak()
                    .sound(SoundType.GRASS)
                    .pushReaction(PushReaction.POPPED));

    private AvocadoBlocks() {
    }

    static void bootstrap() {
        Flammability.register(AVOCADO_LEAVES, 30, 60);
    }
}
