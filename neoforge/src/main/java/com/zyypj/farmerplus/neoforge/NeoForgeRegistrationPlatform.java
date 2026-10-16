package com.zyypj.farmerplus.neoforge;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import com.zyypj.farmerplus.platform.RegistrationPlatform;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Function;
import java.util.function.Supplier;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class NeoForgeRegistrationPlatform implements RegistrationPlatform {

    private static final Map<ResourceKey<?>, DeferredRegister<?>> REGISTERS = new LinkedHashMap<>();

    static void bind(IEventBus modBus) {
        REGISTERS.values().forEach(register -> register.register(modBus));
    }

    @Override
    public <R, T extends R> RegistryEntry<T> register(ResourceKey<? extends Registry<R>> registry, String name, Function<ResourceKey<R>, T> factory) {
        DeferredHolder<R, T> holder = deferredRegister(registry).register(name, id -> factory.apply(ResourceKey.create(registry, id)));
        return new RegistryEntry<>(holder.getId(), holder);
    }

    @Override
    public RegistryEntry<CreativeModeTab> registerCreativeTab(String name, Component title, Supplier<ItemStack> icon, Supplier<Collection<ItemStack>> contents) {
        return register(Registries.CREATIVE_MODE_TAB, name, key -> CreativeModeTab.builder()
                .title(title)
                .icon(icon)
                .displayItems((parameters, output) -> output.acceptAll(contents.get()))
                .build());
    }

    @SuppressWarnings("unchecked")
    private static <R> DeferredRegister<R> deferredRegister(ResourceKey<? extends Registry<R>> registry) {
        return (DeferredRegister<R>) REGISTERS.computeIfAbsent(registry, key -> DeferredRegister.create(registry, FarmerPlus.MOD_ID));
    }
}
