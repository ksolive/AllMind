import time
from openai import OpenAI
import base64
import requests
from key import OPENAI_API_KEY, GOOGLE_API_KEY, SEARCH_ENGINE_ID

def draw(prompt):
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

def search(question):

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


import edge_tts  
import glob
import os

def get_max_index(directory):
    mp3_files = glob.glob(os.path.join(directory, '*.mp3'))
    indices = [0]  # 默认从 0 开始
    for file in mp3_files:
        file_name = os.path.basename(file)
        try:
            index = int(file_name.split('_')[2].split('.')[0])  # 假设文件名格式为 test_tts_index.mp3
            indices.append(index)
        except ValueError:
            pass
    return max(indices)

async def tts(sentence, VOICE="zh-CN-XiaoyiNeural", OUTPUT_DIR="voice"):
    max_index = get_max_index(OUTPUT_DIR)
    new_index = max_index + 1
    new_filename = f"tts_{new_index}.mp3"
    communicate = edge_tts.Communicate(sentence, VOICE)  
    await communicate.save(new_filename) 
