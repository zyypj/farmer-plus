package com.zyypj.farmerplus.core.trampling;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.BonemealSource;
import net.minecraft.world.level.block.CropBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

public class TrampledCropBlock extends CropBlock {

    public static final int BENT = 1;
    public static final int FLATTENED = 2;
    public static final int CRUSHED = 3;
    public static final IntegerProperty FLATTENING = IntegerProperty.create("flattening", BENT, CRUSHED);
    public static final EnumProperty<Direction> FACING = BlockStateProperties.HORIZONTAL_FACING;

    private static final int BENT_RECOVERY_CHANCE = 3;
    private static final int FLATTENED_RECOVERY_CHANCE = 6;
    private static final int MIN_GROWTH_BRIGHTNESS = 9;
    private static final int MATURE_COLOR_AGE = 6;
    private static final VoxelShape[] SHAPES = {
            Block.column(16.0, 0.0, 8.0),
            Block.column(16.0, 0.0, 4.0),
            Block.column(16.0, 0.0, 2.0)
    };

    private final Supplier<? extends CropBlock> standingCrop;

    public TrampledCropBlock(Supplier<? extends CropBlock> standingCrop, BlockBehaviour.Properties properties) {
        super(properties);
        this.standingCrop = standingCrop;
        registerDefaultState(stateDefinition.any()
                .setValue(AGE, 0)
                .setValue(FLATTENING, BENT)
                .setValue(FACING, Direction.NORTH));
    }

    public static BlockBehaviour.Properties cropProperties() {
        return BlockBehaviour.Properties.of()
                .mapColor(state -> state.getValue(AGE) >= MATURE_COLOR_AGE ? MapColor.COLOR_YELLOW : MapColor.PLANT)
                .noCollision()
                .randomTicks()
                .instabreak()
                .sound(SoundType.CROP)
                .pushReaction(PushReaction.POPPED);
    }

    public static int flattening(BlockState state) {
        return state.getValue(FLATTENING);
    }

    public CropBlock standingCrop() {
        return standingCrop.get();
    }

    public BlockState trampledState(int age, int flattening, Direction facing) {
        return defaultBlockState()
                .setValue(AGE, age)
                .setValue(FLATTENING, flattening)
                .setValue(FACING, facing);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPES[flattening(state) - BENT];
    }

    @Override
    protected boolean isRandomlyTicking(BlockState state) {
        int flattening = flattening(state);
        return flattening == BENT || (flattening == FLATTENED && !isMaxAge(state));
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (level.getRawBrightness(pos, 0) < MIN_GROWTH_BRIGHTNESS) {
            return;
        }

        int flattening = flattening(state);
        if (flattening == BENT && random.nextInt(BENT_RECOVERY_CHANCE) == 0) {
            standUp(state, level, pos);
        } else if (flattening == FLATTENED && random.nextInt(FLATTENED_RECOVERY_CHANCE) == 0) {
            level.setBlock(pos, state.setValue(FLATTENING, BENT), Block.UPDATE_CLIENTS);
        }
    }

    @Override
    public void growCrops(Level level, BlockPos pos, BlockState state) {
        int age = Math.min(getMaxAge(), getAge(state) + getBonemealAgeIncrease(level));
        level.setBlock(pos, state.setValue(AGE, age), Block.UPDATE_CLIENTS);
    }

    @Override
    public boolean isValidBonemealTarget(LevelReader level, BlockPos pos, BlockState state, BonemealSource source) {
        return flattening(state) == BENT && !isMaxAge(state);
    }

    @Override
    protected ItemLike getBaseSeedId() {
        return standingCrop();
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        super.createBlockStateDefinition(builder);
        builder.add(FLATTENING, FACING);
    }

    private void standUp(BlockState state, ServerLevel level, BlockPos pos) {
        level.setBlock(pos, standingCrop().getStateForAge(getAge(state)), Block.UPDATE_CLIENTS);
    }
}
