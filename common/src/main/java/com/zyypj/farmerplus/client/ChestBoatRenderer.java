package com.zyypj.farmerplus.client;

import com.mojang.blaze3d.vertex.PoseStack;
import java.util.Set;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.object.boat.BoatModel;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.BoatRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.state.BoatRenderState;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.Identifier;

public class ChestBoatRenderer extends BoatRenderer {

    private static final Identifier VANILLA_CHEST = Identifier.withDefaultNamespace("textures/entity/chest_boat/oak.png");
    private static final Set<String> CHEST_PARTS = Set.of("chest_bottom", "chest_lid", "chest_lock");

    private final BoatModel hull;
    private final BoatModel chest;

    public ChestBoatRenderer(EntityRendererProvider.Context context, ModelLayerLocation layer) {
        super(context, layer);
        this.hull = new BoatModel(context.bakeLayer(layer));
        this.chest = new BoatModel(context.bakeLayer(layer));
        ModelPart hullRoot = hull.root();
        ModelPart chestRoot = chest.root();
        chestRoot.getAllParts().forEach(part -> part.visible = false);
        chestRoot.visible = true;
        CHEST_PARTS.forEach(name -> {
            hullRoot.getChild(name).visible = false;
            chestRoot.getChild(name).visible = true;
        });
    }

    @Override
    protected EntityModel<BoatRenderState> model() {
        return hull;
    }

    @Override
    protected void submitTypeAdditions(BoatRenderState state, PoseStack poseStack, SubmitNodeCollector submitNodeCollector, int lightCoords) {
        super.submitTypeAdditions(state, poseStack, submitNodeCollector, lightCoords);
        submitNodeCollector.submitModel(chest, state, poseStack, VANILLA_CHEST, lightCoords, OverlayTexture.NO_OVERLAY, state.outlineColor);
    }
}
