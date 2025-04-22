# io_client/cli.py
import requests

def main():
    messages = []
    print("LLM CLI Demo (type 'exit' to quit)")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        messages.append({"role": "user", "content": user_input})
        
        res = requests.post("http://localhost:8000/chat", json={"messages": messages})
        reply = res.json()["reply"]
        print("Bot:", reply)
        
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()