#!/bin/sh
set -e

# Use PORT env var (Heroku) or default to 3000
export GF_SERVER_HTTP_PORT="${PORT:-3000}"

# Set Prometheus URL default if not provided
export PROMETHEUS_URL="${PROMETHEUS_URL:-http://prometheus:9090}"

# Start Grafana
exec /run.sh
