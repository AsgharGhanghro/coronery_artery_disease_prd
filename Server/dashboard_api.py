# server/dashboard_api.py
from flask import Blueprint, jsonify, request
import json
import os
from datetime import datetime, timedelta
import random

dashboard_bp = Blueprint('dashboard', __name__)

# Load dataset for analytics
def load_dataset():
    try:
        data_path = os.path.join(os.path.dirname(__file__), '../data/coronary_artery.json')
        with open(data_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return []

@dashboard_bp.route('/api/dashboard/overview', methods=['GET'])
def get_dashboard_overview():
    """Get overview statistics"""
    data = load_dataset()
    
    total_patients = len(data)
    avg_age = sum(patient['age'] for patient in data) / total_patients if data else 0
    avg_chol = sum(patient['chol'] for patient in data) / total_patients if data else 0
    avg_bp = sum(patient['trestbps'] for patient in data) / total_patients if data else 0
    
    # Risk distribution
    risk_distribution = {}
    for patient in data:
        risk_class = patient.get('class', 0)
        risk_distribution[risk_class] = risk_distribution.get(risk_class, 0) + 1
    
    return jsonify({
        'total_patients': total_patients,
        'average_age': round(avg_age, 1),
        'average_cholesterol': round(avg_chol, 1),
        'average_blood_pressure': round(avg_bp, 1),
        'risk_distribution': risk_distribution,
        'last_updated': datetime.now().isoformat()
    })

@dashboard_bp.route('/api/dashboard/age-analysis', methods=['GET'])
def get_age_analysis():
    """Get age-based analysis"""
    data = load_dataset()
    
    age_groups = {'20-30': 0, '31-40': 0, '41-50': 0, '51-60': 0, '61-70': 0, '71+': 0}
    age_risk_correlation = []
    
    for patient in data:
        age = patient['age']
        risk = patient.get('class', 0)
        
        # Age groups
        if age <= 30: age_groups['20-30'] += 1
        elif age <= 40: age_groups['31-40'] += 1
        elif age <= 50: age_groups['41-50'] += 1
        elif age <= 60: age_groups['51-60'] += 1
        elif age <= 70: age_groups['61-70'] += 1
        else: age_groups['71+'] += 1
        
        # Risk correlation
        age_risk_correlation.append({'age': age, 'risk': risk, 'chol': patient['chol']})
    
    return jsonify({
        'age_groups': age_groups,
        'age_risk_correlation': age_risk_correlation[:100],  # Limit for performance
        'age_ranges': {
            'min': min([p['age'] for p in data]) if data else 0,
            'max': max([p['age'] for p in data]) if data else 0,
            'average': sum([p['age'] for p in data])/len(data) if data else 0
        }
    })

@dashboard_bp.route('/api/dashboard/cholesterol-analysis', methods=['GET'])
def get_cholesterol_analysis():
    """Get cholesterol analysis"""
    data = load_dataset()
    
    chol_ranges = {
        'optimal': 0,    # < 200
        'borderline': 0, # 200-239
        'high': 0        # >= 240
    }
    
    chol_risk_data = []
    
    for patient in data:
        chol = patient['chol']
        risk = patient.get('class', 0)
        
        if chol < 200: chol_ranges['optimal'] += 1
        elif chol < 240: chol_ranges['borderline'] += 1
        else: chol_ranges['high'] += 1
        
        chol_risk_data.append({'cholesterol': chol, 'risk': risk, 'age': patient['age']})
    
    return jsonify({
        'cholesterol_ranges': chol_ranges,
        'chol_risk_data': chol_risk_data[:100],
        'stats': {
            'min': min([p['chol'] for p in data]) if data else 0,
            'max': max([p['chol'] for p in data]) if data else 0,
            'average': sum([p['chol'] for p in data])/len(data) if data else 0
        }
    })

@dashboard_bp.route('/api/dashboard/blood-pressure-analysis', methods=['GET'])
def get_blood_pressure_analysis():
    """Get blood pressure analysis"""
    data = load_dataset()
    
    bp_categories = {
        'normal': 0,      # < 120
        'elevated': 0,    # 120-129
        'high_stage1': 0, # 130-139
        'high_stage2': 0, # 140+
        'crisis': 0       # > 180
    }
    
    bp_data = []
    
    for patient in data:
        bp = patient['trestbps']
        risk = patient.get('class', 0)
        
        if bp < 120: bp_categories['normal'] += 1
        elif bp < 130: bp_categories['elevated'] += 1
        elif bp < 140: bp_categories['high_stage1'] += 1
        elif bp < 180: bp_categories['high_stage2'] += 1
        else: bp_categories['crisis'] += 1
        
        bp_data.append({'blood_pressure': bp, 'risk': risk, 'age': patient['age']})
    
    return jsonify({
        'bp_categories': bp_categories,
        'bp_data': bp_data[:100],
        'stats': {
            'min': min([p['trestbps'] for p in data]) if data else 0,
            'max': max([p['trestbps'] for p in data]) if data else 0,
            'average': sum([p['trestbps'] for p in data])/len(data) if data else 0
        }
    })

@dashboard_bp.route('/api/dashboard/heart-rate-analysis', methods=['GET'])
def get_heart_rate_analysis():
    """Get heart rate analysis"""
    data = load_dataset()
    
    hr_data = []
    hr_by_age = {}
    
    for patient in data:
        hr = patient['thalach']
        age = patient['age']
        risk = patient.get('class', 0)
        
        hr_data.append({'heart_rate': hr, 'risk': risk, 'age': age})
        
        # Group by age decade
        age_decade = (age // 10) * 10
        if age_decade not in hr_by_age:
            hr_by_age[age_decade] = []
        hr_by_age[age_decade].append(hr)
    
    # Calculate averages by age group
    hr_by_age_avg = {}
    for decade, rates in hr_by_age.items():
        hr_by_age_avg[f"{decade}-{decade+9}"] = sum(rates) / len(rates)
    
    return jsonify({
        'hr_data': hr_data[:100],
        'hr_by_age': hr_by_age_avg,
        'stats': {
            'min': min([p['thalach'] for p in data]) if data else 0,
            'max': max([p['thalach'] for p in data]) if data else 0,
            'average': sum([p['thalach'] for p in data])/len(data) if data else 0
        }
    })

@dashboard_bp.route('/api/dashboard/risk-factors', methods=['GET'])
def get_risk_factors():
    """Get risk factor analysis"""
    data = load_dataset()
    
    factors = {
        'chest_pain_types': {},
        'exercise_angina': {'yes': 0, 'no': 0},
        'blood_sugar': {'high': 0, 'normal': 0},
        'ecg_results': {},
        'vessels_colored': {0: 0, 1: 0, 2: 0, 3: 0}
    }
    
    for patient in data:
        # Chest pain types
        cp = patient['cp']
        factors['chest_pain_types'][cp] = factors['chest_pain_types'].get(cp, 0) + 1
        
        # Exercise angina
        exang = patient['exang']
        factors['exercise_angina']['yes' if exang == 'Yes' else 'no'] += 1
        
        # Blood sugar
        fbs = patient['fbs']
        factors['blood_sugar']['high' if fbs else 'normal'] += 1
        
        # ECG results
        ecg = patient['restecg']
        factors['ecg_results'][ecg] = factors['ecg_results'].get(ecg, 0) + 1
        
        # Vessels colored
        ca = patient['ca']
        factors['vessels_colored'][ca] = factors['vessels_colored'].get(ca, 0) + 1
    
    return jsonify(factors)

@dashboard_bp.route('/api/dashboard/predictions', methods=['GET'])
def get_recent_predictions():
    """Get recent prediction history (simulated)"""
    # Simulate recent predictions
    recent_predictions = []
    risk_levels = ['Low', 'Moderate', 'High']
    
    for i in range(10):
        recent_predictions.append({
            'id': i + 1,
            'timestamp': (datetime.now() - timedelta(hours=i*2)).isoformat(),
            'risk_level': random.choice(risk_levels),
            'confidence': round(random.uniform(0.7, 0.95), 2),
            'age': random.randint(35, 75),
            'gender': random.choice(['Male', 'Female'])
        })
    
    return jsonify({
        'recent_predictions': recent_predictions,
        'prediction_stats': {
            'total_predictions': 150,
            'high_risk_predictions': 45,
            'average_confidence': 0.82
        }
    })