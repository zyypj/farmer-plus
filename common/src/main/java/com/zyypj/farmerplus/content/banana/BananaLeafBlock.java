package com.zyypj.farmerplus.content.banana;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.pathfinder.PathComputationType;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

public class BananaLeafBlock extends Block {

    public static final int BASE = 0;
    public static final int BLADE = 1;
    public static final int TIP = 2;
    public static final EnumProperty<LeafDirection> DIRECTION = EnumProperty.create("direction", LeafDirection.class);
    public static final IntegerProperty SEGMENT = IntegerProperty.create("segment", BASE, TIP);
    public static final EnumProperty<LeafAge> AGE = EnumProperty.create("age", LeafAge.class);

    private static final String SHAPES_RESOURCE = "/farmerplus/shapes/banana_leaf.json";
    private static final VoxelShape[] SHAPES = loadShapes();

    public BananaLeafBlock(BlockBehaviour.Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(DIRECTION, LeafDirection.NORTH).setValue(SEGMENT, BASE).setValue(AGE, LeafAge.MATURE));
    }

    public static boolean isSegment(BlockState state, LeafDirection direction, int segment) {
        return state.getBlock() instanceof BananaLeafBlock && state.getValue(DIRECTION) == direction && state.getValue(SEGMENT) == segment;
    }

    public static BlockState of(LeafDirection direction, int step, LeafAge age) {
        return BananaBlocks.BANANA_LEAF.get().defaultBlockState()
                .setValue(DIRECTION, direction)
                .setValue(SEGMENT, direction.segmentAt(step))
                .setValue(AGE, age);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPES[shapeIndex(state.getValue(AGE), state.getValue(DIRECTION), state.getValue(SEGMENT))];
    }

    private static int shapeIndex(LeafAge age, LeafDirection direction, int segment) {
        return (age.ordinal() * LeafDirection.values().length + direction.ordinal()) * (TIP + 1) + segment;
    }

    private static VoxelShape[] loadShapes() {
        try (InputStream stream = BananaLeafBlock.class.getResourceAsStream(SHAPES_RESOURCE)) {
            if (stream == null) {
                throw new IllegalStateException("Missing " + SHAPES_RESOURCE);
            }
            JsonObject json = JsonParser.parseReader(new InputStreamReader(stream, StandardCharsets.UTF_8)).getAsJsonObject();
            JsonArray boxes = json.getAsJsonArray("shapes");
            VoxelShape[] unique = new VoxelShape[boxes.size()];
            for (int i = 0; i < unique.length; i++) {
                VoxelShape shape = Shapes.empty();
                for (JsonElement element : boxes.get(i).getAsJsonArray()) {
                    JsonArray box = element.getAsJsonArray();
                    shape = Shapes.or(shape, Block.box(box.get(0).getAsDouble(), box.get(1).getAsDouble(), box.get(2).getAsDouble(),
                            box.get(3).getAsDouble(), box.get(4).getAsDouble(), box.get(5).getAsDouble()));
                }
                unique[i] = shape.optimize();
            }
            JsonArray states = json.getAsJsonArray("states");
            VoxelShape[] shapes = new VoxelShape[states.size()];
            for (int i = 0; i < shapes.length; i++) {
                shapes[i] = unique[states.get(i).getAsInt()];
            }
            return shapes;
        } catch (IOException exception) {
            throw new UncheckedIOException(exception);
        }
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        LeafDirection direction = LeafDirection.fromYaw(context.getRotation());
        BlockState behind = context.getLevel().getBlockState(direction.offset(context.getClickedPos(), -1));
        int step = 0;
        if (behind.getBlock() instanceof BananaLeafBlock && behind.getValue(DIRECTION) == direction) {
            step = Math.min(behind.getValue(SEGMENT) + 1, direction.length() - 1);
        }
        return of(direction, step, LeafAge.MATURE);
    }

    @Override
    protected void affectNeighborsAfterRemoval(BlockState state, ServerLevel level, BlockPos pos, boolean movedByPiston) {
        LeafDirection direction = state.getValue(DIRECTION);
        BlockPos next = direction.offset(pos, 1);
        BlockState outer = level.getBlockState(next);
        if (outer.getBlock() instanceof BananaLeafBlock && outer.getValue(DIRECTION) == direction && outer.getValue(SEGMENT) > state.getValue(SEGMENT)) {
            level.destroyBlock(next, true);
        }
    }

    @Override
    protected BlockState rotate(BlockState state, Rotation rotation) {
        return state.setValue(DIRECTION, state.getValue(DIRECTION).rotate(rotation));
    }

    @Override
    protected boolean propagatesSkylightDown(BlockState state) {
        return true;
    }

    @Override
    protected boolean isPathfindable(BlockState state, PathComputationType type) {
        return type == PathComputationType.AIR;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(DIRECTION, SEGMENT, AGE);
    }
}
