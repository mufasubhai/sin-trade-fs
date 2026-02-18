#!/bin/sh
set -e

# Use PORT env var (Heroku) or default to 3000
export GF_SERVER_HTTP_PORT="${PORT:-3000}"

# Set Prometheus URL default if not provided
export PROMETHEUS_URL="${PROMETHEUS_URL:-http://prometheus:9090}"

# Set Grafana admin credentials (required for initial setup)
export GF_SECURITY_ADMIN_USER="${GF_SECURITY_ADMIN_USER:-admin}"
export GF_SECURITY_ADMIN_PASSWORD="${GF_SECURITY_ADMIN_PASSWORD:-admin}"
export GF_USERS_ALLOW_SIGN_UP=false

# Start Grafana
exec /run.sh
