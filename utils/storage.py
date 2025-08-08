"""
T4P Competition Law Toolkit - Data Storage Utilities
Handles saving and loading calculation history to JSON files.
"""

import json
import os
from typing import List, Dict, Any, Optional
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

from .constants import APP_STRINGS


def ensure_data_directory() -> str:
    """
    Ensure the data directory exists
    
    Returns:
        Path to data directory
    """
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir


def save_history(module_name: str, payload: Dict[str, Any]) -> bool:
    """
    Save calculation history to JSON file
    
    Args:
        module_name: Name of the module (e.g., 'merger_calculator')
        payload: Data to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        data_dir = ensure_data_directory()
        filename = f"{module_name}_history.json"
        filepath = os.path.join(data_dir, filename)
        
        # Add timestamp
        payload["timestamp"] = datetime.now().isoformat()
        
        # Load existing data
        existing_data = load_history(module_name)
        existing_data.append(payload)
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error saving history: {str(e)}")
        return False


def load_history(module_name: str) -> List[Dict[str, Any]]:
    """
    Load calculation history from JSON file
    
    Args:
        module_name: Name of the module
        
    Returns:
        List of historical calculations
    """
    try:
        data_dir = ensure_data_directory()
        filename = f"{module_name}_history.json"
        filepath = os.path.join(data_dir, filename)
        
        if not os.path.exists(filepath):
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data if isinstance(data, list) else []
    except Exception as e:
        st.warning(f"Error loading history: {str(e)}")
        return []


def clear_history(module_name: str) -> bool:
    """
    Clear calculation history for a module
    
    Args:
        module_name: Name of the module
        
    Returns:
        True if successful, False otherwise
    """
    try:
        data_dir = ensure_data_directory()
        filename = f"{module_name}_history.json"
        filepath = os.path.join(data_dir, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return True
    except Exception as e:
        st.error(f"Error clearing history: {str(e)}")
        return False


def get_history_summary(module_name: str) -> Dict[str, Any]:
    """
    Get summary statistics for module history
    
    Args:
        module_name: Name of the module
        
    Returns:
        Dictionary with summary statistics
    """
    history = load_history(module_name)
    
    if not history:
        return {
            "total_calculations": 0,
            "last_calculation": None,
            "most_common_result": None
        }
    
    # Count calculations
    total = len(history)
    
    # Get last calculation
    last_calculation = max(history, key=lambda x: x.get("timestamp", ""))
    
    # Find most common result (if applicable)
    results = [item.get("result", "Unknown") for item in history if "result" in item]
    
    # Handle unhashable types (like dictionaries) by converting to strings
    hashable_results = []
    for result in results:
        if isinstance(result, dict):
            # For dictionaries, use a summary string
            if "Risk Level" in result:
                hashable_results.append(result["Risk Level"])
            elif "Is Notifiable" in result:
                hashable_results.append("Notifiable" if result["Is Notifiable"] else "Not Notifiable")
            else:
                hashable_results.append("Complex Result")
        elif isinstance(result, (list, tuple)):
            hashable_results.append("List Result")
        else:
            hashable_results.append(str(result))
    
    most_common = max(set(hashable_results), key=hashable_results.count) if hashable_results else None
    
    return {
        "total_calculations": total,
        "last_calculation": last_calculation.get("timestamp"),
        "most_common_result": most_common
    }


def export_history_csv(module_name: str) -> Optional[str]:
    """
    Export history as CSV string
    
    Args:
        module_name: Name of the module
        
    Returns:
        CSV string or None if error
    """
    try:
        import pandas as pd
        
        history = load_history(module_name)
        if not history:
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(history)
        
        # Convert to CSV string
        csv_string = df.to_csv(index=False)
        return csv_string
    except Exception as e:
        st.error(f"Error exporting CSV: {str(e)}")
        return None


def render_history_panel(module_name: str) -> None:
    """
    Render history panel in sidebar
    
    Args:
        module_name: Name of the module
    """
    st.sidebar.markdown("### 📊 Calculation History")
    
    summary = get_history_summary(module_name)
    
    if summary["total_calculations"] == 0:
        st.sidebar.info("No previous calculations found.")
        return
    
    # Display summary
    st.sidebar.metric("Total Calculations", summary["total_calculations"])
    
    if summary["last_calculation"]:
        last_date = datetime.fromisoformat(summary["last_calculation"]).strftime("%Y-%m-%d %H:%M")
        st.sidebar.caption(f"Last: {last_date}")
    
    if summary["most_common_result"]:
        st.sidebar.caption(f"Most common: {summary['most_common_result']}")
    
    # Export options
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("📥 Export CSV", key=f"export_{module_name}"):
            csv_data = export_history_csv(module_name)
            if csv_data:
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"{module_name}_history.csv",
                    mime="text/csv"
                )
    
    with col2:
        if st.button("🗑️ Clear", key=f"clear_{module_name}"):
            if clear_history(module_name):
                st.sidebar.success("History cleared!")
                st.rerun()


def save_calculation_result(module_name: str, inputs: Dict[str, Any], result: Dict[str, Any]) -> bool:
    """
    Save calculation result with inputs and outputs
    
    Args:
        module_name: Name of the module
        inputs: Input parameters
        result: Calculation results
        
    Returns:
        True if successful, False otherwise
    """
    payload = {
        "module": module_name,
        "inputs": inputs,
        "result": result,
        "timestamp": datetime.now().isoformat()
    }
    
    return save_history(module_name, payload)


def get_recent_calculations(module_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get recent calculations for a module
    
    Args:
        module_name: Name of the module
        limit: Maximum number of recent calculations to return
        
    Returns:
        List of recent calculations
    """
    history = load_history(module_name)
    
    # Sort by timestamp (newest first)
    sorted_history = sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return sorted_history[:limit]
