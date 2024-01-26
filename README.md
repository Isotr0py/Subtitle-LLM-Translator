# Subtitle-LLM-Translator
## 介绍
- 使用[Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)进行日语字幕转录
- 使用[Sakura-13B-Galgame](https://github.com/SakuraLLM/Sakura-13B-Galgame)模型对字幕文件进行翻译

## 准备
- **如果你只有mp3、mp4等音频文件，可先用[Faster-Whisper-Colab](https://colab.research.google.com/github/Isotr0py/Sakura-Subtitle/blob/main/whisper/Faster-Whisper-Colab.ipynb)进行字幕转录**
- **按照[Sakura模型部署教程](https://github.com/SakuraLLM/Sakura-13B-Galgame/wiki)完成API部署，并在`config.yaml`的`endpoint`填入你的API地址**

## 运行
- 安装库
```
pip install -r requirements.txt
```
- 将需要翻译的字幕文件放入`sample_project/inputs`
- 运行`main.py`:
```
python main.py
```
- 翻译完成的字幕将输出于`sample_project/outputs`目录
