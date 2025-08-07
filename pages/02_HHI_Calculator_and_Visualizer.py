"""
T4P Competition Law Toolkit - HHI Calculator and Visualizer
Calculate and visualize market concentration using Herfindahl-Hirschman Index.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime

from utils.layout import (
    set_page_config, use_theme, header, render_sidebar, 
    render_export_bar, render_success_message, render_warning_message,
    render_error_message, render_metric_card, render_calculation_summary
)
from utils.constants import HHI_BANDS, HHI_DISCLAIMER, APP_STRINGS
from utils.charts import (
    calculate_hhi, get_hhi_interpretation, validate_market_shares,
    normalize_market_shares, create_hhi_bar_chart, create_hhi_pie_chart,
    create_hhi_concentration_chart, create_csv_from_shares
)
from utils.storage import save_calculation_result
from utils.pdf_export import generate_hhi_report


def main():
    """HHI Calculator and Visualizer main function"""
    
    # Set page configuration
    set_page_config(
        title="HHI Calculator & Visualizer",
        icon="📈"
    )
    
    # Apply theme
    use_theme("T4P Dark")
    
    # Render sidebar
    currency_settings = render_sidebar("hhi_calculator")
    
    # Main content
    header(
        title="HHI Calculator & Visualizer",
        subtitle="Calculate and visualize market concentration using Herfindahl-Hirschman Index"
    )
    
    # Disclaimer
    st.warning(HHI_DISCLAIMER)
    
    # Input section
    st.markdown("### 📝 Market Share Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_firms = st.number_input(
            "Number of Firms",
            min_value=2,
            max_value=20,
            value=5,
            help="Number of firms in the market"
        )
        
        show_charts = st.checkbox(
            "Show Charts",
            value=True,
            help="Display bar chart and pie chart visualizations"
        )
    
    with col2:
        normalize_shares = st.checkbox(
            "Auto-normalize Shares",
            value=False,
            help="Automatically normalize market shares to sum to 100%"
        )
        
        show_concentration_chart = st.checkbox(
            "Show Concentration Chart",
            value=True,
            help="Display HHI concentration level visualization"
        )
    
    # Market shares input
    st.markdown("### 🏢 Market Shares")
    
    market_shares = {}
    
    for i in range(num_firms):
        col1, col2 = st.columns(2)
        
        with col1:
            firm_name = st.text_input(
                f"Firm {i+1} Name",
                value=f"Firm {i+1}",
                key=f"firm_name_{i}"
            )
        
        with col2:
            market_share = st.number_input(
                f"Market Share (%)",
                min_value=0.0,
                max_value=100.0,
                value=20.0 if i < 5 else 0.0,
                step=0.1,
                key=f"market_share_{i}"
            )
        
        if firm_name and market_share > 0:
            market_shares[firm_name] = market_share
    
    # Calculate button
    if st.button("🚀 Calculate HHI", type="primary"):
        if len(market_shares) < 2:
            render_error_message("Please enter at least 2 firms with market share data.")
        else:
            calculate_hhi_and_visualize(
                market_shares, normalize_shares, show_charts, show_concentration_chart
            )


def calculate_hhi_and_visualize(
    market_shares: Dict[str, float],
    normalize_shares: bool,
    show_charts: bool,
    show_concentration_chart: bool
) -> None:
    """
    Calculate HHI and create visualizations
    
    Args:
        market_shares: Dictionary of {firm_name: market_share}
        normalize_shares: Whether to normalize shares
        show_charts: Whether to show charts
        show_concentration_chart: Whether to show concentration chart
    """
    
    try:
        # Validate market shares
        is_valid, error_message = validate_market_shares(market_shares)
        
        if not is_valid:
            render_error_message(error_message)
            return
        
        # Normalize shares if requested
        original_shares = market_shares.copy()
        if normalize_shares:
            market_shares = normalize_market_shares(market_shares)
            st.info(f"Market shares normalized to sum to 100% (original sum: {sum(original_shares.values()):.1f}%)")
        
        # Calculate HHI
        hhi_value = calculate_hhi(market_shares)
        interpretation = get_hhi_interpretation(hhi_value)
        
        # Display results
        st.markdown("### 📊 HHI Calculation Results")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_metric_card(
                "HHI Value",
                f"{hhi_value:.0f}",
                f"Range: 0-10,000"
            )
        
        with col2:
            render_metric_card(
                "Concentration Level",
                interpretation["description"].title(),
                f"Band: {interpretation['band'].title()}"
            )
        
        with col3:
            total_share = sum(market_shares.values())
            render_metric_card(
                "Total Market Share",
                f"{total_share:.1f}%",
                f"Firms: {len(market_shares)}"
            )
        
        # Interpretation
        if interpretation["band"] == "high":
            render_warning_message(
                f"**High Concentration** - HHI of {hhi_value:.0f} indicates high market concentration. "
                "Consider potential competition concerns."
            )
        elif interpretation["band"] == "moderate":
            render_warning_message(
                f"**Moderate Concentration** - HHI of {hhi_value:.0f} indicates moderate market concentration. "
                "Monitor for potential competition issues."
            )
        else:
            render_success_message(
                f"**Low Concentration** - HHI of {hhi_value:.0f} indicates low market concentration. "
                "Generally no immediate competition concerns."
            )
        
        # Detailed analysis
        st.markdown("### 🔍 Detailed Analysis")
        
        analysis_data = {
            "HHI Value": f"{hhi_value:.0f}",
            "Concentration Level": interpretation["description"],
            "Interpretation Band": interpretation["band"].title(),
            "Number of Firms": len(market_shares),
            "Total Market Share": f"{sum(market_shares.values()):.1f}%",
            "Calculation Method": "Sum of squared market shares × 10,000"
        }
        
        render_calculation_summary(analysis_data)
        
        # Market shares table
        st.markdown("### 📋 Market Shares")
        
        shares_data = []
        for firm, share in market_shares.items():
            shares_data.append({
                "Firm": firm,
                "Market Share (%)": f"{share:.1f}%",
                "Squared Share": f"{(share/100)**2:.4f}",
                "Contribution to HHI": f"{((share/100)**2 * 10000):.0f}"
            })
        
        df = pd.DataFrame(shares_data)
        st.dataframe(df, use_container_width=True)
        
        # Charts
        if show_charts:
            st.markdown("### 📊 Visualizations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Bar chart
                bar_chart = create_hhi_bar_chart(market_shares, "Market Shares by Firm")
                if bar_chart:
                    st.image(bar_chart, use_container_width=True)
            
            with col2:
                # Pie chart
                pie_chart = create_hhi_pie_chart(market_shares, "Market Share Distribution")
                if pie_chart:
                    st.image(pie_chart, use_container_width=True)
        
        # Concentration chart
        if show_concentration_chart:
            st.markdown("### 🎯 HHI Concentration Level")
            
            concentration_chart = create_hhi_concentration_chart(hhi_value, "HHI Concentration Analysis")
            if concentration_chart:
                st.image(concentration_chart, use_container_width=True)
        
        # Methodology
        st.markdown("### 📚 Methodology")
        
        st.markdown("""
        **HHI Calculation:**
        - HHI = Σ (Market Share)² × 10,000
        - Each firm's market share is squared and summed
        - Result is multiplied by 10,000 for readability
        
        **Interpretation Bands:**
        - **Low Concentration**: HHI < 1,500
        - **Moderate Concentration**: HHI 1,500 - 2,500
        - **High Concentration**: HHI > 2,500
        
        **Notes:**
        - HHI ranges from 0 (perfect competition) to 10,000 (monopoly)
        - Higher HHI indicates greater market concentration
        - Used by competition authorities worldwide
        """)
        
        # Export functionality
        export_data = {
            "summary": {
                "HHI Value": hhi_value,
                "Concentration Level": interpretation["description"],
                "Interpretation Band": interpretation["band"],
                "Number of Firms": len(market_shares),
                "Total Market Share": sum(market_shares.values()),
                "Calculation Date": datetime.now().isoformat()
            },
            "shares": [
                [firm, share, (share/100)**2, ((share/100)**2 * 10000)]
                for firm, share in market_shares.items()
            ],
            "calculation": {
                "Formula": "HHI = Σ (Market Share)² × 10,000",
                "Result": hhi_value,
                "Interpretation": interpretation["description"]
            },
            "interpretation": f"HHI of {hhi_value:.0f} indicates {interpretation['description']} market concentration"
        }
        
        # Generate exports
        pdf_data = generate_hhi_report(export_data)
        
        # Create CSV data
        csv_data = create_csv_from_shares(market_shares)
        
        # Render export buttons
        render_export_bar(
            pdf_data=pdf_data,
            csv_data=csv_data,
            pdf_filename="hhi_calculation_report.pdf",
            csv_filename="market_shares.csv"
        )
        
        # Save to history
        save_calculation_result(
            "hhi_calculator",
            {
                "market_shares": market_shares,
                "normalize_shares": normalize_shares,
                "num_firms": len(market_shares)
            },
            export_data["summary"]
        )
        
    except Exception as e:
        render_error_message(f"Error during calculation: {str(e)}")


if __name__ == "__main__":
    main()
