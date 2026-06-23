# Osaka Codex 九行动画验证报告

## 自动验证

- 图集：1536×1872 RGBA，8×9，每格 192×208。
- 状态顺序：`idle`、`running-right`、`running-left`、`waving`、`jumping`、`failed`、`waiting`、`running`、`review`。
- 使用帧数：`6, 8, 8, 4, 5, 8, 6, 6, 6`；15 个未使用尾格全透明。
- 每个状态严格限制在自己的行内，没有跨行引用。
- PNG 图集切片与 `frames\000.png`–`071.png` 逐像素一致。
- `package\spritesheet.webp` 为 1536×1872、RGBA、lossless WebP。
- 透明四角、安全边距、alpha 覆盖率、绿色残边和透明像素检查通过。
- 九个状态预览与带标签的 `contact-sheet.png` 已生成。

## 人工检查

- 新的左右拖动姿势具有相反方向的头发与肢体滞后，不是同一行混帧。
- `jumping` 包含预备、起跳、最高点、落地与恢复；反应克制而非过度活泼。
- `waiting` 无问号或气泡，通过抬手、歪头和不确定表情表达等待回答。
- `running` 使用坐着看书的学习动作，对应对话或任务执行。
- Osaka 的发型、制服、脸型、放空眼神和 2.5D 软胶风格在九行中保持一致。
- contact sheet 中绿色边框为使用格，红色边框为空透明格。

## 验证命令

```powershell
python osaka_pet\tools\create_frames.py
python osaka_pet\tools\build_atlas.py
python osaka_pet\tools\validate_assets.py
python -m unittest discover -s osaka_pet\tests -v
```

## 安装交互验证

2026-06-23 已将 `package\pet.json` 与 `package\spritesheet.webp` 安装到 `%USERPROFILE%\.codex\pets\osaka`，两份安装文件的 SHA-256 与运行包逐字节一致。

Codex 26.616.9593 宿主代码确认：向右拖与向左拖分别选择 `running-right` 和 `running-left`；任务执行、等待输入、失败、完成待查看分别选择 `running`、`waiting`、`failed`、`review`。普通点击当前用于打开主窗口；宿主虽然定义 `jumping` 行，但是否在点击时显示由宿主版本控制。

受自动化规则限制，未通过工具操控 Codex 桌面应用。安装后需人工观察左右拖拽方向，以及一次任务从 `running` 切换到 `waiting` 或 `review` 的过程。
