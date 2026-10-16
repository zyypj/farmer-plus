# Art pipeline

**English** | [Português](art-pipeline.pt-BR.md)

Farmer+ art must be indistinguishable from vanilla. If a player cannot tell which items came from the mod, the art is right.

## Style rules

- **16×16 pixels** for every item and block texture. No HD, no 32×32.
- **PNG, RGBA, 8-bit.** Transparent background for items. No semi-transparent pixels except glass-like materials.
- **No anti-aliasing, no gradients, no blur.** Hard pixel edges only.
- **Limited palette.** 4–7 shades per material, sampled from (not copied from) vanilla materials of the same kind (wheat, bread, bowls, hay).
- **Top-left lighting**, like vanilla: highlights on the top-left, darkest shade on the bottom-right.
- **Item silhouettes** have a 1-pixel darker outline on the shaded side, matching vanilla food items.
- **Never copy or trace Mojang textures.** Use them only as visual reference.

## Folders

| What | Where | Shipped in jar |
|---|---|---|
| Item textures | `common/src/main/resources/assets/farmerplus/textures/item/<id>.png` | yes |
| Block textures | `common/src/main/resources/assets/farmerplus/textures/block/<id>[_part].png` | yes |
| Block models (exported) | `common/src/main/resources/assets/farmerplus/models/block/<id>.json` | yes |
| Mod icon | `common/src/main/resources/assets/farmerplus/icon.png` (square, 128×128 or 512×512) | yes |
| Blockbench projects | `art/blockbench/<id>.bbmodel` | no |
| Layered/working files | `art/textures/…` | no |

## Blockbench workflow

1. Create the project as **Java Block/Item**.
2. Keep the model inside the 0–16 block grid when possible (vanilla max is −16…32).
3. Element rotations: only on one axis and only −45, −22.5, 0, 22.5 or 45 degrees.
4. Keep it cheap: **at most 12 elements** per block model. Fewer is better.
5. Name textures exactly as the final resource id (e.g. `wheat_sheaf_side`), and set the texture namespace to `farmerplus` so the exported JSON points at `farmerplus:block/<name>`.
6. Set **Display** transforms for `gui`, `ground`, `fixed`, `thirdperson_righthand` and `firstperson_righthand` so the item looks right in inventories and hands.
7. Save the source as `art/blockbench/<id>.bbmodel`.
8. Export **Block/Item Model** to `models/block/<id>.json` and the textures to `textures/block/`.
9. If the silhouette of a block changes, update the `VoxelShape` in its block class so the outline and collision match.

## Connecting Blockbench to an AI agent (MCP)

The repository ships `.codex/config.toml`, which points Codex at the Blockbench MCP server.

1. Install Blockbench (desktop): <https://www.blockbench.net/downloads>
2. In Blockbench: **File → Plugins → Load Plugin from URL** and paste
   `https://jasonjgardner.github.io/blockbench-mcp-plugin/mcp.js`
3. Keep Blockbench open. The server listens on `http://localhost:3000/bb-mcp`.
4. Codex picks up `.codex/config.toml` for trusted projects. To add it globally instead:
   ```bash
   codex mcp add blockbench --url http://localhost:3000/bb-mcp
   ```
5. Restart Codex and run `/mcp` to confirm `blockbench` is connected.

The plugin can run JavaScript inside Blockbench (`risky_eval`). Leave the server bound to `localhost`.

## Checking your work

```bash
./gradlew :neoforge:runClient
```

Open the **Farmer+** creative tab and check every item in the inventory, in hand, dropped on the ground and placed (for blocks). The log must contain no `farmerplus` texture or model warnings.
