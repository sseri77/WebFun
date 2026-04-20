from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# 구글 GAS 배포 URL (방금 발급받은 배포 ID 포함된 주소)
GAS_URL = "https://script.google.com/macros/s/YOUR_GAS_ID/exec"

@app.route('/')
def index():
    # 제가 드린 HTML 파일을 templates 폴더에 넣고 여기서 서빙합니다.
    return render_template('index.html')

@app.route('/api/inbound', methods=['POST'])
def inbound_data():
    try:
        # 1. 프론트엔드(HTML)에서 보낸 데이터 수신
        client_data = request.json
        
        # 2. 구글 시트로 중계 전송 (Python의 requests 라이브러리 사용)
        # 여기서 'follow_redirects=True' 처리가 중요합니다.
        response = requests.post(GAS_URL, data=json.dumps(client_data))
        
        return jsonify({"status": "success", "message": "데이터가 구글 시트로 전달되었습니다."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Render는 'PORT'라는 환경 변수를 사용하므로 이를 반영해야 합니다.
    import os
    port = int(os.environ.get("PORT", 10000))
    # host를 '0.0.0.0'으로 설정해야 외부 접속이 허용됩니다.
    app.run(host='127.0.0.1', port=port)

