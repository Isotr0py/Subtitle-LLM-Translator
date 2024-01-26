import re

from .base import SubBase


class Lrc(SubBase):
    def __repr__(self) -> str:
        return f"Lrc('{self.name}')"

    def _load_contents(self, lrc_file):
        header_idx = 1 if self.header else 0
        with open(lrc_file, "r", encoding="utf-8") as f:
            contents = f.readlines()[header_idx:]

        blocks = []
        for line in contents:
            time, text = self._filter_line(line)
            if text:
                blocks.append([time, text])
            else:
                blocks[-1].append(time)

        block_len = set(map(lambda x: len(x), blocks))
        if len(block_len) != 1:
            raise ValueError("Unaligned lrc file")
        block_len = block_len.pop()

        match block_len:
            case 2:
                contents = [
                    {"index": id, "start": start, "end": "", "jp": text, "cn": ""}
                    for id, (start, text) in enumerate(blocks)
                ]
            case 3:
                contents = [
                    {"index": id, "start": start, "end": end, "jp": text, "cn": ""}
                    for id, (start, text, end) in enumerate(blocks)
                ]
            case _:
                raise ValueError("Unexpected block length")
        return contents

    def _get_header(self, lrc_file):
        with open(lrc_file, "r", encoding="utf-8") as f:
            header = f.readline()
        header_content = re.findall(r"\[(.*?)\]", header)
        if len(header_content) == 1:
            header_content = re.sub(r"[0-9]+|\:|\.", "", header_content[0])
            return header_content
        return ""

    def _filter_line(self, line):
        return re.findall(r"\[(.*?)\](.*)", line)[0]

    def to_file(self, lrc_file: str):
        with open(lrc_file, "w", encoding="utf-8") as f:
            f.write("[%s]\n" % self.header)
            for c in self.contents:
                if c["end"]:
                    s = "[%s]%s\n[%s]\n" % (c["start"], c["cn"], c["end"])
                else:
                    s = "[%s]%s\n" % (c["start"], c["cn"])
                f.write(s)
