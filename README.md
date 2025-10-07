# Certified Kubernetes Administrator (CKA)

Welcome to the CKA exam preparation repository! This repository contains study materials, practice exercises, and setup guides for the Certified Kubernetes Administrator exam.

## Documentation

- [Minikube Installation Guide for Ubuntu](./minikube-ubuntu-installation.md) - Complete step-by-step guide for installing Minikube on Ubuntu systems

## Quickstart

1. Install Minikube (see the documentation link above).
2. Follow the Day 1 instructions to run the demo app locally or in Minikube.

## Daily Study Materials

- [Day 1: Docker / Demo App](./day1_Docker/readme.md) - Build and run a FastAPI demo app, create Docker image and deploy to Minikube
- [Day 2: Deployment](./day2_Deployment/readme.md) - Kubernetes deployment examples and manifests
- [Day 3: Services](./day3_Service/readme.md) - Understanding and working with Kubernetes Services
- [Day 4: Architecture](./day4_architecture/README.md) - Kubernetes architecture diagrams and visualizations

## Repository Structure

- `day1_Docker/` - Day 1 materials: demo app, Dockerfile, and k8s manifests
- `day2_Deployment/` - Day 2 deployment examples and manifests  
- `day3_Service/` - Day 3 materials: Kubernetes Services examples and manifests
- `day4_architecture/` - Day 4 materials: Kubernetes architecture diagrams and visualizations
- `start_minikube.sh` - Script to start Minikube cluster
- `minikube-ubuntu-installation.md` - Minikube installation documentation

## Adding New Days

When adding new day folders, please:
1. Create a folder named `dayN_Topic` (e.g., `day4_ConfigMaps`)
2. Include a `readme.md` in the folder describing the day's objectives and exercises
3. Add a link to the new day in the "Daily Study Materials" section above