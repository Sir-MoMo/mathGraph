from google import genai
from config import Config
import os

def get_latest_models(output_filename="models_result.txt"):
    """
    获取最新的模型并将其保存到文件中。
    """
    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    
    # 使用 with open 语句来确保文件在写入后能被正确关闭
    with open(output_filename, "w", encoding="utf-8") as f:
        # 准备要写入文件的头部信息
        header = f"{'模型 ID':<40} | {'支持功能'}\n"
        separator = "-" * 60 + "\n"
        
        # 将头部信息写入文件
        f.write(header)
        f.write(separator)
        
        # 获取所有模型列表
        for m in client.models.list():
            # 过滤出支持生成内容（generateContent）的模型
            if 'generateContent' in m.supported_actions:
                # 准备要写入文件的每一行模型信息
                line = f"{m.name:<40} | {m.display_name}\n"
                # 将模型信息写入文件
                f.write(line)
                
    # 在终端打印成功的消息
    print(f"模型列表已成功保存到 {output_filename}")

if __name__ == "__main__":
    try:
        get_latest_models()
    except Exception as e:
        print(f"获取失败: {e}")
