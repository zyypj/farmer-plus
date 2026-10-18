package com.zyypj.farmerplus.content.avocado;

import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import com.zyypj.farmerplus.core.wood.BranchBlock;
import com.zyypj.farmerplus.core.wood.Flammability;
import com.zyypj.farmerplus.core.wood.WoodSet;
import com.zyypj.farmerplus.core.wood.WoodSets;
import com.zyypj.farmerplus.core.worldgen.GrowingSaplingBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;

public final class AvocadoBlocks {

    private static final int SAPLING_GROWTH_CHANCE = 14;

    public static final WoodSet WOOD = WoodSets.register("avocado", MapColor.SAND, MapColor.COLOR_BROWN);

    public static final RegistryEntry<BranchBlock> AVOCADO_TRUNK = FarmerRegistries.block("avocado_trunk",
            properties -> new BranchBlock(10.0F, properties), () -> branchProperties(2.0F));

    public static final RegistryEntry<BranchBlock> AVOCADO_BRANCH = FarmerRegistries.block("avocado_branch",
            properties -> new BranchBlock(6.0F, properties), () -> branchProperties(1.0F));

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

    public static final RegistryEntry<AvocadoFruitBlock> AVOCADO_FRUIT = FarmerRegistries.block("avocado_fruit", AvocadoFruitBlock::new,
            () -> BlockBehaviour.Properties.of()
                    .mapColor(MapColor.PLANT)
                    .strength(0.2F)
                    .randomTicks()
                    .noCollision()
                    .noOcclusion()
                    .sound(SoundType.CROP)
                    .pushReaction(PushReaction.POPPED));

    public static final RegistryEntry<GrowingSaplingBlock> AVOCADO_SAPLING = FarmerRegistries.block("avocado_sapling",
            properties -> new GrowingSaplingBlock(AvocadoTrees.GROWER, SAPLING_GROWTH_CHANCE, properties),
            () -> BlockBehaviour.Properties.of()
                    .mapColor(MapColor.PLANT)
                    .noCollision()
                    .randomTicks()
                    .instabreak()
                    .sound(SoundType.GRASS)
                    .pushReaction(PushReaction.POPPED));

    private AvocadoBlocks() {
    }

    private static BlockBehaviour.Properties branchProperties(float strength) {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.COLOR_BROWN)
                .instrument(NoteBlockInstrument.BASS)
                .strength(strength)
                .sound(SoundType.WOOD)
                .noOcclusion()
                .ignitedByLava();
    }

    static void bootstrap() {
        Flammability.register(AVOCADO_TRUNK, 5, 5);
        Flammability.register(AVOCADO_BRANCH, 5, 5);
        Flammability.register(AVOCADO_LEAVES, 30, 60);
    }
}
