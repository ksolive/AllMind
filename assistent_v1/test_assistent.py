# from functions import get_city_for_date
# from dall_e_3 import get_dalle_image
# from assistant import create_assistant, create_thread, get_completion

from utils import create_assistant, create_thread, get_completion, get_dalle_image, search_oline, get_city_for_date
from prompts import black_cat_instructions

# 定义数据模型
    
DEBUG = True

# 创建 Assistant
assistant_id = create_assistant(
    name="测试机",
    instructions=black_cat_instructions,
    model="gpt-4-1106-preview",
    tools=[
        {
            "type": "retrieval"  # 知识检索
        },
        {
            "type": "code_interpreter"  # 代码解释器 好像会导致他自动写很多程序。
        },
        {
            "type": "function",  # 函数调用是 每隔函数自动调用的
            "function": {
                "name": "get_city_for_date",
                "description": "根据传入的日期获取对应的城市.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date_str": {
                            "type": "string",
                            "description": "用于获取对应城市的日期，格式为YYYY-MM-DD."
                        },
                    },
                    "required": ["date_str"]
                }
            }
        },
        {
            "type": "function",  # 在线搜索
            "function": {
                "name": "search_oline",
                "description": "使用谷歌搜索，用于解决黑猫的好奇问题",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "好奇的问题，即搜索关键词"
                        },
                    },
                    "required": ["question"]
                }
            }
        },
        {
            "type": "function",  # 用于获取图片
            "function": {
                "name": "get_dalle_image",
                "description": "根据传入的prompt生成图片.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Prompt of DALL-E 3."
                        },
                    },
                    "required": ["prompt"]
                }
            }
        }
    ],
    files=["/Users/ksolive/Documents/LittleInteresting/AllMind/test_assistent/files/knowledge.txt"],
    debug=DEBUG
)

# 创建函数调用列表
funcs = [get_city_for_date, search_oline, get_dalle_image]

def test():
    # assistant_id = create_assistant
    assistant_name = "raavi"
    assistant_id = create_assistant(assistant_name)
    thread_id = create_thread(debug=DEBUG)
    while(True):
        user_input = input("\n-------user-------\n")
        if user_input == "exit":
            return
        message = get_completion(assistant_id, thread_id, user_input, funcs, debug=DEBUG)
        print("--------gpt--------\n")
        if isinstance(message, dict) and "image" in message.keys():
            print("is image")
        else:
            print(message)

test()