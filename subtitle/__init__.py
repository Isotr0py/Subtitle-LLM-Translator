from pathlib import Path

from .lrc import Lrc
from .webvtt import WebVTT
from .translator import Translator


class AutoSub:
    @classmethod
    def from_file(cls, file):
        file = Path(file)
        if file.suffix.lower() == ".lrc":
            return Lrc.from_file(file)
        if file.suffix.lower() == ".vtt":
            return WebVTT.from_file(file)
        raise ValueError("Unsupported file format")

    @classmethod
    def from_json(cls, json_file, format):
        if format == "lrc":
            return Lrc.from_json(json_file)
        if format == "vtt":
            return WebVTT.from_json(json_file)
        raise ValueError("Unsupported file format")
