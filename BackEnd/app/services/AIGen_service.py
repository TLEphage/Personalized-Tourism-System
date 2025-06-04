import requests
import logging
import os
import uuid
import base64
from app.config import VIDEO_DIR, AI_VIDEO_TASK
from app.services.diary_service import diary_append
from utils.file_utils import read_json, write_json
from zhipuai import ZhipuAI

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置智谱清影API Key
ZHIPUAI_API_KEY = "58660068559c405c981d8517a3fb6f6d.K4aIo3hBB4eGkH5F"  # 替换为你的API Key
ZHIPUAI_API_URL = "https://open.bigmodel.cn/api/paas/v4/videos/generations"
client = ZhipuAI(api_key=ZHIPUAI_API_KEY)

def generate_video_api(image_url: str, prompt: str, quality: str):
    """调用智谱清影API生成视频"""
    if not image_url:
        response = client.videos.generations(
            model="cogvideox-2",
            prompt=prompt,
            quality=quality,  # 输出模式，"quality"为质量优先，"speed"为速度优先
            with_audio=True,
            size="1920x1080",  # 视频分辨率，支持最高4K（如: "3840x2160"）
            fps=30,  # 帧率，可选为30或60
        )
    else:
        with open(image_url, "rb") as image_file:
            base64_data = base64.b64encode(image_file.read()).decode('utf-8')
        response = client.videos.generations(
            model="cogvideox-2",
            image_url=base64_data,  # 提供的图片URL地址或者 Base64 编码
            prompt=prompt,
            quality=quality,  # 输出模式，"quality"为质量优先，"speed"为速度优先
            with_audio=True,
            size="1920x1080",  # 视频分辨率，支持最高4K（如: "3840x2160"）
            fps=30,  # 帧率，可选为30或60
        )
    
    print(response)
    if(response.task_status == "PROCESSING"):
        print("正在生成视频")
        return response.id
    elif(response.task_status == "SUCCESS"):
        print("视频已生成")
        return response.id
    else:
        print("视频生成失败")
        return -1

def generate_video_request(
    username: str,
    diary_id: int,
    image_url: str,
    prompt: str,
    quality:str
) -> dict :
    task_cache = read_json(AI_VIDEO_TASK)
    try:
        logger.info(f"生成视频请求，提示词: {prompt}")
        task_id = generate_video_api(image_url, prompt, quality)
        if task_id == -1:
            logger.error(f"视频生成失败: {str(e)}")
            raise Exception("视频生成失败")
        
        new_task = {
            "task_id": task_id,
            "output_path": username,
            "diary_id": diary_id,
            "prompt": prompt,
            "quality": quality
        }
        task_cache.append(new_task)
        write_json(AI_VIDEO_TASK, task_cache)
        logger.info(f"视频生成任务已创建，任务ID: {task_id}")
        return {"message": f"视频生成任务已创建，任务ID: {task_id}"}
    except Exception as e:
        logger.error(f"视频生成失败: {str(e)}")
        raise Exception("视频生成失败")

def check_video_status(task_id: str) -> dict:
    """检查视频生成状态"""
    response = client.videos.retrieve_videos_result(
        id=task_id
    )
    print(response)
    if(response.task_status == "PROCESSING"):
        print("正在生成视频")
        return {"message": "正在生成视频", "result": []}
    elif(response.task_status == "SUCCESS"):
        print("视频已生成")
        video_list = []
        for video in response.video_result:
            video_list.append(video.url)
        return {"message": "视频已生成", "result": video_list}
    else:
        print("视频生成失败")
        return {"message": "视频生成失败", "result": []}
    
def download_video(url: str, output_path: str) -> dict:
    """下载视频到指定路径"""
    output_path = output_path.lstrip("/")
    output_path = output_path.rstrip("/")
    saved_url = f"http://localhost:8000/videos/{output_path}/"
    output_path = os.path.join(VIDEO_DIR, output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    filename = f"{uuid.uuid4()}.mp4"
    file_path = os.path.join(output_path, filename)
    saved_url = saved_url+filename
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    return {"message": "视频下载成功", "filename": filename, "file_path": file_path, "url": saved_url}

def check_all_video_status():
    task_cache = read_json(AI_VIDEO_TASK, [])
    new_task_cache = []
    for task in task_cache:
        response = check_video_status(task.get("task_id"))
        if response.get("message") == "视频已生成":
            video_list = response.get("result")
            for video in video_list:
                video_info = download_video(video, task.get("output_path"))
                diary_append(task.get("diary_id"), "videos", video_info.get("url"))

        elif response.get("message") == "正在生成视频":
            new_task_cache.append(task)

    write_json(AI_VIDEO_TASK, new_task_cache)
    return {"message": "视频列表状态已更新", "remaining_tasks": len(new_task_cache)}
