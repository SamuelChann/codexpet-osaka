from pathlib import Path
from typing import Iterable
import json

from PIL import Image

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
    print(f"Built {root / 'osaka_pet_atlas.png'} and previews")
