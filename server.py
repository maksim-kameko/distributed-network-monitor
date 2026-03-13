from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/{ip}")

def ping(ip):
	pingProcess = subprocess.Popen(["ping", "-c", "1", ip],
	stdout=subprocess.PIPE, text = True)
	
	output, error = pingProcess.communicate()
	return {"host": ip, "result": output}
	
	
