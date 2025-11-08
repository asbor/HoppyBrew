# Use the official Node.js LTS image as a base
FROM node:lts-alpine

# Accept build arguments for user/group IDs
ARG HOST_UID=1000
ARG HOST_GID=1000

# Create a group and user with the specified GID and UID if they don't exist
# Use 'addgroup' and 'adduser' with checks to handle existing IDs gracefully
RUN if ! getent group ${HOST_GID} > /dev/null 2>&1; then \
      addgroup -g ${HOST_GID} appuser; \
    fi && \
    if ! getent passwd ${HOST_UID} > /dev/null 2>&1; then \
      adduser -u ${HOST_UID} -G $(getent group ${HOST_GID} | cut -d: -f1) -s /bin/sh -D appuser; \
    fi

# Set the working directory in the container
WORKDIR /app

# Create .nuxt directory and set ownership
RUN mkdir -p /app/.nuxt && \
    chown -R ${HOST_UID}:${HOST_GID} /app

# Switch to the app user
USER ${HOST_UID}:${HOST_GID}

# Expose the port that the Nuxt app will run on
EXPOSE 3000

# Set the command to run the Nuxt app in development mode
# This will be overridden by docker-compose command
CMD ["yarn", "dev", "--host", "0.0.0.0"]
