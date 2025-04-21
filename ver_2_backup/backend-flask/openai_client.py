from openai import OpenAI
import json

api_key = ""
with open("keys.json", "r") as f:
    keys = json.load(f)
    api_key = keys["openai_api_key"]

client = OpenAI(api_key=api_key)

def get_openai_response(prompt, chat_history):
    """调用 OpenAI GPT 生成 AI 回复，利用聊天记录上下文"""
    try:
        # 构建完整的对话上下文，确保格式符合 OpenAI 最新规范
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a helpful assistant."}]
            }
        ]
        
        # 遍历历史记录，构造符合格式的 message 列表
        for entry in chat_history:
            messages.append({
                "role": "user",
                "content": [{"type": "text", "text": entry['user']}]
            })
            messages.append({
                "role": "assistant",
                "content": [{"type": "text", "text": entry['ai']}]
            })
        
        # 添加当前用户输入
        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        })
        
        # 调用 OpenAI 生成回复
        completion = client.chat.completions.create(
            model="gpt-4o",  # GPT-4o 模型
            messages=messages, # type: ignore
            max_tokens=200,
            temperature=0.7
        )
        
        # 返回 AI 生成的文本
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"