package com.zyypj.farmerplus.mixin;

import com.zyypj.farmerplus.core.trampling.CropTrampling;
import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.FarmlandBlock;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(FarmlandBlock.class)
public abstract class FarmlandBlockMixin {

    @Inject(method = "turnToBaseBlock", at = @At("HEAD"), cancellable = true)
    private void farmerplus$cushionCrop(Entity sourceEntity, BlockState state, Level level, BlockPos pos, CallbackInfo callback) {
        if (sourceEntity != null && CropTrampling.cushionLanding(level, pos.above(), sourceEntity)) {
            callback.cancel();
        }
    }
}
