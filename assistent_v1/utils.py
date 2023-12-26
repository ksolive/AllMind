import os
import re
import json
import time
from openai import OpenAI
import base64
import requests
import random
import datetime
from key import OPENAI_API_KEY, GOOGLE_API_KEY, SEARCH_ENGINE_ID


# <script async src="https://cse.google.com/cse.js?cx=470eb62025ea0427f">
# </script>
# <div class="gcse-search"></div>

# 实例化 OpenAI 客户端
client = OpenAI(api_key=OPENAI_API_KEY, timeout=600)

# 创建或加载 Assistant
def create_assistant(name="Assistant", instructions="You are a helpful assistant.", model="gpt-4-1106-preview", tools=None, files=None, debug=False):
    """
    Creates an assistant with the given name, instructions, model, tools, and files.

    Args:
        name (str, optional): The name of the assistant. Defaults to "Assistant".
        instructions (str, optional): The instructions for the assistant. Defaults to "You are a helpful assistant.".
        model (str, optional): The model to use for the assistant. Defaults to "gpt-4-1106-preview".
        tools (list, optional): The list of tools to provide to the assistant. Defaults to None.
        files (list or str, optional): The list of files or a single file to upload and associate with the assistant. Defaults to None.

    Returns:
        str: The ID of the created assistant.
    """
    assistant_file_path = "assistant.json"
    assistant_json = []
    # 如果存在同名 assistant 则读取
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, "r") as file:
            assistant_json = json.load(file)
            for assistant_data in assistant_json:
                assistant_name = assistant_data["assistant_name"]
                if assistant_name == name:
                    assistant_id = assistant_data["assistant_id"]
                    print("加载已经存在的 Assistant ID")
                    if debug:
                        print("Assistant ID: ", assistant_id)
                    return assistant_id

    # 上传文件并获取 file_ids
    file_ids = []
    if files:
        if isinstance(files, list):
            for file in files:
                file = client.files.create(
                    file=open(file, "rb"),
                    purpose='assistants'
                )
                file_ids.append(file.id)
        elif isinstance(files, str):
            file = client.files.create(
                file=open(files, "rb"),
                purpose='assistants'
            )
            file_ids.append(file.id)

    # 创建 Assistant
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=tools,
        file_ids=file_ids
    )

    assistant_id = assistant.id
    assistant_name = assistant.name
    
    # 保存 Assistant 信息
    assistant_json.append(
        {
            "assistant_name": assistant_name,
            "assistant_id": assistant_id
        }
    )
    with open(assistant_file_path, "w", encoding="utf-8") as file:
        json.dump(assistant_json, file, ensure_ascii=False, indent=4)
        print("已保存 Assistant 信息")
        
    return assistant_id

# 创建 Thread
def create_thread(debug=False):
    """
    Creates a new thread.

    Returns:
        str: The ID of the newly created thread.
    """
    thread = client.beta.threads.create()
    if debug:
        print("Thread ID: ", thread.id)
    return thread.id

# 获取回答
def get_completion(assistant_id, thread_id, user_input, funcs, debug=False):
    """
    Executes a completion request with the given parameters.

    Args:
        assistant_id (str): The ID of the assistant.
        thread_id (str): The ID of the thread.
        user_input (str): The user input content.
        funcs (list): A list of functions.
        debug (bool, optional): Whether to print debug information. Defaults to False.

    Returns:
        str: The message as a response to the completion request.
    """
    if debug:
        print("获取回答...")
        
    # 创建 Message
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    # 创建 Run
    run = client.beta.threads.runs.create(
      thread_id=thread_id,
      assistant_id=assistant_id,
    )

    # 运行 Run
    while True:
        while run.status in ['queued', 'in_progress']:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            time.sleep(1)

        # 执行 function
        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            for tool_call in tool_calls:
                if debug:
                    print(str(tool_call.function))
                func = next(iter([func for func in funcs if func.__name__ == tool_call.function.name]))
                try:
                    output = func(**eval(tool_call.function.arguments))
                except Exception as e:
                    output = "Error: " + str(e)

                if debug:
                    print(f"{tool_call.function.name}: ", output)
                
                tool_outputs.append(
                    {
                        "tool_call_id": tool_call.id, 
                        "output": json.dumps(output)
                    }
                )

            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        elif run.status == "failed":
            raise Exception("Run Failed. Error: ", run.last_error)
        else:
            messages = client.beta.threads.messages.list(
                thread_id=thread_id
            )
            message = messages.data[0].content[0].text.value
            pattern = r"/imgs/\d{10}\.png"
            match = re.search(pattern, message)
            if match:
                message = {"image": match.group()}
            if debug:
                print(message)
            return message

def get_dalle_image(prompt):
    """
    Generate an image based on a given prompt using the DALL-E model.

    Parameters:
    - prompt (str): The prompt for generating the image.

    Returns:
    - img_file_path (str): The file path of the generated image.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    # 获取当前时间戳
    timestamp = int(time.time())
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        quality="hd",
        size="1792x1024",
        # style="natural",
        response_format='b64_json',
    )
    img_b64 = response.data[0].b64_json
    # 保存图片
    img_name = f"{timestamp}.png"
    img_file_path = f"imgs/{img_name}"
    with open(img_file_path, "wb") as f:
        f.write(base64.b64decode(img_b64))
    # 绘制图片
    # imgs = base64_to_img(img_b64)
    # plt.imshow(imgs)
    # plt.axis('off')
    # plt.show()
    return {"image": "/imgs/" + img_name}

def search_oline(question):

    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': question,
        'num': 3  # 限制搜索结果数量为3
    }
    try:
        response = requests.get(base_url, params=params)
        results = response.json()
        search_data = {
            "search_query": question,
            "total_results": results['searchInformation']['totalResults'],
            "results": []
        }
        if 'items' in results:
            for item in results['items']:
                result_item = {
                    "title": item['title'],
                    "link": item['link'],
                    "snippet": item.get('snippet', '')
                }
                search_data["results"].append(result_item)
        return search_data
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

def get_city_list():
    """
    Retrieves a list of city names from a JSON file and returns the shuffled list.

    Returns:
        list: A list of city names.
    """
    city_list = []
    with open('/Users/ksolive/Documents/LittleInteresting/AllMind/test_assistent/files/city.json', 'r') as f:
        data = json.load(f)
        for province in data['provinces']:
            for city in province['citys']:
                city_list.append(city['cityName'])
    random.shuffle(city_list)
    return city_list


def generate_city_mapping(year):
    """
    Generates a mapping of dates to cities based on the given year.

    Parameters:
        year (int): The year for which the mapping needs to be generated.

    Returns:
        dict: A dictionary containing the mapping of dates to cities.
    """
    city_mapping = {}
    city_list = get_city_list()
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    delta = datetime.timedelta(days=1)
    current_date = start_date
    while current_date <= end_date:
        city_mapping[current_date] = city_list[current_date.timetuple().tm_yday % len(city_list) - 1]
        current_date += delta
    return city_mapping


def get_city_for_date(date_str):
    """
    Given a date string, this function returns the corresponding city for that date.

    Args:
        date_str (str): A string representing a date in the format "YYYY-MM-DD".

    Returns:
        str: The city corresponding to the given date.

    Raises:
        ValueError: If the date string is not in the correct format.

    Examples:
        >>> get_city_for_date("2022-01-01")
        '烟台市'
        >>> get_city_for_date("2022-12-25")
        '北京市'
    """
    date_format = "%Y-%m-%d"
    try:
        input_date = datetime.datetime.strptime(date_str, date_format).date()
    except ValueError:
        return "无效日期格式。请使用YYYY-MM-DD格式。"
    year_mapping = generate_city_mapping(input_date.year)
    return year_mapping.get(input_date, "日期不在当前年份内")