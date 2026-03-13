import requests
from datetime import datetime
import time

class NetworkChecker:
	def get_status(self):
		data = requests.get("http://127.0.0.1:8000/8.8.8.8")
		return data.json()

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

checker = NetworkChecker()
while True:
	output = checker.get_status()
	checker.log_results(output)
	print("Log saved. Next one in 10 sec")
	time.sleep(10)
