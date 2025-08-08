"""
T4P Competition Law Toolkit - Merger Threshold Calculator
Calculate notification thresholds for mergers and acquisitions.
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Page Title", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

from utils.layout import (
    set_page_config, use_theme, header, render_sidebar, 
    render_export_bar, render_success_message, render_warning_message,
    render_error_message, render_metric_card, render_calculation_summary, theme_icon_toggle
)
from utils.constants import MERGER_THRESHOLDS, SUPPORTED_CURRENCIES, APP_STRINGS
from utils.currency import convert_currency, format_currency, convert, get_rate
from utils.storage import save_calculation_result
from utils.pdf_export import generate_merger_report


def party_row(i, role_prefix):
    key_prefix = f"{role_prefix}_{i}"
    name = st.text_input(f"{role_prefix.title()} {i+1} Name", key=f"{key_prefix}_name")
    prev_cur = st.session_state.get(f"{key_prefix}_prev_currency", "TRY")
    cur = st.selectbox("Currency", ["TRY", "EUR", "USD"], key=f"{key_prefix}_currency")
    amount_key = f"{key_prefix}_amount"

    # amount input with dynamic label
    amt = st.number_input(f"Turnover ({cur})", min_value=0.0, step=1000.0, key=amount_key, format="%.2f")

    # if currency changed and there is a value, convert
    if prev_cur != cur and st.session_state.get(amount_key, 0):
        rate = get_rate(prev_cur, cur)  # wrap existing get_rate(base, target)
        new_val = convert(st.session_state[amount_key], prev_cur, cur, override_rate=rate)
        st.session_state[amount_key] = round(float(new_val or 0), 2)

    st.session_state[f"{key_prefix}_prev_currency"] = cur
    return {"name": name, "currency": cur, "amount": st.session_state[amount_key]}


def main():
    """Merger Threshold Calculator main function"""
    
    # Set page configuration
    st.set_page_config(page_title="T4P – Competition Law Toolkit", page_icon="⚖️", layout="wide")
    
    # Apply theme and add theme toggle
    theme_icon_toggle()
    
    # Render sidebar
    currency_settings = render_sidebar("merger_calculator")
    
    # Main content
    header(
        title="Merger Threshold Calculator",
        subtitle="Determine if your transaction requires notification to the Competition Authority"
    )
    
    # Input section
    st.markdown("### 📝 Transaction Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.number_input(
            "Transaction Year",
            min_value=2020,
            max_value=2030,
            value=datetime.now().year,
            help="Year of the transaction for reporting purposes"
        )
        
        if year < 2020:
            st.warning("Value must be ≥ 2020.", icon="⚠️")
        
        country = st.selectbox(
            "Country",
            ["Türkiye", "Other"],
            index=0,
            help="Country where the transaction is taking place"
        )
    
    with col2:
        show_advanced = st.checkbox(
            "Show Advanced Options",
            help="Display additional calculation details and assumptions"
        )
        
        if show_advanced:
            st.info("Advanced options will appear here in a future update (e.g., rate date selection, country presets).", icon="🛠️")
    
    # Parties input
    st.markdown("### 🏢 Parties and Turnovers")
    
    # Buyer parties
    st.markdown("**Buyer(s) - Acquiring Parties**")
    
    buyer_parties = []
    num_buyers = st.number_input("Number of Buyer Parties", min_value=1, max_value=10, value=1)
    
    for i in range(num_buyers):
        buyer_data = party_row(i, "buyer")
        if buyer_data["name"] and buyer_data["amount"] > 0:
            buyer_parties.append(buyer_data)
    
    # Target parties
    st.markdown("**Target(s) - Acquired Parties**")
    
    target_parties = []
    num_targets = st.number_input("Number of Target Parties", min_value=1, max_value=10, value=1)
    
    for i in range(num_targets):
        target_data = party_row(i, "target")
        if target_data["name"] and target_data["amount"] > 0:
            target_parties.append(target_data)
    
    # Calculate button
    if st.button("🚀 Calculate Thresholds", type="primary"):
        if not buyer_parties and not target_parties:
            render_error_message("Please enter at least one party with turnover data.")
        else:
            calculate_merger_thresholds(
                buyer_parties, target_parties, currency_settings, year, country, show_advanced
            )


def calculate_merger_thresholds(
    buyer_parties: List[Dict[str, Any]],
    target_parties: List[Dict[str, Any]],
    currency_settings: Dict[str, Any],
    year: int,
    country: str,
    show_advanced: bool
) -> None:
    """
    Calculate merger thresholds and determine notification requirements
    
    Args:
        buyer_parties: List of buyer party data
        target_parties: List of target party data
        currency_settings: Currency conversion settings
        year: Transaction year
        country: Transaction country
        show_advanced: Whether to show advanced details
    """
    
    try:
        # Convert all turnovers to TRY
        base_currency = "TRY"
        converted_buyers = []
        converted_targets = []
        
        # Convert buyer turnovers
        for party in buyer_parties:
            converted_amount = convert_currency(
                party["amount"],
                party["currency"],
                base_currency,
                currency_settings.get("manual_rate")
            )
            
            if converted_amount is not None:
                converted_buyers.append({
                    "name": party.get("name") or f"Buyer {len(converted_buyers) + 1}",
                    "original_turnover": party["amount"],
                    "original_currency": party["currency"],
                    "converted_turnover": converted_amount,
                    "converted_currency": base_currency
                })
        
        # Convert target turnovers
        for party in target_parties:
            converted_amount = convert_currency(
                party["amount"],
                party["currency"],
                base_currency,
                currency_settings.get("manual_rate")
            )
            
            if converted_amount is not None:
                converted_targets.append({
                    "name": party.get("name") or f"Target {len(converted_targets) + 1}",
                    "original_turnover": party["amount"],
                    "original_currency": party["currency"],
                    "converted_turnover": converted_amount,
                    "converted_currency": base_currency
                })
        
        # Calculate totals
        total_buyer_turnover = sum(party["converted_turnover"] for party in converted_buyers)
        total_target_turnover = sum(party["converted_turnover"] for party in converted_targets)
        total_combined_turnover = total_buyer_turnover + total_target_turnover
        
        # Get thresholds
        thresholds = MERGER_THRESHOLDS["turkish"]
        global_threshold = thresholds["global_threshold"]
        local_threshold = thresholds["local_threshold"]
        
        # Check notification requirements
        global_met = total_combined_turnover >= global_threshold
        local_met = total_buyer_turnover >= local_threshold or total_target_turnover >= local_threshold
        
        is_notifiable = global_met and local_met
        
        # Display results
        st.markdown("### 📊 Calculation Results")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_metric_card(
                "Total Buyer Turnover",
                format_currency(total_buyer_turnover, base_currency)
            )
        
        with col2:
            render_metric_card(
                "Total Target Turnover",
                format_currency(total_target_turnover, base_currency)
            )
        
        with col3:
            render_metric_card(
                "Combined Turnover",
                format_currency(total_combined_turnover, base_currency)
            )
        
        # Verdict
        if is_notifiable:
            render_success_message(
                f"**Likely Notifiable** - This transaction appears to meet the notification thresholds."
            )
        else:
            render_warning_message(
                f"**Likely Not Notifiable** - This transaction appears to be below the notification thresholds."
            )
        
        # Detailed analysis
        st.markdown("### 🔍 Detailed Analysis")
        
        analysis_data = {
            "Global Threshold Test": f"{'✅ PASS' if global_met else '❌ FAIL'} - Combined turnover {format_currency(total_combined_turnover, base_currency)} vs {format_currency(global_threshold, base_currency)} threshold",
            "Local Threshold Test": f"{'✅ PASS' if local_met else '❌ FAIL'} - Individual party turnovers vs {format_currency(local_threshold, base_currency)} threshold",
            "Exchange Rate Used": f"1 {currency_settings['base_currency']} = {currency_settings.get('live_rate', 1.0):.4f} {base_currency}" if currency_settings.get('live_rate') else "Manual rate used",
            "Calculation Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        render_calculation_summary(analysis_data)
        
        # Parties table
        if converted_buyers or converted_targets:
            st.markdown("### 📋 Parties and Turnovers")
            
            all_parties = []
            for party in converted_buyers:
                all_parties.append({
                    "Party": party["name"],
                    "Type": "Buyer",
                    "Original Amount": f"{format_currency(party['original_turnover'], party['original_currency'])}",
                    "Converted Amount": f"{format_currency(party['converted_turnover'], base_currency)}"
                })
            
            for party in converted_targets:
                all_parties.append({
                    "Party": party["name"],
                    "Type": "Target",
                    "Original Amount": f"{format_currency(party['original_turnover'], party['original_currency'])}",
                    "Converted Amount": f"{format_currency(party['converted_turnover'], base_currency)}"
                })
            
            df = pd.DataFrame(all_parties)
            st.dataframe(df, use_container_width=True)
        
        # Advanced details
        if show_advanced:
            st.markdown("### ⚙️ Advanced Details")
            
            st.markdown(f"""
            **Thresholds Applied:**
            - Global Threshold: {format_currency(global_threshold, base_currency)}
            - Local Threshold: {format_currency(local_threshold, base_currency)}
            - Source: {thresholds['description']}
            
            **Calculation Method:**
            - All turnovers converted to {base_currency} using live/manual rates
            - Global test: Combined turnover ≥ {format_currency(global_threshold, base_currency)}
            - Local test: At least one party turnover ≥ {format_currency(local_threshold, base_currency)}
            """)
        
        # Export functionality
        show_pdf_export = True
        export_data = {
            "summary": {
                "Transaction Year": year,
                "Country": country,
                "Is Notifiable": is_notifiable,
                "Global Threshold Met": global_met,
                "Local Threshold Met": local_met,
                "Total Combined Turnover": total_combined_turnover,
                "Global Threshold": global_threshold,
                "Local Threshold": local_threshold
            },
            "parties": [
                [party["name"], party["type"], party["original_amount"], party["converted_amount"]]
                for party in all_parties
            ],
            "thresholds": {
                "Global Threshold": format_currency(global_threshold, base_currency),
                "Local Threshold": format_currency(local_threshold, base_currency),
                "Source": thresholds["description"]
            },
            "conversion": {
                "Base Currency": base_currency,
                "Exchange Rate": currency_settings.get("live_rate", "Manual"),
                "Calculation Date": datetime.now().isoformat()
            },
            "verdict": f"{'NOTIFIABLE' if is_notifiable else 'NOT NOTIFIABLE'} - {'Meets' if is_notifiable else 'Below'} notification thresholds"
        }
        
        # Generate exports
        pdf_data = generate_merger_report(export_data)
        
        # Create CSV data
        csv_data = pd.DataFrame(all_parties).to_csv(index=False) if all_parties else None
        
        # Save to history
        save_calculation_result(
            "merger_calculator",
            {
                "buyer_parties": buyer_parties,
                "target_parties": target_parties,
                "year": year,
                "country": country
            },
            export_data["summary"]
        )
        
    except Exception as e:
        show_pdf_export = False
        st.error(f"An unexpected error occurred during calculation. Please check your inputs and try again.\n\nDetails: {type(e).__name__}", icon="❌")
    
    # Render export buttons only when calculation succeeds
    if show_pdf_export:
        render_export_bar(
            pdf_data=pdf_data,
            csv_data=csv_data,
            pdf_filename=f"merger_threshold_report_{year}.pdf",
            csv_filename=f"merger_parties_{year}.csv"
        )


if __name__ == "__main__":
    main()
