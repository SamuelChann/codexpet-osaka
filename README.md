# Codex Pet: Osaka

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

A chibi Osaka (Ayumu Kasuga) desktop pet package for Codex.

## Preview

![Osaka animation contact sheet](docs/contact-sheet.png)

## Files

- `pet.json`: Codex custom pet manifest.
- `spritesheet.webp`: Transparent animation spritesheet, `1536x1872`.
- `docs/contact-sheet.png`: Preview of all animation states and frames.

## Installation

Copy `pet.json` and `spritesheet.webp` to:

```text
%USERPROFILE%\.codex\pets\osaka
```

Restart Codex and select **Osaka** in the pet settings.

## Animation layout

The spritesheet uses the Codex pet layout: 8 columns, 9 rows, and 192x208 pixels per cell.

| Row | State | Animation |
| --- | --- | --- |
| 0 | idle | Breathing and blinking |
| 1 | running-right | Dragged to the right |
| 2 | running-left | Dragged to the left |
| 3 | waving | Cheerful wave |
| 4 | jumping | Soft delayed jump |
| 5 | failed | Comedic crying pose |
| 6 | waiting | Big smile and active wave |
| 7 | running | Reading, page-turning, and dozing off |
| 8 | review | Seiza pose with a shy upward peek |

## Validation

- WebP / RGBA
- `1536x1872` spritesheet
- `192x208` cells
- Transparent background
