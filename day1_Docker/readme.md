# Day 1 - Docker & Demo App

This directory contains materials for Day 1: building, containerizing, and deploying a FastAPI demo application.

## Objectives

- Build and run a FastAPI demo application locally
- Create Docker images and push to Docker Hub
- Deploy containerized applications to Minikube
- Understand Docker basics and container workflows

## Files

- `readme.md` - This file
- `Dockerfile` - Docker image build instructions for the demo app
- `demoApp/` - FastAPI demo application directory (see demoApp/readme.md for details)

## Quick Start

1. **Run the app locally** (see `demoApp/readme.md` for detailed instructions):
   ```bash
   cd demoApp
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Build Docker image**:
   ```bash
   # From the demoApp directory
   docker build -t yourusername/demoapp:latest .
   ```

3. **Push to Docker Hub**:
   ```bash
   docker login
   docker push yourusername/demoapp:latest
   ```

4. **Deploy to Minikube**:
   ```bash
   # Build image directly in minikube
   cd demoApp
   minikube image build -t demoapp:latest .
   ```

## Directory Structure

- `demoApp/` - Contains the FastAPI application code, requirements, and Dockerfile
  - `main.py` - FastAPI application
  - `requirements.txt` - Python dependencies
  - `Dockerfile` - Container build instructions
  - `static/` - Static files (favicon)
  - `readme.md` - Detailed instructions for running the app

## Demo App Features

The FastAPI demo app includes:
- Root endpoint (`/`) - Welcome message
- Health check (`/healthz`) - Application health status
- Readiness check (`/readiness`) - Application readiness status
- Static files (`/static/favicon.svg`) - Sample static content

## Next Steps

- See Day 2 for Kubernetes Deployment examples
- See Day 3 for Kubernetes Service examples
- Learn about container best practices and multi-stage builds