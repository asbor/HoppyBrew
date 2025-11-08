#!/bin/bash
# Docker Permission Fix Helper Script
# This script helps run docker-compose with the correct user permissions

# Set the HOST_UID and HOST_GID environment variables
export HOST_UID=$(id -u)
export HOST_GID=$(id -g)

echo "================================================"
echo "HoppyBrew Docker Compose Helper"
echo "================================================"
echo ""
echo "Setting up with:"
echo "  HOST_UID: $HOST_UID"
echo "  HOST_GID: $HOST_GID"
echo ""
echo "This ensures files created by Docker containers"
echo "will have the same ownership as your host user."
echo "================================================"
echo ""

# Run docker-compose with the provided arguments
docker compose "$@"
