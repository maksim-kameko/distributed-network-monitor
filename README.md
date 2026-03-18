# Distributed Network Health Monitor

A lightweight, distributed network monitoring system built with Python and FastAPI. It includes a fully automated CI/CD pipeline for continuous testing.

## Architecture
- **Server (Backend)**: Uses FastAPI and `subprocess` to execute system-level ping commands.
- **Tester (Agent)**: An OOP-based client that polls the server for status and logs results with timestamps.

## Tech Stack
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Libraries**: Requests, Subprocess, Datetime, Time
- **Testing**: Pytest (Unit/Integration), Robot Framework (Acceptance/BDD)
- **Infrastructure**: AWS (EC2), Docker, Jenkins (Continuous Integration), Cloudflare Tunnels

---

## CI/CD Pipeline (Live Infrastructure)

This project is continuously integrated and tested using my own Jenkins CI server.  
**The server is hosted on an AWS EC2 instance, running 24/7 inside a Docker container, and is exposed securely via Cloudflare Tunnels.**

🟢 **Live Jenkins Server:**  
https://jenkins.maksim-network.me

The pipeline is written in **Groovy (Declarative Pipeline)** and triggers on every commit to `main`.

**Pipeline Stages:**
- Checkout
- Environment Setup
- Unit Testing (pytest)
- Acceptance Testing (Robot Framework)
- Artifacts (HTML/XML reports)

---

## How to Run

### 1. Start the server:
```bash
uvicorn server:app --reload
```

### 2. Run the monitoring agent:
(It uses `8.8.8.8` by default, or you can specify your own target)

```bash
python3 tester.py [TARGET_IP]
```

Example:
```bash
python3 tester.py 1.1.1.1
```

### 3. View the logs:
```bash
cat history.log
```

---

## Docker Deployment

### 1. Build the image:
```bash
docker build -t monitor-server .
```

### 2. Run the container:
```bash
docker run -p 8000:8000 monitor-server
```

---

## Manual Testing

### Unit Tests:
```bash
python3 -m pytest test_server.py -v
```

### Acceptance Tests:
```bash
python3 -m robot network_tests.robot
```
