# Demo App Deployment Guide

This document provides step-by-step instructions for building, pushing to Docker Hub, and deploying the FastAPI demo application to Minikube.

## 1. Building the Docker Image Locally

Navigate to the demoApp directory and build the image:

```bash
cd day1_Docker/demoApp
docker build -t demoapp:latest .
```

## 2. Pushing to Docker Hub

### Step 1: Tag the Image with Your Docker Hub Username

```bash
# Replace "yourusername" with your actual Docker Hub username
docker tag demoapp:latest yourusername/demoapp:latest
```

### Step 2: Login to Docker Hub

Before pushing images to Docker Hub, you need to authenticate with your Docker Hub account.

```bash
# Interactive login (will prompt for username and password)
docker login

# Or specify username directly (will still prompt for password)
docker login --username yourusername

# For CI/CD environments or scripts (not recommended for security reasons)
# docker login --username yourusername --password yourpassword
```

You can also use a personal access token instead of your password for added security:

1. Create a token on Docker Hub:
   - Go to https://hub.docker.com/settings/security
   - Click "New Access Token"
   - Enter a description and select appropriate permissions
   - Copy the generated token

2. Use the token for login:
   ```bash
   docker login --username yourusername
   # When prompted for password, paste your access token
   ```

To verify you've logged in successfully:

```bash
docker info | grep -A1 "Username"
```

### Step 3: Push the Image to Docker Hub

```bash
# Replace "yourusername" with your actual Docker Hub username
docker push yourusername/demoapp:latest
```

## Alternative: Build image directly into Minikube

If you prefer not to push to Docker Hub while developing, you can build the image directly into Minikube so the cluster can use it without pulling from a remote registry:

```bash
# From repository root or the demoApp directory
cd day1_Docker/demoApp
minikube image build -t demoapp:latest -f Dockerfile .
```

This places the image into Minikube's local registry and you can use `image: demoapp:latest` with `imagePullPolicy: IfNotPresent` in your Deployment.

## Private registry / imagePullSecrets

If you push the image to a private Docker Hub repository (or any private registry), create a Kubernetes secret and reference it in your deployment:

```bash
kubectl create secret docker-registry regcred \
   --docker-server=https://index.docker.io/v1/ \
   --docker-username=yourusername \
   --docker-password=yourpassword \
   --docker-email=your.email@example.com
```

Then add to your pod spec:

```yaml
spec:
   imagePullSecrets:
   - name: regcred
```