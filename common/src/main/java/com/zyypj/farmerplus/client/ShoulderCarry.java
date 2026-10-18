package com.zyypj.farmerplus.client;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import net.minecraft.core.registries.Registries;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

public final class ShoulderCarry {

    public static final TagKey<Item> CARRIED_ON_SHOULDER = TagKey.create(Registries.ITEM, FarmerPlus.id("carried_on_shoulder"));

    private static final float HOLDING_PITCH = -2.2F;

    private ShoulderCarry() {
    }

    public static void pose(HumanoidModel<?> model, HumanoidRenderState state) {
        if (carries(state.rightHandItemStack)) {
            raise(model.rightArm);
        } else if (carries(state.leftHandItemStack)) {
            raise(model.leftArm);
        }
    }

    private static boolean carries(ItemStack stack) {
        return !stack.isEmpty() && stack.is(CARRIED_ON_SHOULDER);
    }

    private static void raise(ModelPart arm) {
        arm.xRot = HOLDING_PITCH;
        arm.yRot = 0.0F;
        arm.zRot = 0.0F;
    }
}
