from config import Config
from google import genai
import os

client = genai.Client(api_key=Config.GEMINI_API_KEY)

# # 使用最新的 Gemini 3.1 Pro 模型
# response = client.models.generate_content(
#     model=Config.DEFAULT_MODEL,
#     contents='我想了解如何缓解落枕的症状，请给我一些建议。'
# )

# print(response.text)

#试着尝试输出当前的ip地址，看看是否能够成功连接到互联网
import requests
def get_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip = response.json()['ip']
        print(f'当前的IP地址是: {ip}')
    except Exception as e:
        print(f'无法获取IP地址: {e}')   