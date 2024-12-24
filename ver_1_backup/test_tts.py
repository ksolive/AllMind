import asyncio  
import random
import edge_tts  

async def tts(TEXT, VOICE="zh-CN-XiaoyiNeural", OUTPUT_FILE="test_tts.mp3"):
    voices = await edge_tts.VoicesManager.create()  
    voice = voices.find(Gender="Male", Language="zh")
    # print(voice)
    voice = random.choice(voice)["Name"]
    print(voice)
    communicate = edge_tts.Communicate(TEXT, voice)  
    await communicate.save(OUTPUT_FILE) 

if __name__ == "__main__":  
    asyncio.run(tts("今天我在中国广西壮族自治区的北海市。"))