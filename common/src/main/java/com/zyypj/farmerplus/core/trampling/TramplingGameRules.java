package com.zyypj.farmerplus.core.trampling;

import com.mojang.brigadier.arguments.BoolArgumentType;
import com.mojang.serialization.Codec;
import com.zyypj.farmerplus.core.registry.RegistryEntry;
import com.zyypj.farmerplus.platform.Services;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.flag.FeatureFlagSet;
import net.minecraft.world.level.gamerules.GameRule;
import net.minecraft.world.level.gamerules.GameRuleCategory;
import net.minecraft.world.level.gamerules.GameRuleType;
import net.minecraft.world.level.gamerules.GameRuleTypeVisitor;

public final class TramplingGameRules {

    public static final RegistryEntry<GameRule<Boolean>> PLAYERS_TRAMPLE_CROPS = booleanRule("crop_trampling", GameRuleCategory.PLAYER, true);
    public static final RegistryEntry<GameRule<Boolean>> MOBS_TRAMPLE_CROPS = booleanRule("mob_crop_trampling", GameRuleCategory.MOBS, true);

    private TramplingGameRules() {
    }

    public static void bootstrap() {
    }

    private static RegistryEntry<GameRule<Boolean>> booleanRule(String name, GameRuleCategory category, boolean defaultValue) {
        return Services.REGISTRATION.register(Registries.GAME_RULE, name, key -> new GameRule<>(
                category,
                GameRuleType.BOOL,
                BoolArgumentType.bool(),
                GameRuleTypeVisitor::visitBoolean,
                Codec.BOOL,
                value -> value ? 1 : 0,
                defaultValue,
                FeatureFlagSet.of()
        ));
    }
}
