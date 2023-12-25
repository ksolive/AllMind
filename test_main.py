from openai import OpenAI
client = OpenAI()
# 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
def gptCheckStart(user_input):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": "判断用户输入是否与'配置环境'、“安装程序”有相似意思：输出yes或no"
        },
        {
        "role": "user",
        "content": user_input
        },
    ],
    temperature=0,
    max_tokens=1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    if response['choices'][0]['message']['content'] == 'yes':
        return True
    else:
        return False

gptCheckStart("我要开始安装sgx了，请记录步骤")