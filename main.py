import re
from glob import glob
from pathlib import Path

from tqdm import tqdm

from subtitle import AutoSub, Translator


def translate_file(file):
    name = Path(file).stem
    output_format = Path(file).suffix
    output_file = output_dir.joinpath(f"{name}{output_format}")
    cache_file = cache_dir.joinpath(f"{name}{output_format}.json")
    sub = AutoSub.from_file(file)
    progress_bar = tqdm(total=len(sub), desc=f"{sub}")
    if not sub.header:
        sub.header = "Translated by SakuraLLM model"
    else:
        sub.header += " / Translated by SakuraLLM model"
    if not Path(cache_file).exists():
        sub = sub.to_json(cache_file)

    sub = sub.from_json(cache_file)
    if len(sub) == 0:
        return

    # 断点检查
    for i in range(len(sub)):
        idx = i
        if not sub.contents[i]["cn"]:
            break
        progress_bar.update(1)

    batch_size = 5  # 每次翻译行数
    if idx != len(sub) - 1:
        for i in range(idx, len(sub), batch_size):
            # 整段翻译
            text_list = [content["jp"] for content in sub.contents[i : i + batch_size]]
            input_text = "\n".join(text_list)
            print(input_text + "\n")
            results = translator.translate(input_text)
            # 输出漏行时，逐行翻译
            if len(text_list) != len(results):
                p = re.compile("「(.*?)」", re.S)
                results = [
                    re.findall(p, "".join(translator.translate(text)))[0]
                    for text in list(map(lambda x: f"「{x.strip()}」\n", text_list))
                ]
            # 写入结果
            for j in range(len(results)):
                sub.contents[i + j]["cn"] = results[j]
            sub = sub.to_json(cache_file)
            progress_bar.update(batch_size)
    # 输出翻译后字幕
    sub.to_file(output_file)


translator = Translator.from_config("config.yaml")
workspace = translator.workspace
input_dir = workspace.joinpath("inputs")
cache_dir = workspace.joinpath("transl_cache")
output_dir = workspace.joinpath("outputs")
output_dir.mkdir(parents=True, exist_ok=True)
cache_dir.mkdir(parents=True, exist_ok=True)
files = glob(f"{input_dir}/*.lrc") + glob(f"{input_dir}/*.vtt")
for file in files:
    translate_file(file)
