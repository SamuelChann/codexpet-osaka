# Osaka

一个以大阪（春日步）为角色的 Codex Q 版桌面宠物包。

## 文件

- `pet.json`: Codex 自定义桌宠清单。
- `spritesheet.webp`: 透明背景动画图集，尺寸为 `1536x1872`。
- `docs/contact-sheet.png`: 动作表预览。

## 预览

![Osaka contact sheet](docs/contact-sheet.png)

## 安装

把整个 `osaka` 文件夹放到：

```text
%USERPROFILE%\.codex\pets\osaka
```

目录结构应为：

```text
osaka/
  pet.json
  spritesheet.webp
```

## 动画状态

图集遵循 Codex 桌宠固定格式：`8` 列、`9` 行，每格 `192x208`。

| 行 | 状态 | 语义 |
| --- | --- | --- |
| 0 | idle | 发呆、呼吸、眨眼 |
| 1 | running-right | 被向右拖动 |
| 2 | running-left | 被向左拖动 |
| 3 | waving | 开心挥手 |
| 4 | jumping | 点击后的慢半拍小跳 |
| 5 | failed | 漫画式捂眼哭泣 |
| 6 | waiting | 张大嘴笑着挥手等待 |
| 7 | running | 看书、翻页和打瞌睡 |
| 8 | review | 跪坐低头并偷偷抬眼 |

## 校验

- 图集格式：WebP / RGBA
- 图集尺寸：`1536x1872`
- 单元格：`192x208`
- 透明像素 RGB 残留：`0`

## 说明

此包只包含桌宠运行所需文件，没有游戏 UI、Logo、水印或背景。角色素材按统一的 Q 版 2.5D 风格制作，并整理为 Codex 桌宠固定九行动画图集。
