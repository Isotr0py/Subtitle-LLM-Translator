import re
from glob import glob

from openai import OpenAI

from core import SakuraLrc


def translate_text(input_text) -> str:
    query = "将下面的日文文本翻译成中文：" + input_text
    messages = [
        {
            "role": "system",
            "content": "你是一个轻小说翻译模型，可以流畅通顺地以日本轻小说的风格将日文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。",
        },
        {"role": "user", "content": f"{query}"},
    ]
    extra_query = {
        "do_sample": False,
        "num_beams": 5,
        "repetition_penalty": 0.5,
    }
    text_output = ""
    for output in client.chat.completions.create(
        model="sakura",
        messages=messages,
        temperature=0.1,
        top_p=0.3,
        max_tokens=512,
        frequency_penalty=0.3,
        seed=-1,
        extra_query=extra_query,
        stream=True,
    ):
        # if output.choices[0].finish_reason:
        #     print("\nfinish reason is", output.choices[0].finish_reason)
        if output.choices[0].delta.content:
            print(output.choices[0].delta.content, end="")
            text_output += output.choices[0].delta.content
    olist = list(filter(None, text_output.split("\n")))
    return olist


def translate(file):
    lrc = SakuraLrc(file)
    if len(lrc) == 0:
        return
    for i in range(0, len(lrc), 5):
        text_list = lrc.untrs_text[i:i + 5]
        print(text_list)
        input_text = "".join(text_list)
        print(input_text)
        results = translate_text(input_text)
        if len(text_list) != len(results):
            p = re.compile("「(.*?)」", re.S)
            results = [
                re.findall(p, "".join(translate_text(text)))[0]
                for text in list(map(lambda x: f"「{x.strip()}」\n", text_list))
            ]
        lrc.write_trans_text(results)


api_base_url = "https://slimy-yaks-pick.loca.lt/v1"
client = OpenAI(api_key="114514", base_url=api_base_url)
files = glob("sample_lrc/*/02*.lrc")
for file in files:
    translate(file)
