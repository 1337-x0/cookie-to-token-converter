
from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    cookie = request.form.get('cookie')
    if not cookie:
        return jsonify({"error": "Cookie cannot be empty."}), 400

    try:
        headers = {
            'Host': 'business.facebook.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4A Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.92 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'content-type': 'text/html; charset=utf-8',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': cookie
        }
        response = requests.get("https://business.facebook.com/creatorstudio/home", headers=headers)
        match = re.search(r'{"accessToken":"(EAA\w+)', response.text)
        if match:
            token = match.group(1)
            return jsonify({"token": token})
        else:
            return jsonify({"error": "Invalid cookie or token not found."}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
