import subprocess

def spotlight_search(query):
    command = ['mdfind', query]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(f"Error: {error.decode('utf-8')}")
    else:
        result = output.decode('utf-8')
        if result:
            print("Search Results:")
            print(result)
        else:
            print("No results found.")

# 在这里调用函数并传入要搜索的内容（例如文件名）
spotlight_search("example.txt")
