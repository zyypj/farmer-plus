package com.zyypj.farmerplus.content.banana;

import com.zyypj.farmerplus.core.registry.FarmerRegistries;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import com.zyypj.farmerplus.core.wood.Flammability;
import com.zyypj.farmerplus.core.worldgen.GrowingSaplingBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;

public final class BananaBlocks {

    private static final int SAPLING_GROWTH_CHANCE = 8;

    public static final RegistryEntry<BananaStemBlock> BANANA_STEM = FarmerRegistries.block("banana_stem", BananaStemBlock::new,
            () -> BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_LIGHT_GREEN)
                    .strength(0.8F)
                    .randomTicks()
                    .sound(SoundType.BAMBOO)
                    .noOcclusion()
                    .pushReaction(PushReaction.POPPED));

    public static final RegistryEntry<BananaLeafBlock> BANANA_LEAF = FarmerRegistries.block("banana_leaf", BananaLeafBlock::new,
            () -> BlockBehaviour.Properties.of()
                    .mapColor(MapColor.PLANT)
                    .strength(0.2F)
                    .noCollision()
                    .noOcclusion()
                    .sound(SoundType.BIG_DRIPLEAF)
                    .ignitedByLava()
                    .isSuffocating((state, level, pos) -> false)
                    .pushReaction(PushReaction.POPPED));

    public static final RegistryEntry<BananaBunchBlock> BANANA_BUNCH = FarmerRegistries.block("banana_bunch", BananaBunchBlock::new,
            () -> BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_YELLOW)
                    .strength(0.4F)
                    .randomTicks()
                    .noCollision()
                    .noOcclusion()
                    .sound(SoundType.CROP)
                    .pushReaction(PushReaction.POPPED));

    public static final RegistryEntry<HarvestedBananaBunchBlock> HARVESTED_BANANA_BUNCH = FarmerRegistries.block("harvested_banana_bunch",
            HarvestedBananaBunchBlock::new,
            () -> BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_YELLOW)
                    .strength(0.3F)
                    .noOcclusion()
                    .sound(SoundType.CROP)
                    .pushReaction(PushReaction.POPPED));

    public static final RegistryEntry<GrowingSaplingBlock> BANANA_SAPLING = FarmerRegistries.block("banana_sapling",
            properties -> new GrowingSaplingBlock(BananaPlants.GROWER, SAPLING_GROWTH_CHANCE, properties),
            () -> BlockBehaviour.Properties.of()
                    .mapColor(MapColor.PLANT)
                    .noCollision()
                    .randomTicks()
                    .instabreak()
                    .sound(SoundType.GRASS)
                    .pushReaction(PushReaction.POPPED));

    private BananaBlocks() {
    }

    static void bootstrap() {
        Flammability.register(BANANA_LEAF, 30, 60);
    }
}
