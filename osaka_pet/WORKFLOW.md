# Osaka 桌宠资产工作流

## 身份与风格

- 仅供本地个人桌面使用。角色必须明确呈现 Ayumu Kasuga / Osaka 的 Q 版桌宠形象。
- `..\osaka.png` 是首要身份参考，`reference\osaka_pet_master.png` 是资产流水线中的唯一主基准。
- 固定特征：2.1–2.3 头身、黑棕色中长直发、圆润脸型、小而深色的放空眼睛、小嘴、红棕与浅色校园制服、2.5D 软胶材质。
- 表情和动作必须安静、真诚、无辜、天然呆，并在动作前保留明显停顿。
- 禁止改变发型、服装、身体比例和渲染方式；禁止额外角色、背景、Logo、水印、UI、武器、动物耳或无关配饰。唯一例外是用户已批准 `drag` 状态顶部用于提起角色的外部手。

## 固定动画映射

`idle 0–7`、`happy 8–13`、`shy 14–19`、`cry 20–25`、`surprised 26–31`、`clicked 32–37`、`drag 38–41`、`sleep 42–49`、`study 50–57`、`thinking 58–63`、`eating 64–71`。

## 生成与构建

1. 使用 `prompts\generation.md` 中的主提示词和 `..\osaka.png` 生成主基准图。
2. 关键姿势必须同时引用 `..\osaka.png` 和主基准图；背景使用纯 `#00FF00`。
3. 使用 Codex imagegen 技能自带的 `remove_chroma_key.py` 去背，启用 soft matte 和 despill。
4. 将关键姿势放进 `keyposes\`，使用确定性小幅位移、旋转、压缩、眨眼和表情覆盖组成源帧。
5. 源帧统一为 192×208 RGBA，站立帧底部锚点为 `(96, 200)`。
6. 运行：

```powershell
python tools\build_atlas.py
python tools\validate_assets.py
python -m unittest discover -s tests -v
```

## 修订规则

- 先通过预览确认具体失败状态，再只修改该状态的关键姿势和对应帧区间。
- 修改后重新构建图集并执行完整验证。
- 只有用户明确否决主基准身份时，才允许重做主基准和全部状态。

## 人工检查

检查 Osaka 身份、脸、头发、制服、体型、锚点、五官风格、颜色、透明边缘、道具遮挡和慢半拍节奏；同时检查背景、文字、水印、UI 或其他角色等意外内容。
