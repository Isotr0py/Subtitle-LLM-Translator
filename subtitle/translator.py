from pathlib import Path
from typing import List

import yaml
from openai import OpenAI


class Translator:
    """
        SakuraLLM Translator
    """
    def __init__(self, endpoint, workspace, generate_config):
        self.client = OpenAI(api_key="114514", base_url=endpoint + "/v1")
        self.workspace = Path(workspace)
        self.generate_config = generate_config

    @classmethod
    def from_config(cls, config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return cls(config["endpoint"], config["workspace"], config["generate_config"])

    def translate(self, input_text) -> List[str]:
        query = "将下面的日文文本翻译成中文：" + input_text
        messages = [
            {
                "role": "system",
                "content": "你是一个轻小说翻译模型，可以流畅通顺地以日本轻小说的风格将日文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。",
            },
            {"role": "user", "content": f"{query}"},
        ]
        text_output = ""
        for output in self.client.chat.completions.create(
            model="Sakura", messages=messages, stream=True, **self.generate_config
        ):
            if output.choices[0].delta.content:
                print(output.choices[0].delta.content, end="")
                text_output += output.choices[0].delta.content
        olist = list(filter(None, text_output.split("\n")))
        return olist
