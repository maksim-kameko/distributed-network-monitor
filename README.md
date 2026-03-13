# Distributed Network Health Monitor

A lightweight, distributed network monitoring system built with Python and FastAPI.

## Architecture
- **Server (Backend)**: Uses FastAPI and `subprocess` to execute system-level ping commands.
- **Tester (Agent)**: An OOP-based client that polls the server for status and logs results with timestamps.

## Tech Stack
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Libraries**: Requests, Subprocess, Datetime, Time
- **Environment**: Linux / Ubuntu

## How to Run
1. Start the server:
   `uvicorn server:app --reload`
2. Run the monitoring agent:
   `python3 tester.py`
3. View the logs:
   `cat history.log`
