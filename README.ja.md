# Codex Pet：大阪

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

大阪（春日歩）をモチーフにした、Codex 用のちびキャラデスクトップペットです。

## プレビュー

![大阪アニメーション一覧](docs/contact-sheet.png)

## ファイル

- `pet.json`：Codex カスタムペットのマニフェスト。
- `spritesheet.webp`：透明背景のアニメーションスプライトシート。サイズは `1536x1872`。
- `docs/contact-sheet.png`：すべてのアニメーション状態とフレームのプレビュー。

## インストール

`pet.json` と `spritesheet.webp` を次のフォルダーへコピーします。

```text
%USERPROFILE%\.codex\pets\osaka
```

Codex を再起動し、ペット設定から **Osaka** を選択してください。

## アニメーション構成

スプライトシートは Codex ペット形式に準拠しています。8 列、9 行、1 セル `192x208` ピクセルです。

| 行 | 状態 | アニメーション |
| --- | --- | --- |
| 0 | idle | 呼吸とまばたき |
| 1 | running-right | 右方向へドラッグ |
| 2 | running-left | 左方向へドラッグ |
| 3 | waving | 楽しそうに手を振る |
| 4 | jumping | 少し遅れてふんわりジャンプ |
| 5 | failed | 漫画風に目を覆って泣く |
| 6 | waiting | 大きく笑って元気に手を振る |
| 7 | running | 読書、ページめくり、居眠り |
| 8 | review | 正座して、恥ずかしそうに上目遣い |

## 検証情報

- WebP / RGBA
- `1536x1872` スプライトシート
- `192x208` セル
- 透明背景
