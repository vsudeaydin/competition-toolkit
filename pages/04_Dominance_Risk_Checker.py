"""
T4P Competition Law Toolkit - Dominance Risk Checker
Assess market dominance risk factors and provide risk analysis.
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
from utils.constants import DOMINANCE_RISK_FACTORS, APP_STRINGS
from utils.storage import save_calculation_result
from utils.pdf_export import generate_dominance_report


def main():
    """Dominance Risk Checker main function"""
    
    # Set page configuration
    set_page_config(
        title="Dominance Risk Checker",
        icon="⚠️"
    )
    
    # Apply theme
    use_theme("T4P Dark")
    
    # Render sidebar
    currency_settings = render_sidebar("dominance_checker")
    
    # Main content
    header(
        title="Dominance Risk Checker",
        subtitle="Assess market dominance risk factors and potential competition concerns"
    )
    
    # Disclaimer
    st.warning("⚠️ This tool provides heuristic risk assessment only. Consult qualified legal counsel for actual competition law analysis.")
    
    # Introduction
    st.markdown("""
    This tool helps assess potential market dominance risks based on various market factors. 
    Enter your market data to receive a risk assessment and recommendations.
    """)
    
    # Input section
    st.markdown("### 📝 Market Analysis Inputs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Your firm's market share
        your_market_share = st.number_input(
            "Your Firm's Market Share (%)",
            min_value=0.0,
            max_value=100.0,
            value=25.0,
            step=0.1,
            help="Your firm's market share in the relevant market"
        )
        
        # HHI (optional)
        hhi_value = st.number_input(
            "Market HHI (Optional)",
            min_value=0.0,
            max_value=10000.0,
            value=0.0,
            step=100.0,
            help="Herfindahl-Hirschman Index for the market (0-10,000)"
        )
        
        # Vertical integration
        vertical_integration = st.checkbox(
            "Vertical Integration",
            help="Does your firm operate at multiple levels of the supply chain?"
        )
    
    with col2:
        # Top 3 rivals
        rival_shares = []
        st.markdown("**Top 3 Rivals' Market Shares**")
        
        for i in range(3):
            rival_share = st.number_input(
                f"Rival {i+1} Market Share (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key=f"rival_{i}"
            )
            if rival_share > 0:
                rival_shares.append(rival_share)
        
        # Network effects
        network_effects = st.checkbox(
            "Network Effects",
            help="Does your product/service benefit from network effects?"
        )
        
        # Market entry barriers
        entry_barriers = st.selectbox(
            "Market Entry Barriers",
            options=["Low", "Medium", "High"],
            index=1,
            help="Level of barriers to entry in the market"
        )
    
    # Calculate button
    if st.button("🚀 Assess Dominance Risk", type="primary"):
        if your_market_share > 0:
            calculate_dominance_risk(
                your_market_share, rival_shares, hhi_value, 
                vertical_integration, network_effects, entry_barriers
            )
        else:
            render_error_message("Please enter your firm's market share to proceed.")


def calculate_dominance_risk(
    your_market_share: float,
    rival_shares: List[float],
    hhi_value: float,
    vertical_integration: bool,
    network_effects: bool,
    entry_barriers: str
) -> None:
    """
    Calculate dominance risk based on market factors
    
    Args:
        your_market_share: Your firm's market share
        rival_shares: List of rival market shares
        hhi_value: Market HHI value
        vertical_integration: Whether firm has vertical integration
        network_effects: Whether product has network effects
        entry_barriers: Level of entry barriers
    """
    
    try:
        # Calculate risk factors
        risk_factors = {}
        total_risk_score = 0
        
        # Market share risk
        if your_market_share >= 50:
            risk_factors["Market Share"] = "High"
            total_risk_score += 3
        elif your_market_share >= 30:
            risk_factors["Market Share"] = "Medium"
            total_risk_score += 2
        else:
            risk_factors["Market Share"] = "Low"
            total_risk_score += 1
        
        # HHI risk (if provided)
        if hhi_value > 0:
            if hhi_value >= 2500:
                risk_factors["Market Concentration (HHI)"] = "High"
                total_risk_score += 3
            elif hhi_value >= 1500:
                risk_factors["Market Concentration (HHI)"] = "Medium"
                total_risk_score += 2
            else:
                risk_factors["Market Concentration (HHI)"] = "Low"
                total_risk_score += 1
        
        # Rival concentration risk
        if rival_shares:
            top_3_share = sum(rival_shares[:3])
            if top_3_share >= 80:
                risk_factors["Rival Concentration"] = "High"
                total_risk_score += 2
            elif top_3_share >= 60:
                risk_factors["Rival Concentration"] = "Medium"
                total_risk_score += 1
            else:
                risk_factors["Rival Concentration"] = "Low"
                total_risk_score += 0
        
        # Vertical integration risk
        if vertical_integration:
            risk_factors["Vertical Integration"] = "Present"
            total_risk_score += 2
        else:
            risk_factors["Vertical Integration"] = "Absent"
            total_risk_score += 0
        
        # Network effects risk
        if network_effects:
            risk_factors["Network Effects"] = "Present"
            total_risk_score += 2
        else:
            risk_factors["Network Effects"] = "Absent"
            total_risk_score += 0
        
        # Entry barriers risk
        if entry_barriers == "High":
            risk_factors["Entry Barriers"] = "High"
            total_risk_score += 2
        elif entry_barriers == "Medium":
            risk_factors["Entry Barriers"] = "Medium"
            total_risk_score += 1
        else:
            risk_factors["Entry Barriers"] = "Low"
            total_risk_score += 0
        
        # Determine overall risk level
        if total_risk_score >= 8:
            risk_level = "High"
            risk_description = "Significant dominance concerns - immediate legal review recommended"
        elif total_risk_score >= 5:
            risk_level = "Medium"
            risk_description = "Moderate dominance concerns - consider legal consultation"
        else:
            risk_level = "Low"
            risk_description = "Low dominance concerns - continue monitoring"
        
        # Display results
        st.markdown("### 📊 Dominance Risk Assessment Results")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_metric_card(
                "Risk Score",
                f"{total_risk_score}",
                f"Max: 12"
            )
        
        with col2:
            render_metric_card(
                "Risk Level",
                risk_level.title(),
                risk_description
            )
        
        with col3:
            render_metric_card(
                "Your Market Share",
                f"{your_market_share:.1f}%",
                f"Rivals: {len(rival_shares)}"
            )
        
        # Risk level message
        if risk_level == "High":
            render_error_message(
                f"**High Risk** - Score of {total_risk_score} indicates significant dominance concerns. "
                "Immediate legal review strongly recommended."
            )
        elif risk_level == "Medium":
            render_warning_message(
                f"**Medium Risk** - Score of {total_risk_score} indicates moderate dominance concerns. "
                "Consider legal consultation and review practices."
            )
        else:
            render_success_message(
                f"**Low Risk** - Score of {total_risk_score} indicates low dominance concerns. "
                "Continue monitoring and stay informed of market developments."
            )
        
        # Detailed analysis
        st.markdown("### 🔍 Detailed Analysis")
        
        analysis_data = {
            "Risk Score": total_risk_score,
            "Risk Level": risk_level.title(),
            "Your Market Share": f"{your_market_share:.1f}%",
            "Market HHI": f"{hhi_value:.0f}" if hhi_value > 0 else "Not provided",
            "Assessment Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        render_calculation_summary(analysis_data)
        
        # Risk factors table
        st.markdown("### 📋 Risk Factor Analysis")
        
        factors_data = []
        for factor, risk in risk_factors.items():
            factors_data.append({
                "Risk Factor": factor,
                "Risk Level": risk,
                "Score": get_factor_score(factor, risk)
            })
        
        df = pd.DataFrame(factors_data)
        st.dataframe(df, use_container_width=True)
        
        # Market analysis
        st.markdown("### 📈 Market Analysis")
        
        market_data = {
            "Your Market Share": f"{your_market_share:.1f}%",
            "Top 3 Rivals Share": f"{sum(rival_shares[:3]):.1f}%" if rival_shares else "Not provided",
            "Market HHI": f"{hhi_value:.0f}" if hhi_value > 0 else "Not provided",
            "Vertical Integration": "Yes" if vertical_integration else "No",
            "Network Effects": "Yes" if network_effects else "No",
            "Entry Barriers": entry_barriers
        }
        
        for key, value in market_data.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**{key}:**")
            with col2:
                st.markdown(value)
        
        # Risk matrix
        st.markdown("### 🎯 Risk Matrix")
        
        risk_matrix = {
            "Market Share": {
                "Low (<30%)": "Low risk",
                "Medium (30-50%)": "Medium risk",
                "High (>50%)": "High risk"
            },
            "Market Concentration": {
                "Low (HHI <1500)": "Low risk",
                "Medium (HHI 1500-2500)": "Medium risk",
                "High (HHI >2500)": "High risk"
            },
            "Market Structure": {
                "Competitive": "Low risk",
                "Oligopolistic": "Medium risk",
                "Dominant firm": "High risk"
            }
        }
        
        for category, levels in risk_matrix.items():
            st.markdown(f"**{category}:**")
            for level, risk in levels.items():
                st.markdown(f"- {level}: {risk}")
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        
        recommendations = []
        
        if risk_level == "high":
            recommendations.extend([
                "Immediately consult with qualified competition law counsel",
                "Review all business practices for potential dominance issues",
                "Consider voluntary commitments to address concerns",
                "Implement comprehensive compliance monitoring",
                "Prepare for potential regulatory scrutiny"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "Schedule consultation with competition law expert",
                "Review high-risk areas identified in the assessment",
                "Monitor market developments closely",
                "Consider proactive compliance measures",
                "Stay informed of regulatory developments"
            ])
        else:
            recommendations.extend([
                "Continue monitoring market position",
                "Stay informed of competition law developments",
                "Conduct regular market analysis",
                "Maintain documentation of compliance efforts",
                "Consider periodic legal review"
            ])
        
        for i, recommendation in enumerate(recommendations, 1):
            st.markdown(f"{i}. {recommendation}")
        
        # Export functionality
        export_data = {
            "summary": {
                "Risk Score": total_risk_score,
                "Risk Level": risk_level,
                "Risk Description": risk_description,
                "Your Market Share": your_market_share,
                "Assessment Date": datetime.now().isoformat()
            },
            "market_analysis": market_data,
            "risk_factors": [
                [factor, risk, get_factor_score(factor, risk)]
                for factor, risk in risk_factors.items()
            ],
            "recommendations": recommendations
        }
        
        # Generate exports
        pdf_data = generate_dominance_report(export_data)
        
        # Create CSV data
        csv_data = pd.DataFrame(factors_data).to_csv(index=False) if factors_data else None
        
        # Render export buttons
        render_export_bar(
            pdf_data=pdf_data,
            csv_data=csv_data,
            pdf_filename="dominance_risk_assessment.pdf",
            csv_filename="risk_factors.csv"
        )
        
        # Save to history
        save_calculation_result(
            "dominance_checker",
            {
                "your_market_share": your_market_share,
                "rival_shares": rival_shares,
                "hhi_value": hhi_value,
                "vertical_integration": vertical_integration,
                "network_effects": network_effects,
                "entry_barriers": entry_barriers
            },
            export_data["summary"]
        )
        
    except Exception as e:
        render_error_message(f"Error during calculation: {str(e)}")


def get_factor_score(factor: str, risk: str) -> int:
    """
    Get score for a risk factor
    
    Args:
        factor: Risk factor name
        risk: Risk level
        
    Returns:
        Score for the factor
    """
    if risk in ["High", "Present"]:
        return 3
    elif risk in ["Medium"]:
        return 2
    elif risk in ["Low", "Absent"]:
        return 1
    else:
        return 0


if __name__ == "__main__":
    main()
