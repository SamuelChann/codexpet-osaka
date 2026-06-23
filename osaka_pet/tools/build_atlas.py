from pathlib import Path
from typing import Iterable
import json

from PIL import Image, ImageDraw

FRAME_SIZE = (192, 208)
GRID = (8, 9)
ATLAS_SIZE = (1536, 1872)


def _frame_paths(frames_dir: Path) -> Iterable[Path]:
    return (frames_dir / f"{index:03d}.png" for index in range(72))


def build_atlas(frames_dir: Path, atlas_path: Path) -> None:
    atlas = Image.new("RGBA", ATLAS_SIZE, (0, 0, 0, 0))
    for index, path in enumerate(_frame_paths(Path(frames_dir))):
        if not path.exists():
            raise FileNotFoundError(path)
        with Image.open(path) as source:
            frame = source.convert("RGBA")
        if frame.size != FRAME_SIZE:
            raise ValueError(f"{path.name}: expected {FRAME_SIZE}, got {frame.size}")
        x = (index % GRID[0]) * FRAME_SIZE[0]
        y = (index // GRID[0]) * FRAME_SIZE[1]
        atlas.paste(frame, (x, y), frame)
    atlas_path = Path(atlas_path)
    atlas_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(atlas_path)


def split_atlas(atlas_path: Path):
    with Image.open(atlas_path) as source:
        atlas = source.convert("RGBA")
        if atlas.size != ATLAS_SIZE:
            raise ValueError(f"expected atlas size {ATLAS_SIZE}, got {atlas.size}")
        frames = []
        for index in range(72):
            x = (index % GRID[0]) * FRAME_SIZE[0]
            y = (index // GRID[0]) * FRAME_SIZE[1]
            frames.append(atlas.crop((x, y, x + FRAME_SIZE[0], y + FRAME_SIZE[1])).copy())
    return frames


def build_previews(frames_dir: Path, manifest_path: Path, output_dir: Path) -> None:
    data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for old in output_dir.glob("*.webp"):
        old.unlink()
    for name, animation in data["animations"].items():
        images = []
        for index in animation["frames"]:
            with Image.open(Path(frames_dir) / f"{index:03d}.png") as source:
                images.append(source.convert("RGBA"))
        images[0].save(
            output_dir / f"{name}.webp",
            save_all=True,
            append_images=images[1:],
            duration=animation["durationsMs"],
            loop=0 if animation["loop"] else 1,
            lossless=True,
        )


def build_package(atlas_path: Path, package_path: Path) -> None:
    with Image.open(atlas_path) as source:
        atlas = source.convert("RGBA")
    if atlas.size != ATLAS_SIZE:
        raise ValueError(f"expected atlas size {ATLAS_SIZE}, got {atlas.size}")
    package_path = Path(package_path)
    package_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(package_path, format="WEBP", lossless=True, exact=True, method=6)


def build_contact_sheet(frames_dir: Path, manifest_path: Path, output_path: Path) -> None:
    data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    row_height = FRAME_SIZE[1] + 28
    sheet = Image.new("RGBA", (ATLAS_SIZE[0], row_height * GRID[1]), (14, 17, 22, 255))
    draw = ImageDraw.Draw(sheet)
    animations = list(data["animations"].items())
    for row, (name, animation) in enumerate(animations):
        top = row * row_height
        draw.text((8, top + 7), f"row {row}  {name}  {len(animation['frames'])} frames", fill=(240, 244, 250, 255))
        for column in range(GRID[0]):
            cell_x = column * FRAME_SIZE[0]
            cell_y = top + 28
            tile = 16
            for y in range(0, FRAME_SIZE[1], tile):
                for x in range(0, FRAME_SIZE[0], tile):
                    shade = 236 if (x // tile + y // tile) % 2 == 0 else 208
                    draw.rectangle(
                        (cell_x + x, cell_y + y, cell_x + min(x + tile, FRAME_SIZE[0]) - 1, cell_y + min(y + tile, FRAME_SIZE[1]) - 1),
                        fill=(shade, shade, shade, 255),
                    )
            index = row * GRID[0] + column
            with Image.open(Path(frames_dir) / f"{index:03d}.png") as source:
                frame = source.convert("RGBA")
            sheet.alpha_composite(frame, (cell_x, cell_y))
            border = (43, 164, 91, 255) if index in animation["frames"] else (205, 61, 71, 255)
            draw.rectangle((cell_x, cell_y, cell_x + FRAME_SIZE[0] - 1, cell_y + FRAME_SIZE[1] - 1), outline=border, width=2)
            draw.text((cell_x + 5, cell_y + 4), str(column), fill=(15, 20, 25, 255))
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, optimize=True)


def sync_manifest_geometry(frames_dir: Path, manifest_path: Path) -> None:
    manifest_path = Path(manifest_path)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    for animation in data["animations"].values():
        union = None
        for index in animation["frames"]:
            with Image.open(Path(frames_dir) / f"{index:03d}.png") as source:
                bbox = source.convert("RGBA").getchannel("A").getbbox()
            if not bbox:
                continue
            if union is None:
                union = list(bbox)
            else:
                union = [min(union[0], bbox[0]), min(union[1], bbox[1]), max(union[2], bbox[2]), max(union[3], bbox[3])]
        if union is None:
            raise ValueError(f"{animation['name']}: all frames are empty")
        x1, y1, x2, y2 = union
        width, height = x2 - x1, y2 - y1
        animation["bounds"] = {"x": x1, "y": y1, "width": width, "height": height}
        inset_x = min(8, max(0, (width - 1) // 2))
        inset_y = min(8, max(0, (height - 1) // 2))
        animation["hitbox"] = {
            "x": x1 + inset_x,
            "y": y1 + inset_y,
            "width": max(1, width - inset_x * 2),
            "height": max(1, height - inset_y * 2),
        }
    manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    sync_manifest_geometry(root / "frames", root / "osaka_pet.animations.json")
    build_atlas(root / "frames", root / "osaka_pet_atlas.png")
    build_previews(root / "frames", root / "osaka_pet.animations.json", root / "previews")
    build_package(root / "osaka_pet_atlas.png", root / "package" / "spritesheet.webp")
    build_contact_sheet(root / "frames", root / "osaka_pet.animations.json", root / "contact-sheet.png")
    print(f"Built {root / 'osaka_pet_atlas.png'}, previews, package spritesheet, and contact sheet")
