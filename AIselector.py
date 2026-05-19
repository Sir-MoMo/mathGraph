import os

# 1. 基础读取方式（如果变量不存在，会返回 None）
api_key = os.environ.get("GEMINI_API_KEY")

# 2. 严谨的读取方式（针对你的 MATHGRAPH 项目，如果找不到 Key 直接报错拦截，防止后续绘图或 AI 逻辑崩溃）
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("错误：未在系统中检测到 GEMINI_API_KEY 环境变量，请检查配置！")

print(f"成功获取到 API Key，开头为: {api_key[:44]}...")  # 仅展示前4位，保护隐私