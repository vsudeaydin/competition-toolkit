"""
T4P Competition Law Toolkit - Layout and UI Utilities
Handles shared UI components, CSS styling, and consistent page layout.
"""

import streamlit as st
from typing import Optional, Dict, Any
from datetime import datetime

from .constants import APP_STRINGS, EXTERNAL_LINKS, PAGE_CONFIG
from .currency import render_currency_panel
from .storage import render_history_panel
from .theme import PALETTES, CURRENT_THEME_KEY


def set_page_config(title: str, icon: Optional[str] = None) -> None:
    """
    Set page configuration with consistent styling
    
    Args:
        title: Page title
        icon: Page icon (optional)
    """
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )


def use_theme(palette_name: str = "T4P Dark") -> None:
    """
    Apply theme with CSS variables based on selected palette
    
    Args:
        palette_name: Name of the palette to use
    """
    pal = PALETTES.get(st.session_state.get(CURRENT_THEME_KEY, palette_name), PALETTES["T4P Dark"])
    st.session_state[CURRENT_THEME_KEY] = pal.name
    
    css = f"""
    <style>
      :root {{
        --bg: {pal.bg};
        --bg-soft: {pal.bg_soft};
        --surface: {pal.surface};
        --surface-alt: {pal.surface_alt};
        --text: {pal.text};
        --text-muted: {pal.text_muted};
        --primary: {pal.primary};
        --primary-hover: {pal.primary_hover};
        --ring: {pal.ring};
        --success: {pal.success};
        --warning: {pal.warning};
        --danger: {pal.danger};
        --border: {pal.border};
        --shadow: {pal.shadow};
        --radius: 16px;
        --gap: 14px;
        --card-pad: 18px;
        --maxw: 1240px;
      }}
      
      .main, .stApp {{
        background: var(--bg);
        color: var(--text);
      }}
      
      /* Page width */
      section.block-container {{ 
        max-width: var(--maxw); 
        padding-top: 1.2rem; 
        padding-bottom: 2rem;
      }}
      
      /* Cards */
      .t4p-card {{
        background: linear-gradient(180deg, var(--surface), var(--surface-alt));
        border: 1px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        padding: var(--card-pad);
        margin-bottom: calc(var(--gap) * 1.2);
      }}
      
      /* Buttons */
      .stButton > button {{
        background: var(--primary);
        color: #fff;
        border-radius: 12px;
        border: 1px solid transparent;
        font-weight: 500;
        transition: all 0.2s ease;
      }}
      
      .stButton > button:hover {{ 
        background: var(--primary-hover); 
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
      }}
      
      /* Inputs */
      .stTextInput > div > div > input,
      .stNumberInput input, 
      .stSelectbox div[data-baseweb="select"] {{
        background: var(--surface);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 12px;
      }}
      
      /* Banners */
      .t4p-banner {{
        border-radius: 14px;
        padding: 14px 16px;
        border: 1px solid var(--border);
        margin-bottom: var(--gap);
      }}
      
      .t4p-success {{ 
        background: rgba(34,197,94,0.12); 
        border-color: var(--success);
        color: var(--success);
      }}
      
      .t4p-warning {{ 
        background: rgba(245,158,11,0.12); 
        border-color: var(--warning);
        color: var(--warning);
      }}
      
      .t4p-danger {{ 
        background: rgba(239,68,68,0.12); 
        border-color: var(--danger);
        color: var(--danger);
      }}
      
      /* Links & focus ring */
      a, .stMarkdown a {{ color: var(--ring); }}
      *:focus {{ outline: 2px solid var(--ring); outline-offset: 2px; }}
      
      /* Tables */
      .stDataFrame, .stTable {{ 
        background: var(--surface); 
        border-radius: 12px; 
        border: 1px solid var(--border);
      }}
      
      /* Metric cards */
      .metric-container {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
        border-radius: var(--radius);
        padding: 1rem;
        color: white;
        margin: 1rem 0;
        box-shadow: var(--shadow);
      }}
      
      /* Header styling */
      .header-container {{
        background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);
        border-radius: var(--radius);
        padding: 2rem;
        margin-bottom: 2rem;
        color: var(--text);
        text-align: center;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
      }}
      
      /* Sidebar styling */
      .css-1d391kg {{
        background-color: var(--bg-soft);
      }}
      
      /* Responsive design */
      @media (max-width: 768px) {{
        section.block-container {{
          padding: 1rem;
        }}
        
        .header-container {{
          padding: 1rem;
        }}
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def sidebar_theme_switcher() -> None:
    """Render theme switcher in sidebar"""
    with st.sidebar:
        st.markdown("### 🎨 Theme")
        choice = st.selectbox(
            "Select Theme", 
            list(PALETTES.keys()), 
            index=list(PALETTES).index(st.session_state.get(CURRENT_THEME_KEY, "T4P Dark"))
        )
        st.session_state[CURRENT_THEME_KEY] = choice
    use_theme(choice)


def inject_css() -> None:
    """
    Inject custom CSS for consistent styling (legacy function)
    """
    # This function is now deprecated in favor of use_theme()
    # Keeping for backward compatibility
    use_theme("T4P Dark")


def header(title: str, subtitle: Optional[str] = None) -> None:
    """
    Render consistent page header
    
    Args:
        title: Page title
        subtitle: Optional subtitle
    """
    st.markdown(f"""
    <div class="header-container">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 600;">{title}</h1>
        {f'<p style="font-size: 1.2rem; opacity: 0.8; margin: 0.5rem 0 0 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(module_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Render consistent sidebar with currency panel and links
    
    Args:
        module_name: Optional module name for history panel
        
    Returns:
        Dictionary with sidebar settings
    """
    st.sidebar.markdown("## T4P Competition Law Toolkit")
    
    # Theme switcher
    sidebar_theme_switcher()
    
    # Currency panel
    currency_settings = render_currency_panel()
    
    # External links
    st.sidebar.markdown("### 🔗 Useful Links")
    
    with st.sidebar.expander("External Resources", expanded=False):
        st.markdown(f"""
        - [Competition Authority]({EXTERNAL_LINKS["competition_authority"]})
        - [Legislation]({EXTERNAL_LINKS["legislation"]})
        - [Guidelines]({EXTERNAL_LINKS["guidelines"]})
        - [Contact]({EXTERNAL_LINKS["contact"]})
        """)
    
    # History panel for specific modules
    if module_name:
        render_history_panel(module_name)
    
    # Disclaimer
    st.sidebar.markdown("---")
    st.sidebar.caption(APP_STRINGS["disclaimer"])
    
    return currency_settings


def render_export_bar(pdf_data: Optional[bytes] = None, csv_data: Optional[str] = None,
                     pdf_filename: str = "report.pdf", csv_filename: str = "data.csv") -> None:
    """
    Render export buttons bar
    
    Args:
        pdf_data: PDF bytes data
        csv_data: CSV string data
        pdf_filename: PDF filename
        csv_filename: CSV filename
    """
    if pdf_data or csv_data:
        st.markdown("### 📤 Export Options")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if pdf_data:
                st.download_button(
                    label="📄 Export PDF",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
            else:
                st.button("📄 Export PDF", disabled=True)
        
        with col2:
            if csv_data:
                st.download_button(
                    label="📊 Export CSV",
                    data=csv_data,
                    file_name=csv_filename,
                    mime="text/csv"
                )
            else:
                st.button("📊 Export CSV", disabled=True)
        
        with col3:
            st.caption("Export your calculation results for record keeping")


def render_success_message(message: str) -> None:
    """
    Render success message with consistent styling
    
    Args:
        message: Success message
    """
    st.markdown(f"""
    <div class="t4p-banner t4p-success">
        ✅ {message}
    </div>
    """, unsafe_allow_html=True)


def render_warning_message(message: str) -> None:
    """
    Render warning message with consistent styling
    
    Args:
        message: Warning message
    """
    st.markdown(f"""
    <div class="t4p-banner t4p-warning">
        ⚠️ {message}
    </div>
    """, unsafe_allow_html=True)


def render_error_message(message: str) -> None:
    """
    Render error message with consistent styling
    
    Args:
        message: Error message
    """
    st.markdown(f"""
    <div class="t4p-banner t4p-danger">
        ❌ {message}
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(title: str, value: str, delta: Optional[str] = None) -> None:
    """
    Render metric card with consistent styling
    
    Args:
        title: Metric title
        value: Metric value
        delta: Optional delta value
    """
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="margin: 0; font-size: 0.9rem; opacity: 0.8;">{title}</h3>
        <h2 style="margin: 0.5rem 0; font-size: 2rem;">{value}</h2>
        {f'<p style="margin: 0; font-size: 0.8rem; opacity: 0.8;">{delta}</p>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)


def render_info_card(title: str, content: str, icon: str = "ℹ️") -> None:
    """
    Render info card with consistent styling
    
    Args:
        title: Card title
        content: Card content
        icon: Card icon
    """
    st.markdown(f"""
    <div class="t4p-card">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem; font-weight: 600;">{icon} {title}</h3>
        <p style="margin: 0; line-height: 1.5; color: var(--text-muted);">{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_help_tooltip(text: str, help_text: str) -> None:
    """
    Render help tooltip with consistent styling
    
    Args:
        text: Main text
        help_text: Help text for tooltip
    """
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.5rem;">
        <span>{text}</span>
        <span title="{help_text}" style="cursor: help; color: #666;">ⓘ</span>
    </div>
    """, unsafe_allow_html=True)


def render_page_navigation() -> None:
    """
    Render page navigation cards
    """
    st.markdown("## 📋 Available Tools")
    
    # Create navigation cards
    cols = st.columns(2)
    
    for i, (key, config) in enumerate(PAGE_CONFIG.items()):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div class="t4p-card" style="cursor: pointer; transition: transform 0.2s ease;" onclick="window.location.href='{key}'">
                    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem; font-weight: 600;">{config['icon']} {config['title']}</h3>
                    <p style="margin: 0; line-height: 1.5; color: var(--text-muted);">{config['description']}</p>
                </div>
                """, unsafe_allow_html=True)


def render_footer() -> None:
    """
    Render consistent footer
    """
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>T4P Competition Law Toolkit v1.0.0</p>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)


def render_loading_spinner(message: str = "Processing...") -> None:
    """
    Render loading spinner with message
    
    Args:
        message: Loading message
    """
    with st.spinner(message):
        st.markdown(f"<div style='text-align: center;'>{message}</div>", unsafe_allow_html=True)


def render_input_validation_error(field: str, message: str) -> None:
    """
    Render input validation error
    
    Args:
        field: Field name
        message: Error message
    """
    st.error(f"**{field}**: {message}")


def render_calculation_summary(summary_data: Dict[str, Any]) -> None:
    """
    Render calculation summary with consistent styling
    
    Args:
        summary_data: Summary data dictionary
    """
    st.markdown("### 📊 Calculation Summary")
    
    for key, value in summary_data.items():
        if isinstance(value, (int, float)):
            formatted_value = f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
        else:
            formatted_value = str(value)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"**{key.replace('_', ' ').title()}:**")
        with col2:
            st.markdown(formatted_value)
    
    st.markdown("---")
