package com.zyypj.farmerplus.core.registry;

import java.util.function.Supplier;
import net.minecraft.resources.Identifier;

public record RegistryEntry<T>(Identifier id, Supplier<T> value) implements Supplier<T> {

    @Override
    public T get() {
        return value.get();
    }
}
