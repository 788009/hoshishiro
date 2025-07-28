from stable import generate_frame

entry = {
    "pic": {
        "type": "normal",
        "char": "カルハ",
        "illust": "karuha_11face.png",
        "bg": "bg020a.png"
    },
    "char": "狩叶",
    "chs": "这座城市好奇怪呀，空无一人。",
    "jp": "ねえ、この街変なのよ、誰もいないの。",
    "voice": "kar1053.wav"
}

frame, voice_path = generate_frame(entry)
temp_frame_path = "temp_frame.png"
frame.save(temp_frame_path)

