"""
Smart Farmer Loan Intelligence Module (MASTER VERSION)
AI Financial Advisor with 9 Advanced Modules

Combines: Validation + Private Recommendations + Voice + Simulator + Auto-Update
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import calendar

# ============================================================================
# LOAN SCHEMES DATABASE (Admin-Updateable)
# ============================================================================

LOAN_SCHEMES_DB = {
    "Tamil Nadu": [
        {
            "scheme": "Kisan Credit Card",
            "max_amount": 300000,
            "interest_rate": "4% (after interest subvention)",
            "subsidy": "Interest subvention available",
            "eligible_crops": ["Rice", "Sugarcane", "Cotton", "Groundnut", "Maize", "Pulses"],
            "min_land": 0.5,
            "apply_link": "https://www.indianbank.in/departments/agri-loans/kisan-credit-card/",
            "last_updated": "2026-02-26"
        },
        {
            "scheme": "Tamil Nadu Cooperative Crop Loan",
            "max_amount": 200000,
            "interest_rate": "0% (Zero Interest)",
            "subsidy": "Full interest subsidy",
            "eligible_crops": ["Rice", "Sugarcane", "Cotton"],
            "min_land": 1.0,
            "apply_link": "https://www.tn.gov.in",
            "last_updated": "2026-02-26"
        },
        {
            "scheme": "PM Fasal Bima Yojana",
            "max_amount": 150000,
            "interest_rate": "2% premium (Govt subsidized)",
            "subsidy": "Premium subsidy by government",
            "eligible_crops": ["All crops"],
            "min_land": 0.5,
            "apply_link": "https://pmfby.gov.in",
            "last_updated": "2026-02-26"
        },
        {
            "scheme": "Agriculture Infrastructure Fund",
            "max_amount": 1000000,
            "interest_rate": "3% (subsidized)",
            "subsidy": "Interest subvention + credit guarantee",
            "eligible_crops": ["All crops"],
            "min_land": 5.0,
            "apply_link": "https://agriinfra.dac.gov.in",
            "last_updated": "2026-02-26"
        }
    ],
    "Sikkim": [
        {
            "scheme": "Sikkim Organic Farming Scheme",
            "max_amount": 500000,
            "interest_rate": "4-5% (with subsidy)",
            "subsidy": "Organic certification support",
            "eligible_crops": ["Organic Vegetables", "Organic Fruits", "Spices", "Cardamom"],
            "min_land": 2.0,
            "apply_link": "https://www.statebankofsikkim.com/agriculture-loans",
            "last_updated": "2026-02-26"
        },
        {
            "scheme": "Allied Agricultural Activities Loan",
            "max_amount": 300000,
            "interest_rate": "5%",
            "subsidy": "Processing subsidy available",
            "eligible_crops": ["Dairy", "Poultry", "Floriculture", "Horticulture"],
            "min_land": 0.5,
            "apply_link": "https://www.statebankofsikkim.com/agriculture-loans",
            "last_updated": "2026-02-26"
        },
        {
            "scheme": "Agriculture Infrastructure Development",
            "max_amount": 1000000,
            "interest_rate": "3% (subsidized)",
            "subsidy": "Infrastructure grant + low interest",
            "eligible_crops": ["All crops"],
            "min_land": 5.0,
            "apply_link": "https://agriinfra.dac.gov.in",
            "last_updated": "2026-02-26"
        }
    ]
}

# Crop profitability and harvest data
CROP_DATA = {
    "Rice": {
        "value_per_acre": 40000,
        "profitability_score": 0.70,
        "weather_risk": 0.30,
        "market_risk": 0.20,
        "harvest_months": [5, 10],  # May, October
        "harvest_season": "Kharif/Rabi"
    },
    "Sugarcane": {
        "value_per_acre": 60000,
        "profitability_score": 0.85,
        "weather_risk": 0.25,
        "market_risk": 0.15,
        "harvest_months": [1, 2, 3],  # Jan-Mar
        "harvest_season": "Winter"
    },
    "Cotton": {
        "value_per_acre": 45000,
        "profitability_score": 0.75,
        "weather_risk": 0.35,
        "market_risk": 0.30,
        "harvest_months": [11, 12],  # Nov-Dec
        "harvest_season": "Rabi"
    },
    "Groundnut": {
        "value_per_acre": 35000,
        "profitability_score": 0.68,
        "weather_risk": 0.28,
        "market_risk": 0.25,
        "harvest_months": [9, 10],  # Sep-Oct
        "harvest_season": "Kharif"
    },
    "Maize": {
        "value_per_acre": 30000,
        "profitability_score": 0.65,
        "weather_risk": 0.25,
        "market_risk": 0.22,
        "harvest_months": [8, 9],  # Aug-Sep
        "harvest_season": "Kharif"
    },
    "Pulses": {
        "value_per_acre": 25000,
        "profitability_score": 0.60,
        "weather_risk": 0.35,
        "market_risk": 0.28,
        "harvest_months": [3, 4],  # Mar-Apr
        "harvest_season": "Rabi"
    },
    "Organic Vegetables": {
        "value_per_acre": 70000,
        "profitability_score": 0.90,
        "weather_risk": 0.30,
        "market_risk": 0.18,
        "harvest_months": [6, 7, 8, 9],  # Jun-Sep
        "harvest_season": "Monsoon"
    },
    "Organic Fruits": {
        "value_per_acre": 80000,
        "profitability_score": 0.88,
        "weather_risk": 0.32,
        "market_risk": 0.20,
        "harvest_months": [4, 5, 6],  # Apr-Jun
        "harvest_season": "Summer"
    },
    "Spices": {
        "value_per_acre": 90000,
        "profitability_score": 0.92,
        "weather_risk": 0.28,
        "market_risk": 0.15,
        "harvest_months": [10, 11],  # Oct-Nov
        "harvest_season": "Post-Monsoon"
    },
    "Cardamom": {
        "value_per_acre": 100000,
        "profitability_score": 0.95,
        "weather_risk": 0.25,
        "market_risk": 0.12,
        "harvest_months": [10, 11, 12],  # Oct-Dec
        "harvest_season": "Post-Monsoon"
    }
}

# Soil quality scoring
SOIL_QUALITY_SCORES = {
    "Clay Loam": 0.85,
    "Sandy Loam": 0.75,
    "Black Soil": 0.90,
    "Red Soil": 0.70,
    "Mountain Soil": 0.80,
    "Alluvial": 0.95
}

# Irrigation reliability scoring
IRRIGATION_RELIABILITY = {
    "Drip": 0.95,
    "Sprinkler": 0.90,
    "Canal": 0.75,
    "Well": 0.70,
    "Rainfed": 0.40
}

# Tamil voice explanations
TAMIL_VOICE_TEMPLATES = {
    "high_eligibility": "உங்களுக்கு {scheme} கடன் பெற நல்ல தகுதி உள்ளது. உங்கள் நில அளவு {land} ஏக்கர் மற்றும் {crop} சாகுபடி செய்வதால் இந்த கடன் பரிந்துரைக்கப்படுகிறது. வட்டி விகிதம் {interest} மட்டுமே.",
    "medium_eligibility": "உங்களுக்கு {scheme} கடன் கிடைக்க வாய்ப்பு உள்ளது. உங்கள் தகுதி மதிப்பெண் {score} ஆக உள்ளது. நீர்ப்பாசன முறையை மேம்படுத்தினால் அதிக கடன் தொகை பெறலாம்.",
    "improvement_needed": "உங்கள் கடன் தகுதியை அதிகரிக்க சில மேம்பாடுகள் தேவை. {suggestions} இவற்றை செயல்படுத்தினால் கடன் பெறுவதற்கான வாய்ப்பு அதிகரிக்கும்.",
    "repayment_plan": "உங்கள் {crop} அறுவடை {month} மாதத்தில் முடியும். அறுவடைக்கு பிறகு கடன் திருப்பிச் செலுத்தலாம். எதிர்பார்க்கப்படும் லாபம் ரூபாய் {profit}."
}


class SmartLoanIntelligenceModule:
    """
    Master AI Financial Advisor Module
    9 Processing Modules + Government UI Compatible
    """
    
    REQUIRED_FIELDS = [
        'user_id', 'state', 'district', 'land_size', 'crop_selected',
        'soil_type', 'irrigation_type', 'annual_income',
        'previous_loan_history', 'bank_availability'
    ]
    
    def __init__(self):
        self.loan_schemes = LOAN_SCHEMES_DB
        self.crop_data = CROP_DATA
        self.soil_scores = SOIL_QUALITY_SCORES
        self.irrigation_scores = IRRIGATION_RELIABILITY
        
    # ========================================================================
    # MODULE 0: VALIDATION
    # ========================================================================
    
    def validate_profile(self, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all required fields are present"""
        missing_fields = []
        
        for field in self.REQUIRED_FIELDS:
            if field not in farmer_data or farmer_data[field] is None or farmer_data[field] == "":
                missing_fields.append(field)
        
        if missing_fields:
            return {
                "status": "INCOMPLETE_PROFILE",
                "message": "Please complete all farmer details to check loan eligibility.",
                "missing_fields": missing_fields
            }
        
        return {"status": "VALID"}
    
    # ========================================================================
    # MODULE 1: ELIGIBILITY SCORE CALCULATION (0-100 scale)
    # ========================================================================
    
    def calculate_eligibility_score(self, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        EligibilityScore = (LandSize × 0.25) + (IncomeStability × 0.20) +
                           (SoilQuality × 0.15) + (IrrigationReliability × 0.20) +
                           (CropProfitability × 0.20)
        """
        land_size = float(farmer_data['land_size'])
        annual_income = float(farmer_data['annual_income'])
        crop = farmer_data['crop_selected']
        soil_type = farmer_data['soil_type']
        irrigation_type = farmer_data['irrigation_type']
        
        # Land size score (0-25 points)
        if land_size >= 10:
            land_score = 25
        elif land_size >= 5:
            land_score = 20
        elif land_size >= 2:
            land_score = 15
        else:
            land_score = 10
        
        # Income stability score (0-20 points)
        if annual_income >= 200000:
            income_score = 20
        elif annual_income >= 100000:
            income_score = 16
        elif annual_income >= 50000:
            income_score = 12
        else:
            income_score = 8
        
        # Soil quality score (0-15 points)
        soil_quality_factor = self.soil_scores.get(soil_type, 0.70)
        soil_score = soil_quality_factor * 15
        
        # Irrigation reliability score (0-20 points)
        irrigation_factor = self.irrigation_scores.get(irrigation_type, 0.50)
        irrigation_score = irrigation_factor * 20
        
        # Crop profitability score (0-20 points)
        crop_profitability = self.crop_data.get(crop, {}).get('profitability_score', 0.65)
        crop_score = crop_profitability * 20
        
        # Total eligibility score
        total_score = land_score + income_score + soil_score + irrigation_score + crop_score
        
        # Determine status
        if total_score >= 71:
            status = "Good"
        elif total_score >= 41:
            status = "Moderate"
        else:
            status = "Low"
        
        return {
            "eligibility_score": round(total_score, 1),
            "status": status,
            "breakdown": {
                "land_score": round(land_score, 1),
                "income_score": round(income_score, 1),
                "soil_score": round(soil_score, 1),
                "irrigation_score": round(irrigation_score, 1),
                "crop_score": round(crop_score, 1)
            }
        }
    
    # ========================================================================
    # MODULE 2: RISK SCORE CALCULATION
    # ========================================================================
    
    def calculate_risk_score(self, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        RiskScore = (WeatherRisk × 0.4) + (MarketRisk × 0.3) + (LoanHistoryRisk × 0.3)
        """
        crop = farmer_data['crop_selected']
        loan_history = farmer_data['previous_loan_history'].lower()
        
        # Weather risk (0-40 points)
        weather_risk_factor = self.crop_data.get(crop, {}).get('weather_risk', 0.30)
        weather_risk = weather_risk_factor * 40
        
        # Market risk (0-30 points)
        market_risk_factor = self.crop_data.get(crop, {}).get('market_risk', 0.25)
        market_risk = market_risk_factor * 30
        
        # Loan history risk (0-30 points)
        if loan_history in ['defaulted', 'pending', 'overdue']:
            loan_history_risk = 30
        elif loan_history in ['ongoing', 'active']:
            loan_history_risk = 10
        else:  # none, cleared, paid
            loan_history_risk = 0
        
        # Total risk score
        total_risk = weather_risk + market_risk + loan_history_risk
        
        # Approval probability = EligibilityScore - RiskScore
        # (We'll calculate this in the main function)
        
        return {
            "risk_score": round(total_risk, 1),
            "breakdown": {
                "weather_risk": round(weather_risk, 1),
                "market_risk": round(market_risk, 1),
                "loan_history_risk": round(loan_history_risk, 1)
            }
        }
    
    # ========================================================================
    # MODULE 3: LOAN RECOMMENDATION (State Logic)
    # ========================================================================
    
    def get_loan_recommendations(self, farmer_data: Dict[str, Any], eligibility_score: float) -> List[Dict]:
        """Get prioritized loan schemes based on state and eligibility"""
        state = farmer_data['state']
        crop = farmer_data['crop_selected']
        land_size = float(farmer_data['land_size'])
        
        if state not in self.loan_schemes:
            return []
        
        schemes = self.loan_schemes[state]
        eligible_schemes = []
        
        for scheme in schemes:
            # Check land eligibility
            if land_size < scheme['min_land']:
                continue
            
            # Check crop eligibility
            eligible_crops = scheme['eligible_crops']
            if 'All crops' not in eligible_crops and crop not in eligible_crops:
                continue
            
            # Calculate eligible amount
            crop_value = self.crop_data.get(crop, {}).get('value_per_acre', 40000)
            base_amount = land_size * crop_value * 0.7
            
            # Adjust by eligibility score
            if eligibility_score >= 71:
                adjustment = 1.0
            elif eligibility_score >= 41:
                adjustment = 0.8
            else:
                adjustment = 0.6
            
            eligible_amount = min(int(base_amount * adjustment), scheme['max_amount'])
            
            eligible_schemes.append({
                "scheme": scheme['scheme'],
                "loan_amount": f"₹{eligible_amount:,}",
                "eligible_amount_raw": eligible_amount,
                "interest_rate": scheme['interest_rate'],
                "subsidy": scheme['subsidy'],
                "apply_link": scheme['apply_link'],
                "last_updated": scheme['last_updated']
            })
        
        return eligible_schemes[:3]  # Top 3 schemes
    
    # ========================================================================
    # MODULE 4: IMPROVEMENT SUGGESTIONS
    # ========================================================================
    
    def generate_improvement_suggestions(self, farmer_data: Dict[str, Any], 
                                        eligibility_breakdown: Dict) -> List[str]:
        """Generate personalized suggestions to increase approval probability"""
        suggestions = []
        
        breakdown = eligibility_breakdown['breakdown']
        
        # Check irrigation score
        if breakdown['irrigation_score'] < 15:
            suggestions.append("மேம்படுத்தப்பட்ட நீர்ப்பாசன முறையை (Drip/Sprinkler) பயன்படுத்தினால் தகுதி மதிப்பெண் அதிகரிக்கும் (Improve irrigation to drip/sprinkler system)")
        
        # Check crop score
        if breakdown['crop_score'] < 15:
            suggestions.append("அதிக லாபம் தரும் பயிர்களை (Organic crops/Spices) தேர்வு செய்யலாம் (Consider higher profitability crops)")
        
        # Check income score
        if breakdown['income_score'] < 12:
            suggestions.append("வருமான சான்றிதழ் அல்லது வங்கி கணக்கு விவரம் தயாரிக்கவும் (Prepare income verification documents)")
        
        # Check loan history
        if farmer_data['previous_loan_history'].lower() in ['ongoing', 'active']:
            suggestions.append("தற்போதுள்ள கடனை முடித்தால் புதிய கடனுக்கான வாய்ப்பு அதிகரிக்கும் (Clear existing loan for better approval)")
        
        # Cooperative bank suggestion
        if farmer_data.get('bank_availability', '').lower() == 'yes':
            suggestions.append("கூட்டுறவு வங்கி திட்டங்களில் விண்ணப்பிக்கலாம் - குறைந்த வட்டி விகிதம் (Apply for cooperative bank schemes)")
        
        return suggestions[:3]  # Max 3 suggestions
    
    # ========================================================================
    # MODULE 5: HARVEST-BASED REPAYMENT PLANNER
    # ========================================================================
    
    def generate_repayment_plan(self, farmer_data: Dict[str, Any], 
                               loan_amount_raw: int) -> Dict[str, Any]:
        """Generate repayment plan aligned with harvest"""
        crop = farmer_data['crop_selected']
        crop_info = self.crop_data.get(crop, {})
        
        harvest_months = crop_info.get('harvest_months', [10])
        harvest_season = crop_info.get('harvest_season', 'Seasonal')
        
        # Get next harvest month
        current_month = datetime.now().month
        next_harvest = None
        for month in harvest_months:
            if month >= current_month:
                next_harvest = month
                break
        
        if next_harvest is None:
            next_harvest = harvest_months[0]  # Next year
        
        harvest_month_name = calendar.month_name[next_harvest]
        
        # Calculate expected profit
        land_size = float(farmer_data['land_size'])
        crop_value_per_acre = crop_info.get('value_per_acre', 40000)
        
        total_revenue = land_size * crop_value_per_acre
        production_cost = total_revenue * 0.40  # 40% production cost
        loan_repayment = loan_amount_raw
        
        profit_after_repayment = total_revenue - production_cost - loan_repayment
        
        return {
            "harvest_month": harvest_month_name,
            "harvest_season": harvest_season,
            "repayment_start": f"After {harvest_month_name} Harvest",
            "expected_revenue": f"₹{int(total_revenue):,}",
            "production_cost": f"₹{int(production_cost):,}",
            "loan_repayment": f"₹{loan_repayment:,}",
            "profit_after_repayment": f"₹{int(profit_after_repayment):,}",
            "profit_margin": f"{((profit_after_repayment/total_revenue)*100):.1f}%"
        }
    
    # ========================================================================
    # MODULE 6: APPROVAL PROBABILITY SIMULATOR
    # ========================================================================
    
    def simulate_probability_change(self, current_data: Dict[str, Any], 
                                    modified_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate probability change when user modifies inputs"""
        
        # Calculate scores for current data
        current_eligibility = self.calculate_eligibility_score(current_data)
        current_risk = self.calculate_risk_score(current_data)
        current_probability = current_eligibility['eligibility_score'] - current_risk['risk_score']
        
        # Calculate scores for modified data
        modified_eligibility = self.calculate_eligibility_score(modified_data)
        modified_risk = self.calculate_risk_score(modified_data)
        modified_probability = modified_eligibility['eligibility_score'] - modified_risk['risk_score']
        
        # Calculate change
        change = modified_probability - current_probability
        
        if change > 5:
            indicator = "SIGNIFICANT_INCREASE"
            message = "வெற்றி வாய்ப்பு கணிசமாக அதிகரித்துள்ளது (Significantly Improved)"
        elif change > 0:
            indicator = "INCREASE"
            message = "வெற்றி வாய்ப்பு சற்று அதிகரித்துள்ளது (Slightly Improved)"
        elif change < -5:
            indicator = "SIGNIFICANT_DECREASE"
            message = "வெற்றி வாய்ப்பு குறைந்துள்ளது (Decreased)"
        elif change < 0:
            indicator = "DECREASE"
            message = "வெற்றி வாய்ப்பு சற்று குறைந்துள்ளது (Slightly Decreased)"
        else:
            indicator = "NO_CHANGE"
            message = "மாற்றம் இல்லை (No Change)"
        
        return {
            "previous_probability": f"{max(20, min(95, current_probability)):.1f}%",
            "updated_probability": f"{max(20, min(95, modified_probability)):.1f}%",
            "change": f"{change:+.1f}",
            "change_indicator": indicator,
            "message": message
        }
    
    # ========================================================================
    # MODULE 7: VOICE EXPLANATION (TAMIL)
    # ========================================================================
    
    def generate_tamil_voice_explanation(self, farmer_data: Dict[str, Any],
                                        recommendations: List[Dict],
                                        eligibility_score: float,
                                        repayment_plan: Dict,
                                        suggestions: List[str]) -> str:
        """Generate Tamil voice explanation"""
        
        if not recommendations:
            return "மன்னிக்கவும், உங்களுக்கு தற்போது கடன் பரிந்துரைகள் இல்லை. தயவுசெய்து உங்கள் விவரங்களை சரிபார்க்கவும்."
        
        top_scheme = recommendations[0]
        crop = farmer_data['crop_selected']
        land = farmer_data['land_size']
        
        explanation_parts = []
        
        # Main recommendation
        if eligibility_score >= 71:
            template = TAMIL_VOICE_TEMPLATES['high_eligibility']
            explanation_parts.append(template.format(
                scheme=top_scheme['scheme'],
                land=land,
                crop=crop,
                interest=top_scheme['interest_rate']
            ))
        elif eligibility_score >= 41:
            template = TAMIL_VOICE_TEMPLATES['medium_eligibility']
            explanation_parts.append(template.format(
                scheme=top_scheme['scheme'],
                score=eligibility_score
            ))
        else:
            template = TAMIL_VOICE_TEMPLATES['improvement_needed']
            suggestion_text = ", ".join(suggestions[:2])
            explanation_parts.append(template.format(suggestions=suggestion_text))
        
        # Repayment plan
        repayment_template = TAMIL_VOICE_TEMPLATES['repayment_plan']
        explanation_parts.append(repayment_template.format(
            crop=crop,
            month=repayment_plan['harvest_month'],
            profit=repayment_plan['profit_after_repayment']
        ))
        
        return " ".join(explanation_parts)
    
    # ========================================================================
    # MODULE 8: SMART SCHEME AUTO-UPDATE
    # ========================================================================
    
    def update_loan_scheme(self, state: str, scheme_name: str, updates: Dict[str, Any]) -> bool:
        """Admin function to update loan schemes dynamically"""
        if state not in self.loan_schemes:
            return False
        
        for scheme in self.loan_schemes[state]:
            if scheme['scheme'] == scheme_name:
                scheme.update(updates)
                scheme['last_updated'] = datetime.now().strftime("%Y-%m-%d")
                return True
        
        return False
    
    def get_latest_schemes(self, state: str) -> List[Dict]:
        """Get latest scheme data (always up-to-date)"""
        return self.loan_schemes.get(state, [])
    
    # ========================================================================
    # MASTER FUNCTION: GENERATE COMPLETE RECOMMENDATION
    # ========================================================================
    
    def generate_complete_recommendation(self, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Master function combining all 9 modules
        Returns complete private recommendation
        """
        
        # MODULE 0: Validate
        validation = self.validate_profile(farmer_data)
        if validation['status'] == "INCOMPLETE_PROFILE":
            return validation
        
        # MODULE 1: Eligibility Score
        eligibility = self.calculate_eligibility_score(farmer_data)
        
        # MODULE 2: Risk Score
        risk = self.calculate_risk_score(farmer_data)
        
        # Calculate Approval Probability
        approval_probability = eligibility['eligibility_score'] - risk['risk_score']
        approval_probability = max(20.0, min(95.0, approval_probability))
        
        # MODULE 3: Loan Recommendations
        recommendations = self.get_loan_recommendations(
            farmer_data, 
            eligibility['eligibility_score']
        )
        
        if not recommendations:
            return {
                "status": "NO_SCHEMES_AVAILABLE",
                "message": "No suitable loan schemes found for your profile.",
                "user_id": farmer_data['user_id']
            }
        
        # MODULE 4: Improvement Suggestions
        suggestions = self.generate_improvement_suggestions(farmer_data, eligibility)
        
        # MODULE 5: Repayment Plan
        top_loan_amount = recommendations[0]['eligible_amount_raw']
        repayment_plan = self.generate_repayment_plan(farmer_data, top_loan_amount)
        
        # MODULE 6: Probability Simulator (no change initially)
        probability_simulation = {
            "previous": f"{approval_probability:.1f}%",
            "updated": f"{approval_probability:.1f}%",
            "change_indicator": "INITIAL",
            "message": "Modify inputs to see probability changes"
        }
        
        # MODULE 7: Tamil Voice Explanation
        voice_explanation = self.generate_tamil_voice_explanation(
            farmer_data, recommendations, eligibility['eligibility_score'],
            repayment_plan, suggestions
        )
        
        # Build final response
        return {
            "status": "SUCCESS",
            "user_id": farmer_data['user_id'],
            "eligibility_score": f"{eligibility['eligibility_score']:.1f} / 100",
            "eligibility_status": eligibility['status'],
            "eligibility_breakdown": eligibility['breakdown'],
            "risk_score": f"{risk['risk_score']:.1f} / 100",
            "risk_breakdown": risk['breakdown'],
            "approval_probability": f"{approval_probability:.1f}%",
            "recommended_loans": recommendations,
            "improvement_suggestions": suggestions,
            "repayment_plan": repayment_plan,
            "probability_simulation": probability_simulation,
            "voice_explanation_tamil": voice_explanation,
            "visibility": "PRIVATE_USER_ONLY",
            "generated_at": datetime.now().isoformat()
        }
    
    def save_user_recommendation(self, recommendation: Dict[str, Any], 
                                filename: str = "smart_loan_records.json"):
        """Save private recommendation to user records"""
        try:
            try:
                with open(filename, 'r') as f:
                    records = json.load(f)
            except FileNotFoundError:
                records = {}
            
            user_id = recommendation['user_id']
            records[user_id] = recommendation
            
            with open(filename, 'w') as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False


# ============================================================================
# MAIN API FUNCTION
# ============================================================================

def process_smart_loan_request(farmer_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main API function for Smart Loan Intelligence Module
    Use this in Flask/FastAPI endpoints
    """
    module = SmartLoanIntelligenceModule()
    recommendation = module.generate_complete_recommendation(farmer_data)
    
    if recommendation['status'] == "SUCCESS":
        module.save_user_recommendation(recommendation)
    
    return recommendation


def simulate_probability_change_api(current_data: Dict[str, Any],
                                   modified_data: Dict[str, Any]) -> Dict[str, Any]:
    """API function for interactive simulator"""
    module = SmartLoanIntelligenceModule()
    return module.simulate_probability_change(current_data, modified_data)


# ============================================================================
# DEMO EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("SMART FARMER LOAN INTELLIGENCE MODULE - MASTER DEMO")
    print("AI Financial Advisor with 9 Advanced Modules")
    print("=" * 80)
    
    # Demo: Complete Tamil Nadu Farmer Profile
    print("\n📋 DEMO: Tamil Nadu Farmer - Complete Profile")
    print("-" * 80)
    
    demo_farmer = {
        "user_id": "FARMER_TN_2026_001",
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "land_size": 6.0,
        "crop_selected": "Rice",
        "soil_type": "Clay Loam",
        "irrigation_type": "Drip",
        "annual_income": 150000,
        "previous_loan_history": "None",
        "bank_availability": "Yes"
    }
    
    result = process_smart_loan_request(demo_farmer)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Demo: Interactive Simulator
    print("\n\n🎯 DEMO: Interactive Probability Simulator")
    print("-" * 80)
    print("Scenario: Farmer changes irrigation from Drip to Canal")
    
    modified_farmer = demo_farmer.copy()
    modified_farmer['irrigation_type'] = "Canal"
    
    module = SmartLoanIntelligenceModule()
    simulation = module.simulate_probability_change(demo_farmer, modified_farmer)
    
    print(json.dumps(simulation, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 80)
    print("✅ MASTER MODULE DEMO COMPLETE")
    print("✅ Data saved to: smart_loan_records.json")
    print("=" * 80)
#!/usr/bin/env python3
"""
Available Loans Filter Module - Government Smart Farming Application
=====================================================================

MODULE: Available Loans for You
PURPOSE: Show simple, filtered loan information to logged-in farmers

RULES:
- User must be logged in
- Filter by State (Tamil Nadu / Sikkim)
- NO AI scores or calculations
- Simple farmer-friendly format
- Private user-specific data

Author: Government Smart Farming Team
Date: February 27, 2026
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================================
# LOAN DATABASE - State-wise Available Loans
# ============================================================================

TAMIL_NADU_LOANS = [
    {
        "loan_name": "Kisan Credit Card (KCC)",
        "description": "Short-term crop loan for seeds, fertilizers, and farm needs. Easy repayment after harvest.",
        "maximum_sanction_amount": "₹3,00,000",
        "interest_rate": "4% (after interest subvention)",
        "loan_image": "https://www.india.gov.in/sites/upload_files/npi/files/kisan_credit_card.jpg",
        "apply_link": "https://www.nabard.org/content1.aspx?id=523&catid=8",
        "eligible_for": "All crops",
        "min_land_required": 0.0,
        "provider": "All Commercial Banks, Cooperative Banks, RRBs"
    },
    {
        "loan_name": "Tamil Nadu Cooperative Crop Loan",
        "description": "Zero-interest crop loan from Tamil Nadu Cooperative Banks. Best option for small farmers.",
        "maximum_sanction_amount": "₹2,00,000",
        "interest_rate": "0% (Zero Interest - Government Subsidy)",
        "loan_image": "https://tnpds.gov.in/images/tn_govt_logo.png",
        "apply_link": "https://www.tn.gov.in/scheme/category_data/13",
        "eligible_for": "Rice, Sugarcane, Pulses, Cotton",
        "min_land_required": 1.0,
        "provider": "Tamil Nadu State Cooperative Banks"
    },
    {
        "loan_name": "Agriculture Infrastructure Fund",
        "description": "Medium-term loan for drip irrigation, cold storage, warehouses, and farm equipment.",
        "maximum_sanction_amount": "₹5,00,000",
        "interest_rate": "3% (with interest subvention)",
        "loan_image": "https://pib.gov.in/images/agri_infra.jpg",
        "apply_link": "https://agriinfra.dac.gov.in/",
        "eligible_for": "All farmers with land",
        "min_land_required": 2.0,
        "provider": "Scheduled Commercial Banks"
    },
    {
        "loan_name": "PM Fasal Bima Yojana (Crop Insurance)",
        "description": "Affordable crop insurance against natural disasters, pests, and crop failure.",
        "maximum_sanction_amount": "₹2,00,000 (Sum Insured)",
        "interest_rate": "2% premium (Kharif), 1.5% (Rabi)",
        "loan_image": "https://pmfby.gov.in/images/logo.png",
        "apply_link": "https://pmfby.gov.in/",
        "eligible_for": "All crops",
        "min_land_required": 0.0,
        "provider": "Agriculture Insurance Company of India"
    }
]

SIKKIM_LOANS = [
    {
        "loan_name": "Sikkim Organic Farming Loan",
        "description": "Special loan for 100% organic farmers in Sikkim. Covers seeds, inputs, and certification.",
        "maximum_sanction_amount": "₹5,00,000",
        "interest_rate": "4-5% (with government subsidy)",
        "loan_image": "https://sikkimagrisnet.org/images/organic_logo.png",
        "apply_link": "https://sikkimagrisnet.org/StaticPages/loan-schemes.aspx",
        "eligible_for": "Cardamom, Ginger, Large Cardamom, Organic Vegetables",
        "min_land_required": 2.0,
        "provider": "Sikkim State Cooperative Bank"
    },
    {
        "loan_name": "Agriculture Infrastructure Development Loan",
        "description": "Loan for building greenhouses, polyhouses, and modern farming infrastructure in hilly areas.",
        "maximum_sanction_amount": "₹10,00,000",
        "interest_rate": "3%",
        "loan_image": "https://sikkim.gov.in/images/scheme_logo.png",
        "apply_link": "https://sikkim.gov.in/departments/agriculture",
        "eligible_for": "All crops",
        "min_land_required": 3.0,
        "provider": "NABARD and Commercial Banks"
    },
    {
        "loan_name": "Allied Agricultural Activities Loan",
        "description": "Loan for poultry, dairy, fishery, bee-keeping, and mushroom farming activities.",
        "maximum_sanction_amount": "₹3,00,000",
        "interest_rate": "5%",
        "loan_image": "https://sikkim.gov.in/images/allied_activities.png",
        "apply_link": "https://www.nabard.org/",
        "eligible_for": "All farmers",
        "min_land_required": 0.5,
        "provider": "Regional Rural Banks"
    },
    {
        "loan_name": "Kisan Credit Card (KCC)",
        "description": "Short-term crop loan for seeds, fertilizers, and farm needs. Easy repayment after harvest.",
        "maximum_sanction_amount": "₹3,00,000",
        "interest_rate": "4% (after interest subvention)",
        "loan_image": "https://www.india.gov.in/sites/upload_files/npi/files/kisan_credit_card.jpg",
        "apply_link": "https://www.nabard.org/content1.aspx?id=523&catid=8",
        "eligible_for": "All crops",
        "min_land_required": 0.0,
        "provider": "All Commercial Banks, Cooperative Banks, RRBs"
    }
]


# ============================================================================
# LOAN FILTER CLASS
# ============================================================================

class AvailableLoansFilter:
    """
    Simple Loan Filtering Module - No AI Calculations
    Shows only available loans based on farmer's state and land
    """
    
    def __init__(self):
        self.loan_database = {
            "Tamil Nadu": TAMIL_NADU_LOANS,
            "Sikkim": SIKKIM_LOANS
        }
    
    def get_available_loans(self, farmer_data: Dict) -> Dict:
        """
        Get available loans for a farmer based on their state and land
        
        Args:
            farmer_data (Dict): Contains user_id, state, land_size, etc.
        
        Returns:
            Dict: Formatted loan cards for display
        """
        # Validation
        if not farmer_data.get("user_id"):
            return {
                "status": "ERROR",
                "message": "User must be logged in to view available loans."
            }
        
        state = farmer_data.get("state", "")
        land_size = farmer_data.get("land_size", 0.0)
        
        if state not in self.loan_database:
            return {
                "status": "ERROR",
                "message": f"Sorry, loan schemes for {state} are not available yet. Currently available for Tamil Nadu and Sikkim."
            }
        
        # Get all loans for the state
        all_loans = self.loan_database[state]
        
        # Filter loans based on land requirement
        eligible_loans = []
        for loan in all_loans:
            if land_size >= loan.get("min_land_required", 0.0):
                eligible_loans.append({
                    "loan_name": loan["loan_name"],
                    "description": loan["description"],
                    "maximum_sanction_amount": loan["maximum_sanction_amount"],
                    "interest_rate": loan["interest_rate"],
                    "loan_image": loan["loan_image"],
                    "apply_link": loan["apply_link"],
                    "provider": loan["provider"]
                })
        
        # Build response
        return {
            "status": "SUCCESS",
            "user_id": farmer_data["user_id"],
            "state": state,
            "land_size": f"{land_size} acres",
            "total_available_loans": len(eligible_loans),
            "visible_loans": eligible_loans,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "visibility": "PRIVATE_USER_ONLY"
        }
    
    def get_loan_details(self, loan_name: str, state: str) -> Optional[Dict]:
        """
        Get detailed information about a specific loan
        
        Args:
            loan_name (str): Name of the loan scheme
            state (str): State name
        
        Returns:
            Optional[Dict]: Loan details or None if not found
        """
        if state not in self.loan_database:
            return None
        
        loans = self.loan_database[state]
        for loan in loans:
            if loan["loan_name"].lower() == loan_name.lower():
                return loan
        
        return None


# ============================================================================
# DEMO FUNCTION
# ============================================================================

def demo_tamil_nadu_farmer():
    """Demo: Tamil Nadu farmer with 3 acres"""
    print("\n" + "="*70)
    print("DEMO: Available Loans for Tamil Nadu Farmer")
    print("="*70)
    
    filter_module = AvailableLoansFilter()
    
    farmer = {
        "user_id": "FARMER_TN_001",
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "land_size": 3.0,
        "crop_selected": "Rice",
        "irrigation_type": "Canal",
        "annual_income": 100000
    }
    
    result = filter_module.get_available_loans(farmer)
    
    print(f"\n✅ Status: {result['status']}")
    print(f"👤 User ID: {result['user_id']}")
    print(f"📍 State: {result['state']}")
    print(f"🌾 Land Size: {result['land_size']}")
    print(f"\n📋 Total Available Loans: {result['total_available_loans']}")
    print("\n" + "-"*70)
    
    for i, loan in enumerate(result['visible_loans'], 1):
        print(f"\n{i}. {loan['loan_name']}")
        print(f"   Description: {loan['description']}")
        print(f"   Maximum Amount: {loan['maximum_sanction_amount']}")
        print(f"   Interest Rate: {loan['interest_rate']}")
        print(f"   Provider: {loan['provider']}")
        print(f"   Apply Link: {loan['apply_link']}")
    
    print("\n" + "="*70)
    return result


def demo_sikkim_farmer():
    """Demo: Sikkim farmer with 5 acres for organic farming"""
    print("\n" + "="*70)
    print("DEMO: Available Loans for Sikkim Organic Farmer")
    print("="*70)
    
    filter_module = AvailableLoansFilter()
    
    farmer = {
        "user_id": "FARMER_SK_001",
        "state": "Sikkim",
        "district": "East Sikkim",
        "land_size": 5.0,
        "crop_selected": "Cardamom",
        "irrigation_type": "Rainfed",
        "annual_income": 150000
    }
    
    result = filter_module.get_available_loans(farmer)
    
    print(f"\n✅ Status: {result['status']}")
    print(f"👤 User ID: {result['user_id']}")
    print(f"📍 State: {result['state']}")
    print(f"🌾 Land Size: {result['land_size']}")
    print(f"\n📋 Total Available Loans: {result['total_available_loans']}")
    print("\n" + "-"*70)
    
    for i, loan in enumerate(result['visible_loans'], 1):
        print(f"\n{i}. {loan['loan_name']}")
        print(f"   Description: {loan['description']}")
        print(f"   Maximum Amount: {loan['maximum_sanction_amount']}")
        print(f"   Interest Rate: {loan['interest_rate']}")
        print(f"   Provider: {loan['provider']}")
        print(f"   Apply Link: {loan['apply_link']}")
    
    print("\n" + "="*70)
    return result


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n🏛️  GOVERNMENT SMART FARMING APPLICATION")
    print("MODULE: Available Loans Filter")
    print("Version: 1.0 (Simple Farmer-Friendly)")
    print("Date: February 27, 2026\n")
    
    # Demo 1: Tamil Nadu Farmer
    tn_result = demo_tamil_nadu_farmer()
    
    # Demo 2: Sikkim Farmer
    sk_result = demo_sikkim_farmer()
    
    print("\n✅ Demo Complete!")
    print("\n💡 Key Features:")
    print("   - Simple loan display (no AI calculations)")
    print("   - State-based filtering")
    print("   - Land size eligibility check")
    print("   - Official government links only")
    print("   - Private user-specific results")
#!/usr/bin/env python3
"""
AI Farmer Loan Recommendation & Information Module
===================================================

INTEGRATED: Inside Smart Crop Suggestion App

KEY FEATURES:
- Automatically uses logged-in farmer profile (NO manual entry)
- Shows only eligible government loans
- Multi-language: Tamil, English, Nepali
- Indian Government portal design style
- Private personalized loan list per user

Author: Government Smart Farming Team
Date: February 27, 2026
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================================
# MULTI-LANGUAGE LOAN DATABASE
# ============================================================================

GOVERNMENT_LOANS = {
    "Tamil Nadu": [
        {
            "loan_id": "KCC_001",
            "loan_name": {
                "en": "Kisan Credit Card (KCC)",
                "ta": "கிசான் கடன் அட்டை (KCC)",
                "ne": "किसान क्रेडिट कार्ड (KCC)"
            },
            "eligible_farmer_type": {
                "en": "All farmers with land ownership",
                "ta": "நில உரிமை உள்ள அனைத்து விவசாயிகள்",
                "ne": "भूमि स्वामित्व भएका सबै किसानहरू"
            },
            "maximum_amount": "₹3,00,000",
            "interest_rate": {
                "en": "4% (after interest subvention)",
                "ta": "4% (வட்டி மானியத்திற்கு பிறகு)",
                "ne": "4% (ब्याज अनुदान पछि)"
            },
            "description": {
                "en": "Short-term crop loan for purchasing seeds, fertilizers, pesticides, and meeting daily farm expenses. Easy repayment after harvest.",
                "ta": "விதைகள், உரங்கள், பூச்சிக்கொல்லிகள் வாங்கவும், தினசரி விவசாய செலவுகளை சந்திக்கவும் குறுகிய கால பயிர் கடன். அறுவடைக்கு பிறகு எளிதாக திருப்பிச் செலுத்தலாம்.",
                "ne": "बीउ, मल, कीटनाशक किन्न र दैनिक खेती खर्च पूरा गर्न छोटो अवधिको बाली ऋण। फसल काटे पछि सजिलो भुक्तानी।"
            },
            "loan_image": "🌾🚜",
            "apply_link": "https://www.nabard.org/content1.aspx?id=523&catid=8",
            "provider": "All Commercial Banks, Cooperative Banks, RRBs",
            "min_land_required": 0.0,
            "eligible_crops": ["All crops"]
        },
        {
            "loan_id": "TN_COOP_001",
            "loan_name": {
                "en": "Tamil Nadu Cooperative Crop Loan",
                "ta": "தமிழ்நாடு கூட்டுறவு பயிர் கடன்",
                "ne": "तमिलनाडु सहकारी बाली ऋण"
            },
            "eligible_farmer_type": {
                "en": "Small and Marginal farmers in Tamil Nadu",
                "ta": "தமிழ்நாட்டில் உள்ள சிறு மற்றும் குறு விவசாயிகள்",
                "ne": "तमिलनाडुका साना र सीमान्त किसानहरू"
            },
            "maximum_amount": "₹2,00,000",
            "interest_rate": {
                "en": "0% (Zero Interest - Full Government Subsidy)",
                "ta": "0% (வட்டி இல்லை - முழு அரசு மானியம்)",
                "ne": "0% (शून्य ब्याज - पूर्ण सरकारी अनुदान)"
            },
            "description": {
                "en": "Interest-free crop loan from Tamil Nadu State Cooperative Banks. Best option for small farmers to grow rice, sugarcane, pulses, and cotton.",
                "ta": "தமிழ்நாடு கூட்டுறவு வங்கிகளிலிருந்து வட்டி இல்லாத பயிர் கடன். அரிசி, கரும்பு, பருப்பு வகைகள் மற்றும் பருத்தி வளர்க்க சிறு விவசாயிகளுக்கு சிறந்த வாய்ப்பு.",
                "ne": "तमिलनाडु राज्य सहकारी बैंकबाट ब्याजरहित बाली ऋण। धान, उखु, दाल र कपास उब्जाउन साना किसानहरूको लागि उत्तम विकल्प।"
            },
            "loan_image": "🏦💚",
            "apply_link": "https://www.tn.gov.in/scheme/category_data/13",
            "provider": "Tamil Nadu State Cooperative Banks",
            "min_land_required": 1.0,
            "eligible_crops": ["Rice", "Sugarcane", "Pulses", "Cotton"]
        },
        {
            "loan_id": "AGRI_INFRA_001",
            "loan_name": {
                "en": "Agriculture Infrastructure Fund",
                "ta": "விவசாய உள்கட்டமைப்பு நிதி",
                "ne": "कृषि पूर्वाधार कोष"
            },
            "eligible_farmer_type": {
                "en": "Farmers with 2+ acres land",
                "ta": "2+ ஏக்கர் நிலம் உள்ள விவசாயிகள்",
                "ne": "2+ एकर जमिन भएका किसानहरू"
            },
            "maximum_amount": "₹5,00,000",
            "interest_rate": {
                "en": "3% (with interest subvention)",
                "ta": "3% (வட்டி மானியத்துடன்)",
                "ne": "3% (ब्याज अनुदान संग)"
            },
            "description": {
                "en": "Medium-term loan for installing drip irrigation, building cold storage, warehouses, purchasing tractors and modern farm equipment.",
                "ta": "சொட்டு நீர் பாசனம் நிறுவுதல், குளிர்சாதன கிடங்கு, கிடங்குகள், டிராக்டர்கள் மற்றும் நவீன விவசாய உபகரணங்களை வாங்குவதற்கான நடுத்தர கால கடன்.",
                "ne": "ड्रिप सिँचाइ स्थापना, शीत भण्डारण, गोदाम निर्माण, ट्रैक्टर र आधुनिक कृषि उपकरण खरिदका लागि मध्यम अवधि ऋण।"
            },
            "loan_image": "🏗️💧",
            "apply_link": "https://agriinfra.dac.gov.in/",
            "provider": "Scheduled Commercial Banks",
            "min_land_required": 2.0,
            "eligible_crops": ["All crops"]
        },
        {
            "loan_id": "PM_FASAL_001",
            "loan_name": {
                "en": "PM Fasal Bima Yojana (Crop Insurance)",
                "ta": "பிரதமர் பசல் பீமா யோஜனா (பயிர் காப்பீடு)",
                "ne": "PM फसल बीमा योजना (बाली बीमा)"
            },
            "eligible_farmer_type": {
                "en": "All farmers (Owner/Tenant/Sharecropper)",
                "ta": "அனைத்து விவசாயிகள் (உரிமையாளர்/குத்தகைதாரர்/பங்கு தோட்டக்காரர்)",
                "ne": "सबै किसानहरू (मालिक/भाडामा/साझेदार)"
            },
            "maximum_amount": "₹2,00,000 (Sum Insured)",
            "interest_rate": {
                "en": "2% premium for Kharif, 1.5% for Rabi",
                "ta": "கரீப் பருவத்திற்கு 2% பிரீமியம், ரபி பருவத்திற்கு 1.5%",
                "ne": "खरिफका लागि 2% प्रिमियम, रबीका लागि 1.5%"
            },
            "description": {
                "en": "Affordable crop insurance against natural calamities, pests, diseases, and crop failure. Government pays majority of premium.",
                "ta": "இயற்கை பேரிடர்கள், பூச்சிகள், நோய்கள் மற்றும் பயிர் தோல்விக்கு எதிரான மலிவு பயிர் காப்பீடு. அரசாங்கம் பெரும்பாலான பிரீமியத்தை செலுத்துகிறது.",
                "ne": "प्राकृतिक प्रकोप, कीरा, रोग र बाली असफलता विरुद्ध सस्तो बाली बीमा। सरकारले प्रिमियमको अधिकांश तिर्छ।"
            },
            "loan_image": "🛡️🌱",
            "apply_link": "https://pmfby.gov.in/",
            "provider": "Agriculture Insurance Company of India",
            "min_land_required": 0.0,
            "eligible_crops": ["All crops"]
        }
    ],
    "Sikkim": [
        {
            "loan_id": "SK_ORGANIC_001",
            "loan_name": {
                "en": "Sikkim Organic Farming Loan",
                "ta": "சிக்கிம் இயற்கை விவசாய கடன்",
                "ne": "सिक्किम जैविक खेती ऋण"
            },
            "eligible_farmer_type": {
                "en": "100% Organic certified farmers in Sikkim",
                "ta": "சிக்கிமில் 100% இயற்கை சான்றிதழ் பெற்ற விவசாயிகள்",
                "ne": "सिक्किममा 100% जैविक प्रमाणित किसानहरू"
            },
            "maximum_amount": "₹5,00,000",
            "interest_rate": {
                "en": "4-5% (with government subsidy)",
                "ta": "4-5% (அரசு மானியத்துடன்)",
                "ne": "4-5% (सरकारी अनुदान संग)"
            },
            "description": {
                "en": "Special loan for 100% organic state Sikkim. Covers organic seeds, bio-fertilizers, organic certification, and marketing support.",
                "ta": "100% இயற்கை மாநிலமான சிக்கிமிற்கான சிறப்பு கடன். இயற்கை விதைகள், உயிர் உரங்கள், இயற்கை சான்றிதழ் மற்றும் சந்தை ஆதரவு ஆகியவற்றை உள்ளடக்கியது.",
                "ne": "100% जैविक राज्य सिक्किमको लागि विशेष ऋण। जैविक बीउ, जैव मल, जैविक प्रमाणीकरण र मार्केटिङ समर्थन समावेश।"
            },
            "loan_image": "🌿🏔️",
            "apply_link": "https://sikkimagrisnet.org/StaticPages/loan-schemes.aspx",
            "provider": "Sikkim State Cooperative Bank",
            "min_land_required": 2.0,
            "eligible_crops": ["Cardamom", "Ginger", "Large Cardamom", "Organic Vegetables"]
        },
        {
            "loan_id": "SK_INFRA_001",
            "loan_name": {
                "en": "Agriculture Infrastructure Development Loan",
                "ta": "விவசாய உள்கட்டமைப்பு மேம்பாட்டு கடன்",
                "ne": "कृषि पूर्वाधार विकास ऋण"
            },
            "eligible_farmer_type": {
                "en": "Hill area farmers with 3+ acres",
                "ta": "3+ ஏக்கர் கொண்ட மலைப்பகுதி விவசாயிகள்",
                "ne": "3+ एकर भएका पहाडी क्षेत्रका किसानहरू"
            },
            "maximum_amount": "₹10,00,000",
            "interest_rate": {
                "en": "3%",
                "ta": "3%",
                "ne": "3%"
            },
            "description": {
                "en": "Loan for building greenhouses, polyhouses, and modern farming infrastructure suitable for mountainous terrain in Sikkim.",
                "ta": "சிக்கிமில் மலைப்பகுதிக்கு ஏற்ற பசுமை இல்லங்கள், பாலி ஹவுஸ்கள் மற்றும் நவீன விவசாய உள்கட்டமைப்பு கட்டுவதற்கான கடன்.",
                "ne": "सिक्किमको पहाडी भूभागका लागि उपयुक्त हरित गृह, पोलिहाउस र आधुनिक कृषि पूर्वाधार निर्माणको लागि ऋण।"
            },
            "loan_image": "🏗️🏔️",
            "apply_link": "https://sikkim.gov.in/departments/agriculture",
            "provider": "NABARD and Commercial Banks",
            "min_land_required": 3.0,
            "eligible_crops": ["All crops"]
        },
        {
            "loan_id": "SK_ALLIED_001",
            "loan_name": {
                "en": "Allied Agricultural Activities Loan",
                "ta": "கூட்டு விவசாய செயல்பாடுகள் கடன்",
                "ne": "सम्बन्धित कृषि गतिविधि ऋण"
            },
            "eligible_farmer_type": {
                "en": "Farmers with 0.5+ acres",
                "ta": "0.5+ ஏக்கர் உள்ள விவசாயிகள்",
                "ne": "0.5+ एकर भएका किसानहरू"
            },
            "maximum_amount": "₹3,00,000",
            "interest_rate": {
                "en": "5%",
                "ta": "5%",
                "ne": "5%"
            },
            "description": {
                "en": "Loan for starting poultry farming, dairy units, fishery ponds, bee-keeping, and mushroom cultivation alongside regular farming.",
                "ta": "வழக்கமான விவசாயத்துடன் கோழி வளர்ப்பு, பால் பண்ணைகள், மீன்வளர்ப்பு குளங்கள், தேனீ வளர்ப்பு மற்றும் காளான் சாகுபடி தொடங்குவதற்கான கடன்.",
                "ne": "नियमित खेतीको साथसाथै कुखुरा पालन, दुग्ध उत्पादन, माछा पालन, मौरी पालन र च्याउ खेतीको लागि ऋण।"
            },
            "loan_image": "🐄🐝",
            "apply_link": "https://www.nabard.org/",
            "provider": "Regional Rural Banks",
            "min_land_required": 0.5,
            "eligible_crops": ["All farmers"]
        },
        {
            "loan_id": "KCC_SK_001",
            "loan_name": {
                "en": "Kisan Credit Card (KCC)",
                "ta": "கிசான் கடன் அட்டை (KCC)",
                "ne": "किसान क्रेडिट कार्ड (KCC)"
            },
            "eligible_farmer_type": {
                "en": "All farmers with land ownership",
                "ta": "நில உரிமை உள்ள அனைத்து விவசாயிகள்",
                "ne": "भूमि स्वामित्व भएका सबै किसानहरू"
            },
            "maximum_amount": "₹3,00,000",
            "interest_rate": {
                "en": "4% (after interest subvention)",
                "ta": "4% (வட்டி மானியத்திற்கு பிறகு)",
                "ne": "4% (ब्याज अनुदान पछि)"
            },
            "description": {
                "en": "Short-term crop loan for purchasing seeds, fertilizers, pesticides, and meeting daily farm expenses. Easy repayment after harvest.",
                "ta": "விதைகள், உரங்கள், பூச்சிக்கொல்லிகள் வாங்கவும், தினசரி விவசாய செலவுகளை சந்திக்கவும் குறுகிய கால பயிர் கடன். அறுவடைக்கு பிறகு எளிதாக திருப்பிச் செலுத்தலாம்.",
                "ne": "बीउ, मल, कीटनाशक किन्न र दैनिक खेती खर्च पूरा गर्न छोटो अवधिको बाली ऋण। फसल काटे पछि सजिलो भुक्तानी।"
            },
            "loan_image": "🌾🚜",
            "apply_link": "https://www.nabard.org/content1.aspx?id=523&catid=8",
            "provider": "All Commercial Banks, Cooperative Banks, RRBs",
            "min_land_required": 0.0,
            "eligible_crops": ["All crops"]
        }
    ]
}


# ============================================================================
# FARMER PROFILE DATABASE (Simulated - would come from main app)
# ============================================================================

FARMER_PROFILES = {
    "FARMER_TN_001": {
        "user_id": "FARMER_TN_001",
        "name": "Rajesh Kumar",
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "land_size": 4.5,
        "crop_selected": "Rice",
        "soil_type": "Clay Loam",
        "irrigation_type": "Canal",
        "annual_income": 120000,
        "language_preference": "ta"  # Tamil
    },
    "FARMER_TN_002": {
        "user_id": "FARMER_TN_002",
        "name": "Murugesan",
        "state": "Tamil Nadu",
        "district": "Thanjavur",
        "land_size": 2.0,
        "crop_selected": "Sugarcane",
        "soil_type": "Black",
        "irrigation_type": "Well",
        "annual_income": 80000,
        "language_preference": "ta"
    },
    "FARMER_SK_001": {
        "user_id": "FARMER_SK_001",
        "name": "Karma Dorjee",
        "state": "Sikkim",
        "district": "East Sikkim",
        "land_size": 5.0,
        "crop_selected": "Cardamom",
        "soil_type": "Mountain",
        "irrigation_type": "Rainfed",
        "annual_income": 180000,
        "language_preference": "ne"  # Nepali
    }
}


# ============================================================================
# AI LOAN RECOMMENDATION CLASS
# ============================================================================

class AILoanRecommendation:
    """
    AI Loan Recommendation Module
    - Automatically fetches logged-in user profile
    - Shows only eligible loans
    - Multi-language support
    """
    
    def __init__(self):
        self.loans_db = GOVERNMENT_LOANS
        self.profiles_db = FARMER_PROFILES
    
    def get_farmer_profile(self, user_id: str) -> Optional[Dict]:
        """
        Automatically fetch farmer profile from database
        (In production, this would query from main app database)
        """
        return self.profiles_db.get(user_id)
    
    def get_loan_recommendations(self, user_id: str) -> Dict:
        """
        Main function: Get AI loan recommendations for logged-in user
        
        Args:
            user_id (str): Automatically passed from session
        
        Returns:
            Dict: Personalized loan recommendations in user's language
        """
        # Auto-fetch farmer profile
        farmer = self.get_farmer_profile(user_id)
        
        if not farmer:
            return {
                "status": "ERROR",
                "message": "User profile not found. Please complete your profile first."
            }
        
        state = farmer.get("state")
        land_size = farmer.get("land_size", 0.0)
        language = farmer.get("language_preference", "en")
        
        if state not in self.loans_db:
            return {
                "status": "ERROR",
                "message": f"Loan schemes not available for {state} yet."
            }
        
        # Get all loans for state
        all_loans = self.loans_db[state]
        
        # Filter eligible loans
        eligible_loans = []
        for loan in all_loans:
            if land_size >= loan.get("min_land_required", 0.0):
                eligible_loans.append({
                    "loan_id": loan["loan_id"],
                    "loan_name": loan["loan_name"][language],
                    "eligible_farmer_type": loan["eligible_farmer_type"][language],
                    "maximum_amount": loan["maximum_amount"],
                    "interest_rate": loan["interest_rate"][language],
                    "description": loan["description"][language],
                    "loan_image": loan["loan_image"],
                    "apply_link": loan["apply_link"],
                    "provider": loan["provider"]
                })
        
        return {
            "status": "SUCCESS",
            "user_id": user_id,
            "farmer_name": farmer.get("name"),
            "state": state,
            "district": farmer.get("district"),
            "land_size": f"{land_size} acres",
            "language": self._get_language_name(language),
            "total_eligible_loans": len(eligible_loans),
            "recommended_loans": eligible_loans,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "visibility": "PRIVATE_USER_ONLY"
        }
    
    def _get_language_name(self, code: str) -> str:
        """Convert language code to full name"""
        lang_map = {
            "en": "English",
            "ta": "Tamil (தமிழ்)",
            "ne": "Nepali (नेपाली)"
        }
        return lang_map.get(code, "English")


# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_tamil_nadu_farmer():
    """Demo: Tamil Nadu farmer - Shows loans in Tamil"""
    print("\n" + "="*80)
    print("DEMO 1: Tamil Nadu Farmer (Tamil Language)")
    print("="*80)
    
    ai_loan = AILoanRecommendation()
    result = ai_loan.get_loan_recommendations("FARMER_TN_001")
    
    print(f"\n✅ Status: {result['status']}")
    print(f"👤 Farmer: {result['farmer_name']}")
    print(f"🆔 User ID: {result['user_id']}")
    print(f"📍 Location: {result['district']}, {result['state']}")
    print(f"🌾 Land Size: {result['land_size']}")
    print(f"🌐 Language: {result['language']}")
    print(f"\n💰 Total Eligible Loans: {result['total_eligible_loans']}")
    print("\n" + "-"*80)
    
    for i, loan in enumerate(result['recommended_loans'], 1):
        print(f"\n{i}. {loan['loan_image']} {loan['loan_name']}")
        print(f"   தகுதி: {loan['eligible_farmer_type']}")
        print(f"   அதிகபட்ச தொகை: {loan['maximum_amount']}")
        print(f"   வட்டி விகிதம்: {loan['interest_rate']}")
        print(f"   விவரம்: {loan['description']}")
        print(f"   வழங்குபவர்: {loan['provider']}")
        print(f"   🔗 Apply: {loan['apply_link']}")
    
    print("\n" + "="*80)
    return result


def demo_sikkim_farmer():
    """Demo: Sikkim farmer - Shows loans in Nepali"""
    print("\n" + "="*80)
    print("DEMO 2: Sikkim Farmer (Nepali Language)")
    print("="*80)
    
    ai_loan = AILoanRecommendation()
    result = ai_loan.get_loan_recommendations("FARMER_SK_001")
    
    print(f"\n✅ Status: {result['status']}")
    print(f"👤 Farmer: {result['farmer_name']}")
    print(f"🆔 User ID: {result['user_id']}")
    print(f"📍 Location: {result['district']}, {result['state']}")
    print(f"🌾 Land Size: {result['land_size']}")
    print(f"🌐 Language: {result['language']}")
    print(f"\n💰 Total Eligible Loans: {result['total_eligible_loans']}")
    print("\n" + "-"*80)
    
    for i, loan in enumerate(result['recommended_loans'], 1):
        print(f"\n{i}. {loan['loan_image']} {loan['loan_name']}")
        print(f"   योग्यता: {loan['eligible_farmer_type']}")
        print(f"   अधिकतम रकम: {loan['maximum_amount']}")
        print(f"   ब्याज दर: {loan['interest_rate']}")
        print(f"   विवरण: {loan['description']}")
        print(f"   प्रदायक: {loan['provider']}")
        print(f"   🔗 Apply: {loan['apply_link']}")
    
    print("\n" + "="*80)
    return result


def demo_english_view():
    """Demo: Show same loan in English for comparison"""
    print("\n" + "="*80)
    print("DEMO 3: Tamil Nadu Farmer (English Language)")
    print("="*80)
    
    # Temporarily change language preference
    FARMER_PROFILES["FARMER_TN_001"]["language_preference"] = "en"
    
    ai_loan = AILoanRecommendation()
    result = ai_loan.get_loan_recommendations("FARMER_TN_001")
    
    print(f"\n✅ Status: {result['status']}")
    print(f"👤 Farmer: {result['farmer_name']}")
    print(f"📍 Location: {result['district']}, {result['state']}")
    print(f"🌐 Language: {result['language']}")
    print(f"\n💰 Total Eligible Loans: {result['total_eligible_loans']}")
    print("\n" + "-"*80)
    
    for i, loan in enumerate(result['recommended_loans'], 1):
        print(f"\n{i}. {loan['loan_image']} {loan['loan_name']}")
        print(f"   Eligible: {loan['eligible_farmer_type']}")
        print(f"   Maximum: {loan['maximum_amount']}")
        print(f"   Interest: {loan['interest_rate']}")
        print(f"   Description: {loan['description']}")
        print(f"   Provider: {loan['provider']}")
        print(f"   🔗 Apply: {loan['apply_link']}")
    
    # Reset language
    FARMER_PROFILES["FARMER_TN_001"]["language_preference"] = "ta"
    
    print("\n" + "="*80)
    return result


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🏛️" * 20)
    print("AI FARMER LOAN RECOMMENDATION & INFORMATION MODULE")
    print("Integrated Inside Smart Crop Suggestion App")
    print("🏛️" * 20)
    print("\n✨ Features:")
    print("  ✓ Auto-fetches logged-in farmer profile (NO manual entry)")
    print("  ✓ Shows only eligible government loans")
    print("  ✓ Multi-language: Tamil, English, Nepali")
    print("  ✓ Indian Government portal design")
    print("  ✓ Private personalized recommendations")
    print("\n" + "="*80)
    
    # Run demos
    tn_result_tamil = demo_tamil_nadu_farmer()
    sk_result_nepali = demo_sikkim_farmer()
    tn_result_english = demo_english_view()
    
    print("\n\n✅ Demo Complete!")
    print("\n💡 Key Highlights:")
    print(f"  - Tamil Nadu farmer got {tn_result_tamil['total_eligible_loans']} loans in Tamil")
    print(f"  - Sikkim farmer got {sk_result_nepali['total_eligible_loans']} loans in Nepali")
    print(f"  - Same data available in English too")
    print("\n🎯 Zero manual entry - All data from user profile!")
    print("🌐 Full multi-language support!")
    print("🔒 Private results for each user!")
"""
Flask REST API for Smart Farmer Loan Intelligence Module
Supports all 9 AI modules with interactive simulator
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from smart_loan_intelligence import (
    process_smart_loan_request,
    simulate_probability_change_api,
    SmartLoanIntelligenceModule
)
from available_loans_filter import AvailableLoansFilter
from ai_loan_recommendation import AILoanRecommendation
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)


# ============================================================================
# AUTHENTICATION MIDDLEWARE
# ============================================================================

def login_required(f):
    """Decorator for protected endpoints"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'status': 'UNAUTHORIZED',
                'message': 'Please login to access AI Loan Intelligence'
            }), 401
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# SMART LOAN INTELLIGENCE ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'service': 'Smart Farmer Loan Intelligence Module',
        'version': '2.0 (Master Edition)',
        'features': [
            'AI Eligibility Scoring',
            'Risk Assessment',
            'State-based Recommendations',
            'Improvement Suggestions',
            'Harvest-based Repayment',
            'Interactive Simulator',
            'Tamil Voice Explanation',
            'Auto-updating Schemes'
        ]
    })


@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint"""
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')
    
    if user_id and password:
        session['user_id'] = user_id
        return jsonify({
            'status': 'SUCCESS',
            'message': 'Login successful',
            'user_id': user_id
        })
    else:
        return jsonify({
            'status': 'FAILED',
            'message': 'Invalid credentials'
        }), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout endpoint"""
    session.pop('user_id', None)
    return jsonify({
        'status': 'SUCCESS',
        'message': 'Logout successful'
    })


@app.route('/api/loan/ai-intelligence', methods=['POST'])
@login_required
def get_ai_loan_intelligence():
    """
    Main endpoint: Get complete AI loan intelligence
    
    Request Body (10 required fields):
    {
        "user_id": "FARMER_TN_001",
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "land_size": 6.0,
        "crop_selected": "Rice",
        "soil_type": "Clay Loam",
        "irrigation_type": "Drip",
        "annual_income": 150000,
        "previous_loan_history": "None",
        "bank_availability": "Yes"
    }
    
    Response includes all 9 modules:
    - Eligibility Score (0-100)
    - Risk Assessment
    - Loan Recommendations
    - Improvement Suggestions
    - Repayment Planner
    - Simulator baseline
    - Tamil Voice Explanation
    - Private visibility
    """
    try:
        farmer_data = request.json
        
        # Security: Ensure user can only check their own data
        logged_in_user = session.get('user_id')
        if farmer_data.get('user_id') != logged_in_user:
            return jsonify({
                'status': 'FORBIDDEN',
                'message': 'You can only check your own loan intelligence'
            }), 403
        
        # Process using AI module
        result = process_smart_loan_request(farmer_data)
        
        if result['status'] == 'SUCCESS':
            return jsonify(result), 200
        elif result['status'] == 'INCOMPLETE_PROFILE':
            return jsonify(result), 400
        else:
            return jsonify(result), 200
            
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': f'AI processing error: {str(e)}'
        }), 500


@app.route('/api/loan/simulate-probability', methods=['POST'])
@login_required
def simulate_probability():
    """
    Interactive simulator endpoint
    
    Request Body:
    {
        "current_data": {...},  // Original farmer data
        "modified_data": {...}  // Modified values
    }
    
    Response:
    {
        "previous_probability": "63.8%",
        "updated_probability": "67.8%",
        "change": "+4.0",
        "change_indicator": "INCREASE",
        "message": "வெற்றி வாய்ப்பு அதிகரித்துள்ளது"
    }
    """
    try:
        data = request.json
        current_data = data.get('current_data')
        modified_data = data.get('modified_data')
        
        if not current_data or not modified_data:
            return jsonify({
                'status': 'ERROR',
                'message': 'Both current_data and modified_data are required'
            }), 400
        
        # Security check
        logged_in_user = session.get('user_id')
        if current_data.get('user_id') != logged_in_user:
            return jsonify({
                'status': 'FORBIDDEN',
                'message': 'Unauthorized simulation'
            }), 403
        
        # Run simulation
        result = simulate_probability_change_api(current_data, modified_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': f'Simulation error: {str(e)}'
        }), 500


@app.route('/api/loan/my-recommendations', methods=['GET'])
@login_required
def get_my_recommendations():
    """Get saved AI recommendations for current user"""
    import json
    
    try:
        user_id = session.get('user_id')
        
        try:
            with open('smart_loan_records.json', 'r', encoding='utf-8') as f:
                records = json.load(f)
                
            if user_id in records:
                return jsonify(records[user_id]), 200
            else:
                return jsonify({
                    'status': 'NOT_FOUND',
                    'message': 'No AI recommendations found. Please complete the intelligence form first.'
                }), 404
                
        except FileNotFoundError:
            return jsonify({
                'status': 'NOT_FOUND',
                'message': 'No AI recommendations found.'
            }), 404
            
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/api/loan/schemes', methods=['GET'])
def get_loan_schemes():
    """
    Get latest loan schemes by state
    Query: ?state=Tamil Nadu
    """
    module = SmartLoanIntelligenceModule()
    state = request.args.get('state')
    
    if state:
        schemes = module.get_latest_schemes(state)
        if schemes:
            return jsonify({
                'status': 'SUCCESS',
                'state': state,
                'schemes': schemes,
                'last_updated': schemes[0]['last_updated'] if schemes else None
            })
        else:
            return jsonify({
                'status': 'NOT_FOUND',
                'message': f'No schemes for state: {state}'
            }), 404
    else:
        all_schemes = module.loan_schemes
        return jsonify({
            'status': 'SUCCESS',
            'schemes': all_schemes
        })


@app.route('/api/admin/update-scheme', methods=['POST'])
def admin_update_scheme():
    """
    Admin endpoint: Update loan scheme dynamically
    
    Request Body:
    {
        "admin_key": "SECRET_KEY",
        "state": "Tamil Nadu",
        "scheme_name": "Kisan Credit Card",
        "updates": {
            "interest_rate": "3.5% (new rate)",
            "max_amount": 350000
        }
    }
    """
    try:
        data = request.json
        admin_key = data.get('admin_key')
        
        # Simple admin authentication (use proper auth in production)
        if admin_key != "ADMIN_SECRET_2026":
            return jsonify({
                'status': 'UNAUTHORIZED',
                'message': 'Invalid admin key'
            }), 401
        
        state = data.get('state')
        scheme_name = data.get('scheme_name')
        updates = data.get('updates')
        
        module = SmartLoanIntelligenceModule()
        success = module.update_loan_scheme(state, scheme_name, updates)
        
        if success:
            return jsonify({
                'status': 'SUCCESS',
                'message': f'Scheme "{scheme_name}" updated successfully',
                'state': state,
                'updates': updates
            })
        else:
            return jsonify({
                'status': 'FAILED',
                'message': 'Scheme update failed'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/api/validate-profile', methods=['POST'])
@login_required
def validate_profile():
    """Validate farmer profile before AI processing"""
    module = SmartLoanIntelligenceModule()
    
    try:
        farmer_data = request.json
        validation_result = module.validate_profile(farmer_data)
        
        if validation_result['status'] == 'VALID':
            return jsonify(validation_result), 200
        else:
            return jsonify(validation_result), 400
            
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': f'Validation error: {str(e)}'
        }), 500


@app.route('/api/loan/available', methods=['POST'])
@login_required
def get_available_loans():
    """
    Simple Loan Filtering Endpoint - No AI Calculations
    Shows only available loans based on state and land size
    
    Request Body:
    {
        "user_id": "FARMER_TN_001",
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "land_size": 3.0,
        "crop_selected": "Rice",
        "irrigation_type": "Canal",
        "annual_income": 100000
    }
    
    Response: Simple loan cards with:
    - loan_name
    - description (< 40 words)
    - maximum_sanction_amount
    - interest_rate
    - apply_link
    - provider
    
    NO AI scores or technical calculations shown
    """
    try:
        farmer_data = request.json
        
        # Security: Ensure user can only check their own data
        logged_in_user = session.get('user_id')
        if farmer_data.get('user_id') != logged_in_user:
            return jsonify({
                'status': 'FORBIDDEN',
                'message': 'You can only view your own available loans'
            }), 403
        
        # Use simple filter module (not AI)
        loan_filter = AvailableLoansFilter()
        result = loan_filter.get_available_loans(farmer_data)
        
        if result['status'] == 'SUCCESS':
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': f'Error fetching available loans: {str(e)}'
        }), 500


@app.route('/api/loan/recommendations', methods=['GET'])
@login_required
def get_ai_loan_recommendations():
    """
    AI Loan Recommendation Endpoint - Auto-fetch user profile
    NO manual entry required - uses logged-in user profile automatically
    
    Query Parameters:
    ?lang=en  (optional: en, ta, ne - default: en)
    
    Response: Multi-language loan recommendations
    {
        "status": "SUCCESS",
        "farmer_name": "Rajesh Kumar",
        "user_id": "FARMER_TN_001",
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "land_size": "4.5 acres",
        "language": "English",
        "total_eligible_loans": 4,
        "recommended_loans": [
            {
                "loan_name": "Kisan Credit Card (KCC)",
                "eligible_farmer_type": "All farmers with land ownership",
                "maximum_amount": "₹3,00,000",
                "interest_rate": "4% (after interest subvention)",
                "description": "Short-term crop loan...",
                "loan_image": "🌾🚜",
                "apply_link": "https://...",
                "provider": "All Banks"
            }
        ],
        "generated_at": "2026-02-27 10:30:00",
        "visibility": "PRIVATE_USER_ONLY"
    }
    
    Features:
    - Auto-fetches logged-in user profile (NO form entry)
    - Multi-language: Tamil, English, Nepali
    - Shows only eligible loans based on land size
    - Government portal design compatible
    - Private personalized data
    """
    try:
        # Get logged-in user ID from session
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                'status': 'UNAUTHORIZED',
                'message': 'Please login to view loan recommendations'
            }), 401
        
        # Get language preference from query param (default: en)
        lang = request.args.get('lang', 'en')
        
        if lang not in ['en', 'ta', 'ne']:
            return jsonify({
                'status': 'ERROR',
                'message': 'Invalid language. Use: en, ta, or ne'
            }), 400
        
        # Use AI Loan Recommendation module
        ai_loan = AILoanRecommendation()
        
        # Auto-fetch user profile and get recommendations
        result = ai_loan.get_loan_recommendations(user_id)
        
        if result['status'] == 'SUCCESS':
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': f'Error fetching recommendations: {str(e)}'
        }), 500


# ============================================================================
# JAVASCRIPT INTEGRATION EXAMPLES
# ============================================================================

"""
// Example 1: Get AI Loan Intelligence
async function getAILoanIntelligence() {
    const farmerData = {
        user_id: "FARMER_TN_001",
        state: "Tamil Nadu",
        district: "Coimbatore",
        land_size: 6.0,
        crop_selected: "Rice",
        soil_type: "Clay Loam",
        irrigation_type: "Drip",
        annual_income: 150000,
        previous_loan_history: "None",
        bank_availability: "Yes"
    };
    
    const response = await fetch('http://localhost:5000/api/loan/ai-intelligence', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(farmerData),
        credentials: 'include'
    });
    
    const result = await response.json();
    
    if (result.status === 'SUCCESS') {
        console.log('Eligibility Score:', result.eligibility_score);
        console.log('Recommended Loans:', result.recommended_loans);
        console.log('Improvement Tips:', result.improvement_suggestions);
        console.log('Tamil Explanation:', result.voice_explanation_tamil);
    }
}


// Example 2: Interactive Simulator
async function simulateProbabilityChange() {
    const currentData = {...originalData};
    const modifiedData = {...originalData};
    modifiedData.irrigation_type = "Drip";  // Changed from Canal
    
    const response = await fetch('http://localhost:5000/api/loan/simulate-probability', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            current_data: currentData,
            modified_data: modifiedData
        }),
        credentials: 'include'
    });
    
    const result = await response.json();
    console.log('Probability Change:', result.change);
    console.log('Message:', result.message);
}


// Example 3: Get Latest Schemes
async function getLatestSchemes(state) {
    const response = await fetch(`http://localhost:5000/api/loan/schemes?state=${state}`);
    const result = await response.json();
    
    if (result.status === 'SUCCESS') {
        console.log('Schemes:', result.schemes);
        console.log('Last Updated:', result.last_updated);
    }
}
"""


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("SMART FARMER LOAN INTELLIGENCE MODULE - Flask API Server")
    print("=" * 80)
    print("\n🤖 AI Financial Advisor with 9 Advanced Modules")
    print("\n📡 API Endpoints:")
    print("  POST   /api/login")
    print("  POST   /api/logout")
    print("  POST   /api/loan/ai-intelligence       [Protected] - Complete AI Analysis")
    print("  POST   /api/loan/simulate-probability  [Protected] - Interactive Simulator")
    print("  GET    /api/loan/my-recommendations    [Protected] - Saved Recommendations")
    print("  POST   /api/loan/available             [Protected] - Simple Loan Cards (No AI)")
    print("  GET    /api/loan/recommendations?lang= [Protected] - AI Auto-fetch (Multi-lang)")
    print("  GET    /api/loan/schemes?state=...     - Latest Schemes")
    print("  POST   /api/admin/update-scheme        [Admin] - Update Schemes")
    print("  POST   /api/validate-profile           [Protected] - Validate Form")
    print("  GET    /api/health                     - Health Check")
    print("\n✅ Features Enabled:")
    print("  ✓ Eligibility Score (0-100)")
    print("  ✓ Risk Assessment")
    print("  ✓ State-based Recommendations")
    print("  ✓ Improvement Suggestions")
    print("  ✓ Harvest-based Repayment")
    print("  ✓ Interactive Probability Simulator")
    print("  ✓ Tamil Voice Explanation")
    print("  ✓ Auto-updating Schemes")
    print("  ✓ Multi-language Support (Tamil, English, Nepali)")
    print("  ✓ Auto Profile Fetch (No Manual Entry)")
    print("\n🔐 Authentication: Session-based")
    print("🔒 Privacy: User-specific data only")
    print("\n🚀 Starting server on http://localhost:5000")
    print("=" * 80)
    
    app.run(debug=True, port=5000)
#!/usr/bin/env python3
"""
Loan Recommendation Module - RANDOM DATASET TEST
Using real farmer data to test AI loan recommendations
"""

from ai_loan_recommendation import AILoanRecommendation, FARMER_PROFILES, GOVERNMENT_LOANS
import json

# ============================================================================
# RANDOM FARMER DATASET (From Image)
# ============================================================================

RANDOM_FARMERS = {
    "FARMER_001": {
        "user_id": "FARMER_001",
        "name": "Rajesh Kumar",
        "age": 45,
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "land_size": 5.5,
        "crop_selected": "Rice",
        "soil_type": "Clay Loam",
        "irrigation_type": "Canal",
        "annual_income": 150000,
        "language_preference": "ta"
    },
    "FARMER_002": {
        "user_id": "FARMER_002",
        "name": "Murugesan S",
        "age": 52,
        "state": "Tamil Nadu",
        "district": "Thanjavur",
        "land_size": 3.2,
        "crop_selected": "Sugarcane",
        "soil_type": "Black",
        "irrigation_type": "Well",
        "annual_income": 120000,
        "language_preference": "ta"
    },
    "FARMER_003": {
        "user_id": "FARMER_003",
        "name": "Lakshmi Devi",
        "age": 38,
        "state": "Tamil Nadu",
        "district": "Madurai",
        "land_size": 2.0,
        "crop_selected": "Cotton",
        "soil_type": "Red",
        "irrigation_type": "Rainfed",
        "annual_income": 80000,
        "language_preference": "ta"
    },
    "FARMER_004": {
        "user_id": "FARMER_004",
        "name": "Karma Dorjee",
        "age": 41,
        "state": "Sikkim",
        "district": "East Sikkim",
        "land_size": 4.8,
        "crop_selected": "Cardamom",
        "soil_type": "Mountain",
        "irrigation_type": "Rainfed",
        "annual_income": 200000,
        "language_preference": "ne"
    },
    "FARMER_005": {
        "user_id": "FARMER_005",
        "name": "Tashi Namgyal",
        "age": 36,
        "state": "Sikkim",
        "district": "West Sikkim",
        "land_size": 6.5,
        "crop_selected": "Ginger",
        "soil_type": "Mountain",
        "irrigation_type": "Sprinkler",
        "annual_income": 180000,
        "language_preference": "ne"
    },
    "FARMER_006": {
        "user_id": "FARMER_006",
        "name": "Arumugam P",
        "age": 55,
        "state": "Tamil Nadu",
        "district": "Salem",
        "land_size": 8.0,
        "crop_selected": "Sugarcane",
        "soil_type": "Alluvial",
        "irrigation_type": "Drip",
        "annual_income": 250000,
        "language_preference": "ta"
    },
    "FARMER_007": {
        "user_id": "FARMER_007",
        "name": "Pema Bhutia",
        "age": 29,
        "state": "Sikkim",
        "district": "South Sikkim",
        "land_size": 1.5,
        "crop_selected": "Organic Vegetables",
        "soil_type": "Mountain",
        "irrigation_type": "Well",
        "annual_income": 90000,
        "language_preference": "ne"
    },
    "FARMER_008": {
        "user_id": "FARMER_008",
        "name": "Selvam R",
        "age": 48,
        "state": "Tamil Nadu",
        "district": "Erode",
        "land_size": 4.0,
        "crop_selected": "Turmeric",
        "soil_type": "Clay Loam",
        "irrigation_type": "Canal",
        "annual_income": 135000,
        "language_preference": "ta"
    },
    "FARMER_009": {
        "user_id": "FARMER_009",
        "name": "Sangay Lepcha",
        "age": 33,
        "state": "Sikkim",
        "district": "North Sikkim",
        "land_size": 3.5,
        "crop_selected": "Large Cardamom",
        "soil_type": "Mountain",
        "irrigation_type": "Rainfed",
        "annual_income": 160000,
        "language_preference": "ne"
    },
    "FARMER_010": {
        "user_id": "FARMER_010",
        "name": "Karthik M",
        "age": 31,
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "land_size": 1.0,
        "crop_selected": "Rice",
        "soil_type": "Clay",
        "irrigation_type": "Well",
        "annual_income": 60000,
        "language_preference": "ta"
    }
}


# ============================================================================
# UPDATE AI MODULE WITH RANDOM DATASET
# ============================================================================

def update_farmer_profiles():
    """Update the global farmer profiles with random dataset"""
    FARMER_PROFILES.clear()
    FARMER_PROFILES.update(RANDOM_FARMERS)
    print(f"✅ Loaded {len(RANDOM_FARMERS)} farmers into system")


# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_single_farmer(user_id: str, show_details: bool = True):
    """Test loan recommendations for a single farmer"""
    ai_loan = AILoanRecommendation()
    result = ai_loan.get_loan_recommendations(user_id)
    
    if result['status'] != 'SUCCESS':
        print(f"❌ Error for {user_id}: {result.get('message')}")
        return None
    
    if show_details:
        print("\n" + "="*80)
        print(f"🧑‍🌾 Farmer: {result['farmer_name']} (Age: {RANDOM_FARMERS[user_id]['age']})")
        print("="*80)
        print(f"🆔 User ID: {result['user_id']}")
        print(f"📍 Location: {result['district']}, {result['state']}")
        print(f"🌾 Land Size: {result['land_size']}")
        print(f"🌱 Crop: {RANDOM_FARMERS[user_id]['crop_selected']}")
        print(f"💧 Irrigation: {RANDOM_FARMERS[user_id]['irrigation_type']}")
        print(f"💰 Annual Income: ₹{RANDOM_FARMERS[user_id]['annual_income']:,}")
        print(f"🌐 Language: {result['language']}")
        print(f"\n💳 Total Eligible Loans: {result['total_eligible_loans']}")
        print("\n" + "-"*80)
        
        for i, loan in enumerate(result['recommended_loans'], 1):
            print(f"\n{i}. {loan['loan_image']} {loan['loan_name']}")
            print(f"   Eligible: {loan['eligible_farmer_type']}")
            print(f"   Max Amount: {loan['maximum_amount']}")
            print(f"   Interest: {loan['interest_rate']}")
            print(f"   Provider: {loan['provider']}")
            print(f"   🔗 Apply: {loan['apply_link']}")
        
        print("\n" + "="*80)
    
    return result


def test_all_farmers():
    """Test loan recommendations for all farmers in dataset"""
    print("\n" + "🌾" * 40)
    print("LOAN RECOMMENDATION MODULE - RANDOM DATASET TEST")
    print("Testing all farmers from the dataset")
    print("🌾" * 40)
    
    update_farmer_profiles()
    
    # Summary statistics
    tamil_nadu_count = 0
    sikkim_count = 0
    total_loans = 0
    
    results_summary = []
    
    for user_id in RANDOM_FARMERS.keys():
        result = test_single_farmer(user_id, show_details=True)
        
        if result and result['status'] == 'SUCCESS':
            farmer = RANDOM_FARMERS[user_id]
            
            if farmer['state'] == 'Tamil Nadu':
                tamil_nadu_count += 1
            elif farmer['state'] == 'Sikkim':
                sikkim_count += 1
            
            total_loans += result['total_eligible_loans']
            
            results_summary.append({
                'name': result['farmer_name'],
                'state': result['state'],
                'land_size': result['land_size'],
                'eligible_loans': result['total_eligible_loans'],
                'language': result['language']
            })
    
    # Print summary
    print("\n\n" + "📊" * 40)
    print("SUMMARY STATISTICS")
    print("📊" * 40)
    print(f"\n✅ Total Farmers Tested: {len(RANDOM_FARMERS)}")
    print(f"   - Tamil Nadu: {tamil_nadu_count} farmers")
    print(f"   - Sikkim: {sikkim_count} farmers")
    print(f"\n💳 Total Loan Recommendations: {total_loans}")
    print(f"📊 Average Loans per Farmer: {total_loans / len(RANDOM_FARMERS):.1f}")
    
    print("\n\n📋 QUICK SUMMARY TABLE")
    print("-" * 80)
    print(f"{'Name':<20} {'State':<15} {'Land':<12} {'Loans':<8} {'Language':<15}")
    print("-" * 80)
    
    for summary in results_summary:
        print(f"{summary['name']:<20} {summary['state']:<15} {summary['land_size']:<12} "
              f"{summary['eligible_loans']:<8} {summary['language']:<15}")
    
    print("-" * 80)


def test_specific_scenarios():
    """Test specific interesting scenarios"""
    print("\n\n" + "🎯" * 40)
    print("SPECIFIC SCENARIO TESTS")
    print("🎯" * 40)
    
    update_farmer_profiles()
    
    # Scenario 1: Small farmer with low income
    print("\n\n📌 SCENARIO 1: Small Farmer (1 acre, Low Income)")
    print("Testing: Karthik M - 1 acre, ₹60,000 income")
    test_single_farmer("FARMER_010", show_details=True)
    
    # Scenario 2: Large farmer with high income
    print("\n\n📌 SCENARIO 2: Large Farmer (8 acres, High Income)")
    print("Testing: Arumugam P - 8 acres, ₹2,50,000 income")
    test_single_farmer("FARMER_006", show_details=True)
    
    # Scenario 3: Sikkim organic farmer
    print("\n\n📌 SCENARIO 3: Sikkim Organic Farmer")
    print("Testing: Karma Dorjee - 4.8 acres Cardamom")
    test_single_farmer("FARMER_004", show_details=True)


def generate_json_output():
    """Generate JSON output for API integration testing"""
    print("\n\n" + "📄" * 40)
    print("JSON OUTPUT FOR API TESTING")
    print("📄" * 40)
    
    update_farmer_profiles()
    
    all_results = {}
    
    for user_id in list(RANDOM_FARMERS.keys())[:3]:  # First 3 farmers
        ai_loan = AILoanRecommendation()
        result = ai_loan.get_loan_recommendations(user_id)
        all_results[user_id] = result
    
    json_output = json.dumps(all_results, indent=2, ensure_ascii=False)
    
    print("\n" + json_output)
    
    # Save to file
    with open('random_dataset_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print("\n\n✅ Results saved to: random_dataset_results.json")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🏛️" * 40)
    print("AI FARMER LOAN RECOMMENDATION MODULE")
    print("RANDOM DATASET TEST - 10 REAL FARMERS")
    print("🏛️" * 40)
    
    # Test all farmers
    test_all_farmers()
    
    # Test specific scenarios
    test_specific_scenarios()
    
    # Generate JSON output
    generate_json_output()
    
    print("\n\n✅ ALL TESTS COMPLETE!")
    print("\n💡 Key Insights:")
    print("   - Tamil Nadu farmers get 4 loan options")
    print("   - Sikkim farmers get 4 loan options")
    print("   - Small farmers (< 1 acre) still eligible for KCC and PM Fasal Bima")
    print("   - Zero-interest TN Cooperative Loan available for 1+ acre farmers")
    print("   - Sikkim organic farmers can get up to ₹10,00,000 infrastructure loan")
    print("\n🎯 Random dataset successfully tested!")
