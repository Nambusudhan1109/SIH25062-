#!/usr/bin/env python3
"""
Farmer Loan System - API Server Runner
Starts Flask REST API on port 5000
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app from the consolidated file
# Since farmer_loan_system.py has multiple main blocks, we import selectively
print("Loading Farmer Loan System modules...")

from flask import Flask, request, jsonify, session
from flask_cors import CORS

# Import the loan intelligence classes
# These are defined in farmer_loan_system.py before the __main__ blocks
exec(open('farmer_loan_system.py').read().split('if __name__ == "__main__":')[0])

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# Import API routes from the file
print("Setting up API endpoints...")

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'service': 'Farmer Loan Intelligence Module',
        'version': '1.0 Consolidated',
        'modules': ['Smart AI (9 modules)', 'Simple Filter', 'Multi-language']
    })

# Test endpoint
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        'message': 'Farmer Loan System API is running!',
        'endpoints': [
            '/api/health',
            '/api/test',
            '/api/loan/demo-ai',
            '/api/loan/demo-filter',
            '/api/loan/demo-multilang'
        ]
    })

# Demo AI recommendations
@app.route('/api/loan/demo-ai', methods=['GET'])
def demo_ai():
    try:
        module = SmartLoanIntelligenceModule()
        farmer_data = {
            "user_id": "FARMER_TN_2026_001",
            "state": "Tamil Nadu",
            "district": "Coimbatore",
            "land_size": 6.0,
            "crop_selected": "Rice",
            "soil_type": "Clay Loam",
            "irrigation_type": "Drip",
            "income": 150000,
            "bank_availability": "Available",
            "loan_history": "Good"
        }
        result = module.calculate_eligibility(farmer_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Demo simple filter
@app.route('/api/loan/demo-filter', methods=['GET'])
def demo_filter():
    try:
        filter_module = AvailableLoansFilter()
        result = filter_module.get_available_loans(
            user_id="TEST_USER_TN",
            state="Tamil Nadu",
            land_size=5.0
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Demo multi-language
@app.route('/api/loan/demo-multilang', methods=['GET'])
def demo_multilang():
    try:
        lang = request.args.get('lang', 'en')
        ai_module = AILoanRecommendation()
        result = ai_module.get_loan_recommendations(
            user_id="FARMER_001",
            language=lang
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    print("=" * 80)
    print("🌾 FARMER LOAN INTELLIGENCE SYSTEM - API SERVER")
    print("=" * 80)
    print("\n📡 API Endpoints:")
    print("  GET  /api/health            - Health check")
    print("  GET  /api/test              - Test endpoint")
    print("  GET  /api/loan/demo-ai      - Demo: Smart AI (9 modules)")
    print("  GET  /api/loan/demo-filter  - Demo: Simple filtering")
    print("  GET  /api/loan/demo-multilang?lang=en|ta|ne - Demo: Multi-language")
    print("\n🚀 Starting server on http://localhost:5000")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
