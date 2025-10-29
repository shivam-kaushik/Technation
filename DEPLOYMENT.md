# Deployment Guide

## Deploy to Streamlit Community Cloud (FREE)

### Prerequisites
- GitHub account
- This repository pushed to GitHub

### Steps

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your repository: `shivam-kaushik/Technation`
   - Main file path: `app.py`
   - Click "Deploy"!

3. **Your app will be live at:**
   ```
   https://shivam-kaushik-technation.streamlit.app
   ```

### Configuration
- Max file upload: 200MB
- Python version: 3.10
- All dependencies in `requirements.txt`

### Environment Variables
Add these in Streamlit Cloud settings if needed:
- `USE_TF=NO`
- `TRANSFORMERS_NO_TF=1`

### Monitoring
- Check logs in Streamlit Cloud dashboard
- App auto-wakes when accessed
- Sleeps after 7 days of inactivity (free tier)

## Alternative: Deploy to Other Platforms

### Heroku
1. Create `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py
   ```
2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```

### Docker
1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py"]
   ```

### AWS/GCP/Azure
- Use container services (ECS, Cloud Run, Container Apps)
- Set environment variables for PyTorch CPU-only builds
- Configure auto-scaling based on traffic

## Important Notes

1. **First deployment takes 5-10 minutes** (downloading ML models)
2. **Data privacy**: All processing happens server-side, user data not stored
3. **Model caching**: sentence-transformers model cached after first load
4. **PDF generation**: Stored temporarily in `output/` folder

## Troubleshooting

### Out of Memory
- Reduce model size in `utils.py`
- Use `sentence-transformers/all-MiniLM-L6-v2` (already using this)

### Slow Cold Starts
- Models downloaded on first request
- Consider pre-downloading in container build

### TensorFlow Errors
- Environment variables already set in `app.py`
- No TensorFlow needed (PyTorch only)

## Support
- Streamlit docs: https://docs.streamlit.io/
- Community forum: https://discuss.streamlit.io/
