package com.zyypj.farmerplus.fabric;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import com.zyypj.farmerplus.platform.RegistrationPlatform;
import java.util.Collection;
import java.util.function.Function;
import java.util.function.Supplier;
import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;

public final class FabricRegistrationPlatform implements RegistrationPlatform {

    @Override
    public <R, T extends R> RegistryEntry<T> register(ResourceKey<? extends Registry<R>> registry, String name, Function<ResourceKey<R>, T> factory) {
        ResourceKey<R> key = ResourceKey.create(registry, FarmerPlus.id(name));
        T value = Registry.register(lookup(registry), key, factory.apply(key));
        return new RegistryEntry<>(key.identifier(), () -> value);
    }

    @Override
    public RegistryEntry<CreativeModeTab> registerCreativeTab(String name, Component title, Supplier<ItemStack> icon, Supplier<Collection<ItemStack>> contents) {
        return register(Registries.CREATIVE_MODE_TAB, name, key -> FabricCreativeModeTab.builder()
                .title(title)
                .icon(icon)
                .displayItems((parameters, output) -> output.acceptAll(contents.get()))
                .build());
    }

    @SuppressWarnings("unchecked")
    private static <R> Registry<R> lookup(ResourceKey<? extends Registry<R>> registry) {
        return (Registry<R>) BuiltInRegistries.REGISTRY.getValue(registry.identifier());
    }
}
