# hoshishiro

[游戏官方网站](http://shiratamaco.com/)

初衷是做[这些视频](https://space.bilibili.com/476232350/lists/5105429)。

仓库只有[原台本文件](https://github.com/788009/hoshishiro/blob/main/MonoBehaviour/hoshishiro_01.book.json)和[文件名对照文件](https://github.com/788009/hoshishiro/blob/main/MonoBehaviour/Chapter01.chapter.json)，其他素材请自行使用 [AssetStudio](https://github.com/Perfare/AssetStudio) 拆包获取，并填入 `bg`、`cg`、`AudioClip` 和 `Texture2D` 中，导出时图片选择 `png` 格式，音频选择 `wav` 格式。

以下所有内容均基于游戏的官中版本，其他版本在一些细节上有所差异，尤其是 `hoshishiro_01.book` 和 `Chapter01.chapter`。

## 代码说明

### [extractChars.py](https://github.com/788009/hoshishiro/blob/main/extractChars.py)

这个程序不需要拆包获取其他文件。

提取指定角色的台本数据，包含中日文本、对应音频和画面，具体格式可自行提取查看。

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

### [simpleJoin.py](https://github.com/788009/hoshishiro/blob/main/simpleJoin.py)

读取 AudioClip 中的所有音频并按照字典序拼接。

### [stable.py](https://github.com/788009/hoshishiro/blob/main/stable.py)

生成视频的核心代码，从一个 JSON 文件中读取画面信息，并使用各文件夹内的素材，合成视频，该 JSON 文件内数据的格式与 `extractChars.py` 的输出相同。

修改第 9 行的文件路径，并在 `bg`、`cg`、`AudioClip` 和 `Texture2D` 中填入相应的素材，运行即可。

台词背景为 `data/message.png`，对应包内图片 `window_messageName`，但与原图尺寸略有不同，因此请勿改动。

字体使用 `STZHONGS.TTF`，请确保存在路径 `C:\Windows\Fonts\STZHONGS.TTF`，或者更改第 20 行 `FONT_PATH` 的值。

若要生成主要角色的所有语音，耗时可能极长，且对电脑内存有要求。

### [generate_frame.py](https://github.com/788009/hoshishiro/blob/main/generate_frame.py)

生成包含背景、人物和台词的图片，直接调用 `stable.py` 中的函数。

### processxxx.py

从 [Chapter01.chapter.json](https://github.com/788009/hoshishiro/blob/main/MonoBehaviour/Chapter01.chapter.json) 中提取其他代码需要用到的 `data/xxx.json`，已生成，无需再次操作。

## 拆包细节

用 AssetStudio 可直接获取所有素材，不需要手动解密。

涉及到角色的 `tgtEng` 值[见上](https://github.com/788009/hoshishiro?tab=readme-ov-file#extractcharspy)。

### 文本

#### 台本

所有台词、音频（文件名，不是音频文件）和画面信息（背景、角色立绘、CG）都在 `hoshishiro_01.book` 中，以 JSON 格式存储，具体结构过于复杂，不在此赘述。

#### 其他

即 `Chapter01.chapter`，亦以 JSON 格式存储，内容包括但不限于：

- BG、CG 别名
- 立绘差分别名
- 角色名字的中日英三语
- BGM 名称、SE 内容

其中前三者在本仓库有单独提取的版本，分别是 [BCGs.json](https://github.com/788009/hoshishiro/blob/main/data/BCGs.json)、[chars.json](https://github.com/788009/hoshishiro/blob/main/data/chars.json) 和 [names.json](https://github.com/788009/hoshishiro/blob/main/data/names.json)（仅中日），音频相关内容列于下文。

### 音频

#### 语音

文件名示例：`kar0001`，表示狩叶的第一条语音，`kar` 是狩叶对应的 `tgtEng` 的前三个字母，其他角色同理。

有些语音名字后有 `_b`，如 `noi0416_b`，可能是配音时改动重新配的音（参考[贴吧](https://tieba.baidu.com/p/7474577881)）。

数字大于等于 `6000` 的，如 `kar6000`，是游戏[各个宣传片](https://www.youtube.com/watch?v=MEJC0FsCido&list=PL-PtwSDik6nTAPjGgkBUGY8IMr9A4LAUx)中的语音。

#### BGM

`bgm01` - `bgm11`

<details>
<summary>曲名对照</summary>

|文件名|曲名|备注|
|-|-|-|
|`bgm01`|星空鉄道ミルキーウェイ||
|`bgm02`|気ままな日常||
|`bgm03`|星の海||
|`bgm04`|列車はゆく||
|`bgm05`|猫耳としっぽ||
|`bgm06`|cutie conductor|狩叶搞事曲|
|`bgm07`|おかえりなさい|音理|
|`bgm08`|暗影|恐怖场景|
|`bgm09`|砕け散る星|如泣如诉|
|`bgm10`|終わらない旅||
|`bgm11`|OPのピアノVer|スタートリップ Piano Ver.|

</details>

#### 音效

`SE001` - `SE054`  
`SE100` - `SE103`

<details>
<summary>内容对照（日语）</summary>

|文件名|内容|
|-|-|
|`SE001`|蒸気機関車：汽笛|
|`SE002`|蒸気機関車：停止するためにブレーキ|
|`SE003`|蒸気機関車：停車中|
|`SE004`|蒸気機関車：走行中|
|`SE005`|木製ドア開く|
|`SE006`|抱きつく音|
|`SE007`|ライターの音|
|`SE008`|ベル|
|`SE009`|エンジン始動音|
|`SE010`|倒れる音|
|`SE011`|紙めくる|
|`SE012`|金属開ける|
|`SE013`|シューという蒸気音|
|`SE014`|セミの声|
|`SE015`|冷蔵庫開ける音|
|`SE017`|蒸気機関車_蒸気を出す音|
|`SE018`|椅子から立ち上がる|
|`SE021`|天窓閉める|
|`SE022`|缶を置く１|
|`SE023`|プルタブ開ける|
|`SE024`|プルタブ開ける（ビール）|
|`SE024a`|プルタブ開ける（ビール）|
|`SE025`|木製ドア強く開く|
|`SE026`|スケッチブックに鉛筆で書く|
|`SE027`|水をかける|
|`SE028`|手を合わせる|
|`SE029`|ビニールがさ|
|`SE030`|手持ち花火|
|`SE031`|線香花火|
|`SE032`|カーテン開ける|
|`SE033`|南京錠鍵をあける|
|`SE034`|木製扉あける（重め）|
|`SE035`|予告ベル|
|`SE036`|心臓の音|
|`SE036b`|心臓の音（トクントクン|
|`SE037`|アパートの鍵ドア開ける（ガチャ|
|`SE038`|アパートの鍵開ける（ガチャ|
|`SE039`|アパートのドア開ける（ガチャン|
|`SE040`|アパートのドア叩く（ガンガンガンガン|
|`SE041`|茂み（ガサッ|
|`SE042`|冷蔵庫を開ける|
|`SE043`|スケッチブックのページをめくる|
|`SE044`|コケる（どしーん|
|`SE045`|自動ドア開く|
|`SE046`|物がさごそ|
|`SE047`|病室のドアに触れる（ガチャ|
|`SE048`|病室のスライドドアを開ける|
|`SE049`|物音（ガタッ|
|`SE050`|猫の声|
|`SE051`|ざわめき|
|`SE052`|病室ドア閉める|
|`SE053`|叩かれる|
|`SE054`|心電図音|
|`SE100`|足音_ノワール_歩く|
|`SE101`|足音_ノワール_走る|
|`SE102`|足音_女性_歩く|
|`SE103`|足音_女性_走る|

</details>

### 视频

筛选 `VideoClip` 只有两个文件：`OP` 和 `ED`。

### 图片

全部属于 `Texture2D`。

#### BG 与 CG

筛选 `Texture2D` 后分别搜索 `bg` 和 `evcg`，除 `TutorialBg1` 和 `TutorialBg2` 之外都是用到的素材。

#### 角色立绘

筛选 `Texture2D` 后搜索所需角色的 `tgtEng`。

#### 其他

`stable.py` 中还需要用到 `window_messageName`，即台词背景。

## 声明

提取的素材仅供交流学习，均归しらたまこ所有。