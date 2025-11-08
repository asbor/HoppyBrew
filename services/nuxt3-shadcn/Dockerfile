# Use the official Node.js LTS image as a base
FROM node:lts-alpine

# Accept UID and GID as build arguments (defaults to 1000 if not provided)
ARG USER_UID=1000
ARG USER_GID=1000

# Create a non-root user with the specified UID/GID
RUN addgroup -g ${USER_GID} appgroup && \
    adduser -D -u ${USER_UID} -G appgroup appuser

# Set the working directory in the container
WORKDIR /app

# Change ownership of the working directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Copy package.json and yarn.lock to the container
COPY --chown=appuser:appgroup package.json yarn.lock ./

# Install dependencies using Yarn
RUN yarn install

# Copy the rest of the application files to the container
COPY --chown=appuser:appgroup . .

# Build the Nuxt 3 application
RUN yarn build

# Expose the port that the Nuxt app will run on
EXPOSE 3000

# Set the command to run the Nuxt app
CMD ["yarn", "start"]
