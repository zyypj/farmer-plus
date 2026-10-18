package com.zyypj.farmerplus.content.banana;

import java.util.Locale;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.StringRepresentable;
import net.minecraft.world.level.block.Rotation;

public enum LeafDirection implements StringRepresentable {
    NORTH(0, -1),
    NORTH_EAST(1, -1),
    EAST(1, 0),
    SOUTH_EAST(1, 1),
    SOUTH(0, 1),
    SOUTH_WEST(-1, 1),
    WEST(-1, 0),
    NORTH_WEST(-1, -1);

    public static final int CARDINAL_LENGTH = 3;
    public static final int DIAGONAL_LENGTH = 2;

    private final int dx;
    private final int dz;

    LeafDirection(int dx, int dz) {
        this.dx = dx;
        this.dz = dz;
    }

    public static LeafDirection fromYaw(float yaw) {
        int index = Math.floorMod(Math.round(yaw / 45.0F) + 4, 8);
        return values()[index];
    }

    public static LeafDirection of(Direction direction) {
        return switch (direction) {
            case EAST -> EAST;
            case SOUTH -> SOUTH;
            case WEST -> WEST;
            default -> NORTH;
        };
    }

    public boolean isDiagonal() {
        return dx != 0 && dz != 0;
    }

    public int length() {
        return isDiagonal() ? DIAGONAL_LENGTH : CARDINAL_LENGTH;
    }

    public int segmentAt(int step) {
        return isDiagonal() && step > 0 ? BananaLeafBlock.TIP : step;
    }

    public BlockPos offset(BlockPos pos, int steps) {
        return pos.offset(dx * steps, 0, dz * steps);
    }

    public LeafDirection rotate(Rotation rotation) {
        int quarterTurns = switch (rotation) {
            case NONE -> 0;
            case CLOCKWISE_90 -> 1;
            case CLOCKWISE_180 -> 2;
            case COUNTERCLOCKWISE_90 -> 3;
        };
        return values()[(ordinal() + quarterTurns * 2) % 8];
    }

    @Override
    public String getSerializedName() {
        return name().toLowerCase(Locale.ROOT);
    }
}
