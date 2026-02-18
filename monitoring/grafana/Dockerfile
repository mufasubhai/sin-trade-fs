FROM grafana/grafana:latest

ARG GF_SECURITY_ADMIN_USER=admin
ARG GF_SECURITY_ADMIN_PASSWORD=admin
ENV GF_SECURITY_ADMIN_USER=${GF_SECURITY_ADMIN_USER}
ENV GF_SECURITY_ADMIN_PASSWORD=${GF_SECURITY_ADMIN_PASSWORD}
ENV GF_USERS_ALLOW_SIGN_UP=false

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
