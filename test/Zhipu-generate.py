from zhipuai import ZhipuAI
client = ZhipuAI(api_key="58660068559c405c981d8517a3fb6f6d.K4aIo3hBB4eGkH5F") # 请填写您自己的APIKey

response = client.videos.generations(
    model="cogvideox-2",
    prompt="比得兔开小汽车，游走在马路上，脸上的表情充满开心喜悦。",
    quality="speed",  # 输出模式，"quality"为质量优先，"speed"为速度优先
    with_audio=True,
    size="1920x1080",  # 视频分辨率，支持最高4K（如: "3840x2160"）
    fps=30,  # 帧率，可选为30或60
)
print(response)
