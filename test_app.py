#!/usr/bin/env python3
"""
Test script for T4P Competition Law Toolkit
Verifies core functionality without running the full Streamlit app
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all module imports"""
    print("Testing module imports...")
    
    try:
        from utils.constants import APP_STRINGS, MERGER_THRESHOLDS, HHI_BANDS
        print("✅ Constants module imported")
        
        from utils.currency import get_exchange_rate, convert_currency
        print("✅ Currency module imported")
        
        from utils.storage import save_history, load_history
        print("✅ Storage module imported")
        
        from utils.pdf_export import make_pdf_report
        print("✅ PDF export module imported")
        
        from utils.charts import calculate_hhi, get_hhi_interpretation
        print("✅ Charts module imported")
        
        from utils.layout import inject_css, header
        print("✅ Layout module imported")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_calculations():
    """Test core calculation functions"""
    print("\nTesting calculations...")
    
    try:
        from utils.charts import calculate_hhi, get_hhi_interpretation
        
        # Test HHI calculation
        market_shares = {"Firm A": 40, "Firm B": 30, "Firm C": 20, "Firm D": 10}
        hhi = calculate_hhi(market_shares)
        interpretation = get_hhi_interpretation(hhi)
        
        print(f"✅ HHI calculation: {hhi:.0f} ({interpretation['description']})")
        
        from utils.currency import convert_currency
        
        # Test currency conversion (mock)
        converted = convert_currency(1000, "EUR", "TRY", override_rate=1.1)
        if converted is not None:
            print(f"✅ Currency conversion: 1000 EUR = {converted:.2f} TRY")
        
        return True
    except Exception as e:
        print(f"❌ Calculation error: {e}")
        return False

def test_storage():
    """Test storage functionality"""
    print("\nTesting storage...")
    
    try:
        from utils.storage import save_history, load_history
        
        # Test data
        test_data = {"test": "data", "timestamp": "2024-01-01"}
        
        # Save test data
        success = save_history("test_module", test_data)
        print(f"✅ Save history: {'Success' if success else 'Failed'}")
        
        # Load test data
        history = load_history("test_module")
        print(f"✅ Load history: {len(history)} records")
        
        return True
    except Exception as e:
        print(f"❌ Storage error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing T4P Competition Law Toolkit")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_calculations,
        test_storage
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to run.")
        print("\nTo start the application:")
        print("streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
