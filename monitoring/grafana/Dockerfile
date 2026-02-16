FROM grafana/grafana:latest

# Copy provisioning configurations
COPY provisioning /etc/grafana/provisioning

# Copy dashboards
COPY dashboards /var/lib/grafana/dashboards

# Copy entrypoint script
USER root
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
USER grafana

# Default port (overridden by Heroku's $PORT)
EXPOSE 3000

ENTRYPOINT ["/entrypoint.sh"]
