# Server/test_api.py
import requests
import json

def test_api():
    print("🧪 Testing API endpoints...")
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get('http://localhost:5000/health')
        print(f"   ✅ Health check: {response.status_code}")
        print(f"   📊 Response: {response.json()}")
        
        # Test features endpoint
        print("\n2. Testing features endpoint...")
        response = requests.get('http://localhost:5000/features')
        print(f"   ✅ Features endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📋 Features count: {len(data.get('features', {}))}")
            print(f"   🎯 Model accuracy: {data.get('model_info', {}).get('model_accuracy', 'Unknown')}")
        else:
            print(f"   ❌ Error: {response.json()}")
            
        # Test prediction endpoint
        print("\n3. Testing prediction endpoint...")
        test_data = {
            'age': 55,
            'sex': 1,
            'cp': 2,
            'trestbps': 130,
            'chol': 220,
            'fbs': 0,
            'restecg': 1,
            'thalach': 150,
            'exang': 0,
            'oldpeak': 1.2,
            'slope': 1,
            'ca': 0,
            'thal': 2
        }
        response = requests.post('http://localhost:5000/predict', json=test_data)
        print(f"   ✅ Prediction endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   🎯 Prediction: {result.get('prediction')}")
            print(f"   📈 Risk Level: {result.get('risk_level')}")
            print(f"   💯 Confidence: {result.get('confidence')}")
        else:
            print(f"   ❌ Error: {response.json()}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 5000")
        print("💡 Run: python server.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_api()