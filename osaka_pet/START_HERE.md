# Osaka Codex 桌宠：九行动画工作流

1. `..\osaka.png` 是身份首要参考，`reference\osaka_pet_master.png` 是资产流水线的角色基准。
2. 阅读 `WORKFLOW.md`、`prompts\generation.md` 和 `osaka_pet.animations.json`。
3. 运行图集固定为 8 列×9 行、每格 192×208；每一行只对应一个 Codex 状态。
4. 源帧位于 `frames\000.png` 至 `frames\071.png`。未使用单元格必须为全透明 RGBA。
5. 修改关键姿势后依次运行：

```powershell
python tools\create_frames.py
python tools\build_atlas.py
python tools\validate_assets.py
python -m unittest discover -s tests -v
```

6. `build_atlas.py` 同时更新 PNG 图集、九个状态预览、contact sheet 和 `package\spritesheet.webp`。
7. 只修改失败状态的关键姿势和对应行，不整体重做已通过的角色素材。

