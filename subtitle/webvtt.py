import re

from .base import SubBase


class WebVTT(SubBase):
    def __repr__(self) -> str:
        return f"WebVTT('{self.name}')"

    def _load_contents(self, vtt_file):
        with open(vtt_file, "r", encoding="utf-8") as f:
            contents = f.readlines()[1:]

        blocks = []
        for line in contents:
            line_content = self._filter_line(line)
            if line_content:
                if isinstance(line_content, tuple) and len(line_content) == 2:
                    blocks.append(list(line_content))
                else:
                    blocks[-1].append(line_content)

        contents = [
            {"index": id, "start": start, "end": end, "jp": text, "cn": ""}
            for id, (start, end, text) in enumerate(blocks)
        ]
        return contents

    def _get_header(self, vtt_file):
        with open(vtt_file, "r", encoding="utf-8") as f:
            header = f.readline()
        if not header.startswith("WEBVTT"):
            raise ValueError("Not a WEBVTT file")
        if header_content := re.findall("WEBVTT - (.*)", header):
            return header_content[0]
        return ""

    def _filter_line(self, line: str):
        TIMEFRAME_LINE_PATTERN = re.compile(
            r"\s*((?:\d+:)?\d{2}:\d{2}.\d{3})\s*-->\s*((?:\d+:)?\d{2}:\d{2}.\d{3})"
        )
        COMMENT_PATTERN = re.compile(r"NOTE(?:\s.+|$)")
        STYLE_PATTERN = re.compile(r"STYLE[ \t]*$")
        line = line.strip()
        if time_frame := re.findall(TIMEFRAME_LINE_PATTERN, line):
            return time_frame[0]
        if re.findall(COMMENT_PATTERN, line) or re.findall(STYLE_PATTERN, line):
            return ""
        return line

    def to_file(self, vtt_file: str):
        with open(vtt_file, "w", encoding="utf-8") as f:
            f.write("WEBVTT - %s\n\n" % self.header)
            for c in self.contents:
                s = "%s --> %s\n%s\n\n" % (c["start"], c["end"], c["cn"])
                f.write(s)
