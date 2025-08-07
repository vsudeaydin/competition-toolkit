"""
T4P Competition Law Toolkit - PDF Export Utilities
Handles PDF generation using ReportLab for professional reports.
"""

import io
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from .constants import PDF_CONFIG, APP_STRINGS


def build_header(canvas, title: str, subtitle: Optional[str] = None) -> None:
    """
    Build PDF header with title and subtitle
    
    Args:
        canvas: ReportLab canvas
        title: Main title
        subtitle: Optional subtitle
    """
    canvas.saveState()
    
    # Title
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(PDF_CONFIG["margin"], PDF_CONFIG["page_height"] - PDF_CONFIG["margin"] - 20, title)
    
    # Subtitle
    if subtitle:
        canvas.setFont("Helvetica", 12)
        canvas.drawString(PDF_CONFIG["margin"], PDF_CONFIG["page_height"] - PDF_CONFIG["margin"] - 40, subtitle)
    
    # Date and time
    canvas.setFont("Helvetica", 10)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    canvas.drawString(PDF_CONFIG["margin"], PDF_CONFIG["page_height"] - PDF_CONFIG["margin"] - 60, f"Generated: {timestamp}")
    
    # Line separator
    canvas.line(PDF_CONFIG["margin"], PDF_CONFIG["page_height"] - PDF_CONFIG["margin"] - 70, 
                PDF_CONFIG["page_width"] - PDF_CONFIG["margin"], PDF_CONFIG["page_height"] - PDF_CONFIG["margin"] - 70)
    
    canvas.restoreState()


def paragraph(text: str, style: str = "Normal") -> Paragraph:
    """
    Create a styled paragraph
    
    Args:
        text: Text content
        style: Style name
        
    Returns:
        Styled paragraph
    """
    styles = getSampleStyleSheet()
    return Paragraph(text, styles[style])


def h_rule() -> Spacer:
    """
    Create a horizontal rule spacer
    
    Returns:
        Spacer element
    """
    return Spacer(1, 12)


def create_table(data: List[List[str]], header: Optional[List[str]] = None) -> Table:
    """
    Create a styled table
    
    Args:
        data: Table data as list of lists
        header: Optional header row
        
    Returns:
        Styled table
    """
    if header:
        table_data = [header] + data
    else:
        table_data = data
    
    table = Table(table_data)
    
    # Style the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    
    table.setStyle(style)
    return table


def make_pdf_report(buffer: io.BytesIO, title: str, sections: List[Tuple[str, Any]]) -> bool:
    """
    Generate a complete PDF report
    
    Args:
        buffer: BytesIO buffer to write PDF to
        title: Report title
        sections: List of (heading, content) tuples
        
    Returns:
        True if successful, False otherwise
    """
    try:
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=getSampleStyleSheet()['Title'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 20))
        
        # Disclaimer
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=getSampleStyleSheet()['Normal'],
            fontSize=8,
            textColor=colors.red,
            alignment=TA_CENTER
        )
        story.append(Paragraph(APP_STRINGS["disclaimer"], disclaimer_style))
        story.append(Spacer(1, 20))
        
        # Sections
        for heading, content in sections:
            # Section heading
            heading_style = ParagraphStyle(
                'SectionHeading',
                parent=getSampleStyleSheet()['Heading2'],
                fontSize=14,
                spaceAfter=12,
                spaceBefore=20
            )
            story.append(Paragraph(heading, heading_style))
            
            # Section content
            if isinstance(content, str):
                story.append(paragraph(content))
            elif isinstance(content, list):
                # Handle list of key-value pairs
                if content and isinstance(content[0], (list, tuple)) and len(content[0]) == 2:
                    # Convert to table format
                    table_data = [[str(k), str(v)] for k, v in content]
                    table = create_table(table_data, ["Parameter", "Value"])
                    story.append(table)
                else:
                    # Simple list
                    for item in content:
                        story.append(paragraph(f"• {item}"))
            elif isinstance(content, dict):
                # Convert dict to key-value list
                kv_list = [[k, str(v)] for k, v in content.items()]
                table = create_table(kv_list, ["Parameter", "Value"])
                story.append(table)
            
            story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story, onFirstPage=lambda canvas, doc: build_header(canvas, title))
        return True
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return False


def generate_merger_report(calculation_data: Dict[str, Any]) -> Optional[bytes]:
    """
    Generate merger threshold calculation report
    
    Args:
        calculation_data: Calculation results and inputs
        
    Returns:
        PDF bytes or None if error
    """
    buffer = io.BytesIO()
    
    title = "Merger Threshold Calculation Report"
    
    sections = [
        ("Calculation Summary", calculation_data.get("summary", {})),
        ("Parties and Turnovers", calculation_data.get("parties", [])),
        ("Threshold Analysis", calculation_data.get("thresholds", {})),
        ("Currency Conversion", calculation_data.get("conversion", {})),
        ("Verdict", calculation_data.get("verdict", ""))
    ]
    
    if make_pdf_report(buffer, title, sections):
        buffer.seek(0)
        return buffer.getvalue()
    
    return None


def generate_hhi_report(calculation_data: Dict[str, Any]) -> Optional[bytes]:
    """
    Generate HHI calculation report
    
    Args:
        calculation_data: Calculation results and inputs
        
    Returns:
        PDF bytes or None if error
    """
    buffer = io.BytesIO()
    
    title = "HHI Calculation Report"
    
    sections = [
        ("Market Concentration Analysis", calculation_data.get("summary", {})),
        ("Market Shares", calculation_data.get("shares", [])),
        ("HHI Calculation", calculation_data.get("calculation", {})),
        ("Interpretation", calculation_data.get("interpretation", ""))
    ]
    
    if make_pdf_report(buffer, title, sections):
        buffer.seek(0)
        return buffer.getvalue()
    
    return None


def generate_compliance_report(calculation_data: Dict[str, Any]) -> Optional[bytes]:
    """
    Generate compliance checklist report
    
    Args:
        calculation_data: Calculation results and inputs
        
    Returns:
        PDF bytes or None if error
    """
    buffer = io.BytesIO()
    
    title = "Compliance Assessment Report"
    
    sections = [
        ("Risk Assessment Summary", calculation_data.get("summary", {})),
        ("Question Responses", calculation_data.get("responses", [])),
        ("Recommendations", calculation_data.get("recommendations", []))
    ]
    
    if make_pdf_report(buffer, title, sections):
        buffer.seek(0)
        return buffer.getvalue()
    
    return None


def generate_dominance_report(calculation_data: Dict[str, Any]) -> Optional[bytes]:
    """
    Generate dominance risk assessment report
    
    Args:
        calculation_data: Calculation results and inputs
        
    Returns:
        PDF bytes or None if error
    """
    buffer = io.BytesIO()
    
    title = "Dominance Risk Assessment Report"
    
    sections = [
        ("Risk Assessment Summary", calculation_data.get("summary", {})),
        ("Market Analysis", calculation_data.get("market_analysis", {})),
        ("Risk Factors", calculation_data.get("risk_factors", [])),
        ("Recommendations", calculation_data.get("recommendations", []))
    ]
    
    if make_pdf_report(buffer, title, sections):
        buffer.seek(0)
        return buffer.getvalue()
    
    return None


def render_export_buttons(pdf_data: Optional[bytes], csv_data: Optional[str], 
                         pdf_filename: str, csv_filename: str) -> None:
    """
    Render export buttons for PDF and CSV
    
    Args:
        pdf_data: PDF bytes data
        csv_data: CSV string data
        pdf_filename: PDF filename
        csv_filename: CSV filename
    """
    col1, col2 = st.columns(2)
    
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
