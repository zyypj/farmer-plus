package com.zyypj.farmerplus.forge;

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
import net.minecraftforge.eventbus.api.bus.BusGroup;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

public final class ForgeRegistrationPlatform implements RegistrationPlatform {

    private static final Map<ResourceKey<?>, DeferredRegister<?>> REGISTERS = new LinkedHashMap<>();

    static void bind(BusGroup modBusGroup) {
        REGISTERS.values().forEach(register -> register.register(modBusGroup));
    }

    @Override
    public <R, T extends R> RegistryEntry<T> register(ResourceKey<? extends Registry<R>> registry, String name, Function<ResourceKey<R>, T> factory) {
        ResourceKey<R> key = ResourceKey.create(registry, FarmerPlus.id(name));
        RegistryObject<T> object = deferredRegister(registry).register(name, () -> factory.apply(key));
        return new RegistryEntry<>(key.identifier(), object);
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
