from datetime import datetime
import json
import threading
import time

class QueueData:
    def __init__(self, content, type):
        self.timestamp = datetime.now()
        self.content = content
        self.type = type

    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'content': self.content,
            'type': self.type
        }
    
    def to_string(self):
        return f"{self.timestamp.isoformat()} - {self.type}: {self.content}"

class FileQueue:
    _instances = {}

    def __new__(cls, file_name):
        if file_name not in cls._instances:
            cls._instances[file_name] = super().__new__(cls)
        return cls._instances[file_name]

    def __init__(self, file_name):
        if not hasattr(self, 'initialized'):
            self.file_name = file_name
            self.lock = threading.Lock()
            self.initialized = True

    def write(self, data):
        with self.lock:
            with open(self.file_name, 'a') as file:
                file.write(json.dumps(data) + '\n')

    def read(self):
        with self.lock:
            with open(self.file_name, 'r+') as file:
                lines = file.readlines()
                if lines:
                    # 从文件中读取一行数据并返回为QueueData对象
                    data = json.loads(lines[0])
                    file.seek(0)  # 将文件指针移至开头
                    file.writelines(lines[1:])  # 删除已读取的数据行
                    file.truncate()  # 截断文件，删除多余内容
                    return QueueData(data['content'], data['type'])
                else:
                    return None

    def read_all(self):
        with self.lock:
            with open(self.file_name, 'r+') as file:
                lines = file.readlines()
                data_list = []
                for line in lines:
                    data = json.loads(line)
                    data_list.append(QueueData(data['content'], data['type']))

                file.seek(0)  # 将文件指针移至开头
                file.truncate()  # 清空文件内容
                return data_list

    def peek(self):
        with self.lock:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
                if lines:
                    data = json.loads(lines[0])
                    return QueueData(data['content'], data['type'])
                else:
                    return None

    def size(self):
        with self.lock:
            with open(self.file_name, 'r') as file:
                return len(file.readlines())


def test_file_queue_operations():
    

    # 生产者函数
    def producer(type):
        file_queue = FileQueue('file1.txt')
        data_obj = QueueData("Sample Content", type)
        while True:
            file_queue.write(data_obj.to_dict())
            time.sleep(1)

    # 消费者函数
    def consumer():
        file_queue = FileQueue('file1.txt')
        while True:
            data = file_queue.read()
            if data:
                print(f"Read data: {data.to_dict()}")

    producer_threads = [threading.Thread(target=producer, args=(i,)) for i in range(3)]
    consumer_thread = threading.Thread(target=consumer, args=())

    for producer_thread in producer_threads:
        producer_thread.start()
    consumer_thread.start()
    # producer_thread.start()
    


if __name__ == "__main__":
    test_file_queue_operations()