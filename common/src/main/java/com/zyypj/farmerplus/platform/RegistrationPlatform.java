package com.zyypj.farmerplus.platform;

import com.zyypj.farmerplus.core.registry.RegistryEntry;
import java.util.Collection;
import java.util.function.Function;
import java.util.function.Supplier;
import net.minecraft.core.Registry;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;

public interface RegistrationPlatform {

    <R, T extends R> RegistryEntry<T> register(ResourceKey<? extends Registry<R>> registry, String name, Function<ResourceKey<R>, T> factory);

    RegistryEntry<CreativeModeTab> registerCreativeTab(String name, Component title, Supplier<ItemStack> icon, Supplier<Collection<ItemStack>> contents);
}
