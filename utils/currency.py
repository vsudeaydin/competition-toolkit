"""
T4P Competition Law Toolkit - Currency Conversion Utilities
Handles currency conversion with live rates and manual override options.
"""

import requests
import streamlit as st
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import time

from .constants import SUPPORTED_CURRENCIES, DEFAULT_BASE_CURRENCY, DEFAULT_TARGET_CURRENCY, APP_STRINGS


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_exchange_rate(base: str = "TRY", target: str = "EUR") -> Optional[float]:
    """
    Fetch live exchange rate from open.er-api.com
    
    Args:
        base: Base currency code
        target: Target currency code
        
    Returns:
        Exchange rate as float, or None if API fails
    """
    try:
        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get("result") == "success":
            rates = data.get("rates", {})
            if target in rates:
                return rates[target]
        
        return None
    except Exception as e:
        st.warning(f"Currency API error: {str(e)}")
        return None


def convert_currency(amount: float, base: str, target: str, override_rate: Optional[float] = None) -> Optional[float]:
    """
    Convert amount from base currency to target currency
    
    Args:
        amount: Amount to convert
        base: Base currency code
        target: Target currency code
        override_rate: Manual exchange rate override
        
    Returns:
        Converted amount, or None if conversion fails
    """
    if base == target:
        return amount
    
    if override_rate is not None:
        return amount * override_rate
    
    rate = get_exchange_rate(base, target)
    if rate is not None:
        return amount * rate
    
    return None


def convert(amount: float, base: str, target: str, override_rate: Optional[float] = None) -> Optional[float]:
    """
    Alias for convert_currency for backward compatibility
    
    Args:
        amount: Amount to convert
        base: Base currency code
        target: Target currency code
        override_rate: Manual exchange rate override
        
    Returns:
        Converted amount, or None if conversion fails
    """
    return convert_currency(amount, base, target, override_rate)


def get_rate(base: str, target: str) -> Optional[float]:
    """
    Get exchange rate between two currencies
    
    Args:
        base: Base currency code
        target: Target currency code
        
    Returns:
        Exchange rate as float, or None if API fails
    """
    return get_exchange_rate(base, target)


def format_currency(amount: float, currency: str) -> str:
    """
    Format currency amount with proper symbol and formatting
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    currency_symbols = {
        "TRY": "₺",
        "EUR": "€",
        "USD": "$"
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    if amount >= 1_000_000:
        return f"{symbol}{amount/1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"{symbol}{amount/1_000:.1f}K"
    else:
        return f"{symbol}{amount:,.2f}"


def render_currency_panel() -> Dict[str, Any]:
    """
    Render currency conversion panel in sidebar
    
    Returns:
        Dictionary with currency settings
    """
    st.sidebar.markdown("### 💱 Currency Settings")
    
    # Base currency selection
    base_currency = st.sidebar.selectbox(
        "Base Currency",
        SUPPORTED_CURRENCIES,
        index=SUPPORTED_CURRENCIES.index(DEFAULT_BASE_CURRENCY)
    )
    
    # Target currency selection
    target_currency = st.sidebar.selectbox(
        "Target Currency",
        SUPPORTED_CURRENCIES,
        index=SUPPORTED_CURRENCIES.index(DEFAULT_TARGET_CURRENCY)
    )
    
    # Exchange rate display
    if base_currency != target_currency:
        rate = get_exchange_rate(base_currency, target_currency)
        
        if rate is not None:
            st.sidebar.metric(
                f"Exchange Rate ({base_currency} → {target_currency})",
                f"1 {base_currency} = {rate:.4f} {target_currency}",
                help="Live rate from open.er-api.com"
            )
            
            # Last updated info
            st.sidebar.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        else:
            st.sidebar.warning(APP_STRINGS["currency_api_error"])
    
    # Manual override option
    use_manual_rate = st.sidebar.checkbox("Use Manual Exchange Rate")
    manual_rate = None
    
    if use_manual_rate and base_currency != target_currency:
        manual_rate = st.sidebar.number_input(
            f"Manual Rate ({base_currency} → {target_currency})",
            min_value=0.0001,
            max_value=1000.0,
            value=1.0,
            step=0.0001,
            format="%.4f"
        )
    
    return {
        "base_currency": base_currency,
        "target_currency": target_currency,
        "manual_rate": manual_rate if use_manual_rate else None,
        "live_rate": get_exchange_rate(base_currency, target_currency) if base_currency != target_currency else 1.0
    }


def convert_amounts_to_base(amounts: Dict[str, float], target_base: str = "TRY") -> Dict[str, float]:
    """
    Convert multiple amounts to a common base currency
    
    Args:
        amounts: Dictionary of {currency: amount} pairs
        target_base: Target base currency
        
    Returns:
        Dictionary of converted amounts
    """
    converted = {}
    
    for currency, amount in amounts.items():
        if currency == target_base:
            converted[currency] = amount
        else:
            converted_amount = convert_currency(amount, currency, target_base)
            if converted_amount is not None:
                converted[currency] = converted_amount
    
    return converted


def validate_currency_input(currency: str) -> bool:
    """
    Validate if currency code is supported
    
    Args:
        currency: Currency code to validate
        
    Returns:
        True if supported, False otherwise
    """
    return currency in SUPPORTED_CURRENCIES


def get_currency_info() -> Dict[str, Any]:
    """
    Get current currency conversion information
    
    Returns:
        Dictionary with currency conversion details
    """
    base = DEFAULT_BASE_CURRENCY
    target = DEFAULT_TARGET_CURRENCY
    
    rate = get_exchange_rate(base, target)
    
    return {
        "base_currency": base,
        "target_currency": target,
        "exchange_rate": rate,
        "last_updated": datetime.now().isoformat(),
        "supported_currencies": SUPPORTED_CURRENCIES
    }
