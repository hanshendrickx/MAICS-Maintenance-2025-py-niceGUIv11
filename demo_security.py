#!/usr/bin/env python3
"""
MACS Security Demonstration
===========================
This script demonstrates the multi-layer security system.
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from security_manager import SecurityManager
except ImportError:
    print("❌ Security manager not available")
    print("💡 Install dependencies: pip install cryptography")
    sys.exit(1)


def demo_security_levels():
    """Demonstrate different security levels."""
    print("🔒 MACS Security System Demonstration")
    print("=" * 50)
    
    security = SecurityManager()
    
    # Test Hatch connectivity
    print("\n1. Testing Hatch Service Connectivity...")
    hatch_available = security.check_hatch_status()
    print(f"   Hatch Status: {'✅ Available' if hatch_available else '❌ Unavailable'}")
    
    # Test license system
    print("\n2. Testing License System...")
    license_status = security.load_license()
    print(f"   License Status: {'✅ Valid' if license_status['valid'] else '❌ Invalid'}")
    if not license_status['valid']:
        print(f"   Reason: {license_status.get('error', 'Unknown')}")
    
    # Determine security level
    print("\n3. Determining Security Level...")
    level = security.determine_security_level()
    print(f"   Current Level: {level}")
    
    if level == "OPEN":
        print("   🌐 Open source mode - full functionality")
    elif level == "PROTECTED":
        print("   ⚠️  Protected mode - limited functionality")
    elif level == "PRO":
        print("   🏥 Professional mode - full medical features")
    
    # Apply security measures
    print("\n4. Applying Security Measures...")
    security.apply_security_measures()
    
    return security


def demo_license_generation():
    """Demonstrate license generation for medical professionals."""
    print("\n" + "=" * 50)
    print("🏥 Medical Professional License Demo")
    print("=" * 50)
    
    security = SecurityManager()
    
    # Generate sample license
    test_email = "dr.demo@hospital.com"
    print(f"\n📧 Generating license for: {test_email}")
    
    license_key = security.generate_license_key(test_email, "PRO")
    print(f"🔑 Generated License Key: {license_key[:50]}...")
    
    # Validate the license
    print("\n🔍 Validating license...")
    validation = security.validate_license(license_key, test_email)
    
    if validation["valid"]:
        print("✅ License validation successful!")
        print(f"   Email: {validation['email']}")
        print(f"   Type: {validation['type']}")
        print(f"   Issued: {validation['issued']}")
        print(f"   Expires: {validation['expires']}")
    else:
        print(f"❌ License validation failed: {validation['error']}")


def demo_security_features():
    """Demonstrate security features by level."""
    print("\n" + "=" * 50)
    print("🛡️ Security Features by Level")
    print("=" * 50)
    
    features = {
        "OPEN": [
            "✅ Basic medical analysis",
            "✅ Open source transparency", 
            "✅ Community support",
            "✅ Educational use",
            "❌ Advanced encryption",
            "❌ HIPAA compliance logging",
            "❌ Professional support"
        ],
        "PROTECTED": [
            "✅ Limited medical analysis",
            "✅ Code obfuscation",
            "✅ Anti-reverse engineering",
            "✅ Runtime protection",
            "❌ Full functionality",
            "❌ Advanced features",
            "❌ Medical compliance"
        ],
        "PRO": [
            "✅ Complete medical suite",
            "✅ AES-256 encryption",
            "✅ HIPAA compliance",
            "✅ Audit trail logging",
            "✅ Professional support",
            "✅ Hospital integration",
            "✅ Advanced analytics"
        ]
    }
    
    for level, feature_list in features.items():
        print(f"\n🔒 {level} Mode Features:")
        for feature in feature_list:
            print(f"   {feature}")


def main():
    """Main demonstration function."""
    print("🏥 MACS - Medical Analysis Security System")
    print("Professional Medical Software with Ethical Security")
    print("=" * 60)
    
    # Demo 1: Security Level Detection
    security = demo_security_levels()
    
    # Demo 2: License Generation  
    demo_license_generation()
    
    # Demo 3: Security Features
    demo_security_features()
    
    # Interactive options
    print("\n" + "=" * 60)
    print("🎯 Interactive Options:")
    print("1. Request PRO trial license")
    print("2. Check security status")
    print("3. Run MACS with current security level")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            security.request_pro_license()
            break
        elif choice == "2":
            status = security.security_status()
            print(f"\n📊 Security Status:")
            print(f"   Level: {status['level']}")
            print(f"   Hatch Available: {status['hatch_available']}")
            print(f"   License Valid: {status['license_valid']}")
            print(f"   Timestamp: {status['timestamp']}")
        elif choice == "3":
            print("\n🚀 Starting MACS with current security level...")
            print("💡 Run: python main.py")
            break
        elif choice == "4":
            print("\n👋 Thanks for trying MACS Security Demo!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
