package com.zyypj.farmerplus.core.worldgen;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class BiomeFeatures {

    private static final List<BiomeFeature> FEATURES = new ArrayList<>();

    private BiomeFeatures() {
    }

    public static void add(BiomeFeature feature) {
        FEATURES.add(feature);
    }

    public static List<BiomeFeature> all() {
        return Collections.unmodifiableList(FEATURES);
    }
}
