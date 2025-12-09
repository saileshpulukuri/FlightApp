# ✈️ Flight Delay Analysis Dashboard

A comprehensive interactive dashboard for analyzing flight delays with visualizations, predictive analytics, and chatbot assistance.

## 🚀 Quick Start (Local)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the dashboard:**
```bash
streamlit run app.py
```

3. **Open your browser:**
   - Navigate to: http://localhost:8501
   - Data automatically loads from `data/cleaned_flights.parquet/`

## Features

- **Interactive Filters**: Select airlines, months, days of week, airports, and more
- **Comprehensive Visualizations**:
  - Delay reasons breakdown (Weather, Carrier, NAS, Security, Late Aircraft)
  - Delay trends by airline, month, and day of week
  - Delay distribution analysis
  - Route analysis for top delayed routes
  - Delay rate gauge
- **Data Export**: Download filtered data as CSV
- **Model Integration**: Ready for Spark ML model predictions

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have Java installed (required for PySpark):
```bash
# On macOS
brew install openjdk

# On Ubuntu/Debian
sudo apt-get install openjdk-11-jdk
```

## Usage

1. **Prepare your data** (optional):
   - Place your flight data CSV file in the project root
   - Supported file names: `data.csv`, `flights.csv`, `flight_data.csv`, or `.parquet` files
   - If no data file is found, the app will use sample data for demonstration

2. **Run the dashboard**:
```bash
streamlit run app.py
```

3. **Use the dashboard**:
   - Select filters from the sidebar (airline, month, day, airports, etc.)
   - Click the "Visualize" button
   - Explore the interactive visualizations
   - Download filtered data if needed

## Data Format

Your CSV file should include the following columns (at minimum):
- `AIRLINE`: Airline code (e.g., 'AA', 'DL', 'UA')
- `ORIGIN_AIRPORT`: Origin airport code
- `DESTINATION_AIRPORT`: Destination airport code
- `MONTH`: Month (1-12)
- `DAY_OF_WEEK`: Day of week (1-7)
- `DEPARTURE_DELAY`: Departure delay in minutes
- `ARRIVAL_DELAY`: Arrival delay in minutes
- `DISTANCE`: Flight distance in miles
- `WEATHER_DELAY`: Weather delay in minutes
- `CARRIER_DELAY`: Carrier delay in minutes
- `NAS_DELAY`: National Air System delay in minutes
- `SECURITY_DELAY`: Security delay in minutes
- `LATE_AIRCRAFT_DELAY`: Late aircraft delay in minutes
- `DELAYED`: Binary indicator (0 or 1) for delayed flights

## Model

The dashboard is configured to work with the Spark ML model located in `Models/best_spark_model/`. The model uses:
- Features: MONTH, DAY_OF_WEEK, DEPARTURE_DELAY, DISTANCE, AIRLINE, ORIGIN_AIRPORT, DESTINATION_AIRPORT
- Target: LABEL_DELAYED (binary classification)

## 📦 Deployment to Streamlit Cloud

### Step 1: Initialize Git Repository

```bash
cd /Users/sailesh/Desktop/FlightApp
git init
git add .
git commit -m "Initial commit: Flight Delay Analysis Dashboard"
```

### Step 2: Create GitHub Repository

1. Go to GitHub.com and create a new repository
2. Name it: `flight-delay-analysis` (or your preferred name)
3. **Don't** initialize with README (we already have one)

### Step 3: Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/flight-delay-analysis.git
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `flight-delay-analysis`
5. Main file path: `app.py`
6. Click "Deploy"

### Step 5: Configure Streamlit Cloud (if needed)

If you need PySpark (optional for predictions):
- Go to app settings
- Add secrets if needed
- Note: PySpark requires Java, which may need special configuration on Streamlit Cloud

## 🎯 Features

### 1. Home Page
- Dataset overview with key metrics
- Quick insights and visualizations
- Automatic data loading

### 2. Analytics Dashboard
- **Dynamic Filters**: Real-time filtering by airline, month, airport, etc.
- **Airline-Specific Analysis**: Detailed breakdown when airline is selected
- **Hub Analysis**: Analysis of major airport hubs
- **Cascading Effects**: How delayed flights affect subsequent flights
- **Delay Predictions**: Real-time predictions based on filters
- **Visualizations**: 
  - Delay distribution (histogram & pie chart)
  - Delays by airline, month, airport
  - Confusion matrix & model metrics

### 3. Prediction Tool
- Input flight details (month, day, airline, airports, delays, distance)
- Model-based delay prediction
- Probability scores
- Feature importance explanations

### 4. Chatbot Assistant
- Interactive Q&A about flight delays
- Airline performance queries
- Airport statistics
- Seasonal pattern analysis

## 📊 Data Format

The app automatically loads from `data/cleaned_flights.parquet/`. Your data should include:
- `AIRLINE`, `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT`
- `MONTH`, `DAY_OF_WEEK`
- `DEPARTURE_DELAY`, `ARRIVAL_DELAY`, `DISTANCE`
- `WEATHER_DELAY`, `CARRIER_DELAY`, `NAS_DELAY`, `SECURITY_DELAY`, `LATE_AIRCRAFT_DELAY`
- `DELAYED` (binary: 0 or 1)

## 🔧 Troubleshooting

- **Connection errors**: Make sure Streamlit is running (`streamlit run app.py`)
- **No data shown**: Check that `data/cleaned_flights.parquet/` exists with `.parquet` files
- **PySpark errors**: PySpark is optional - analytics work without it
- **Model loading**: Ensure `Models/best_spark_model/` exists for predictions

## 📝 Notes

- **PySpark is optional**: The dashboard works perfectly for analytics without PySpark
- **Data auto-loads**: No need to upload data each time - it loads from `data/cleaned_flights.parquet/`
- **Dynamic filtering**: All visualizations update in real-time when filters change

