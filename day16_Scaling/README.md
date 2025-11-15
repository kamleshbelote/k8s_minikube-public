Horizontal Pod Autoscaler (HPA) Demo

## Overview

This demo showcases Kubernetes Horizontal Pod Autoscaler functionality with ingress load balancing.

### Components
- **Deployment**: scaling-demo with CPU resource requests/limits
- **Service**: ClusterIP service for internal communication
- **Ingress**: External access via ingress-nginx controller
- **HPA**: Scales pods based on CPU utilization (target: 50%)

## Setup

1. Apply the deployment configuration:
```bash
kubectl apply -f deploy.yaml
```

2. Verify resources are created:
```bash
kubectl get deployment,svc,ingress,hpa
```

## Testing HPA Scaling

### Access the Application
The application is accessible via ingress through NodePort:

```bash
# Get the NodePort for the ingress controller
kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.spec.ports[0].nodePort}'

# Test access (replace PORT with the NodePort number from above)
curl -H "Host: scaling-demo.local" http://$(minikube ip):$(kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.spec.ports[0].nodePort}')
```

### Generate Load to Trigger Scaling
There are two ways to generate load for testing HPA:

1. Using a load generator pod (preferred method):
```bash
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://scaling-demo-service; done"
```

2. Using a busy loop (alternative method):
```bash
kubectl run load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://scaling-demo-service; done"
```

### Monitor Scaling

1. Watch HPA metrics and scaling decisions:
```bash
# Monitor HPA status with metrics
kubectl get hpa scaling-demo-hpa --watch
```

2. Monitor pod scaling:
```bash
# Watch pods being created/terminated
kubectl get pods -l app=scaling-demo --watch
```

3. Check resource utilization:
```bash
# Monitor CPU usage of all pods
kubectl top pods

# Get detailed HPA description
kubectl describe hpa scaling-demo-hpa
```

## Scaling Behavior

### Configuration
- **Min Replicas**: 1 pod
- **Max Replicas**: 10 pods
- **Target CPU**: 50% utilization threshold
- **Scale Out**: When average CPU > 50% for sustained period
- **Scale In**: When average CPU < 50% for sustained period

### Scaling Algorithm
1. Desired replicas = ceil(current_replicas * (current_cpu / target_cpu))
2. Example: If current CPU is 75% and target is 50%:
   - 75/50 = 1.5
   - ceil(1 * 1.5) = 2 replicas

## Cleanup

1. Remove load generators:
```bash
kubectl delete pod load-generator
```

2. Remove demo resources:
```bash
kubectl delete -f deploy.yaml
```

## Key Concepts

### HPA (Horizontal Pod Autoscaler)
- Automatically scales number of pods
- Based on resource metrics (CPU/Memory)
- Uses metrics-server for data collection
- Follows a scale-out/scale-in algorithm

### Resource Management
- **Requests**: Minimum guaranteed resources
- **Limits**: Maximum resource cap
- Critical for proper HPA functioning
- Metrics based on request values

### Ingress Configuration
- Load balancing across pods
- NodePort access in minikube
- Host-based routing
- Integration with HPA for scaling

### Prerequisites
- metrics-server addon enabled
- ingress-nginx controller running
- CPU requests defined in pods
- Working ingress configuration

