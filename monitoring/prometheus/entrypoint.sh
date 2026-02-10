#!/bin/sh
set -e

export SCRAPE_SCHEME="${SCRAPE_SCHEME:-http}"

envsubst '${SIN_TRADE_BE_HOST} ${SIN_TRADE_DS_HOST} ${SCRAPE_SCHEME}' < /etc/prometheus/prometheus.yml.template > /tmp/prometheus.yml

  exec prometheus \
    --config.file=/tmp/prometheus.yml \
    --storage.tsdb.path=/prometheus \
    --web.enable-lifecycle
