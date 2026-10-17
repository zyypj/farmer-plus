package com.zyypj.farmerplus.client;

import com.zyypj.farmerplus.FarmerPlus;
import com.zyypj.farmerplus.core.wood.WoodSets;
import java.util.function.Supplier;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.object.boat.BoatModel;
import net.minecraft.client.renderer.entity.BoatRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.vehicle.boat.AbstractBoat;

public final class BoatRendering {

    private static final String LAYER = "main";

    private BoatRendering() {
    }

    public static void registerLayerDefinitions(LayerDefinitionRegistrar registrar) {
        WoodSets.all().forEach(set -> {
            registrar.register(boatLayer(set.name()), BoatModel::createBoatModel);
            registrar.register(chestBoatLayer(set.name()), BoatModel::createChestBoatModel);
        });
    }

    public static void registerRenderers(RendererRegistrar registrar) {
        WoodSets.all().forEach(set -> {
            ModelLayerLocation boat = boatLayer(set.name());
            ModelLayerLocation chestBoat = chestBoatLayer(set.name());
            registrar.register(set.boat().get(), context -> new BoatRenderer(context, boat));
            registrar.register(set.chestBoat().get(), context -> new BoatRenderer(context, chestBoat));
        });
    }

    private static ModelLayerLocation boatLayer(String wood) {
        return new ModelLayerLocation(FarmerPlus.id("boat/" + wood), LAYER);
    }

    private static ModelLayerLocation chestBoatLayer(String wood) {
        return new ModelLayerLocation(FarmerPlus.id("chest_boat/" + wood), LAYER);
    }

    @FunctionalInterface
    public interface LayerDefinitionRegistrar {

        void register(ModelLayerLocation layer, Supplier<LayerDefinition> definition);
    }

    @FunctionalInterface
    public interface RendererRegistrar {

        void register(EntityType<? extends AbstractBoat> type, EntityRendererProvider<AbstractBoat> provider);
    }
}
