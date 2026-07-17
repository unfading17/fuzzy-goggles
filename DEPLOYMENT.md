# Permitai - Deployment Guide

## Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account (done ✅)
- Streamlit account (free)

### Step 1: Connect GitHub
1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your GitHub repo: `unfading17/fuzzy-goggles`
4. Select branch: `main`
5. Select file: `main_app.py`

### Step 2: Configure Secrets (Optional)
1. In Streamlit Cloud dashboard, click "Advanced settings"
2. Add secrets from `.streamlit/secrets.toml`
3. Save

### Step 3: Deploy
- Click "Deploy"
- Wait 2-3 minutes
- Your app will be live at: `https://share.streamlit.io/unfading17/fuzzy-goggles/main/main_app.py`

## Local Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Locally
```bash
streamlit run main_app.py
```

Visit: http://localhost:8501

## Docker Deployment

### Build Image
```bash
docker build -t permitai .
```

### Run Container
```bash
docker run -p 8501:8501 permitai
```

Visit: http://localhost:8501

## Docker Compose (Full Stack)

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

## Cloud Deployment Options

### Option 1: Render.com
- Free tier available
- Auto-deploys from GitHub
- Good uptime

### Option 2: DigitalOcean
- $5/month droplet
- Full control
- Easy app deployment

### Option 3: Heroku
- Simple deployment
- Has free tier
- Good for small projects

### Option 4: Railway.app
- Modern alternative to Heroku
- Pay as you go
- Simple GitHub integration

## Production Checklist

- [ ] Change SECRET_KEY in production
- [ ] Enable HTTPS only
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Enable CORS properly
- [ ] Set up CDN for static files
- [ ] Configure email notifications
- [ ] Set up SSL certificates

## Support

For issues or questions:
- Check logs: `logs/permitai.log`
- Check errors: `logs/permitai_errors.log`
- Open issue on GitHub: https://github.com/unfading17/fuzzy-goggles/issues
