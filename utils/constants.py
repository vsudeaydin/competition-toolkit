"""
T4P Competition Law Toolkit - Constants and Configuration
Centralized configuration for thresholds, currencies, and app-wide settings.
"""

from typing import List, Dict, Any

# =============================================================================
# MERGER THRESHOLD CONFIGURATION
# =============================================================================
# UPDATE thresholds here before production with current Competition Authority values

MERGER_THRESHOLDS = {
    "turkish": {
        "global_threshold": 500_000_000,  # TRY - Global turnover threshold
        "local_threshold": 50_000_000,    # TRY - Local turnover threshold
        "description": "Turkish Competition Authority thresholds"
    }
}

# =============================================================================
# CURRENCY CONFIGURATION
# =============================================================================

SUPPORTED_CURRENCIES: List[str] = ["TRY", "EUR", "USD"]
DEFAULT_BASE_CURRENCY: str = "TRY"
DEFAULT_TARGET_CURRENCY: str = "EUR"

# =============================================================================
# HHI INTERPRETATION BANDS
# =============================================================================
# Heuristic interpretation - not legal advice

HHI_BANDS = {
    "low": {"max": 1500, "description": "Low concentration", "color": "green"},
    "moderate": {"min": 1500, "max": 2500, "description": "Moderate concentration", "color": "orange"},
    "high": {"min": 2500, "description": "High concentration", "color": "red"}
}

HHI_DISCLAIMER = "⚠️ HHI interpretation is heuristic and for educational purposes only. Consult legal counsel for actual competition law analysis."

# =============================================================================
# DOMINANCE RISK ASSESSMENT
# =============================================================================

DOMINANCE_RISK_FACTORS = {
    "market_share": {
        "low": {"max": 30, "score": 1},
        "medium": {"min": 30, "max": 50, "score": 2},
        "high": {"min": 50, "score": 3}
    },
    "hhi": {
        "low": {"max": 1500, "score": 1},
        "medium": {"min": 1500, "max": 2500, "score": 2},
        "high": {"min": 2500, "score": 3}
    },
    "vertical_integration": {"score": 2},
    "network_effects": {"score": 2}
}

# =============================================================================
# COMPLIANCE CHECKLIST QUESTIONS
# =============================================================================

COMPLIANCE_QUESTIONS = [
    {
        "id": "pricing_practices",
        "question": "Do you engage in price fixing or coordinate prices with competitors?",
        "category": "Pricing",
        "weight": 3
    },
    {
        "id": "market_sharing",
        "question": "Do you agree with competitors to divide markets or customers?",
        "category": "Market Division",
        "weight": 3
    },
    {
        "id": "bid_rigging",
        "question": "Do you coordinate bidding with competitors in tenders?",
        "category": "Bid Rigging",
        "weight": 3
    },
    {
        "id": "information_exchange",
        "question": "Do you exchange competitively sensitive information with competitors?",
        "category": "Information Exchange",
        "weight": 2
    },
    {
        "id": "exclusive_dealing",
        "question": "Do you require customers to purchase exclusively from you?",
        "category": "Exclusive Dealing",
        "weight": 2
    },
    {
        "id": "tying_bundling",
        "question": "Do you tie the sale of one product to another?",
        "category": "Tying & Bundling",
        "weight": 2
    },
    {
        "id": "predatory_pricing",
        "question": "Do you set prices below cost to eliminate competitors?",
        "category": "Predatory Pricing",
        "weight": 2
    },
    {
        "id": "refusal_to_deal",
        "question": "Do you refuse to deal with certain customers without objective justification?",
        "category": "Refusal to Deal",
        "weight": 1
    },
    {
        "id": "discriminatory_pricing",
        "question": "Do you charge different prices to similar customers without justification?",
        "category": "Price Discrimination",
        "weight": 1
    },
    {
        "id": "resale_price_maintenance",
        "question": "Do you control the resale prices of your products?",
        "category": "Resale Price Maintenance",
        "weight": 2
    }
]

COMPLIANCE_SCORING = {
    "low": {"max_score": 5, "description": "Low risk - Continue monitoring"},
    "medium": {"min_score": 5, "max_score": 15, "description": "Medium risk - Review practices"},
    "high": {"min_score": 15, "description": "High risk - Seek legal counsel"}
}

# =============================================================================
# APP-WIDE STRINGS
# =============================================================================

APP_STRINGS = {
    "app_title": "T4P – Competition Law Toolkit",
    "app_description": "Professional competition law analysis and compliance tools",
    "disclaimer": "⚠️ This tool is for educational purposes only. Always consult qualified legal counsel for competition law matters.",
    "currency_api_error": "Unable to fetch exchange rates. Please use manual override or try again later.",
    "export_success": "Export completed successfully!",
    "input_validation_error": "Please check your inputs and try again.",
    "calculation_error": "An error occurred during calculation. Please verify your inputs.",
    "no_data_available": "No data available for this calculation.",
    "loading_message": "Processing...",
    "success_message": "Calculation completed successfully!",
    "warning_message": "Please review the results carefully.",
    "error_message": "An error occurred. Please try again."
}

# =============================================================================
# NAVIGATION AND PAGES
# =============================================================================

PAGE_CONFIG = {
    "merger_calculator": {
        "title": "Merger Threshold Calculator",
        "description": "Calculate notification thresholds for mergers and acquisitions",
        "icon": "📊"
    },
    "hhi_calculator": {
        "title": "HHI Calculator & Visualizer",
        "description": "Calculate and visualize market concentration using HHI",
        "icon": "📈"
    },
    "compliance_checklist": {
        "title": "Compliance Checklist",
        "description": "Self-assessment for competition law compliance",
        "icon": "✅"
    },
    "dominance_checker": {
        "title": "Dominance Risk Checker",
        "description": "Assess market dominance risk factors",
        "icon": "⚠️"
    },
    "help_about": {
        "title": "Help & About",
        "description": "User guide and application information",
        "icon": "❓"
    }
}

# =============================================================================
# EXTERNAL LINKS (PLACEHOLDERS)
# =============================================================================

EXTERNAL_LINKS = {
    "competition_authority": "https://www.rekabet.gov.tr/",  # UPDATE with actual URL
    "legislation": "https://www.mevzuat.gov.tr/",  # UPDATE with actual URL
    "guidelines": "https://www.rekabet.gov.tr/kilavuzlar",  # UPDATE with actual URL
    "contact": "mailto:info@t4p.com"  # UPDATE with actual contact
}

# =============================================================================
# PDF EXPORT CONFIGURATION
# =============================================================================

PDF_CONFIG = {
    "page_width": 595,
    "page_height": 842,
    "margin": 50,
    "font_size": 10,
    "title_font_size": 16,
    "header_font_size": 12,
    "line_height": 14
}
