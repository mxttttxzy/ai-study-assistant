#!/bin/bash

# Start the backend in the background and log output
cd /app/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 > /app/backend.log 2>&1 &

# Wait a few seconds for backend to start, then print the log
sleep 5
echo "==== BACKEND LOG ===="
cat /app/backend.log

# Start nginx in the foreground
nginx -g "daemon off;" 