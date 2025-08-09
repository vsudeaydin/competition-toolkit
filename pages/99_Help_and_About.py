"""
T4P Competition Law Toolkit - Help and About
User guide, glossary, and application information.
"""

import streamlit as st
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Page Title", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

from utils.layout import (
    set_page_config, use_theme, header, render_sidebar, 
    render_info_card, render_footer, theme_icon_toggle
)
from utils.constants import APP_STRINGS, EXTERNAL_LINKS


def main():
    """Help and About main function"""
    
    # Set page configuration
    st.set_page_config(page_title="T4P – Competition Law Toolkit", page_icon="⚖️", layout="wide")
    
    # Apply theme and add theme toggle
    theme_icon_toggle()
    
    # Render sidebar
    currency_settings = render_sidebar()
    
    # Main content
    header(
        title="Help & About",
        subtitle="User guide and application information"
    )
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs([
        "📖 How to Use", "📚 Glossary", "🔗 Resources"
    ])
    
    with tab1:
        render_how_to_use()
    
    with tab2:
        render_glossary()
    
    with tab3:
        render_resources()


def render_how_to_use():
    """Render how to use guide"""
    
    st.markdown("## 📖 How to Use the T4P Competition Law Toolkit")
    
    st.markdown("""
    This toolkit provides professional tools for competition law analysis and compliance checking. 
    Follow these steps to get started:
    """)
    
    # Getting Started
    st.markdown("### 🚀 Getting Started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_info_card(
            title="1. Choose a Tool",
            content="Select the appropriate tool from the navigation menu based on your needs.",
            icon="🎯"
        )
        
        render_info_card(
            title="2. Enter Data",
            content="Fill in the required information using the input forms provided.",
            icon="📝"
        )
    
    with col2:
        render_info_card(
            title="3. Calculate Results",
            content="Click the calculate button to process your data and view results.",
            icon="🚀"
        )
        
        render_info_card(
            title="4. Export Reports",
            content="Download PDF reports or CSV data for record keeping.",
            icon="📤"
        )
    
    # Tool-specific guides
    st.markdown("### 🛠️ Tool-Specific Guides")
    
    st.markdown("""
    **📊 Merger Threshold Calculator**
    - Enter transaction details including buyer and target parties
    - Provide turnover data in your preferred currency
    - Review calculation results and notification requirements
    - Export detailed reports for legal review
    
    **📈 HHI Calculator & Visualizer**
    - Input market shares for all relevant firms
    - View HHI calculation and concentration analysis
    - Explore interactive charts and visualizations
    - Understand market concentration implications
    
    **✅ Compliance Checklist**
    - Answer comprehensive self-assessment questions
    - Receive risk scoring and recommendations
    - Identify areas requiring legal attention
    - Track compliance improvements over time
    
    **⚠️ Dominance Risk Checker**
    - Assess your firm's market position
    - Analyze competitive landscape factors
    - Receive risk assessment and recommendations
    - Monitor dominance risk factors
    """)
    
    # Tips and best practices
    st.markdown("### 💡 Tips and Best Practices")
    
    st.markdown("""
    - **Currency Settings**: Use the sidebar to set your preferred currencies for calculations
    - **Data Accuracy**: Ensure all input data is accurate and up-to-date
    - **Regular Updates**: Check for threshold updates and regulatory changes
    - **Legal Review**: Always consult qualified legal counsel for actual compliance matters
    - **Documentation**: Export and save reports for your records
    """)


def render_glossary():
    """Render glossary of terms"""
    
    st.markdown("## 📚 Glossary of Competition Law Terms")
    
    glossary = {
        "HHI (Herfindahl-Hirschman Index)": {
            "definition": "A measure of market concentration calculated by summing the squared market shares of all firms in a market.",
            "range": "0 (perfect competition) to 10,000 (monopoly)",
            "interpretation": "Higher values indicate greater market concentration"
        },
        "Market Share": {
            "definition": "The percentage of total market sales or revenue controlled by a specific firm.",
            "calculation": "Firm's sales ÷ Total market sales × 100",
            "significance": "Key indicator of market power and competitive position"
        },
        "Merger Notification": {
            "definition": "A requirement to notify competition authorities before completing certain mergers or acquisitions.",
            "thresholds": "Based on turnover or market share criteria",
            "purpose": "Prevents anti-competitive mergers"
        },
        "Market Dominance": {
            "definition": "A position of economic strength that enables a firm to behave independently of competitors.",
            "indicators": "High market share, barriers to entry, pricing power",
            "concerns": "Potential for anti-competitive behavior"
        },
        "Vertical Integration": {
            "definition": "When a firm operates at multiple levels of the supply chain.",
            "examples": "Manufacturer also owns distribution or retail",
            "concerns": "Potential foreclosure of competitors"
        },
        "Network Effects": {
            "definition": "When a product's value increases as more people use it.",
            "examples": "Social media platforms, payment systems",
            "concerns": "Can create barriers to entry and market dominance"
        },
        "Entry Barriers": {
            "definition": "Obstacles that make it difficult for new firms to enter a market.",
            "types": "Economic, regulatory, technological, strategic",
            "impact": "Can protect incumbent firms from competition"
        },
        "Price Fixing": {
            "definition": "An agreement between competitors to set prices at a specific level.",
            "status": "Illegal per se in most jurisdictions",
            "penalties": "Severe fines and criminal sanctions"
        },
        "Market Division": {
            "definition": "An agreement between competitors to divide markets, customers, or territories.",
            "status": "Illegal per se in most jurisdictions",
            "examples": "Geographic market allocation, customer allocation"
        },
        "Exclusive Dealing": {
            "definition": "When a supplier requires customers to purchase exclusively from it.",
            "analysis": "Rule of reason approach",
            "concerns": "Potential foreclosure of competitors"
        }
    }
    
    for term, details in glossary.items():
        with st.expander(term, expanded=False):
            st.markdown(f"**Definition:** {details['definition']}")
            if 'range' in details:
                st.markdown(f"**Range:** {details['range']}")
            if 'calculation' in details:
                st.markdown(f"**Calculation:** {details['calculation']}")
            if 'significance' in details:
                st.markdown(f"**Significance:** {details['significance']}")
            if 'examples' in details:
                st.markdown(f"**Examples:** {details['examples']}")
            if 'concerns' in details:
                st.markdown(f"**Competition Concerns:** {details['concerns']}")
            if 'status' in details:
                st.markdown(f"**Legal Status:** {details['status']}")
            if 'penalties' in details:
                st.markdown(f"**Penalties:** {details['penalties']}")
            if 'analysis' in details:
                st.markdown(f"**Legal Analysis:** {details['analysis']}")


def render_resources():
    """Render external resources"""
    
    st.markdown("## 🔗 External Resources")
    
    st.markdown("""
    ### 📋 Official Sources
    
    **Competition Authorities:**
    - [Turkish Competition Authority](https://www.rekabet.gov.tr/) - Official website with guidelines and decisions
    - [European Commission - Competition](https://ec.europa.eu/competition/) - EU competition policy and enforcement
    - [US Federal Trade Commission](https://www.ftc.gov/) - US antitrust enforcement
    
    **Legislation and Guidelines:**
    - [Turkish Competition Law](https://www.mevzuat.gov.tr/) - Official legislation database
    - [EU Competition Law](https://eur-lex.europa.eu/) - EU legal framework
    - [US Antitrust Laws](https://www.justice.gov/atr) - US antitrust enforcement
    
    ### 📚 Educational Resources
    
    **Academic and Research:**
    - [OECD Competition Policy](https://www.oecd.org/competition/) - International competition policy research
    - [World Bank Competition Policy](https://www.worldbank.org/en/topic/competition-policy) - Global competition policy
    - [ICN (International Competition Network)](https://www.internationalcompetitionnetwork.org/) - International cooperation
    
    **Professional Organizations:**
    - [American Bar Association - Antitrust](https://www.americanbar.org/groups/antitrust_law/) - Professional development
    - [European Competition Lawyers Association](https://www.ecla.org/) - European competition law community
    
    ### 📚 Publications and Reports

    **Annual Reports**
    - [Competition Authority Annual Reports](https://www.rekabet.gov.tr/)
    - [EU Competition Policy Reports](https://competition-policy.ec.europa.eu/)
    - [OECD Competition Policy Reviews](https://www.oecd.org/competition/)

    **Guidelines and Manuals**
    - [EU Merger Regulation & Guidance](https://competition-policy.ec.europa.eu/mergers_en)
    """)
    
    
    # Contact information
    st.markdown("""
    ### 📬 Contact & Support
    For questions, feedback, or collaboration inquiries, please contact **Vildan Sude Aydın** at **vsudeaydin01@gmail.com**.

    _This toolkit concept was initiated by **Vildan Sude AYDIN** as part of a competition-law focused legal technology project._
    """)
    
    st.markdown("""
    ### 🔗 Useful Links
    - [Turkish Competition Authority](https://www.rekabet.gov.tr/)
    - [EU Competition Policy](https://competition-policy.ec.europa.eu/)
    - [OECD Competition](https://www.oecd.org/competition/)
    - Contact: **vsudeaydin01@gmail.com**
    """)





if __name__ == "__main__":
    main()
