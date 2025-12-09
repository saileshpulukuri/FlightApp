# 🚀 How to Keep Dashboard Running

## Quick Start (Recommended)

### Start Dashboard (Persistent)
```bash
cd /Users/sailesh/Desktop/FlightApp
./keep_running.sh
```

This will:
- ✅ Start the dashboard in the background
- ✅ Keep it running even if you close the terminal
- ✅ Log everything to `streamlit.log`

### Check Status
```bash
./check_status.sh
```

### Stop Dashboard
```bash
./stop_dashboard.sh
```

## Manual Start (Alternative)

If you want to see the output in real-time:
```bash
cd /Users/sailesh/Desktop/FlightApp
python3 -m streamlit run app.py --server.port 8501
```

**Note:** This will stop when you close the terminal. Use `keep_running.sh` for persistent operation.

## Auto-Start on Boot (Optional)

To make the dashboard start automatically when your Mac boots:

1. **Install the service:**
```bash
cd /Users/sailesh/Desktop/FlightApp
cp com.flightdelay.streamlit.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.flightdelay.streamlit.plist
```

2. **Start it now:**
```bash
launchctl start com.flightdelay.streamlit
```

3. **Stop it:**
```bash
launchctl stop com.flightdelay.streamlit
```

4. **Remove auto-start:**
```bash
launchctl unload ~/Library/LaunchAgents/com.flightdelay.streamlit.plist
rm ~/Library/LaunchAgents/com.flightdelay.streamlit.plist
```

## Troubleshooting

### Dashboard stops after a few minutes
- Use `./keep_running.sh` instead of running manually
- Check logs: `tail -f streamlit.log`

### Can't access http://localhost:8501
- Check if running: `./check_status.sh`
- Restart: `./stop_dashboard.sh && ./keep_running.sh`

### Port already in use
```bash
./stop_dashboard.sh
# Wait 5 seconds
./keep_running.sh
```

## Current Status

Run this to check:
```bash
./check_status.sh
```

## Logs

View logs:
```bash
tail -f streamlit.log
```


