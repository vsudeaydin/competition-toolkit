# T4P Competition Law Toolkit - Deployment Guide

## 🚀 Quick Start

### Local Development

1. **Clone or download the project**
   ```bash
   cd competition-law
   ```

2. **Run the quick start script**
   ```bash
   ./quick_start.sh
   ```

3. **Or manually set up:**
   ```bash
   # Create virtual environment
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Test the application
   python3 test_app.py
   
   # Start the application
   streamlit run app.py
   ```

### Production Deployment

#### Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set Python version to 3.11
   - Deploy

#### Heroku

1. **Create Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy to Heroku**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

#### Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run**
   ```bash
   docker build -t t4p-competition-toolkit .
   docker run -p 8501:8501 t4p-competition-toolkit
   ```

## 📋 Requirements

### System Requirements
- Python 3.11 or higher
- 2GB RAM minimum
- 500MB disk space

### Python Dependencies
- streamlit>=1.38
- requests>=2.32
- pandas>=2.2
- matplotlib>=3.9
- reportlab>=4.2
- python-dateutil>=2.9

## 🔧 Configuration

### Environment Variables
- `STREAMLIT_SERVER_PORT`: Port for the application (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

### Customization

#### Update Thresholds
Edit `utils/constants.py`:
```python
MERGER_THRESHOLDS = {
    "turkish": {
        "global_threshold": 500_000_000,  # UPDATE with current values
        "local_threshold": 50_000_000,    # UPDATE with current values
    }
}
```

#### Update Branding
1. **Logo**: Replace `assets/logo.svg`
2. **Colors**: Edit `.streamlit/config.toml`
3. **Links**: Update `utils/constants.py` EXTERNAL_LINKS

#### Update Currency Settings
Edit `utils/constants.py`:
```python
SUPPORTED_CURRENCIES = ["TRY", "EUR", "USD"]  # Add/remove currencies
DEFAULT_BASE_CURRENCY = "TRY"
```

## 🧪 Testing

### Run Tests
```bash
python3 test_app.py
```

### Manual Testing Checklist
- [ ] All pages load without errors
- [ ] Currency conversion works
- [ ] PDF export generates correctly
- [ ] CSV export works
- [ ] History tracking functions
- [ ] Charts render properly
- [ ] Responsive design works on mobile

## 📊 Monitoring

### Logs
- Application logs: Check Streamlit console output
- Error logs: Review browser console for client-side errors
- Performance: Monitor memory usage and response times

### Health Checks
- Application endpoint: `http://localhost:8501`
- API endpoints: Currency conversion API
- File system: Data directory permissions

## 🔒 Security

### Data Privacy
- All data processed locally
- No external data transmission
- Local JSON storage only
- No cookies or tracking

### Access Control
- No authentication required (public tool)
- Consider adding authentication for production use
- Implement rate limiting if needed

## 🚨 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

#### Currency API Errors
- Check internet connection
- Verify API endpoint availability
- Use manual override in sidebar

#### PDF Generation Errors
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install python3-dev
pip install reportlab
```

#### Port Already in Use
```bash
# Kill existing process
lsof -ti:8501 | xargs kill -9
# Or use different port
streamlit run app.py --server.port 8502
```

### Performance Optimization
- Enable caching for expensive calculations
- Optimize chart generation for large datasets
- Consider pagination for history data

## 📈 Scaling

### Horizontal Scaling
- Deploy multiple instances behind load balancer
- Use Redis for session storage
- Implement database for history (optional)

### Vertical Scaling
- Increase server resources
- Optimize Python memory usage
- Use CDN for static assets

## 🔄 Updates

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Updating Thresholds
1. Edit `utils/constants.py`
2. Test calculations
3. Update documentation
4. Deploy new version

### Backup and Recovery
- Backup `data/` directory
- Export calculation history
- Version control for configuration

## 📞 Support

### Getting Help
1. Check the Help & About page in the application
2. Review this deployment guide
3. Test with `python3 test_app.py`
4. Check Streamlit documentation

### Reporting Issues
- Include error messages
- Provide system information
- Describe steps to reproduce
- Attach relevant log files

---

**Note**: This tool is for educational purposes only. Always consult qualified legal counsel for actual competition law matters.
