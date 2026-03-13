import requests
from datetime import datetime
import time
import sys

class NetworkChecker:
	def __init__(self, target_ip):
		self.target_ip = target_ip

	def get_status(self):
		try:
			data = requests.get(f"http://127.0.0.1:8000/{self.target_ip}")
			data.raise_for_status()
			return data.json()
		except requests.exceptions.RequestException as e:
			return {"host": self.target_ip, "result": f"Connection Error: {e}"}

	def log_results(self, results):
		now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		host = results.get("host")
		if "1 received" in str(results):
			status = "[ OK ]"
		else:
			status = "[ ERROR ]"
		log_entry = f"[{now}] {host:15} {status}\n"

		with open("history.log", "a") as f:
			f.write(log_entry)


if len(sys.argv) > 1:
	target_ip = sys.argv[1]
else:
	target_ip = "8.8.8.8"

checker = NetworkChecker(target_ip)

while True:
	output = checker.get_status()
	checker.log_results(output)
	print(f"Log saved for {target_ip}. Next one in 10 sec")
	time.sleep(10)

