#!/bin/sh
set -e

# Set defaults for all variables
export SCRAPE_SCHEME="${SCRAPE_SCHEME:-https}"
export SIN_TRADE_BE_HOST="${SIN_TRADE_BE_HOST:-backend:5002}"
export SIN_TRADE_DS_HOST="${SIN_TRADE_DS_HOST:-ds:5004}"

# Substitute environment variables in the prometheus config template
envsubst '${SIN_TRADE_BE_HOST} ${SIN_TRADE_DS_HOST} ${SCRAPE_SCHEME}' < /etc/prometheus/prometheus.yml.template > /tmp/prometheus.yml

# Use PORT env var (Heroku) or default to 9090
WEB_PORT="${PORT:-9090}"

# Start Prometheus with the generated config
exec prometheus \
    --config.file=/tmp/prometheus.yml \
    --storage.tsdb.path=/prometheus \
    --web.listen-address=":${WEB_PORT}" \
    --web.enable-lifecycle
