FROM alpine:latest

# Install Prometheus and envsubst (from gettext)
RUN apk add --no-cache prometheus gettext

# Copy configuration template and entrypoint
COPY prometheus.yml.template /etc/prometheus/prometheus.yml.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 9090

ENTRYPOINT ["/entrypoint.sh"]
