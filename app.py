import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# [설정] 기획자님이 제공해주신 구글 Apps Script 웹앱 URL입니다.
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxCutTgjSvKw1aeZbff1a6Z6ic6-SRwX_QXukJWywBJk_nzfqedFkONjPWfKG_vAdBgyQ/exec"

@app.route('/')
def home():
    # templates 폴더 안의 index.html 파일을 사용자에게 보여줍니다.
    return render_template('index.html')

@app.route('/api/inbound', methods=['POST'])
def inbound():
    try:
        # 1. UI(index.html)에서 보낸 데이터를 받습니다.
        data = request.json
        print(f"수신 데이터: {data}") # 로그 확인용
        
        # 2. 받은 데이터를 구글 Apps Script URL로 배달합니다.
        # 인증 키 없이 웹앱 URL을 통해 통신하는 핵심 로직입니다.
        response = requests.post(APPS_SCRIPT_URL, json=data)
        
        # 3. 구글 시트의 처리 결과(성공/실패)를 다시 UI로 전달합니다.
        return jsonify(response.json())
        
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": "서버 내부 통신 에러가 발생했습니다."
        }), 500

if __name__ == '__main__':
    # Render 환경의 포트 설정을 따르며, 기본값은 10000입니다.
    port = int(os.environ.get("PORT", 10000))
    # 외부 접속 허용을 위해 host를 0.0.0.0으로 설정합니다.
    app.run(host='127.0.0.1', port=port)
