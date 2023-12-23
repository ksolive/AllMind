"""
在配置环境时经常会出现为了解决一个bug而去查找一堆问题，最后记不清主线的情况
尝试用chatgpt来记录并总结这种配置过程，自动写一个readme
大概流程是：
1. 用户说开始配环境了，程序开始记录；
2. 用户每次搜索都从程序处进行搜索，程序依次记录；
3. 用户说完成了，程序停止记录，把记录的搜索记录给gpt，让他总结。

ver 0.1:
最简单的实现，用户会提供几乎所有数据，包括搜索目的、访问的搜索结果、搜索结果是否有用，这样gpt只需要将没用的搜索结果踢出掉，然后总结出前后关系就行了。
"""

# ver 0.1
import json

def gptCheckStart(user_input):
    return True

def gptCheckEnd(user_input): 
    return True

def gptSummary(search_list):
    return ""

def main():
    search_list = []
    while True:
        user_input = input()
        # 用gpt来判断是不是控制单元（开始、结束）
        if gptCheckStart(user_input):
            print("debug 开始配环境")
        elif gptCheckEnd(user_input):
            print("debug 配环境结束")
            with open("./search_list.json", "w") as f:
                json.dump(search_list, f)
            break
        else:
            # 把user_input记录到log文件里面,json格式
            search_list.append(user_input)
    summary = gptSummary(search_list)   
    print(summary)
        
            