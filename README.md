# hoshishiro

初衷是做[这些视频](https://space.bilibili.com/476232350/lists/5105429)。

仓库只有[原台本文件](https://github.com/788009/hoshishiro/blob/main/MonoBehaviour/hoshishiro_01.book.json)和[文件名对照文件](https://github.com/788009/hoshishiro/blob/main/MonoBehaviour/Chapter01.chapter.json)，其他素材请自行使用 [AssetStudio](https://github.com/Perfare/AssetStudio) 拆包获取，并填入 `bg`、`cg`、`AudioClip` 和 `Texture2D` 中。

## [extractChars.py](https://github.com/788009/hoshishiro/blob/main/extractChars.py)

这个程序不需要拆包获取其他文件。

提取指定角色的台本数据，包含中日文本、对应音频和画面，具体可自行提取查看。

修改 51、52 行的人名，运行即可，输出在 `data/{tgtEng}.json` 中，主要角色对照表：

|`target`|`tgtEng`|中文|
|:-:|:-:|:-:|
|ノワール|noir|诺瓦|
|カルハ|karuha|狩叶|
|ねり|neri|音理|
|ジビエ|jibie|野鸟|
|花江|hanae|花江|
|タカセ|takase|鹰世|
|真白|mashiro|真白|

无法提取男主的台词，因为最粗（最表层）的定位是 `if tgtEng in strings[10]`，而 `strings[10]` 是音频文件名，男主此项为空。

## [simpleJoin.py](https://github.com/788009/hoshishiro/blob/main/simpleJoin.py)

读取 AudioClip 中的所有音频并按照字典序拼接。

## [stable.py](https://github.com/788009/hoshishiro/blob/main/stable.py)

生成视频的核心代码，修改第 9 行的文件名，并在 `bg`、`cg`、`AudioClip` 和 `Texture2D` 中填入相应的素材，运行即可。

若要生成主要角色的所有语音，耗时可能极长，且对电脑内存有要求。

## [generate_frame.py](https://github.com/788009/hoshishiro/blob/main/generate_frame.py)

生成包含背景、人物和台词的图片，直接调用 `stable.py` 中的函数。

## processxxx.py

生成 `data/xxx.py`，已生成，无需再次操作。
