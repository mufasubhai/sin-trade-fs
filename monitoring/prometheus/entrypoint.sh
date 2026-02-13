#!/bin/sh
set -e

# Set defaults for all variables
export SCRAPE_SCHEME="${SCRAPE_SCHEME:-https}"
export SIN_TRADE_BE_HOST="${SIN_TRADE_BE_HOST:-backend:5002}"
export SIN_TRADE_DS_HOST="${SIN_TRADE_DS_HOST:-ds:5004}"

# Substitute environment variables in the prometheus config template
envsubst '${SIN_TRADE_BE_HOST} ${SIN_TRADE_DS_HOST} ${SCRAPE_SCHEME}' < /etc/prometheus/prometheus.yml.template > /tmp/prometheus.yml

# Start Prometheus with the generated config
exec prometheus \
    --config.file=/tmp/prometheus.yml \
    --storage.tsdb.path=/prometheus \
    --web.enable-lifecycle
