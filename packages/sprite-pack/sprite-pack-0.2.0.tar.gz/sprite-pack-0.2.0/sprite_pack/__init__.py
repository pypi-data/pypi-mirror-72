__version__ = "0.1.0"

from argparse import ArgumentParser, FileType
from itertools import chain, repeat, permutations
from pathlib import Path
from json import dump
from collections import namedtuple
import logging
import coloredlogs

from PIL import Image
from rpack import pack, enclosing_size


_logger = logging.getLogger(__name__)


def pack_sprites(sheet_fh, scene_fh, animated, landscape, static, static_unpack):
    static.extend(chain.from_iterable(map(PackedSprites.unpack, static_unpack)))
    sizes = list(map(Sprite.get_size, chain(animated, landscape, static)))
    positions = pack(sizes)
    sheet_img = Image.new("RGBA", enclosing_size(sizes, positions))
    sheet_path = Path(sheet_fh.name)
    if not sheet_path.is_absolute():
        sheet_path = sheet_path.relative_to(Path(scene_fh.name).parent)
    scene = {
        "sheet": str(sheet_path),
        "sprites": {},
    }
    anim_pos, rest = split_at(positions, len(animated))
    land_pos, static_pos = split_at(rest, len(landscape))
    for (x, y), anim in zip(anim_pos, animated):
        scene["sprites"][anim.name] = {
            "type": "animated",
            "x": x,
            "y": y,
            "w": anim.pack_size.w,
            "h": anim.pack_size.h,
            "frames": anim.num_packed,
            "direction": anim.direction,
        }
        box = (x, y, x + anim.img.width, y + anim.img.height)
        sheet_img.paste(anim.img, box=box)
        _logger.info(f"Pasted {anim.name} to {box}")
    for (x, y), land in zip(land_pos, landscape):
        scene["sprites"][land.name] = {
            "type": "landscape",
            "x": x,
            "y": y,
            "w": land.pack_size.w,
            "h": land.pack_size.h,
            "frames": land.num_packed,
            "direction": land.direction,
        }
        box = (x, y, x + land.img.width, y + land.img.height)
        sheet_img.paste(land.img, box=box)
        _logger.info(f"Pasted {land.name} to {box}")
    for (x, y), static in zip(static_pos, static):
        scene["sprites"][static.name] = {
            "type": "static",
            "x": x,
            "y": y,
            "w": static.img.width,
            "h": static.img.height,
        }
        box = (x, y, x + static.img.width, y + static.img.height)
        sheet_img.paste(static.img, box=box)
        _logger.info(f"Pasted {static.name} to {box}")
    sheet_img.save(sheet_fh)
    _logger.info(f"Saved sprite sheet to {sheet_fh.name}")
    dump(scene, scene_fh, indent=2)
    _logger.info(f"Saved sprite sheet info to {scene_fh.name}")


Size = namedtuple("Size", "w h")


class Sprite:
    def get_size(self):
        return Size(*self.img.size)


class PackedSprites(Sprite):
    def __init__(self, file_width):
        split = file_width.rsplit(":", 2)
        if len(split) == 3:
            f, w, names = split
        else:
            names = None
            f, w = split
        if w.startswith("h"):
            d = "column"
            w = w[1:]
        elif w.startswith("w"):
            d = "row"
            w = w[1:]
        elif w.startswith("s"):
            d = "square"
            w = w[1:]
        else:
            d = "row"
        path = Path(f)
        self.name = path.name[: -len(path.suffix)]
        self.img = Image.open(f)
        self.pack_width = int(w)
        if d == "row":
            self.pack_size = Size(self.pack_width, self.img.height)
            self.num_packed = int(self.img.width / self.pack_width)
            positions = zip(range(0, self.img.width, self.pack_width), repeat(0))
        elif d == "column":
            self.pack_size = Size(self.img.width, self.pack_width)
            self.num_packed = int(self.img.height / self.pack_width)
            positions = zip(repeat(0), range(0, self.img.height, self.pack_width))
        elif d == "square":
            self.pack_size = Size(self.pack_width, self.pack_width)
            x_packed = int(self.img.width / self.pack_width)
            self.num_packed = x_packed ** 2
            positions = permutations(range(0, self.img.width, self.pack_width), 2)
        self.direction = d
        if names is None:
            self.names = [f"{self.name}-{n}" for n in range(self.num_packed)]
        else:
            self.names = [f"{self.name}-{n}" for n in map(str.strip, names.split(","))]
        self.boxes = [
            (x, y, x + self.pack_size.w, y + self.pack_size.h) for x, y in positions
        ]
        _logger.debug(f"Created packed sprite: {self.name}")

    def unpack(self):
        _logger.info(f"Unpacking {self.name}")
        for name, box in zip(self.names, self.boxes):
            sub_img = self.img.crop(box)
            _logger.debug(f"Extracted {name} from {self.name} at {box}")
            yield StaticSprite(name, sub_img)


class StaticSprite(Sprite):
    def __init__(self, name, img):
        self.name = name
        self.img = img
        _logger.debug(f"Created static sprite: {self.name}")

    @classmethod
    def from_file(cls, f):
        path = Path(f)
        name = path.name[: -len(path.suffix)]
        _logger.debug(f"Loading static sprite, {name}, from file: {f}")
        return cls(name, Image.open(f))


def main():
    parser = ArgumentParser("sprite-pack")
    parser.add_argument("--sheet", type=FileType("wb"), default="sprites.png")
    parser.add_argument("--scene", type=FileType("w"), default="sprites.json")
    parser.add_argument(
        "--animated", "-a", action="append", type=PackedSprites, default=[]
    )
    parser.add_argument(
        "--landscape", "-l", action="append", type=PackedSprites, default=[]
    )
    parser.add_argument(
        "--static", "-s", action="append", type=StaticSprite.from_file, default=[]
    )
    parser.add_argument(
        "--static-unpack", action="append", type=PackedSprites, default=[]
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices={"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"},
    )
    args = parser.parse_args()
    coloredlogs.install(fmt="%(levelname)08s: %(message)s", level=args.log_level)
    pack_sprites(
        args.sheet,
        args.scene,
        args.animated,
        args.landscape,
        args.static,
        args.static_unpack,
    )


def split_at(l, i):
    return l[0:i], l[i:]


if __name__ == "__main__":
    main()
