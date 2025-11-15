# Multi-Container Pods in Kubernetes

Multi-container pods allow you to run multiple containers within a single pod that share resources and can communicate directly with each other. This pattern is useful for tightly coupled application components.

## Types of Multi-Container Patterns

1. **Init Containers**
   - Run before app containers start
   - Must complete successfully before app containers run
   - Run sequentially in order
   - Used for setup, registration, or prerequisite tasks

2. **Sidecar Containers**
   - Run alongside the main container
   - Enhance or support the main container
   - Examples: logging agents, monitoring, data sync

3. **Ambassador Containers**
   - Proxy network connections to/from main container
   - Handle network routing or connection management
   - Example: routing traffic to different database shards

4. **Adapter Containers**
   - Standardize and normalize main container's output
   - Transform data to match required format
   - Example: converting log formats

## Demo Implementation

Our example demonstrates an Init Container pattern:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
  labels:
    app: multi-container-app
    env: dev
spec:
  # Main Application Container
  containers:
  - name: demoapp-container
    image: busybox:latest
    env:
    - name: DEMO_ENV
      value: dev
    command: ['sh', '-c', 'echo "Running the main application..."; sleep 10; echo "Main application complete."']
    resources:
      requests:
        memory: "64Mi"
        cpu: "100m"
      limits:
        memory: "128Mi"
        cpu: "250m"

  # Init Container - Runs before main container
  initContainers:
  - name: init-demoapp-container
    image: busybox:latest
    command: ['sh', '-c', 'echo "Initializing the application..."; sleep 5; echo "Initialization complete."']
    env:
    - name: INIT_ENV
      value: init-dev
    resources:
      requests:
        memory: "32Mi"
        cpu: "50m"
      limits:
        memory: "64Mi"
        cpu: "100m"
```

## Key Features

1. **Resource Sharing**:
   - Shared network namespace (localhost)
   - Shared storage volumes
   - Shared IPC namespace
   - Same pod lifecycle

2. **Communication**:
   - Inter-container communication via localhost
   - Shared volumes for file-based communication
   - Environment variables

3. **Resource Management**:
   - Individual container resource limits
   - Combined pod resource allocation
   - Separate logging and monitoring

## Common Commands

1. **Pod Management**:
```bash
# Create pod
kubectl apply -f pod.yaml

# Check pod status
kubectl get pod multi-container-pod

# Delete pod
kubectl delete pod multi-container-pod
```

2. **Container Logs**:
```bash
# View init container logs
kubectl logs multi-container-pod -c init-demoapp-container

# View main container logs
kubectl logs multi-container-pod -c demoapp-container

# Follow logs in real-time
kubectl logs -f multi-container-pod -c demoapp-container
```

3. **Container Access**:
```bash
# Execute command in main container
kubectl exec -it multi-container-pod -c demoapp-container -- /bin/sh

# Check container status
kubectl describe pod multi-container-pod
```

## Best Practices

1. **Container Design**:
   - Keep containers focused on single responsibility
   - Use appropriate container patterns
   - Share resources efficiently

2. **Resource Management**:
   - Set appropriate resource limits
   - Consider pod-level resource requirements
   - Monitor resource usage

3. **Logging and Monitoring**:
   - Implement proper logging strategy
   - Monitor all containers
   - Use labels for better organization

4. **Security**:
   - Follow principle of least privilege
   - Secure inter-container communication
   - Use security contexts appropriately

## Common Use Cases

1. **Application Setup**:
   - Database initialization
   - Configuration management
   - Service registration

2. **Monitoring and Logging**:
   - Log collection
   - Metric gathering
   - Application monitoring

3. **Proxy and Adaptation**:
   - Service mesh sidecars
   - Protocol adaptation
   - Data transformation

## Troubleshooting

1. **Check Pod Status**:
```bash
kubectl describe pod multi-container-pod
```

2. **View Container Logs**:
```bash
kubectl logs multi-container-pod -c [container-name]
```

3. **Common Issues**:
   - Init container failures
   - Resource constraints
   - Container startup order
   - Volume mounting issues

## Cleanup

To remove the demo resources:
```bash
kubectl delete pod multi-container-pod
```
