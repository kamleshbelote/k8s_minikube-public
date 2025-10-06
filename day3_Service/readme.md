# Day 3 - Kubernetes Services & Autoscaling

This directory contains materials for Day 3: understanding and working with Kubernetes Services and Horizontal Pod Autoscaling.

## Objectives

- Understand different types of Kubernetes Services
- Learn how to expose applications using Services
- Practice with NodePort, ClusterIP, and LoadBalancer services
- Configure service discovery and networking
- Implement Horizontal Pod Autoscaling (HPA)

## Prerequisites

- Minikube running with metrics-server enabled
- Demo app deployment from Day 2 (or any app with label `app: demoapp`)
- For HPA: `kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`

## Files

- `readme.md` - This file
- `k8s-service.yaml` - Basic NodePort service manifest for the demo app
- `k8s-hap.yaml` - Horizontal Pod Autoscaler configuration

## Exercises

1. Create and deploy a basic Service manifest
2. Test service connectivity and port forwarding
3. Explore service endpoints and DNS resolution
4. Practice with different service types
5. Deploy and test Horizontal Pod Autoscaler

## Service Types Overview

### NodePort
Exposes the service on each node's IP at a static port. External traffic can access the service via `<NodeIP>:<NodePort>`.

### ClusterIP (Default)
Exposes the service on a cluster-internal IP. The service is only reachable from within the cluster.

### LoadBalancer
Exposes the service externally using a cloud provider's load balancer.

## 1. Review the Service Manifest

The `k8s-service.yaml` file contains a NodePort service configuration:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: demoapp-service
spec:
  selector:
    app: demoapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: NodePort
```

## 2. Deploy the Service

Apply the service manifest:

```bash
kubectl apply -f k8s-service.yaml
```

## 3. Verify the Service

Get service details:

```bash
kubectl get services
kubectl describe service demoapp-service
```

## 4. Access the Service

Access the service (if using Minikube):

```bash
minikube service demoapp-service --url
```

Or use port-forward:

```bash
kubectl port-forward service/demoapp-service 8080:80
```

## 5. Test the Endpoints

```bash
# Get service URL
SERVICE_URL=$(minikube service demoapp-service --url)

# Test the endpoints
curl $SERVICE_URL/
curl $SERVICE_URL/healthz
curl $SERVICE_URL/readiness
```

## 6. Deploy Horizontal Pod Autoscaler

First, make sure metrics-server is running:

```bash
# Check if metrics-server is running
kubectl get pods -n kube-system | grep metrics-server

# If not installed, install it
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Deploy the HPA:

```bash
kubectl apply -f k8s-hap.yaml
```

## 7. Verify HPA

Check HPA status:

```bash
kubectl get hpa
kubectl describe hpa demoapp-hpa
```

## 8. Test Autoscaling

Generate load to trigger scaling:

```bash
# In one terminal, watch the HPA and pods
kubectl get hpa -w

# In another terminal, generate load
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh

# Inside the busybox container, run:
while true; do wget -q -O- http://demoapp-service/; done
```

## 9. Explore Service Discovery

```bash
# Get service endpoints
kubectl get endpoints demoapp-service

# DNS resolution (from inside a pod)
kubectl run debug --image=busybox -it --rm -- nslookup demoapp-service
```

## 10. Cleaning Up

Delete the resources:

```bash
kubectl delete -f k8s-hap.yaml
kubectl delete -f k8s-service.yaml

# Or delete by name
kubectl delete hpa demoapp-hpa
kubectl delete service demoapp-service
```

## Common Commands Reference

```bash
# Services
kubectl get services
kubectl describe service demoapp-service
kubectl get endpoints

# HPA
kubectl get hpa
kubectl describe hpa demoapp-hpa
kubectl top pods

# Port forward
kubectl port-forward service/demoapp-service 8080:80

# Access via minikube
minikube service demoapp-service --url
```

## Troubleshooting

### HPA Issues
- Make sure metrics-server is running: `kubectl get pods -n kube-system | grep metrics-server`
- Check if resource requests are set in deployment: `kubectl describe deployment demoapp-deployment`
- Verify metrics are available: `kubectl top pods`

### Service Issues
- Check service selector matches pod labels: `kubectl get pods --show-labels`
- Verify endpoints exist: `kubectl get endpoints demoapp-service`
- Test DNS resolution from inside cluster

## Next Steps

- Explore Ingress controllers for more advanced routing
- Learn about service mesh technologies (Istio, Linkerd)
- Practice with headless services
- Study network policies and security
- Implement vertical pod autoscaling (VPA)