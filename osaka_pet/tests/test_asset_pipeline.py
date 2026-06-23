import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_atlas import build_atlas, split_atlas, sync_manifest_geometry
from create_frames import compose_frames, fit_keypose
from validate_assets import validate_assets


class AssetPipelineTests(unittest.TestCase):
    def make_frames(self, directory: Path):
        directory.mkdir(parents=True, exist_ok=True)
        for index in range(72):
            image = Image.new("RGBA", (192, 208), (0, 0, 0, 0))
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
            names = ["happy", "shy", "cry", "surprised", "clicked", "drag", "sleep", "study", "thinking", "eating"]
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


if __name__ == "__main__":
    unittest.main()
