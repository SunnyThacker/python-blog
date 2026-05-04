# Build and run instructions for the Blog Application

## Prerequisites
- Docker installed on your system
- Git (optional, for cloning)

## Building the Docker Image

```bash
# Navigate to the project directory
cd test-project

# Build the Docker image
docker build -t my-blog:latest .
```

## Running the Container

### Option 1: Basic run (interactive mode)
```bash
docker run -p 3000:3000 my-blog:latest
```

### Option 2: Run in detached mode (background)
```bash
docker run -d -p 3000:3000 --name my-blog-container my-blog:latest
```

### Option 3: Run with environment variables
```bash
docker run -d -p 3000:3000 -e FLASK_ENV=production my-blog:latest
```

## Accessing the Application

Once the container is running, visit:
- **Home Page:** http://localhost:3000
- **Create Post:** http://localhost:3000/create
- **About:** http://localhost:3000/about
- **API Endpoints:** http://localhost:3000/api/posts

## Container Management Commands

```bash
# View running containers
docker ps

# View all containers (including stopped ones)
docker ps -a

# Stop the container
docker stop my-blog-container

# Start a stopped container
docker start my-blog-container

# Remove a container
docker rm my-blog-container

# View container logs
docker logs my-blog-container

# Remove the image
docker rmi my-blog:latest
```

## Development Notes

- The application runs on port 3000 inside and outside the container
- Flask debug mode is enabled in the container
- Posts are stored in memory (resets when container restarts)
- For production use, modify app.py to use a database instead of in-memory storage

## Docker Compose (Optional)

If you want to use Docker Compose, create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  blog:
    build: .
    ports:
      - "3000:3000"
    environment:
      - FLASK_ENV=development
```

Then run: `docker-compose up`
