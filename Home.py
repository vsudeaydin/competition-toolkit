"""
T4P Competition Law Toolkit - Main Application
Entry point for the Streamlit multi-page application.
"""

import streamlit as st
from datetime import datetime

from utils.layout import (
    set_page_config, use_theme, header, render_sidebar, 
    render_page_navigation, render_footer, render_info_card, theme_icon_toggle
)
from utils.constants import APP_STRINGS, PAGE_CONFIG


def main():
    """Main application entry point"""
    
    # Set page configuration
    st.set_page_config(page_title="T4P – Competition Law Toolkit", page_icon="⚖️", layout="wide")
    
    # Apply theme and add theme toggle
    theme_icon_toggle()
    
    # Render sidebar with custom title
    with st.sidebar:
        st.markdown("### ⚖️ Competition Law Toolkit")
    
    currency_settings = render_sidebar()
    
    # Main content
    header(
        title="T4P Competition Law Toolkit",
        subtitle="Professional competition law analysis and compliance tools"
    )
    
    # Welcome message
    st.markdown("""
    Welcome to the T4P Competition Law Toolkit! This application provides professional tools for 
    competition law analysis, compliance checking, and market concentration assessment.
    
    **Key Features:**
    - 📊 **Merger Threshold Calculator**: Determine if your transaction requires notification
    - 📈 **HHI Calculator & Visualizer**: Analyze market concentration with visual charts
    - ✅ **Compliance Checklist**: Self-assessment for competition law compliance
    - ⚠️ **Dominance Risk Checker**: Assess market dominance risk factors
    """)
    
    # Navigation cards
    render_page_navigation()
    
    # Quick start guide
    st.markdown("### 🚀 Quick Start Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_info_card(
            title="Getting Started",
            content="Choose a tool from the navigation above. Each tool includes detailed instructions and help text.",
            icon="🎯"
        )
        
        render_info_card(
            title="Currency Conversion",
            content="Use the sidebar to set your preferred currencies. Live exchange rates are automatically fetched.",
            icon="💱"
        )
    
    with col2:
        render_info_card(
            title="Export Options",
            content="All calculations can be exported as PDF reports or CSV data for record keeping.",
            icon="📤"
        )
        
        render_info_card(
            title="History Tracking",
            content="Your calculation history is automatically saved and can be accessed from the sidebar.",
            icon="📊"
        )
    
    # Recent activity (placeholder)
    st.markdown("### 📈 Recent Activity")
    
    # Placeholder for recent calculations
    st.info("No recent calculations yet. Start using the tools above to see your activity here!")
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()
