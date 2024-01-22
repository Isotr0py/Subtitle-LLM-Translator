import re
from pathlib import Path
from tqdm import tqdm


class SakuraLrc:
    def __init__(self, lrc, progress_bar=True):
        self.progress_bar = progress_bar
        self.ori_lrc = Path(lrc)
        self.trs_lrc = Path(self.ori_lrc.stem + ".zh-cn.lrc")
        self.header = self.__get_header()
        N, self.trs_text = self.load_translated()
        self.start, self.untrs_text, self.end = self.load_contents(N)

    def __len__(self):
        return len(self.untrs_text)

    def __repr__(self) -> str:
        return f"SakuraLrc('{self.ori_lrc.name}')"

    def load_contents(self, idx):
        header_idx = 1 if self.header else 0
        with open(self.ori_lrc, "r", encoding="utf-8") as f:
            contents = f.readlines()[header_idx:]

        start = list(map(lambda x: self.__filter_time(x), contents[::2]))
        texts = list(map(lambda x, y: y.removeprefix(f"[{x}]"), start, contents[::2]))
        end = list(map(lambda x: self.__filter_time(x), contents[1::2]))

        if self.progress_bar:
            self.progress_bar = tqdm(total=len(texts), desc=f"[{self.ori_lrc.name}]")
            self.progress_bar.update(idx)

        return start[idx:][::-1], texts[idx:], end[idx:][::-1]

    def load_translated(self):
        if self.trs_lrc.exists():
            with open(self.trs_lrc, "r", encoding="utf-8") as f:
                contents = f.readlines()
            texts = list(map(lambda x: x[10:], contents[::2]))
        else:
            texts = []
        return len(texts), texts

    def write_trans_text(self, text: list):
        for t in text:
            with open(self.trs_lrc, "a", encoding="utf-8") as f:
                s = "[%s]%s\n%s\n" % (self.header, t, self.header)
                f.write(s)
            self.progress_bar.update(1)

    def __get_header(self):
        with open(self.ori_lrc, "r", encoding="utf-8") as f:
            header = f.readline()
        header_content = re.findall(r"\[(.*?)\]", header)
        if len(header_content) == 1:
            header_content = re.sub(r"[0-9]+|\:|\.", "", header_content[0])
            return header_content
        return ""

    def __filter_time(self, line):
        return re.findall(r"\[(.*?)\]", line)[0]
