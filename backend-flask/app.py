from flask import Flask, render_template, request, session
from flask_session import Session

from openai_client import get_openai_response

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 配置 Flask-Session 存储在服务器内存中
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route("/", methods=["GET"])
def home():
    # 初始化聊天记录
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template("index.html", chat_history=session['chat_history'])

@app.route("/echo", methods=["POST"])
def echo():
    user_input = request.form.get("msgInput", "")
    
    # 模拟 AI 回复
    ai_response = f"AI：已收到你的输入「{user_input}」"
    
    # 确保 session 里存在 chat_history
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    # 将用户输入和 AI 回复保存到聊天记录
    session['chat_history'].append({"user": user_input, "ai": ai_response})
    
    # 保存 session（确保持久化）
    session.modified = True
    
    # 重新渲染页面，带着完整的聊天记录
    return render_template("index.html", chat_history=session['chat_history'])

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("msgInput", "")
    
    # 确保聊天记录存在
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    # 调用 OpenAI 模块生成回复，传递历史记录
    ai_response = get_openai_response(user_input, session['chat_history'])
    
    # 保存用户输入和 AI 回复到聊天记录
    session['chat_history'].append({"user": user_input, "ai": ai_response})
    session.modified = True  # 确保 session 保存
    
    return render_template("index.html", chat_history=session['chat_history'])


if __name__ == "__main__":
    app.run(debug=True)
