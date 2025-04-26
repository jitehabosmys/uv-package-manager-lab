import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "你好！这是由 UV 包管理器管理的环境中运行的应用。"

@app.route('/get')
def get_example():
    response = requests.get('https://httpbin.org/get')
    return jsonify(response.json())

if __name__ == '__main__':
    print("启动 Flask 应用...")
    print("请访问: http://127.0.0.1:5000/ 和 http://127.0.0.1:5000/get 来测试功能")
    app.run(debug=True) 