from config import Config
from google import genai
import os

client = genai.Client(api_key=Config.GEMINI_API_KEY)

# 使用最新的 Gemini 3.1 Pro 模型
response = client.models.generate_content(
    model=Config.DEFAULT_MODEL,
    contents='我想了解如何缓解落枕的症状，请给我一些建议。'
)

print(response.text)