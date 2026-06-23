# Osaka 桌宠：下一阶段 Codex 从这里开始

1. 读取 `..\osaka.png`，它是 Osaka 身份的首要参考。
2. 读取 `WORKFLOW.md`、`prompts\generation.md` 和 `osaka_pet.animations.json`。
3. `reference\osaka_pet_master.png` 是生成后唯一有效的角色基准；所有状态必须保持相同脸型、黑棕直发、制服配色、比例和 2.5D 软胶风格。
4. 72 张帧必须位于 `frames\000.png` 至 `frames\071.png`，每张为 192×208 RGBA。
5. 修改关键姿势后先运行 `python tools\create_frames.py`，再运行 `python tools\build_atlas.py` 构建 1536×1872、8×9 的图集及状态预览。
6. 运行 `python tools\validate_assets.py` 和 `python -m unittest discover -s tests -v`。
7. 某状态不合格时只重做该状态的关键姿势和帧，不得整体重新生成。

完整规格以 `WORKFLOW.md` 和动画 JSON 为准。
