from zhipuai import ZhipuAI
client = ZhipuAI(api_key="58660068559c405c981d8517a3fb6f6d.K4aIo3hBB4eGkH5F") # 请填写您自己的APIKey

response = client.videos.retrieve_videos_result(
    id="13371748747042288-8666098929308469048"
)
print(response)