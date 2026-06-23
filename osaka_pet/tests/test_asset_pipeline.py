import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_atlas as atlas_tools
from build_atlas import build_atlas, build_previews, split_atlas, sync_manifest_geometry
from create_frames import compose_frames, fit_keypose
from validate_assets import validate_assets


class AssetPipelineTests(unittest.TestCase):
    CODEX_LAYOUT = {
        "idle": list(range(0, 6)),
        "running-right": list(range(8, 16)),
        "running-left": list(range(16, 24)),
        "waving": list(range(24, 28)),
        "jumping": list(range(32, 37)),
        "failed": list(range(40, 48)),
        "waiting": list(range(48, 54)),
        "running": list(range(56, 62)),
        "review": list(range(64, 70)),
    }

    def make_frames(self, directory: Path):
        directory.mkdir(parents=True, exist_ok=True)
        used = {frame for frames in self.CODEX_LAYOUT.values() for frame in frames}
        for index in range(72):
            image = Image.new("RGBA", (192, 208), (0, 0, 0, 0))
            if index in used:
                image.putpixel((96, 100), (80, 50, 40, 255))
            image.save(directory / f"{index:03d}.png")

    def test_build_and_split_atlas_are_pixel_exact(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            frames = base / "frames"
            self.make_frames(frames)
            atlas_path = base / "atlas.png"
            build_atlas(frames, atlas_path)
            with Image.open(atlas_path) as atlas:
                self.assertEqual(atlas.mode, "RGBA")
                self.assertEqual(atlas.size, (1536, 1872))
            split = split_atlas(atlas_path)
            self.assertEqual(len(split), 72)
            with Image.open(frames / "071.png") as source:
                self.assertEqual(split[71].tobytes(), source.tobytes())

    def test_manifest_uses_codex_nine_row_contract(self):
        manifest = json.loads((ROOT / "osaka_pet.animations.json").read_text(encoding="utf-8"))
        animations = manifest["animations"]
        self.assertEqual(list(animations), list(self.CODEX_LAYOUT))
        self.assertEqual(
            {name: animation["frames"] for name, animation in animations.items()},
            self.CODEX_LAYOUT,
        )

    def test_unused_codex_cells_are_fully_transparent(self):
        referenced = {frame for frames in self.CODEX_LAYOUT.values() for frame in frames}
        unused = sorted(set(range(72)) - referenced)
        for index in unused:
            with Image.open(ROOT / "frames" / f"{index:03d}.png") as frame:
                self.assertIsNone(frame.convert("RGBA").getchannel("A").getbbox(), index)

    def test_validator_accepts_complete_asset_set(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            frames = base / "frames"
            self.make_frames(frames)
            build_atlas(frames, base / "osaka_pet_atlas.png")
            manifest = json.loads((ROOT / "osaka_pet.animations.json").read_text(encoding="utf-8"))
            (base / "osaka_pet.animations.json").write_text(json.dumps(manifest), encoding="utf-8")
            errors = validate_assets(base)
            self.assertEqual(errors, [])

    def test_sync_manifest_geometry_uses_visible_union(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            frames = base / "frames"
            self.make_frames(frames)
            manifest = json.loads((ROOT / "osaka_pet.animations.json").read_text(encoding="utf-8"))
            path = base / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            sync_manifest_geometry(frames, path)
            updated = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(updated["animations"]["idle"]["bounds"], {"x": 96, "y": 100, "width": 1, "height": 1})

    def test_build_previews_removes_legacy_state_files(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            frames = base / "frames"
            self.make_frames(frames)
            output = base / "previews"
            output.mkdir()
            (output / "sleep.webp").write_bytes(b"legacy")
            build_previews(frames, ROOT / "osaka_pet.animations.json", output)
            self.assertEqual(
                sorted(path.stem for path in output.glob("*.webp")),
                sorted(self.CODEX_LAYOUT),
            )

    def test_build_package_writes_lossless_rgba_webp(self):
        self.assertTrue(callable(getattr(atlas_tools, "build_package", None)))
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            frames = base / "frames"
            self.make_frames(frames)
            atlas = base / "atlas.png"
            package = base / "spritesheet.webp"
            build_atlas(frames, atlas)
            atlas_tools.build_package(atlas, package)
            with Image.open(package) as image:
                self.assertEqual(image.format, "WEBP")
                self.assertEqual(image.mode, "RGBA")
                self.assertEqual(image.size, (1536, 1872))

    def test_build_contact_sheet_labels_nine_codex_rows(self):
        self.assertTrue(callable(getattr(atlas_tools, "build_contact_sheet", None)))
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            frames = base / "frames"
            self.make_frames(frames)
            output = base / "contact-sheet.png"
            atlas_tools.build_contact_sheet(frames, ROOT / "osaka_pet.animations.json", output)
            with Image.open(output) as image:
                self.assertEqual(image.mode, "RGBA")
                self.assertEqual(image.size, (1536, 2124))

    def test_fit_keypose_preserves_rgba_and_safe_margin(self):
        source = Image.new("RGBA", (400, 600), (0, 0, 0, 0))
        for x in range(100, 300):
            for y in range(50, 550):
                source.putpixel((x, y), (80, 50, 40, 255))
        fitted = fit_keypose(source, max_size=(160, 196), bottom=200)
        self.assertEqual(fitted.mode, "RGBA")
        self.assertEqual(fitted.size, (192, 208))
        self.assertEqual(fitted.getchannel("A").getbbox()[3], 200)

    def test_compose_frames_creates_all_72_numbered_frames(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            keyposes = base / "keyposes"
            keyposes.mkdir()
            names = [
                "happy", "shy", "cry", "surprised", "clicked", "drag", "sleep", "study", "thinking", "eating",
                "running-right", "running-left", "jumping", "waiting",
            ]
            for name in names:
                image = Image.new("RGBA", (300, 400), (0, 0, 0, 0))
                for x in range(80, 220):
                    for y in range(30, 370):
                        image.putpixel((x, y), (80, 50, 40, 255))
                image.save(keyposes / f"{name}.png")
            reference = base / "reference"
            reference.mkdir()
            master = Image.new("RGBA", (300, 400), (0, 0, 0, 0))
            for x in range(80, 220):
                for y in range(30, 370):
                    master.putpixel((x, y), (80, 50, 40, 255))
            master.save(reference / "osaka_pet_master.png")
            frames = base / "frames"
            compose_frames(keyposes, frames)
            self.assertEqual([p.name for p in frames.glob("*.png")], [f"{i:03d}.png" for i in range(72)])
            for path in frames.glob("*.png"):
                with Image.open(path) as image:
                    self.assertEqual(image.mode, "RGBA")
                    self.assertEqual(image.size, (192, 208))
            referenced = {frame for state_frames in self.CODEX_LAYOUT.values() for frame in state_frames}
            for index in sorted(set(range(72)) - referenced):
                with Image.open(frames / f"{index:03d}.png") as image:
                    self.assertIsNone(image.getchannel("A").getbbox(), index)


if __name__ == "__main__":
    unittest.main()
