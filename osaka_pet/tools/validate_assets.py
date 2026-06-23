from pathlib import Path
import json
import math

from PIL import Image

REQUIRED_STATES = {
    "idle", "happy", "shy", "cry", "surprised", "clicked",
    "drag", "sleep", "study", "thinking", "eating",
}


def _green_residue_ratio(image: Image.Image) -> float:
    pixels = list(image.getdata())
    visible = [p for p in pixels if p[3] > 0]
    if not visible:
        return 0.0
    residue = sum(math.dist(p[:3], (0, 255, 0)) <= 20 for p in visible)
    return residue / len(visible)


def validate_assets(root: Path):
    root = Path(root)
    errors = []
    atlas_path = root / "osaka_pet_atlas.png"
    manifest_path = root / "osaka_pet.animations.json"
    if not atlas_path.exists():
        return ["atlas missing"]
    with Image.open(atlas_path) as atlas:
        if atlas.mode != "RGBA":
            errors.append("atlas must be RGBA")
        if atlas.size != (1536, 1872):
            errors.append("atlas must be 1536x1872")
    if not manifest_path.exists():
        errors.append("manifest missing")
        return errors
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    animations = data.get("animations", {})
    if set(animations) != REQUIRED_STATES:
        errors.append("required animation states mismatch")
    referenced = []
    for name, animation in animations.items():
        for field in ("name", "frames", "durationsMs", "loop", "next", "anchor", "hitbox", "bounds", "pivot"):
            if field not in animation:
                errors.append(f"{name}: missing {field}")
        frames = animation.get("frames", [])
        referenced.extend(frames)
        if len(frames) != len(animation.get("durationsMs", [])):
            errors.append(f"{name}: durations length mismatch")
        if any(not isinstance(i, int) or i < 0 or i >= 72 for i in frames):
            errors.append(f"{name}: invalid frame id")
        for field in ("anchor", "pivot"):
            point = animation.get(field, {})
            if not all(isinstance(point.get(axis), int) for axis in ("x", "y")):
                errors.append(f"{name}: invalid {field}")
        for field in ("bounds", "hitbox"):
            rect = animation.get(field, {})
            if not all(isinstance(rect.get(key), int) for key in ("x", "y", "width", "height")):
                errors.append(f"{name}: invalid {field}")
            elif rect["x"] < 0 or rect["y"] < 0 or rect["width"] <= 0 or rect["height"] <= 0 or rect["x"] + rect["width"] > 192 or rect["y"] + rect["height"] > 208:
                errors.append(f"{name}: {field} outside canvas")
    if sorted(referenced) != list(range(72)):
        errors.append("frame references must cover 0-71 exactly once")
    for index in range(72):
        path = root / "frames" / f"{index:03d}.png"
        if not path.exists():
            errors.append(f"missing frame {index:03d}")
            continue
        with Image.open(path) as source:
            if source.mode != "RGBA":
                errors.append(f"{path.name}: must be RGBA")
                continue
            if source.size != (192, 208):
                errors.append(f"{path.name}: wrong size")
                continue
            image = source.copy()
        alpha = image.getchannel("A")
        corners = (
            alpha.crop((0, 0, 16, 16)), alpha.crop((176, 0, 192, 16)),
            alpha.crop((0, 192, 16, 208)), alpha.crop((176, 192, 192, 208)),
        )
        if any(region.getbbox() is not None for region in corners):
            errors.append(f"{path.name}: corners are not transparent")
        bbox = alpha.getbbox()
        if bbox and (bbox[0] < 4 or bbox[1] < 4 or bbox[2] > 188 or bbox[3] > 204):
            errors.append(f"{path.name}: visible pixels outside safe area")
        if _green_residue_ratio(image) > 0.001:
            errors.append(f"{path.name}: chroma residue exceeds threshold")
        visible = sum(1 for value in alpha.getdata() if value > 0)
        if visible / (192 * 208) > 0.65:
            errors.append(f"{path.name}: opaque coverage too large")
    return errors


if __name__ == "__main__":
    project = Path(__file__).resolve().parents[1]
    problems = validate_assets(project)
    if problems:
        print("Validation failed:")
        for problem in problems:
            print(f"- {problem}")
        raise SystemExit(1)
    print("Validation passed: atlas, 72 frames, manifest, alpha and chroma checks are valid")
