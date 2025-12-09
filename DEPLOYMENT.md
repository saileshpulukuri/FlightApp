# 🚀 Deployment Guide

## Local Testing (Current Status: ✅ Working)

Your dashboard is currently running locally at: **http://localhost:8501**

## Next Steps: Deploy to Streamlit Cloud

### 1. Initialize Git Repository

```bash
cd /Users/sailesh/Desktop/FlightApp

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Flight Delay Analysis Dashboard"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `flight-delay-analysis` (or your choice)
3. Description: "Flight Delay Analysis Dashboard with ML Predictions"
4. **Make it Public** (required for free Streamlit Cloud)
5. **Don't** check "Initialize with README" (we already have one)
6. Click "Create repository"

### 3. Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/flight-delay-analysis.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### 4. Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click **"New app"**
4. Fill in:
   - **Repository**: Select `YOUR_USERNAME/flight-delay-analysis`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: (auto-generated)
5. Click **"Deploy"**

### 5. Wait for Deployment

- First deployment takes 2-3 minutes
- You'll see build logs
- Once done, your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

## Important Notes for Streamlit Cloud

### Data Files
- Your `data/cleaned_flights.parquet/` files will be included in the repo
- If files are too large (>100MB), consider using Git LFS or hosting data separately

### PySpark (Optional)
- PySpark requires Java, which Streamlit Cloud may not support by default
- The dashboard works perfectly without PySpark for analytics
- Only the Prediction Tool needs PySpark

### Environment Variables
- If needed, add secrets in Streamlit Cloud app settings
- Access via: `st.secrets["key"]`

## Troubleshooting Deployment

### Build Fails
- Check `requirements.txt` - remove any problematic packages
- Ensure all imports are available
- Check build logs in Streamlit Cloud

### App Crashes
- Check logs in Streamlit Cloud
- Verify data files are accessible
- Test locally first

### Data Not Loading
- Ensure `data/cleaned_flights.parquet/` is in the repo
- Check file paths are correct
- Verify parquet files are readable

## Current Status

✅ **Local**: Working at http://localhost:8501  
⏳ **Git Repo**: Ready to initialize  
⏳ **GitHub**: Ready to create  
⏳ **Streamlit Cloud**: Ready to deploy  


