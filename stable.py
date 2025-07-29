import json
import os
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip
import traceback
import numpy as np

# 读取数据
import json
with open("data/example.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 全局变量
OUTPUT_VIDEO = "output.mp4"
BG_FOLDER = "bg"
CG_FOLDER = "cg"
ILLUST_FOLDER = "Texture2D"
AUDIO_FOLDER = "AudioClip"
MESSAGE_IMG = "Texture2D/message.png"  # message.png 路径
FONT_PATH = r"C:\Windows\Fonts\STZHONGS.TTF"  # 请替换为系统字体路径
VIDEO_RESOLUTION = (1280, 720)
FRAME_INTERVAL = 0.5  # 前后段间隔时间（秒）

# 加载字体
font_name = ImageFont.truetype(FONT_PATH, 25)  # 用于角色名字
font_text = ImageFont.truetype(FONT_PATH, 25)  # 用于对话内容

def paste_with_preserve_bg_alpha(bg, fg, position):
    bg = bg.convert("RGBA")
    fg = fg.convert("RGBA")

    x, y = position
    bw, bh = bg.size
    fw, fh = fg.size

    # ==== 1. 计算裁剪区域 ====
    # 背景区域
    bg_x1 = max(x, 0)
    bg_y1 = max(y, 0)
    bg_x2 = min(x + fw, bw)
    bg_y2 = min(y + fh, bh)

    if bg_x1 >= bg_x2 or bg_y1 >= bg_y2:
        return bg  # 完全在画布外，不需要合成

    # 前景区域
    fg_x1 = bg_x1 - x
    fg_y1 = bg_y1 - y
    fg_x2 = fg_x1 + (bg_x2 - bg_x1)
    fg_y2 = fg_y1 + (bg_y2 - bg_y1)

    # ==== 2. 转 numpy ====
    bg_arr = np.array(bg, dtype=np.float32)
    fg_arr = np.array(fg, dtype=np.float32)

    sub_bg = bg_arr[bg_y1:bg_y2, bg_x1:bg_x2, :]
    sub_fg = fg_arr[fg_y1:fg_y2, fg_x1:fg_x2, :]

    # ==== 3. Alpha 混合（保持 bg alpha 不变）====
    fg_alpha = sub_fg[..., 3:4] / 255.0
    sub_bg[..., :3] = sub_fg[..., :3] * fg_alpha + sub_bg[..., :3] * (1 - fg_alpha)
    # sub_bg[..., 3] 保持不变

    # ==== 4. 放回去 ====
    bg_arr[bg_y1:bg_y2, bg_x1:bg_x2, :] = sub_bg
    return Image.fromarray(bg_arr.astype(np.uint8), "RGBA")

def draw_text_with_border(draw, position, text, font, fill, border_color='black', border_width=0.7, line_spacing=5):
    x, y = position
    lines = text.split('\n')  # 根据换行符分割文本
    
    # 偏移量设置
    offsets = [(-border_width, -border_width), (border_width, -border_width),
               (-border_width, border_width), (border_width, border_width)]
    
    # 绘制每一行的描边
    for line in lines:
        for offset in offsets:
            draw.text((x + offset[0], y + offset[1]), line, font=font, fill=border_color)
        # 绘制每一行的文字
        draw.text((x, y), line, font=font, fill=fill)
        # 更新y坐标，加上行高和行距
        y += font.getbbox(line)[1] + line_spacing

def draw_bold_text(draw, position, text, font, fill, thickness=2, line_spacing=5):
    x, y = position
    lines = text.split('\n')  # 根据换行符分割文本
    
    # 用不同的偏移量多次绘制文字来模拟加粗
    for line in lines:
        for dx in range(-thickness, thickness + 1):
            for dy in range(-thickness, thickness + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx * 0.1, y + dy * 0.1), line, font=font, fill=fill)
        # 绘制原始文字
        draw.text((x, y), line, font=font, fill=fill)
        # 更新 y 坐标，加上行高和行距
        y += font.getbbox(line)[1] + line_spacing

# 创建对话框
def create_dialogue_box(char_name, text, line_spacing=25):  # 增加行距参数
    img = Image.open(MESSAGE_IMG).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 角色名字绘制（黑色部分）
    name_pos = (223, 5)  # 起点坐标
    #draw_bold_text(draw, name_pos, char_name, font=font_name, fill="white", line_spacing=line_spacing)
    draw.text(name_pos, char_name, font=font_name, fill='white')

    # 对话绘制（蓝色部分）
    text_start_x = 235  # 对齐蓝色部分左五分之一处
    text_start_y = 48
    draw_text_with_border(draw, (text_start_x, text_start_y), text, font=font_text, fill="white", line_spacing=line_spacing)

    return img

# 生成视频帧
def generate_frame(entry):
    print(entry)
    pic = entry['pic']
    char_name = entry['char']
    text = entry['chs']
    voice_path = os.path.join(AUDIO_FOLDER, entry['voice'])

    # 加载背景
    if pic['type'] in ['bg', 'normal']:
        bg_path = os.path.join(BG_FOLDER, pic['bg'])
    elif pic['type'] == 'cg':
        bg_path = os.path.join(CG_FOLDER, pic['cg'])
    else:
        raise ValueError("Unknown picture type")

    bg = Image.open(bg_path).resize(VIDEO_RESOLUTION)

    # 如果是人物插图，叠加角色
    if pic['type'] == 'normal':
        char_illust_path = os.path.join(ILLUST_FOLDER, pic['illust'])
        char_img = Image.open(char_illust_path)

        # 判断是否是 large
        if 'large' in pic['illust']:
            char_img = char_img.crop((0, 190, 1500, 1200))
        else:
            w, h = char_img.size
            char_img = char_img.crop((0, 40, w, h))

        # 合成角色和背景
        bg = paste_with_preserve_bg_alpha(
            bg,
            char_img,
            (VIDEO_RESOLUTION[0] // 2 - char_img.width // 2, 0)
        )
        #bg.paste(char_img, (VIDEO_RESOLUTION[0] // 2 - char_img.width // 2, 0), char_img)

    # 添加对话框
    dialogue_box = create_dialogue_box(char_name, text)
    bg = paste_with_preserve_bg_alpha(
        bg,
        dialogue_box,
        (0, VIDEO_RESOLUTION[1] - dialogue_box.height)
    )
    #bg.paste(dialogue_box, (0, VIDEO_RESOLUTION[1] - dialogue_box.height), dialogue_box)

    return bg, voice_path

if __name__ == '__main__':
    # 主逻辑
    clips = []
    for entry in data:
        try:
            frame, voice_path = generate_frame(entry)

            # 保存帧为临时图像
            temp_frame_path = "temp_frame.png"
            frame.save(temp_frame_path)

            # 创建视频剪辑
            image_clip = ImageClip(temp_frame_path)
            if voice_path:
                audio_clip = AudioFileClip(voice_path)
                image_clip = image_clip.with_audio(audio_clip)
            image_clip = image_clip.with_duration(audio_clip.duration)

            blank_frame = ImageClip(temp_frame_path).with_duration(FRAME_INTERVAL / 2)

            clips.extend([blank_frame, image_clip, blank_frame])
        except Exception as e:
            traceback.print_exc()
            input()
        #input('next')
        
    # 合并所有剪辑
    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(OUTPUT_VIDEO, fps=24)
