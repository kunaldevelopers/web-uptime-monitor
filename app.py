import requests
import time
from datetime import datetime
import os
import random
import logging
import threading
import sys
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, render_template, request, jsonify, Response

# Fix Windows console emoji encoding issues
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Global variables to control the pinger state
is_running = False
ping_thread = None
target_urls = []

# Logging Configuration setup
log_file_path = "auto_pinger.log"

# Custom log handler to keep logs in memory for the web UI
class WebLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []
        self.max_logs = 100

    def emit(self, record):
        log_entry = self.format(record)
        self.logs.append(log_entry)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

web_log_handler = WebLogHandler()
web_log_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

file_handler = TimedRotatingFileHandler(
    log_file_path, 
    when="D",                  
    interval=2,                
    backupCount=0,
    encoding='utf-8'  # <--- Ensure file is saved in utf-8 to accept emojis
)
file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

# Clear existing handlers to prevent duplicates
logging.getLogger().handlers = []
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        file_handler,                           
        logging.StreamHandler(),
        web_log_handler
    ]
)

MIN_INTERVAL = 10
MAX_INTERVAL = 49
TIMEOUT = 10  
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def ping_url(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        elapsed_time = round(response.elapsed.total_seconds(), 2)
        
        if response.status_code == 200:
            logging.info(f"✅ SUCCESS: {url} | Status: {response.status_code} | Time: {elapsed_time}s")
        else:
            logging.warning(f"⚠️ WARNING: {url} | Status: {response.status_code} | Time: {elapsed_time}s")
            
    except requests.exceptions.Timeout:
        logging.error(f"❌ ERROR: {url} | Timeout ({TIMEOUT}s) - Server ne response nahi diya.")
    except requests.exceptions.ConnectionError:
        logging.error(f"❌ ERROR: {url} | Connection Failed - Server down hai ya network issue hai.")
    except Exception as e:
        logging.error(f"❌ ERROR: {url} | Unexpected Error: {type(e).__name__}")

def pinger_loop():
    global is_running
    
    logging.info("🚀 Auto Pinger Started...")
    logging.info(f"Monitoring URLs: {', '.join(target_urls)}")
    logging.info(f"Interval: Random between {MIN_INTERVAL} and {MAX_INTERVAL} seconds")
    logging.info("-" * 50)
    
    while is_running:
        for url in target_urls:
            if not is_running:
                break
            if url.strip(): 
                ping_url(url.strip())
        
        if not is_running:
            break
            
        sleep_time = random.randint(MIN_INTERVAL, MAX_INTERVAL)
        logging.info(f"⏳ Sleeping for {sleep_time} seconds...")
        
        # Sleep in small increments to allow for quick stopping
        for _ in range(sleep_time):
            if not is_running:
                break
            time.sleep(1)

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'is_running': is_running,
        'urls': target_urls
    })

@app.route('/api/start', methods=['POST'])
def start_pinger():
    global is_running, ping_thread, target_urls
    
    data = request.json
    urlsText = data.get('urls', '')
    
    # Process URLs (split by newline, remove empty, basic validation)
    target_urls = [url.strip() for url in urlsText.split('\n') if url.strip() and url.strip().startswith('http')]
    
    if not target_urls:
        return jsonify({'success': False, 'message': 'Please provide at least one valid URL starting with http:// or https://'})
    
    if is_running:
        return jsonify({'success': False, 'message': 'Pinger is already running'})
        
    is_running = True
    ping_thread = threading.Thread(target=pinger_loop)
    ping_thread.daemon = True
    ping_thread.start()
    
    return jsonify({'success': True, 'message': 'Started successfully'})

@app.route('/api/stop', methods=['POST'])
def stop_pinger():
    global is_running
    
    if not is_running:
        return jsonify({'success': False, 'message': 'Pinger is not running'})
        
    is_running = False
    logging.info("🛑 Auto Pinger Stopped by user.")
    return jsonify({'success': True, 'message': 'Stopped successfully'})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify({'logs': web_log_handler.logs})

@app.route('/api/clear_logs', methods=['POST'])
def clear_logs():
    web_log_handler.logs = []
    return jsonify({'success': True})

if __name__ == '__main__':
    # Start the web server
    print("Starting Web GUI on http://127.0.0.1:5000")
    # Setting use_reloader=False is important when combining threaded loops and Flask
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)