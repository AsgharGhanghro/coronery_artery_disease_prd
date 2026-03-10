# Server/run.py
from server import app

if __name__ == '__main__':
    print("🏥 Coronary Artery Disease Prediction Server")
    print("============================================")
    app.run(debug=True, host='0.0.0.0', port=5000)