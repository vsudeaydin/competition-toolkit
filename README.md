# T4P – Competition Law Toolkit

A production-ready MVP web application for competition law analysis and compliance checking, designed to match Trade4People (T4P) look-and-feel.

## Quick Start

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Features

### 📊 Merger Threshold Calculator
- Calculate notification thresholds for mergers and acquisitions
- Support for multiple currencies (TRY, EUR, USD) with live exchange rates
- Automatic conversion and threshold comparison
- PDF export with detailed calculations

### 📈 HHI Calculator & Visualizer
- Herfindahl-Hirschman Index calculation for market concentration
- Interactive bar charts and pie charts
- Market share normalization options
- Risk level interpretation

### ✅ Compliance Checklist
- Self-assessment questionnaire for competition law compliance
- Risk scoring and guidance
- Exportable compliance reports

### ⚠️ Dominance Risk Checker
- Market dominance risk assessment
- Heuristic-based risk matrix
- Multiple factor analysis

## Project Structure

```
t4p_competition_toolkit/
├── app.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
├── data/                           # JSON storage for history
├── assets/                         # Static assets (logo, etc.)
├── utils/                          # Shared utilities
│   ├── constants.py               # App-wide constants and thresholds
│   ├── layout.py                  # UI layout and styling
│   ├── currency.py                # Currency conversion utilities
│   ├── pdf_export.py              # PDF generation
│   ├── charts.py                  # Chart generation
│   └── storage.py                 # Data persistence
├── pages/                         # Streamlit pages
│   ├── 01_Merger_Threshold_Calculator.py
│   ├── 02_HHI_Calculator_and_Visualizer.py
│   ├── 03_Compliance_Checklist.py
│   ├── 04_Dominance_Risk_Checker.py
│   └── 99_Help_and_About.py
└── .streamlit/
    └── config.toml               # Streamlit configuration
```

## Configuration

### Thresholds
Update competition authority thresholds in `utils/constants.py`:
- Merger notification thresholds
- HHI interpretation bands
- Currency conversion settings

### Branding
- Logo: Replace `assets/logo.svg`
- Colors: Modify `.streamlit/config.toml`
- Links: Update placeholder URLs in `utils/layout.py`

## Known Limitations

- **Prototype Status**: Educational use only; not legal advice
- **Thresholds**: Placeholder values; update with current Competition Authority thresholds
- **Currency API**: Depends on external service; manual override available
- **Data Storage**: Local JSON files only; no database
- **Browser Compatibility**: Modern browsers recommended for best experience

## Development

### Adding New Pages
1. Create new file in `pages/` directory
2. Follow naming convention: `XX_Page_Name.py`
3. Import shared utilities from `utils/`
4. Add to navigation in `app.py`

### Styling
- CSS customizations in `utils/layout.py`
- Theme configuration in `.streamlit/config.toml`
- Consistent header/footer via shared layout functions

## Deployment

### Streamlit Cloud
- Connect GitHub repository
- Set Python version to 3.11+
- No additional configuration required

### Heroku
- Use `heroku/python` buildpack
- Set `STREAMLIT_SERVER_PORT` environment variable
- Configure `Procfile` for web dyno

## Version History

- **v1.0.0**: Initial MVP release
  - Merger threshold calculator
  - HHI calculator and visualizer
  - Compliance checklist
  - Dominance risk checker
  - PDF export functionality
  - Currency conversion with live rates

## Support

For questions or issues:
1. Check the Help & About page within the application
2. Review this README for configuration options
3. Update thresholds and branding as needed for production use

---

**Disclaimer**: This tool is for educational purposes only. Always consult qualified legal counsel for competition law matters.
