#!/bin/bash

echo "==== DEBUG: Current directory ===="
pwd
echo "==== DEBUG: List /app ===="
ls -l /app
echo "==== DEBUG: List /app/backend ===="
ls -l /app/backend

# Run database migrations
cd /app/backend || exit 1
echo "==== DEBUG: Running database migrations ===="
python -m alembic upgrade head

# Start the backend in the background and log output
echo "==== DEBUG: Starting backend ===="
python -m uvicorn main:app --host 0.0.0.0 --port 8000 > /app/backend.log 2>&1 &

# Wait a few seconds for backend to start, then print the log
sleep 5
echo "==== BACKEND LOG ===="
cat /app/backend.log || echo "No backend log found"

# Start nginx in the foreground
echo "==== DEBUG: Starting nginx ===="
nginx -g "daemon off;" 