#!/bin/bash
python3 tester.py & 
uvicorn server:app --host 0.0.0.0 --port 8000 
