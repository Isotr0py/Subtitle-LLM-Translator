from pathlib import Path

from .lrc import SakuraLrc
from .webvtt import SakuraWebVTT
from .translator import Translator


class SakuraAutoSub:
    @classmethod
    def from_file(cls, file):
        file = Path(file)
        if file.suffix.lower() == ".lrc":
            return SakuraLrc.from_file(file)
        if file.suffix.lower() == ".vtt":
            return SakuraWebVTT.from_file(file)
        raise ValueError("Unsupported file format")

    @classmethod
    def from_json(cls, json_file, format):
        if format == "lrc":
            return SakuraLrc.from_json(json_file)
        if format == "vtt":
            return SakuraWebVTT.from_json(json_file)
        raise ValueError("Unsupported file format")
