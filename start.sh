#!/bin/bash
set -e
 
uvicorn api.main:app --host 0.0.0.0 --port 8000 &
 
sleep 3
 
export BACKEND_URL="http://localhost:8000"
 
streamlit run frontend/app.py \
  --server.port=7860 \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --browser.gatherUsageStats=false