package com.zyypj.farmerplus.content.strawberry;

import com.zyypj.farmerplus.FarmerPlus;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.BonemealSource;
import net.minecraft.world.level.block.BonemealableBlock;
import net.minecraft.world.level.block.FarmlandBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.VegetationBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

public class StrawberryPlantBlock extends VegetationBlock implements BonemealableBlock {

    public static final int FLOWERING_AGE = 2;
    public static final int RIPE_AGE = BlockStateProperties.MAX_AGE_4;
    public static final IntegerProperty AGE = BlockStateProperties.AGE_4;

    private static final ResourceKey<LootTable> HARVEST_LOOT = ResourceKey.create(Registries.LOOT_TABLE, FarmerPlus.id("harvest/strawberry_plant"));
    private static final int MIN_GROWTH_BRIGHTNESS = 9;
    private static final int HYDRATED_GROWTH_CHANCE = 5;
    private static final int DRY_GROWTH_CHANCE = 8;
    private static final int RUNNER_CHANCE = 20;
    private static final VoxelShape[] SHAPES = {
            Block.column(5.5, -1.0, 1.0),
            Block.column(10.0, -1.0, 2.25),
            Block.column(13.0, -1.0, 5.75),
            Block.column(19.0, -1.0, 6.25),
            Block.column(19.5, -1.0, 5.75)
    };

    public StrawberryPlantBlock(BlockBehaviour.Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(AGE, 0));
    }

    public static BlockBehaviour.Properties plantProperties() {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.PLANT)
                .randomTicks()
                .noCollision()
                .instabreak()
                .sound(SoundType.SWEET_BERRY_BUSH)
                .pushReaction(PushReaction.POPPED);
    }

    public static boolean isRipe(BlockState state) {
        return state.getValue(AGE) == RIPE_AGE;
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
        return state.is(BlockTags.SUPPORTS_CROPS);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPES[state.getValue(AGE)];
    }

    @Override
    protected ItemStack getCloneItemStack(LevelReader level, BlockPos pos, BlockState state, boolean includeData) {
        return new ItemStack(StrawberryItems.STRAWBERRY.get());
    }

    @Override
    protected boolean isRandomlyTicking(BlockState state) {
        return !isRipe(state);
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (isRipe(state) || level.getRawBrightness(pos.above(), 0) < MIN_GROWTH_BRIGHTNESS) {
            return;
        }

        if (random.nextInt(growthChance(level, pos)) == 0) {
            setAge(level, pos, state, state.getValue(AGE) + 1);
        } else if (spreadsRunners() && state.getValue(AGE) >= FLOWERING_AGE && random.nextInt(RUNNER_CHANCE) == 0) {
            spreadRunner(level, pos, random);
        }
    }

    @Override
    protected InteractionResult useItemOn(ItemStack itemStack, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hitResult) {
        if (!isRipe(state) && itemStack.is(Items.BONE_MEAL)) {
            return InteractionResult.PASS;
        }
        return super.useItemOn(itemStack, state, level, pos, player, hand, hitResult);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hitResult) {
        if (!isRipe(state)) {
            return super.useWithoutItem(state, level, pos, player, hitResult);
        }

        if (level instanceof ServerLevel serverLevel) {
            Block.dropFromBlockInteractLootTable(serverLevel, harvestLootTable(), pos, state, null, null, player,
                    (dropLevel, stack) -> Block.popResource(dropLevel, pos, stack));
            float pitch = 0.8F + serverLevel.getRandom().nextFloat() * 0.4F;
            serverLevel.playSound(null, pos, SoundEvents.SWEET_BERRY_BUSH_PICK_BERRIES, SoundSource.BLOCKS, 1.0F, pitch);
            BlockState flowering = state.setValue(AGE, FLOWERING_AGE);
            serverLevel.setBlock(pos, flowering, Block.UPDATE_CLIENTS);
            serverLevel.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(player, flowering));
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    public boolean isValidBonemealTarget(LevelReader level, BlockPos pos, BlockState state, BonemealSource source) {
        return !isRipe(state);
    }

    @Override
    public boolean isBonemealSuccess(Level level, RandomSource random, BlockPos pos, BlockState state, BonemealSource source) {
        return true;
    }

    @Override
    public void performBonemeal(ServerLevel level, RandomSource random, BlockPos pos, BlockState state, BonemealSource source) {
        setAge(level, pos, state, Math.min(RIPE_AGE, state.getValue(AGE) + 1));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(AGE);
    }

    protected int growthChance(ServerLevel level, BlockPos pos) {
        boolean hydrated = level.getBlockState(pos.below()).getValueOrElse(FarmlandBlock.MOISTURE, 0) > 0;
        return hydrated ? HYDRATED_GROWTH_CHANCE : DRY_GROWTH_CHANCE;
    }

    protected boolean spreadsRunners() {
        return true;
    }

    protected ResourceKey<LootTable> harvestLootTable() {
        return HARVEST_LOOT;
    }

    private void spreadRunner(ServerLevel level, BlockPos pos, RandomSource random) {
        Direction direction = Direction.Plane.HORIZONTAL.getRandomDirection(random);
        BlockPos target = pos.relative(direction);
        BlockState seedling = defaultBlockState();
        if (level.isEmptyBlock(target) && seedling.canSurvive(level, target)) {
            level.setBlock(target, seedling, Block.UPDATE_ALL);
            level.gameEvent(GameEvent.BLOCK_PLACE, target, GameEvent.Context.of(seedling));
        }
    }

    private static void setAge(ServerLevel level, BlockPos pos, BlockState state, int age) {
        BlockState grown = state.setValue(AGE, age);
        level.setBlock(pos, grown, Block.UPDATE_CLIENTS);
        level.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(grown));
    }
}
