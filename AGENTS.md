# Agent guide — Farmer+

Farmer+ is a vanilla-style farming mod for Minecraft 26.3 with one shared codebase for Fabric, NeoForge and Forge.

## Read first

- `docs/architecture.md` — code layout, modules, performance rules.
- `docs/art-pipeline.md` — texture and Blockbench rules. **Mandatory for any art task.**
- `docs/art-tasks/` — the current art backlog with exact file names.
- `docs/trampling.md` — crop trampling: trampled block states, generated models (`art/trampled_wheat.py`) and the single allowed mixin.

## Hard rules

- All assets and data live in `common/src/main/resources`. Never put assets in `fabric/`, `neoforge/` or `forge/`.
- Wheat overhaul textures and all existing wheat-related item/block textures are 32×32 PNG. Other content defaults to 16×16; the icon is excepted. Use realistic Vanilla+ pixel art, hard pixels and no anti-aliasing. Never copy or trace Mojang textures.
- Blockbench sources go in `art/blockbench/<id>.bbmodel`; exported models go in `assets/farmerplus/models/block/<id>.json` and must reference textures as `farmerplus:block/<name>`.
- Do not rename registry ids, item model files or texture files that already exist — code and data depend on them.
- Do not write code comments. Do not use fully-qualified class names inline.
- Every user-facing name exists in both `lang/en_us.json` and `lang/pt_br.json`.
- Documentation is bilingual: `<name>.md` (English) and `<name>.pt-BR.md` (Portuguese).

## Tools

- Blockbench MCP server: `http://localhost:3000/bb-mcp` (configured in `.codex/config.toml`). Blockbench must be open with the MCP plugin loaded.

## Verify

```bash
./gradlew build
./gradlew :neoforge:runClient
```

The log must show no `farmerplus` model or texture warnings.
