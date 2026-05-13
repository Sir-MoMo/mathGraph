from google import genai
from config import Config
import os

def get_latest_models():
    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    print(f"{'模型 ID':<40} | {'支持功能'}")
    print("-" * 60)
    
    # 获取所有模型列表
    for m in client.models.list():
        # 过滤出支持生成内容（generateContent）的模型
        if 'generateContent' in m.supported_actions:
            print(f"{m.name:<40} | {m.display_name}")

if __name__ == "__main__":
    try:
        get_latest_models()
    except Exception as e:
        print(f"获取失败: {e}")


