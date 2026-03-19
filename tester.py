import requests
from datetime import datetime
import time
import sys
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    """Send a text message to a configured Telegram chat (no-op if env vars are missing)."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Błąd Telegrama: {e}")

class NetworkChecker:
    def get_current_target_from_api(self):
        """Fetch the current target IP from the local API, falling back to a default."""
        try:
            r = requests.get("http://127.0.0.1:8000/get-current-target", timeout=5)
            return r.json().get("target", "8.8.8.8")
        except:
            return "8.8.8.8" 

    def get_status(self, target_ip):
        """Call the local ping API for the given target and return its JSON response (or error)."""
        try:
            data = requests.get(f"http://127.0.0.1:8000/{target_ip}")
            data.raise_for_status()
            return data.json()
        except requests.exceptions.RequestException as e:
            return {"host": target_ip, "result": f"Connection Error: {e}"}

    def log_results(self, results):
        """Append a formatted status line to history.log and forward it to Telegram."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        host = results.get("host")
        if "1 received" in str(results):
            status = "🟢 [ OK ]"
        else:
            status = "🔴 [ ERROR ]"
        log_entry = f"[{now}] {host:15} {status}\n"

        with open("history.log", "a") as f:
            f.write(log_entry)

        print(f"Sending log to Telegram: {log_entry}")
        send_telegram_message(log_entry)

if len(sys.argv) > 1:
    target_ip = sys.argv[1]
else:
    target_ip = "8.8.8.8"

checker = NetworkChecker()

while True:
    current_target = checker.get_current_target_from_api()
    output = checker.get_status(current_target)
    checker.log_results(output)
    print(f"Log saved for {current_target}. Next one in 10 sec")
    time.sleep(10)

