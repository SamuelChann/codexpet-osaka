# Osaka Codex 桌宠资产工作流

## 身份与风格

- 仅供本地个人桌面使用。角色必须明确呈现 Ayumu Kasuga / Osaka 的 Q 版桌宠形象。
- `..\osaka.png` 是首要身份参考，`reference\osaka_pet_master.png` 是资产流水线的角色基准。
- 固定特征：2.1–2.3 头身、黑棕色中长直发、圆润脸型、小而放空的深色眼睛、小嘴、红粉与浅色校园制服、2.5D 软胶材质。
- 表情和动作安静、真诚、无辜、天然呆；快速动作前保留短暂停顿。
- 禁止改变发型、服装、身体比例和渲染方式；禁止背景、Logo、水印、文字、动物耳、武器或额外角色。

## Codex 固定九行

| 行 | 状态 | 使用格 | Osaka 语义 |
| --- | --- | ---: | --- |
| 0 | `idle` | 6 | 发呆、呼吸、眨眼 |
| 1 | `running-right` | 8 | 被向右拖动，头发和肢体向左滞后 |
| 2 | `running-left` | 8 | 被向左拖动，头发和肢体向右滞后 |
| 3 | `waving` | 4 | 开心地轻轻回应 |
| 4 | `jumping` | 5 | 点击后慢半拍受惊小跳 |
| 5 | `failed` | 8 | 委屈、含泪 |
| 6 | `waiting` | 6 | 注意用户、歪头、抬手等待回答 |
| 7 | `running` | 6 | 对话或任务执行时坐着看书学习 |
| 8 | `review` | 6 | 完成待查看时害羞抱肚子 |

第 0、3、4、6、7、8 行未使用的尾格必须全透明。宿主不会读取自定义状态名来重新解释图集，因此状态不得跨行。

## 素材来源

- 复用源姿势：`happy → waving`、`cry → failed`、`study → running`、`shy → review`。
- 新关键姿势：`running-right`、`running-left`、`jumping`、`waiting`。
- 旧 `drag`、`surprised`、`clicked`、`sleep`、`thinking`、`eating` 只作为素材历史，不进入运行图集。

## 构建与修订

1. 关键姿势同时引用 `..\osaka.png` 与主基准图，使用纯 `#00FF00` 背景。
2. 使用 imagegen 技能的 `remove_chroma_key.py`，启用 soft matte 与 despill。
3. 每帧统一为 192×208 RGBA；常规站立脚底锚点为 `(96, 200)`。
4. 运行 `python tools\create_frames.py`、`python tools\build_atlas.py`、`python tools\validate_assets.py`。
5. 运行 `python -m unittest discover -s tests -v`。
6. 修改失败状态时只替换该关键姿势与对应行，再重新构建并验证。

## 人工检查

检查 Osaka 身份、脸、头发、制服、体型、方向感、脚底锚点、循环衔接、透明边缘和慢半拍节奏；同时排除背景、文字、水印、UI、额外角色和绿色残边。

