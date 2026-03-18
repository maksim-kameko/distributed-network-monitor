# 🌐 Distributed Network Health Monitor

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Python](https://img.shields.io/badge/python-3.10-yellow)

A lightweight, distributed network monitoring system built with **Python**, **FastAPI**, and **Docker**. Features a multi-process architecture with real-time **Telegram notifications** and a fully automated **CI/CD pipeline**.

## 🚀 Key Features
- **Real-time Monitoring**: OOP-based agent performing active network checks via ICMP.
- **Dual-Process Container**: Custom entrypoint to run both the FastAPI server and the monitoring agent simultaneously in a single container.
- **Instant Alerts**: Telegram Bot integration for immediate status reports and failure alerts.
- **Interactive API**: Fully documented with Swagger UI for remote target management and manual ping execution.
- **Enterprise CI/CD**: Automated testing and deployment orchestrated by Jenkins on AWS.

## 🏗 Tech Stack
- **Language**: Python 3.10
- **Framework**: FastAPI, Uvicorn
- **DevOps**: Docker, Jenkins (Groovy Declarative Pipelines), AWS EC2
- **Testing**: Pytest (Unit/Integration), Robot Framework (Acceptance/BDD)
- **Networking**: Cloudflare Tunnels (Secure Exposure), ICMP/Ping
- **Messaging**: Telegram Bot API

---

## ⚙️ Architecture & CI/CD

The system is designed for high availability and continuous delivery. Every commit to `main` triggers a full validation suite.

### Live Infrastructure
- **Jenkins Server**: https://jenkins.maksim-network.me
- **Deployment**: Hosted on an **AWS EC2** instance, running within an isolated Docker environment.

### Pipeline Stages
1. `Checkout`  
2. `Environment Setup`  
3. `Unit Tests (Pytest)`  
4. `Acceptance Tests (Robot)`  
5. `Docker Build & Deploy`

---

## 🚦 Getting Started

### 1. Environment Configuration
Create a `.env` file in the root directory:

```env
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

---

### 2. Run with Docker (Recommended)

The Docker image starts both the API and the monitoring agent:

```bash
# Build the image
docker build -t monitor-server .

# Run the container
docker run -d \
  --name fastapi-monitor \
  -p 8000:8000 \
  --env-file .env \
  monitor-server
```

---

### 3. Manual Usage (Local Development)

Run services separately:

```bash
# Start FastAPI Server
uvicorn server:app --host 0.0.0.0 --port 8000

# Start Monitoring Agent
python3 tester.py
```

---

## 🧪 Testing & Documentation

- **Swagger UI**: http://your-ip:8000/docs  
- **Unit/Integration Tests**:
```bash
python3 -m pytest test_server.py -v
```

- **Acceptance Tests (BDD)**:
```bash
python3 -m robot network_tests.robot
```

- **Real-time Logs**:
```bash
docker logs -f fastapi-monitor
```
