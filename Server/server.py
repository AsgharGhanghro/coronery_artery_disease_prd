# Server/server.py
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore

# Import dashboard blueprint
from dashboard_api import dashboard_bp

# Import from local utils
try:
    from utils import predictor, FEATURE_DESCRIPTIONS, DEFAULT_VALUES # type: ignore
except ImportError:
    # If utils import fails, use simple predictor
    predictor = None
    FEATURE_DESCRIPTIONS = {}
    DEFAULT_VALUES = {}

app = Flask(__name__)
CORS(app)

# Register dashboard blueprint
app.register_blueprint(dashboard_bp)

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore

# Import from local utils
try:
    from utils import predictor, FEATURE_DESCRIPTIONS, DEFAULT_VALUES # type: ignore
except ImportError:
    # If utils import fails, try importing directly
    import importlib.util
    spec = importlib.util.spec_from_file_location("utils", "utils.py")
    utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(utils)
    predictor = utils.predictor
    FEATURE_DESCRIPTIONS = utils.FEATURE_DESCRIPTIONS
    DEFAULT_VALUES = utils.DEFAULT_VALUES

app = Flask(__name__)
CORS(app)

# Rest of your server code...
@app.route('/')
def home():
    return jsonify({
        "message": "Coronary Artery Disease Prediction API",
        "status": "running",
        "model_loaded": predictor is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500
        
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        result = predictor.predict(data)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/features', methods=['GET'])
def get_features():
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500
        
    try:
        feature_info = predictor.get_feature_info()
        return jsonify({
            'features': FEATURE_DESCRIPTIONS,
            'default_values': DEFAULT_VALUES,
            'model_info': feature_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy' if predictor else 'unhealthy',
        'model_loaded': predictor is not None,
        'model_accuracy': predictor.accuracy if predictor else 0.0
    })

if __name__ == '__main__':
    print("🚀 Starting Coronary Artery Disease Prediction Server...")
    if predictor:
        print(f"📊 Model Accuracy: {predictor.accuracy:.2%}")
        print(f"🔢 Features: {len(predictor.feature_names)}")
    else:
        print("❌ Model failed to load!")
    
    print("🌐 Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)