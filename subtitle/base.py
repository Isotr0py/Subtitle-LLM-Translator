import json
from pathlib import Path


class SubBase:
    name: str
    header: str
    contents: list[dict]

    def __init__(self):
        self.name = None
        self.header = ""
        self.contents = []

    def __len__(self):
        return len(self.contents)

    def _load_contents(self, sub_file):
        """
        Load json format contents from subtitle file
        """
        raise NotImplementedError

    def _get_header(self, sub_file):
        """
        Get header from subtitle file
        """
        raise NotImplementedError

    @classmethod
    def from_json(cls, json_file: str):
        with open(json_file, "r", encoding="utf-8") as f:
            s = json.load(f)
        sub = cls()
        sub.name = s["name"]
        sub.header = s["header"]
        sub.contents = s["contents"]
        return sub

    @classmethod
    def from_file(cls, sub_file: str):
        sub = cls()
        sub.name = Path(sub_file).stem
        sub.header = sub._get_header(sub_file)
        sub.contents = sub._load_contents(sub_file)
        return sub

    def to_json(self, json_file: str):
        s = {
            "name": self.name,
            "header": self.header,
            "contents": self.contents,
        }
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=4)
        return self

    def to_file(self, sub_file: str):
        raise NotImplementedError
