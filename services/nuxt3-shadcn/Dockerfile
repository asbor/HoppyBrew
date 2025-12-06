# Use a stable Node.js release that works with Nuxt 3 tooling
FROM node:20-alpine

# Allow API base URL to be injected at build time so the client bundle points to the right backend
ARG API_URL=http://localhost:8000
ENV NUXT_PUBLIC_API_URL=$API_URL

# Set the working directory in the container
WORKDIR /app

# Copy package.json and yarn.lock to the container
COPY package.json yarn.lock ./

# Install dependencies using Yarn
RUN yarn install

# Copy the rest of the application files to the container
COPY . .

# Build the Nuxt 3 application
RUN yarn build

# Expose the port that the Nuxt app will run on
EXPOSE 3000

# Set the command to run the Nuxt app
CMD ["yarn", "start"]
