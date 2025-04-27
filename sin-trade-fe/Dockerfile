# Use the official Node.js image from the Docker Hub
FROM node:22.1.0


ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL="TEST_URL"
# Set the working directory
WORKDIR /app

# Copy the package.json and pnpm-lock.yaml files
COPY package.json pnpm-lock.yaml ./

# Install pnpm
RUN npm install -g pnpm

# Install the dependencies
RUN pnpm install

# Copy the rest of the application code into the container
COPY . .

# Build the application
RUN pnpm run build

# Expose the port the app runs on or the default serve port. We may need to adjust this
EXPOSE ${PORT:-4173}

HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD curl --fail http://localhost:${PORT:-4173} || exit 1

# Command to run the application
CMD ["pnpm", "serve"]