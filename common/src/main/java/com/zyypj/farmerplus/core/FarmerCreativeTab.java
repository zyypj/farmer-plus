package com.zyypj.farmerplus.core;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.module.FarmerModule;
import com.zyypj.farmerplus.core.module.FarmerModules;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import com.zyypj.farmerplus.platform.Services;
import java.util.Collection;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.ItemLike;

public final class FarmerCreativeTab {

    private static RegistryEntry<CreativeModeTab> tab;

    private FarmerCreativeTab() {
    }

    public static void register() {
        tab = Services.REGISTRATION.registerCreativeTab(
                "main",
                Component.translatable("itemGroup." + FarmerPlus.MOD_ID),
                () -> new ItemStack(Items.WHEAT),
                FarmerCreativeTab::contents
        );
    }

    public static RegistryEntry<CreativeModeTab> tab() {
        return tab;
    }

    private static Collection<ItemStack> contents() {
        return FarmerModules.all().stream()
                .map(FarmerModule::creativeTabItems)
                .flatMap(Collection::stream)
                .map(ItemLike::asItem)
                .map(ItemStack::new)
                .toList();
    }
}
