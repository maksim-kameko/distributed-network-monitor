from fastapi import FastAPI

import subprocess

app = FastAPI()

current_config = {"target": "8.8.8.8"}

@app.get("/set-target/{ip}")
def set_target(ip: str):
    """Set the current monitoring target IP in the in-memory config."""
    current_config["target"] = ip
    return {"status": "success", "monitoring_now": ip}

@app.get("/get-current-target")
def get_current():
    """Return the current monitoring configuration (in-memory)."""
    return current_config

@app.get("/{ip}")
def ping(ip: str):
    """Run a single ICMP ping to the given IP and return the raw command output."""
    pingProcess = subprocess.Popen(["ping", "-c", "1", ip], 
                                   stdout=subprocess.PIPE, text=True)
    output, error = pingProcess.communicate()
    return {"host": ip, "result": output}
