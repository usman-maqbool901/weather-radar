FROM node:22-alpine

WORKDIR /app

# Build arguments for environment variables
ARG VITE_MAPBOX_TOKEN
ARG VITE_API_URL

# Set environment variables for build
ENV VITE_MAPBOX_TOKEN=$VITE_MAPBOX_TOKEN
ENV VITE_API_URL=$VITE_API_URL

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source code
COPY . .

# Build the application (Vite will use the env vars)
RUN npm run build

# Install a simple static file server for serving dist
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Start static file server on port 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
