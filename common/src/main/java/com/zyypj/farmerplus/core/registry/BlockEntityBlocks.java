package com.zyypj.farmerplus.core.registry;

import java.util.ArrayList;
import java.util.List;
import java.util.function.BiConsumer;
import java.util.function.Supplier;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntityType;

public final class BlockEntityBlocks {

    private static final List<Entry> ENTRIES = new ArrayList<>();

    private BlockEntityBlocks() {
    }

    @SafeVarargs
    public static void add(Supplier<BlockEntityType<?>> type, RegistryEntry<? extends Block>... blocks) {
        ENTRIES.add(new Entry(type, List.of(blocks)));
    }

    public static void forEach(BiConsumer<BlockEntityType<?>, List<Block>> consumer) {
        ENTRIES.forEach(entry -> consumer.accept(entry.type().get(), entry.blocks().stream().<Block>map(RegistryEntry::get).toList()));
    }

    private record Entry(Supplier<BlockEntityType<?>> type, List<RegistryEntry<? extends Block>> blocks) {
    }
}
