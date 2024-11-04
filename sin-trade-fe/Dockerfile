# Use the official Node.js image from the Docker Hub
FROM node:22.1.0

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

# Expose the port the app runs on
EXPOSE $PORT

# Command to run the application
CMD ["pnpm", "serve"]