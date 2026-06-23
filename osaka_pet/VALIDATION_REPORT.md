# Osaka 桌宠资产验证报告

## 自动验证

- 图集：1536×1872 RGBA，8×9，行优先。
- 源帧：`000.png`–`071.png` 共72张，均为192×208 RGBA。
- 动画：11个必需状态完整，帧号0–71恰好覆盖一次。
- JSON：逐帧时长、循环、next、anchor、pivot、bounds和hitbox完整。
- `bounds` 与 `hitbox` 已从最终帧透明像素并集自动计算。
- 透明四角、安全边距、alpha覆盖率和色键残留检查通过。
- 图集切片与源帧逐像素一致性测试通过。

## 人工检查

- Osaka 的黑棕直发、制服配色、脸型、放空眼神和慢半拍气质在所有状态中保持可辨识。
- 站立状态底线稳定；睡眠、学习和拖拽姿势使用独立锚点。
- 动作以长停顿和轻微位移为主，没有战斗或过度活泼动作。
- 透明轮廓在图集预览中无明显绿色残边。
- `drag` 状态顶部外部手由用户明确批准保留，是“无其他角色/物体”规则的唯一例外。

## 验证命令

```powershell
python -m unittest discover -s osaka_pet\tests -v
python osaka_pet\tools\create_frames.py
python osaka_pet\tools\build_atlas.py
python osaka_pet\tools\validate_assets.py
```
