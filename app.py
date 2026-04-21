import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# [설정] 기획자님의 구글 Apps Script 웹앱 URL
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzwGosVAq2C_upOFzt2Rd3FHNCNVcpXOr4zrn4NC45sJyjGsjCThoDLtv3_OIIt4Y1kRw/exec"

@app.route('/')
def home():
    return render_template('index.html')

# [기능 1] 데이터 저장 (POST) - UI에서 보낸 데이터를 시트에 기록
@app.route('/api/inbound', methods=['POST'])
def inbound():
    try:
        data = request.json
        # 구글 서버로 데이터 전송 (리디렉션 허용)
        response = requests.post(APPS_SCRIPT_URL, json=data, allow_redirects=True)
        return jsonify(response.json())
    except Exception as e:
        print(f"POST 에러: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# [기능 2] 데이터 조회 (GET) - 시트의 전체 데이터를 가져와서 UI에 전달
@app.route('/api/inbound', methods=['GET'])
def get_inventory():
    try:
        # 구글 서버에 데이터 요청 (doGet 함수 호출됨)
        response = requests.get(APPS_SCRIPT_URL, allow_redirects=True)
        return jsonify(response.json())
    except Exception as e:
        print(f"GET 에러: {str(e)}")
        # 에러 발생 시 빈 배열을 반환하여 UI가 멈추지 않게 함
        return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    # [수정] Render 배포를 위해 host를 '0.0.0.0'으로 설정해야 외부에서 접속 가능합니다.
    app.run(host='0.0.0.0', port=port)
