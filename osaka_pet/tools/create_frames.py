from pathlib import Path

from PIL import Image

CANVAS = (192, 208)


def fit_keypose(image: Image.Image, max_size=(160, 196), bottom=200) -> Image.Image:
    image = image.convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        raise ValueError("key pose has no visible pixels")
    subject = image.crop(bbox)
    ratio = min(max_size[0] / subject.width, max_size[1] / subject.height)
    size = (max(1, round(subject.width * ratio)), max(1, round(subject.height * ratio)))
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    x = (CANVAS[0] - subject.width) // 2
    y = bottom - subject.height
    canvas.alpha_composite(subject, (x, y))
    return canvas


def _variant(base: Image.Image, dx=0, dy=0, scale=1.0, angle=0.0) -> Image.Image:
    bbox = base.getchannel("A").getbbox()
    if not bbox:
        return base.copy()
    subject = base.crop(bbox)
    if scale != 1.0:
        subject = subject.resize(
            (max(1, round(subject.width * scale)), max(1, round(subject.height * scale))),
            Image.Resampling.LANCZOS,
        )
    if angle:
        subject = subject.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    x = (CANVAS[0] - subject.width) // 2 + dx
    y = bbox[3] - subject.height + dy
    x = min(max(4, x), CANVAS[0] - 4 - subject.width)
    y = min(max(4, y), CANVAS[1] - 4 - subject.height)
    canvas.alpha_composite(subject, (x, y))
    return canvas


def _load_fitted(keyposes_dir: Path):
    settings = {
        "master": ((152, 192), 200),
        "happy": ((152, 192), 200),
        "shy": ((152, 192), 200),
        "cry": ((152, 192), 200),
        "study": ((166, 164), 200),
        "running-right": ((176, 184), 200),
        "running-left": ((176, 184), 200),
        "jumping": ((160, 184), 196),
        "waiting": ((160, 192), 200),
    }
    result = {}
    for name, (size, bottom) in settings.items():
        if name == "master":
            path = Path(keyposes_dir).parent / "reference" / "osaka_pet_master.png"
        else:
            path = Path(keyposes_dir) / f"{name}.png"
        if not path.exists():
            raise FileNotFoundError(path)
        with Image.open(path) as source:
            result[name] = fit_keypose(source, size, bottom)
    return result


def compose_frames(keyposes_dir: Path, frames_dir: Path) -> None:
    poses = _load_fitted(Path(keyposes_dir))
    # Each group is one fixed Codex row. None emits a transparent unused cell.
    # Source, x offset, y offset, scale, rotation. Long repeated poses preserve
    # Osaka's deliberate pauses while drag and click states stay readable.
    recipes = [
        # row 0 idle: 6 used, 2 transparent
        ("master",0,0,1.000,0),("master",0,-1,1.002,0),("master",0,-1,1.002,0),
        ("master",0,0,1.000,0),("master",1,0,1.000,-1.2),("master",0,0,1.000,0),None,None,
        # row 1 running-right
        ("running-right",-2,0,0.985,-1.2),("running-right",0,-1,0.990,0),
        ("running-right",2,0,0.985,1.2),("running-right",1,1,0.980,0.6),
        ("running-right",-2,0,0.985,-1.2),("running-right",0,-1,0.990,0),
        ("running-right",2,0,0.985,1.2),("running-right",1,1,0.980,0.6),
        # row 2 running-left
        ("running-left",2,0,0.985,1.2),("running-left",0,-1,0.990,0),
        ("running-left",-2,0,0.985,-1.2),("running-left",-1,1,0.980,-0.6),
        ("running-left",2,0,0.985,1.2),("running-left",0,-1,0.990,0),
        ("running-left",-2,0,0.985,-1.2),("running-left",-1,1,0.980,-0.6),
        # row 3 waving: delayed recognition, then a soft happy response
        ("master",0,0,1.000,0),("happy",0,0,0.985,0),("happy",0,-4,0.995,0),("happy",0,0,0.985,0),
        None,None,None,None,
        # row 4 jumping: anticipation, lift, apex, landing, recovery
        ("master",0,2,0.985,0),("jumping",0,-4,0.990,0),("jumping",0,-10,1.000,0),
        ("jumping",0,-4,0.990,0),("master",0,0,1.000,0),None,None,None,
        # row 5 failed
        ("cry",0,0,1.000,0),("cry",0,1,0.995,0),("cry",0,0,1.000,0),("cry",0,2,0.992,0),
        ("cry",0,0,1.000,0),("cry",0,1,0.995,0),("cry",0,0,1.000,0),("cry",0,2,0.992,0),
        # row 6 waiting: notice, raise a hand, and hold a confused expectation
        ("master",0,0,1.000,0),("waiting",0,0,0.990,0),("waiting",0,0,0.995,-1.0),
        ("waiting",0,0,0.995,-1.0),("waiting",0,0,0.990,0),("waiting",0,0,0.990,0),None,None,
        # row 7 running: actively studying while Codex works
        ("study",0,0,1.000,0),("study",0,1,0.997,0),("study",0,2,0.994,0),
        ("study",0,1,0.997,0),("study",1,0,1.000,-1.0),("study",0,0,1.000,0),None,None,
        # row 8 review: completed work, shyly awaiting inspection
        ("master",0,0,1.000,0),("shy",0,1,0.985,0),("shy",0,3,0.975,0),
        ("shy",0,3,0.975,0),("shy",0,2,0.980,0.8),("shy",0,1,0.985,0),None,None,
    ]
    if len(recipes) != 72:
        raise AssertionError(f"expected 72 recipes, got {len(recipes)}")
    frames_dir = Path(frames_dir)
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob("*.png"):
        old.unlink()
    for index, recipe in enumerate(recipes):
        frame = Image.new("RGBA", CANVAS, (0, 0, 0, 0)) if recipe is None else _variant(poses[recipe[0]], *recipe[1:])
        frame.save(frames_dir / f"{index:03d}.png", optimize=True)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    compose_frames(root / "keyposes", root / "frames")
    print("Created 72 RGBA frames")
