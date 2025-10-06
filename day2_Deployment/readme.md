# Day 2 - Kubernetes Deployments

This directory contains materials for Day 2: understanding and working with Kubernetes Deployments.

## Objectives

- Understand Kubernetes Deployment concepts
- Learn how to create and manage Deployments
- Practice with deployment scaling and updates
- Configure health checks (readiness and liveness probes)
- Deploy applications using container images

## Prerequisites

- Minikube running
- Docker Hub account (optional, for custom images)
- Basic understanding of Kubernetes concepts

## Files

- `readme.md` - This file
- `k8s-deployment.yaml` - Deployment manifest

## 1. Review the Deployment Manifest

The `k8s-deployment.yaml` file contains a deployment configuration. Key components:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demoapp-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demoapp
  template:
    spec:
      containers:
      - name: demoapp
        image: kamleshbelote/demoapp:latest
        # Health checks and resource limits included
```

## 2. Deploy to Minikube

Apply the deployment manifest:

```bash
kubectl apply -f k8s-deployment.yaml
```

## 3. Verify Deployment

Check if the pod is running:

```bash
kubectl get deployments
kubectl get pods -l app=demoapp
kubectl describe deployment demoapp-deployment
```

## 4. Access the Application

Since there's no service file in this folder, you can access the app using port-forward:

```bash
kubectl port-forward deployment/demoapp-deployment 8080:8000
```

Then access: http://localhost:8080

## 5. Monitor the Deployment

```bash
# Watch deployment status
kubectl get deployments -w

# Check pod logs
kubectl logs -l app=demoapp

# Describe pods for troubleshooting
kubectl describe pods -l app=demoapp
```

## 6. Update the Deployment

Change the image or configuration:

```bash
# Edit the deployment directly
kubectl edit deployment demoapp-deployment

# Or update using kubectl set
kubectl set image deployment/demoapp-deployment demoapp=kamleshbelote/demoapp:v2
```

## 7. Scaling Operations

Scale the deployment to different replica counts:

```bash
# Scale up to 5 replicas
kubectl scale deployment demoapp-deployment --replicas=5

# Scale down to 2 replicas
kubectl scale deployment demoapp-deployment --replicas=2

# Check the scaling status
kubectl get deployments
kubectl get pods -l app=demoapp
```

## 8. Rolling Updates

Update the deployment with a new image version:

```bash
# Update the image (replace with your image)
kubectl set image deployment/demoapp-deployment demoapp=kamleshbelote/demoapp:v2

# Check rollout status
kubectl rollout status deployment/demoapp-deployment

# View rollout history
kubectl rollout history deployment/demoapp-deployment

# Rollback if needed
kubectl rollout undo deployment/demoapp-deployment
```

## 9. Cleaning Up

To remove the deployment:

```bash
kubectl delete -f k8s-deployment.yaml

# Or delete by name
kubectl delete deployment demoapp-deployment
```

## Common Commands Reference

```bash
# Get deployment status
kubectl get deployments
kubectl describe deployment demoapp-deployment

# Get pods
kubectl get pods -l app=demoapp
kubectl describe pod <pod-name>

# View logs
kubectl logs -l app=demoapp
kubectl logs -f deployment/demoapp-deployment

# Port forward for testing
kubectl port-forward deployment/demoapp-deployment 8080:8000
```

## Next Steps

- Learn about Services to expose deployments (see Day 3)
- Explore StatefulSets for stateful applications
- Practice with ConfigMaps and Secrets
- Study resource quotas and limits