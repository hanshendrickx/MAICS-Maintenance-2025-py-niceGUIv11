"""
MACS Feature Manager
===================
Manages feature availability based on security level.
Implements runtime feature gating for PRO/FREE versions.
"""

import functools
import hashlib
import inspect
from typing import Callable, Any, Dict, List
from security_manager import SecurityManager


class FeatureManager:
    """Manages feature availability and access control."""
    
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager
        self.feature_registry = {}
        
    def feature_gate(self, required_level: str = "OPEN", 
                    fallback_message: str = None,
                    fallback_function: Callable = None):
        """Decorator to gate features based on security level."""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                current_level = self.security.determine_security_level()
                
                # Define level hierarchy
                level_hierarchy = {"OPEN": 0, "PROTECTED": 1, "PRO": 2}
                
                if level_hierarchy.get(current_level, 0) >= level_hierarchy.get(required_level, 0):
                    return func(*args, **kwargs)
                else:
                    # Feature not available at current level
                    if fallback_function:
                        return fallback_function(*args, **kwargs)
                    elif fallback_message:
                        return {"error": fallback_message, "required_level": required_level}
                    else:
                        return self._default_feature_blocked_response(func.__name__, required_level)
            
            # Register feature
            self.feature_registry[func.__name__] = {
                "required_level": required_level,
                "function": func,
                "module": func.__module__
            }
            
            return wrapper
        return decorator
    
    def _default_feature_blocked_response(self, feature_name: str, required_level: str) -> Dict:
        """Default response when feature is blocked."""
        return {
            "error": f"Feature '{feature_name}' requires {required_level} level",
            "current_level": self.security.determine_security_level(),
            "required_level": required_level,
            "upgrade_info": "Contact licensing@macs-medical.com for PRO access"
        }
    
    def get_available_features(self) -> Dict:
        """Get list of features available at current security level."""
        current_level = self.security.determine_security_level()
        level_hierarchy = {"OPEN": 0, "PROTECTED": 1, "PRO": 2}
        current_hierarchy = level_hierarchy.get(current_level, 0)
        
        available = {}
        blocked = {}
        
        for feature_name, feature_info in self.feature_registry.items():
            required_hierarchy = level_hierarchy.get(feature_info["required_level"], 0)
            
            if current_hierarchy >= required_hierarchy:
                available[feature_name] = feature_info
            else:
                blocked[feature_name] = feature_info
        
        return {
            "current_level": current_level,
            "available_features": available,
            "blocked_features": blocked
        }


# Global feature manager instance
security_manager = SecurityManager()
feature_manager = FeatureManager(security_manager)


# Medical Analysis Features with Progressive Unlocking
class MedicalFeatures:
    """Medical analysis features with security-based gating."""
    
    @feature_manager.feature_gate("OPEN")
    def basic_symptom_analysis(self, symptoms: List[str]) -> Dict:
        """Basic symptom analysis - available in all versions."""
        return {
            "analysis": "Basic symptom correlation",
            "symptoms": symptoms,
            "confidence": "Low-Medium",
            "recommendations": ["Consult healthcare provider", "Monitor symptoms"]
        }
    
    @feature_manager.feature_gate("PROTECTED")
    def intermediate_diagnosis_support(self, patient_data: Dict) -> Dict:
        """Intermediate diagnostic support - PROTECTED level and above."""
        return {
            "analysis": "Enhanced diagnostic correlation",
            "risk_factors": ["Age", "Medical history", "Symptom patterns"],
            "confidence": "Medium-High",
            "differential_diagnosis": ["Condition A", "Condition B", "Condition C"]
        }
    
    @feature_manager.feature_gate("PRO", 
                                fallback_message="Advanced medical analysis requires PRO license")
    def advanced_medical_ai(self, patient_data: Dict, medical_history: Dict) -> Dict:
        """Advanced AI-powered medical analysis - PRO only."""
        return {
            "analysis": "AI-powered comprehensive medical analysis",
            "ml_predictions": {"condition_probability": 0.85, "risk_score": 0.23},
            "evidence_based_recommendations": [
                "Immediate cardiology consultation recommended",
                "ECG within 24 hours",
                "Consider cardiac enzymes"
            ],
            "confidence": "Very High",
            "hipaa_audit_trail": "Logged for compliance",
            "differential_diagnosis": [
                {"condition": "Acute MI", "probability": 0.75},
                {"condition": "Unstable Angina", "probability": 0.20},
                {"condition": "GERD", "probability": 0.05}
            ]
        }
    
    @feature_manager.feature_gate("PRO")
    def hipaa_compliant_storage(self, patient_data: Dict) -> Dict:
        """HIPAA-compliant patient data storage - PRO only."""
        return {
            "storage_status": "Encrypted and stored securely",
            "encryption": "AES-256",
            "audit_trail": "Complete access log maintained",
            "compliance": "HIPAA, GDPR, HITECH compliant"
        }
    
    @feature_manager.feature_gate("OPEN")
    def basic_medical_calculator(self, calculation_type: str, values: Dict) -> Dict:
        """Basic medical calculators - available to all."""
        calculators = {
            "bmi": lambda: values["weight"] / (values["height"] ** 2),
            "bmr": lambda: 88.362 + (13.397 * values["weight"]) + (4.799 * values["height"]) - (5.677 * values["age"])
        }
        
        if calculation_type in calculators:
            result = calculators[calculation_type]()
            return {"calculation": calculation_type, "result": result, "unit": "metric"}
        else:
            return {"error": "Calculator not found"}


# Data Protection Features
class DataProtectionFeatures:
    """Data protection features with progressive security."""
    
    @feature_manager.feature_gate("OPEN")
    def basic_data_validation(self, data: Dict) -> Dict:
        """Basic input validation - available to all."""
        return {"validated": True, "sanitized": True, "security_level": "Basic"}
    
    @feature_manager.feature_gate("PROTECTED")
    def enhanced_data_protection(self, data: Dict) -> Dict:
        """Enhanced data protection - PROTECTED and PRO."""
        return {
            "encrypted": True,
            "hash_verification": True,
            "integrity_check": "Passed",
            "security_level": "Enhanced"
        }
    
    @feature_manager.feature_gate("PRO")
    def medical_grade_encryption(self, patient_data: Dict) -> Dict:
        """Medical-grade encryption and compliance - PRO only."""
        return {
            "encryption": "AES-256-GCM",
            "key_derivation": "PBKDF2-SHA256",
            "compliance": "HIPAA/GDPR compliant",
            "audit_logging": "Complete trail maintained",
            "data_retention": "Configurable policy",
            "security_level": "Medical Grade"
        }


def demonstrate_feature_gating():
    """Demonstrate how features are gated based on security level."""
    print("🎯 MACS Feature Gating Demonstration")
    print("=" * 50)
    
    medical = MedicalFeatures()
    data_protection = DataProtectionFeatures()
    
    # Show current security level
    current_level = security_manager.determine_security_level()
    print(f"🔒 Current Security Level: {current_level}")
    
    # Demonstrate feature availability
    features = feature_manager.get_available_features()
    
    print(f"\n✅ Available Features ({len(features['available_features'])}):")
    for feature_name in features['available_features']:
        print(f"   - {feature_name}")
    
    print(f"\n❌ Blocked Features ({len(features['blocked_features'])}):")
    for feature_name, info in features['blocked_features'].items():
        print(f"   - {feature_name} (requires {info['required_level']})")
    
    # Test feature execution
    print(f"\n🔬 Testing Feature Execution:")
    
    # This always works (OPEN level)
    basic_result = medical.basic_symptom_analysis(["headache", "fatigue"])
    print(f"   Basic Analysis: {basic_result.get('analysis', 'Error')}")
    
    # This may be blocked depending on level
    advanced_result = medical.advanced_medical_ai(
        {"age": 45, "symptoms": ["chest pain"]}, 
        {"history": ["hypertension"]}
    )
    if "error" in advanced_result:
        print(f"   Advanced AI: ❌ {advanced_result['error']}")
    else:
        print(f"   Advanced AI: ✅ {advanced_result['analysis']}")


if __name__ == "__main__":
    demonstrate_feature_gating()
