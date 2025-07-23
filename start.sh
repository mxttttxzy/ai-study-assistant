#!/bin/bash

# Start the backend in the background
cd /app/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start nginx in the foreground
nginx -g "daemon off;" 