"""
T4P Competition Law Toolkit - Compliance Checklist
Self-assessment questionnaire for competition law compliance.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime

from utils.layout import (
    set_page_config, use_theme, header, render_sidebar, 
    render_export_bar, render_success_message, render_warning_message,
    render_error_message, render_metric_card, render_calculation_summary, theme_icon_toggle
)
from utils.constants import COMPLIANCE_QUESTIONS, COMPLIANCE_SCORING, APP_STRINGS
from utils.storage import save_calculation_result
from utils.pdf_export import generate_compliance_report


def main():
    """Compliance Checklist main function"""
    
    # Set page configuration
    st.set_page_config(page_title="T4P – Competition Law Toolkit", page_icon="⚖️", layout="wide")
    
    # Apply theme and add theme toggle
    theme_icon_toggle()
    
    # Render sidebar
    currency_settings = render_sidebar("compliance_checklist")
    
    # Main content
    header(
        title="Compliance Checklist",
        subtitle="Self-assessment for competition law compliance"
    )
    
    # Disclaimer
    st.warning("⚠️ This checklist is for educational purposes only. Always consult qualified legal counsel for actual compliance matters.")
    
    # Introduction
    st.markdown("""
    This compliance checklist helps you assess potential competition law risks in your business practices. 
    Answer each question honestly based on your current business activities.
    
    **Scoring:**
    - **Yes** = 3 points (High risk)
    - **Sometimes** = 2 points (Medium risk)  
    - **No** = 0 points (Low risk)
    """)
    
    # Questions input
    st.markdown("### 📋 Compliance Assessment Questions")
    
    responses = {}
    
    # Group questions by category
    categories = {}
    for question in COMPLIANCE_QUESTIONS:
        category = question["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(question)
    
    # Display questions by category
    for category, questions in categories.items():
        st.markdown(f"#### {category}")
        
        for question in questions:
            response = st.selectbox(
                question["question"],
                options=["No", "Sometimes", "Yes"],
                index=0,
                key=question["id"],
                help=f"Weight: {question['weight']} points"
            )
            
            responses[question["id"]] = {
                "question": question["question"],
                "category": question["category"],
                "response": response,
                "weight": question["weight"]
            }
    
    # Calculate button
    if st.button("🚀 Calculate Risk Score", type="primary"):
        if len(responses) == len(COMPLIANCE_QUESTIONS):
            calculate_compliance_score(responses)
        else:
            render_error_message("Please answer all questions before calculating the risk score.")


def calculate_compliance_score(responses: Dict[str, Dict[str, Any]]) -> None:
    """
    Calculate compliance risk score and provide recommendations
    
    Args:
        responses: Dictionary of question responses
    """
    
    try:
        # Calculate scores
        total_score = 0
        category_scores = {}
        
        for question_id, response_data in responses.items():
            response = response_data["response"]
            weight = response_data["weight"]
            category = response_data["category"]
            
            # Calculate points
            if response == "Yes":
                points = weight
            elif response == "Sometimes":
                points = weight * 0.5
            else:  # No
                points = 0
            
            total_score += points
            
            # Track category scores
            if category not in category_scores:
                category_scores[category] = 0
            category_scores[category] += points
        
        # Determine risk level
        risk_level = "low"
        risk_description = ""
        
        for level, criteria in COMPLIANCE_SCORING.items():
            if level == "low" and total_score <= criteria["max_score"]:
                risk_level = level
                risk_description = criteria["description"]
                break
            elif level == "medium" and total_score <= criteria["max_score"]:
                risk_level = level
                risk_description = criteria["description"]
                break
            elif level == "high":
                risk_level = level
                risk_description = criteria["description"]
                break
        
        # Display results
        st.markdown("### 📊 Compliance Assessment Results")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_metric_card(
                "Risk Score",
                f"{total_score:.1f}",
                f"Max: {sum(q['weight'] for q in COMPLIANCE_QUESTIONS)}"
            )
        
        with col2:
            render_metric_card(
                "Risk Level",
                risk_level.title(),
                risk_description
            )
        
        with col3:
            render_metric_card(
                "Questions Answered",
                f"{len(responses)}",
                f"Total: {len(COMPLIANCE_QUESTIONS)}"
            )
        
        # Risk level message
        if risk_level == "high":
            render_error_message(
                f"**High Risk** - Score of {total_score:.1f} indicates significant compliance concerns. "
                "Immediate legal review recommended."
            )
        elif risk_level == "medium":
            render_warning_message(
                f"**Medium Risk** - Score of {total_score:.1f} indicates some compliance concerns. "
                "Review practices and consider legal consultation."
            )
        else:
            render_success_message(
                f"**Low Risk** - Score of {total_score:.1f} indicates generally compliant practices. "
                "Continue monitoring and stay informed of competition law developments."
            )
        
        # Detailed analysis
        st.markdown("### 🔍 Detailed Analysis")
        
        analysis_data = {
            "Total Risk Score": f"{total_score:.1f}",
            "Risk Level": risk_level.title(),
            "Risk Description": risk_description,
            "Questions Answered": len(responses),
            "Assessment Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        render_calculation_summary(analysis_data)
        
        # Category breakdown
        st.markdown("### 📈 Risk by Category")
        
        category_data = []
        for category, score in category_scores.items():
            category_data.append({
                "Category": category,
                "Risk Score": f"{score:.1f}",
                "Risk Level": "High" if score > 5 else "Medium" if score > 2 else "Low"
            })
        
        df = pd.DataFrame(category_data)
        st.dataframe(df, use_container_width=True)
        
        # Responses summary
        st.markdown("### 📋 Question Responses")
        
        responses_data = []
        for question_id, response_data in responses.items():
            responses_data.append({
                "Category": response_data["category"],
                "Question": response_data["question"],
                "Response": response_data["response"],
                "Weight": response_data["weight"]
            })
        
        df_responses = pd.DataFrame(responses_data)
        st.dataframe(df_responses, use_container_width=True)
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        
        recommendations = []
        
        if risk_level == "high":
            recommendations.extend([
                "Immediately consult with qualified competition law counsel",
                "Review all business practices for potential competition law violations",
                "Implement comprehensive compliance training for all staff",
                "Consider voluntary disclosure of potential issues",
                "Establish ongoing monitoring and reporting procedures"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "Schedule consultation with competition law expert",
                "Review high-risk areas identified in the assessment",
                "Implement targeted compliance training",
                "Establish regular compliance monitoring",
                "Stay informed of competition law developments"
            ])
        else:
            recommendations.extend([
                "Continue current compliance practices",
                "Stay informed of competition law developments",
                "Conduct regular self-assessments",
                "Maintain documentation of compliance efforts",
                "Consider periodic legal review"
            ])
        
        for i, recommendation in enumerate(recommendations, 1):
            st.markdown(f"{i}. {recommendation}")
        
        # Export functionality
        export_data = {
            "summary": {
                "Total Risk Score": total_score,
                "Risk Level": risk_level,
                "Risk Description": risk_description,
                "Assessment Date": datetime.now().isoformat(),
                "Questions Answered": len(responses)
            },
            "responses": [
                [response_data["category"], response_data["question"], response_data["response"], response_data["weight"]]
                for response_data in responses.values()
            ],
            "recommendations": recommendations
        }
        
        # Generate exports
        pdf_data = generate_compliance_report(export_data)
        
        # Create CSV data
        csv_data = pd.DataFrame(responses_data).to_csv(index=False) if responses_data else None
        
        # Render export buttons
        render_export_bar(
            pdf_data=pdf_data,
            csv_data=csv_data,
            pdf_filename="compliance_assessment_report.pdf",
            csv_filename="compliance_responses.csv"
        )
        
        # Save to history
        save_calculation_result(
            "compliance_checklist",
            {
                "responses": responses,
                "assessment_date": datetime.now().isoformat()
            },
            export_data["summary"]
        )
        
    except Exception as e:
        render_error_message(f"Error during calculation: {str(e)}")


if __name__ == "__main__":
    main()
