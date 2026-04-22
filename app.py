import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# [설정] 기획자님이 방금 제공해주신 최신 구글 Apps Script 웹앱 URL입니다.
# 만약 Apps Script 코드를 수정하셨다면 '새 배포'를 누르고 URL을 다시 확인해 보세요!
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyTGY7fyrei7VllRfCPlraf1LWd_9bsB0UOpfjN4_pvsfEvZoJUGkJbdHMgjCvPKGjE/exec"

@app.route('/')
def home():
    # templates 폴더 안의 index.html 파일을 사용자에게 보여줍니다.
    return render_template('index.html')

# [기능 1] 데이터 저장 (POST)
@app.route('/api/inbound', methods=['POST'])
def inbound():
    try:
        data = request.json
        print(f"수신 데이터(입력): {data}") # Render 로그에서 확인 가능
        
        # 구글 서버로 데이터 전송 (allow_redirects=True 필수)
        response = requests.post(APPS_SCRIPT_URL, json=data, allow_redirects=True)
        
        # 구글에서 처리된 결과 반환
        return jsonify(response.json())
    except Exception as e:
        print(f"POST 에러 발생: {str(e)}")
        return jsonify({"status": "error", "message": "기록 실패: 구글 서버 응답 없음"}), 500

# [기능 2] 데이터 조회 (GET) - index.html이 로딩될 때 호출됩니다.
@app.route('/api/inbound', methods=['GET'])
def get_inventory():
    try:
        # 구글 서버에 저장된 전체 데이터(구단목록 + 재고현황) 요청
        response = requests.get(APPS_SCRIPT_URL, allow_redirects=True)
        
        # 구글에서 받은 원본 데이터를 그대로 index.html로 배달
        return jsonify(response.json())
    except Exception as e:
        print(f"GET 에러 발생: {str(e)}")
        # 에러 발생 시 데이터가 안 깨지도록 기본 틀만 반환
        return jsonify({"teams": [], "inventory": []})

if __name__ == '__main__':
    # Render 환경의 포트 설정을 따르며, 기본값은 10000입니다.
    port = int(os.environ.get("PORT", 10000))
    # 외부 접속 허용을 위해 host를 0.0.0.0으로 설정합니다. (127.0.0.1은 내부용이라 안 됨)
    app.run(host='0.0.0.0', port=port)
