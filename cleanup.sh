# 1. Clean Docker resources
echo "Cleaning Docker resources..."
docker-compose down -v
docker system prune -af --volumes
# Also remove all containers, images, and volumes explicitly
docker rm -f $(docker ps -aq) 2>/dev/null || true
docker rmi -f $(docker images -aq) 2>/dev/null || true
docker volume rm $(docker volume ls -q) 2>/dev/null || true

# 2. Clean Python environments and cache
echo "Cleaning Python environments and cache..."
# Remove virtual environments
rm -rf sin-trade-be/be-venv/
rm -rf sin-trade-ds/ds-venv/
rm -rf **/.venv/
# Clean Python cache more thoroughly
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.py[cod]" -delete
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name ".coverage" -delete
find . -type d -name ".eggs" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true