package com.zyypj.farmerplus.core.trampling;

public final class Flattening {

    public static final int UPRIGHT = 0;
    public static final int BENT = 1;
    public static final int FLATTENED = 2;
    public static final int CRUSHED = 3;
    public static final int BENT_RECOVERY_CHANCE = 3;
    public static final int FLATTENED_RECOVERY_CHANCE = 6;

    private Flattening() {
    }

    public static int add(int current, int force) {
        return Math.min(CRUSHED, current + force);
    }
}
