# 🚀 Auto Pinger (Keep Apps Awake)

A simple, robust, and web-based Python application that prevents free-tier hosting services (like Render, Heroku) from putting your web apps to sleep after periods of inactivity.

## ✨ Features

- **Multi-URL Pinging:** Monitor and prevent sleep for multiple applications simultaneously.
- **Human-like Ping Intervals:** Randomizes ping intervals (30s to 120s) to appear more natural and avoid simplistic bot detection.
- **Web Interface (GUI):** Clean, responsive dashboard to start/stop pinging and view live logs.
- **Automated Log Rotation:** Logs are kept for maximum 2 days before being discarded to ensure zero storage overhead on production servers.
- **One-Click Deploy:** Ready out of the box for Render using `render.yaml`.

---

## 🚀 Easy Deployment on Render

This project is fully ready for an automated deployment on **dashboard.render.com**!
You **DO NOT** need to configure anything manually. The `render.yaml` specifies the infrastructure automatically.

1. Fork or upload this repository to your GitHub account.
2. Go to your [Render Dashboard](https://dashboard.render.com/).
3. Click on the **New +** button and select **Blueprint**.
4. Connect this repository to your Render account.
5. Watch Render automatically build and deploy your application.

No need to install dependencies manually! It handles it through `requirements.txt` and uses `gunicorn` for a stable deployment.

---

## 💻 Local Development / Testing

If you want to run it on your own computer to test the web interface:

### 1. Prerequisites
- Python 3.11 or later installed.
- Git (optional).

### 2. Installation
Open your terminal and clone the directory (or download the ZIP file). Navigate to the folder:
```bash
cd render-autosleep-prevention
```

Install the required Python modules:
```bash
pip install -r requirements.txt
```

### 3. Run the App
To start the Flask Web GUI, simply run:
```bash
python auto_pinger.py
```

Now open up your browser and visit:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

Enter your Render URLs on the dashboard, hit "Start", and watch the live logs!

---

## 🛠️ Configuration
If you wish to configure intervals, you can modify the bounds in `auto_pinger.py`:
- `MIN_INTERVAL = 30` (Seconds)
- `MAX_INTERVAL = 120` (Seconds)

## 📝 Logs
- Terminal / SSH: The script prints visually formatted logs with emojis to `stdout`.
- Internal logs: Handled automatically by `TimedRotatingFileHandler` which drops 2-day old logs saving space.

## 📄 License
This original code is open and free to modify as per your needs.

---
### 🔍 Tags / Keywords (SEO)
`render`, `heroku`, `autosleep`, `keep-alive`, `stay-awake`, `python-pinger`, `uptime-robot-alternative`, `free-hosting`, `web-gui`, `prevent-sleep`, `flask-app`, `render-blueprint`, `auto-pinger`, `bot`, `24/7-online`
