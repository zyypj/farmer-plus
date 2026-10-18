package com.zyypj.farmerplus.content.banana;

import java.util.Locale;
import net.minecraft.util.StringRepresentable;

public enum LeafAge implements StringRepresentable {
    YOUNG,
    MATURE,
    DRY;

    @Override
    public String getSerializedName() {
        return name().toLowerCase(Locale.ROOT);
    }
}
