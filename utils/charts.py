"""
T4P Competition Law Toolkit - Chart Generation Utilities
Handles matplotlib chart generation for data visualization.
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import io
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

from .constants import HHI_BANDS


def create_hhi_bar_chart(market_shares: Dict[str, float], title: str = "Market Shares") -> Optional[bytes]:
    """
    Create a bar chart for market shares
    
    Args:
        market_shares: Dictionary of {firm_name: market_share}
        title: Chart title
        
    Returns:
        Chart image as bytes or None if error
    """
    try:
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Prepare data
        firms = list(market_shares.keys())
        shares = list(market_shares.values())
        
        # Create bar chart
        bars = ax.bar(firms, shares, color='skyblue', edgecolor='navy', alpha=0.7)
        
        # Customize chart
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Firms', fontsize=12)
        ax.set_ylabel('Market Share (%)', fontsize=12)
        ax.set_ylim(0, max(shares) * 1.1)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, share in zip(bars, shares):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{share:.1f}%', ha='center', va='bottom', fontsize=10)
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Tight layout
        plt.tight_layout()
        
        # Convert to bytes
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error creating bar chart: {str(e)}")
        return None


def create_hhi_pie_chart(market_shares: Dict[str, float], title: str = "Market Share Distribution") -> Optional[bytes]:
    """
    Create a pie chart for market shares
    
    Args:
        market_shares: Dictionary of {firm_name: market_share}
        title: Chart title
        
    Returns:
        Chart image as bytes or None if error
    """
    try:
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Prepare data
        firms = list(market_shares.keys())
        shares = list(market_shares.values())
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(shares, labels=firms, autopct='%1.1f%%',
                                          startangle=90, colors=plt.cm.Set3.colors)
        
        # Customize chart
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        
        # Convert to bytes
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error creating pie chart: {str(e)}")
        return None


def create_hhi_concentration_chart(hhi_value: float, title: str = "HHI Concentration Level") -> Optional[bytes]:
    """
    Create a visualization showing HHI value in context of concentration bands
    
    Args:
        hhi_value: Calculated HHI value
        title: Chart title
        
    Returns:
        Chart image as bytes or None if error
    """
    try:
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Define concentration bands
        bands = [
            (0, 1500, 'Low', 'green'),
            (1500, 2500, 'Moderate', 'orange'),
            (2500, 5000, 'High', 'red')
        ]
        
        # Create horizontal bar chart for bands
        y_pos = 0
        for start, end, label, color in bands:
            ax.barh(y_pos, end - start, left=start, height=0.5, 
                   color=color, alpha=0.7, label=label)
        
        # Mark HHI value
        ax.axvline(x=hhi_value, color='black', linestyle='--', linewidth=2, 
                   label=f'HHI = {hhi_value:.0f}')
        
        # Customize chart
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('HHI Value', fontsize=12)
        ax.set_xlim(0, 5000)
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([])
        
        # Add legend
        ax.legend(loc='upper right')
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Tight layout
        plt.tight_layout()
        
        # Convert to bytes
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error creating HHI concentration chart: {str(e)}")
        return None


def render_chart_selection(chart_type: str, chart_data: bytes, title: str) -> None:
    """
    Render chart with selection options
    
    Args:
        chart_type: Type of chart ('bar', 'pie', 'concentration')
        chart_data: Chart image bytes
        title: Chart title
    """
    if chart_data:
        st.markdown(f"### {title}")
        st.image(chart_data, use_container_width=True)
    else:
        st.warning("Unable to generate chart. Please check your data.")


def create_csv_from_shares(market_shares: Dict[str, float]) -> str:
    """
    Create CSV string from market shares data
    
    Args:
        market_shares: Dictionary of {firm_name: market_share}
        
    Returns:
        CSV string
    """
    try:
        df = pd.DataFrame([
            {"Firm": firm, "Market Share (%)": share}
            for firm, share in market_shares.items()
        ])
        return df.to_csv(index=False)
    except Exception as e:
        st.error(f"Error creating CSV: {str(e)}")
        return ""


def get_hhi_interpretation(hhi_value: float) -> Dict[str, Any]:
    """
    Get HHI interpretation based on value
    
    Args:
        hhi_value: Calculated HHI value
        
    Returns:
        Dictionary with interpretation details
    """
    if hhi_value < HHI_BANDS["low"]["max"]:
        band = "low"
        description = "Low concentration"
        color = "green"
    elif hhi_value < HHI_BANDS["moderate"]["max"]:
        band = "moderate"
        description = "Moderate concentration"
        color = "orange"
    else:
        band = "high"
        description = "High concentration"
        color = "red"
    
    return {
        "band": band,
        "description": description,
        "color": color,
        "hhi_value": hhi_value
    }


def calculate_hhi(market_shares: Dict[str, float]) -> float:
    """
    Calculate HHI from market shares
    
    Args:
        market_shares: Dictionary of {firm_name: market_share}
        
    Returns:
        HHI value
    """
    try:
        # Convert percentages to decimals and square them
        squared_shares = [((share / 100) ** 2) for share in market_shares.values()]
        
        # Sum and multiply by 10000 to get HHI
        hhi = sum(squared_shares) * 10000
        
        return hhi
    except Exception as e:
        st.error(f"Error calculating HHI: {str(e)}")
        return 0.0


def validate_market_shares(market_shares: Dict[str, float]) -> Tuple[bool, str]:
    """
    Validate market shares data
    
    Args:
        market_shares: Dictionary of {firm_name: market_share}
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not market_shares:
        return False, "No market shares provided"
    
    total_share = sum(market_shares.values())
    
    if total_share > 100:
        return False, f"Total market share exceeds 100% ({total_share:.1f}%)"
    
    if total_share < 0:
        return False, "Total market share cannot be negative"
    
    for firm, share in market_shares.items():
        if share < 0:
            return False, f"Market share for {firm} cannot be negative"
        if share > 100:
            return False, f"Market share for {firm} cannot exceed 100%"
    
    return True, ""


def normalize_market_shares(market_shares: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize market shares to sum to 100%
    
    Args:
        market_shares: Dictionary of {firm_name: market_share}
        
    Returns:
        Normalized market shares
    """
    total_share = sum(market_shares.values())
    
    if total_share == 0:
        return market_shares
    
    normalized = {}
    for firm, share in market_shares.items():
        normalized[firm] = (share / total_share) * 100
    
    return normalized
