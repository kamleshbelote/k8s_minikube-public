# Day 6: Kubernetes Pods

## Overview

Pods are the smallest deployable units in Kubernetes. A Pod represents a single instance of a running process in your cluster and can contain one or more containers that share storage, network resources, and a specification for how to run the containers.

### Key Pod Characteristics

- **Shared Context**: All containers in a pod share an IP address, port space, and can communicate using localhost
- **Storage**: Containers in a pod can share volumes
- **Lifecycle**: Pods have a defined lifecycle and are considered ephemeral (not designed to run forever)
- **Scheduling**: Pods are scheduled to run on nodes in the cluster based on resource availability and constraints

## Creating Pods

There are two ways to create Pods in Kubernetes:

### 1. Imperative Method

The imperative approach uses direct commands to create and manage resources. These commands are quick but don't provide version-controlled documentation of your resources.

**Basic Pod Management Commands:**
```bash
# Create a simple nginx pod
kubectl run nginx --image=nginx

# Create a pod with specific labels
kubectl run nginx-labeled --image=nginx --labels="app=web,env=prod"

# Create a pod and expose it through a service
kubectl run nginx-exposed --image=nginx --port=80 --expose

# Create a pod with resource limits
kubectl run resource-pod --image=nginx --requests=cpu=100m,memory=128Mi --limits=cpu=200m,memory=256Mi

# Create a pod with custom command
kubectl run command-pod --image=busybox --command -- sleep 3600

# Create a pod with environment variables
kubectl run env-pod --image=nginx --env="DB_HOST=localhost" --env="DB_PORT=5432"
```

**Viewing and Inspecting Pods:**
```bash
# List all pods
kubectl get pods

# List pods with more details
kubectl get pods -o wide

# Get pods in all namespaces
kubectl get pods --all-namespaces

# List pods with custom columns
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName

# Get detailed information about a pod
kubectl describe pod nginx

# Get pod logs
kubectl logs nginx

# Get logs from previous instance if pod was restarted
kubectl logs nginx --previous

# Get logs and follow them
kubectl logs -f nginx
```

**Managing Running Pods:**
```bash
# Delete a pod
kubectl delete pod nginx

# Delete a pod immediately (no graceful shutdown)
kubectl delete pod nginx --grace-period=0 --force

# Delete all pods
kubectl delete pods --all

# Edit a running pod (note: some fields cannot be changed)
kubectl edit pod nginx

# Execute a command in a running pod
kubectl exec -it nginx -- /bin/bash

# Copy files to/from a pod
kubectl cp nginx:/etc/nginx/nginx.conf ./local-nginx.conf
kubectl cp ./local-file.txt nginx:/tmp/
```

### 2. Declarative Method

The declarative approach uses YAML or JSON files to define the desired state of resources. This is the recommended approach for production environments as it provides version-controlled documentation of your resources.

**Example Pod YAML file:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
    environment: production
  annotations:
    description: "Web server pod"
    contact: "team@example.com"
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
    resources:
      limits:
        memory: "128Mi"
        cpu: "500m"
      requests:
        memory: "64Mi"
        cpu: "250m"
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 15
      timeoutSeconds: 2
      periodSeconds: 10
      failureThreshold: 3
```

**Working with YAML Files:**
```bash
# Generate a pod YAML template (useful starting point)
kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml

# Create/update a pod from YAML
kubectl apply -f pod.yaml

# Create a pod and delete any existing one with the same name
kubectl replace --force -f pod.yaml

# Delete a pod defined in YAML
kubectl delete -f pod.yaml

# Validate a YAML file without creating the resource
kubectl apply -f pod.yaml --dry-run=client --validate=true

# View differences between running pod and local file
kubectl diff -f pod.yaml

# Edit YAML definition for a running pod (some fields cannot be changed)
kubectl get pod nginx -o yaml > nginx-modified.yaml
# Edit the file, then:
kubectl apply -f nginx-modified.yaml
```

**Converting between Imperative and Declarative:**
```bash
# Export existing pod as YAML
kubectl get pod nginx -o yaml > exported-pod.yaml

# Export existing pod as JSON
kubectl get pod nginx -o json > exported-pod.json
```

## Pod Lifecycle

Pods follow a defined lifecycle:

1. **Pending**: The Pod has been accepted but is not yet running (scheduling, downloading images)
2. **Running**: The Pod has been scheduled and all containers are running
3. **Succeeded**: All containers have terminated successfully and will not restart
4. **Failed**: At least one container has terminated in failure
5. **Unknown**: The state of the Pod could not be determined

Check the pod status:
```bash
kubectl get pod nginx-pod -o wide
```

## Multi-Container Pods

Pods can contain multiple containers that work together:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
  - name: sidecar
    image: busybox
    command: ['sh', '-c', 'while true; do echo Logging at $(date); sleep 10; done']
```

Common multi-container patterns:
- **Sidecar**: Enhances the main container (log shipping, file sync)
- **Ambassador**: Proxy network connections (connection pooling)
- **Adapter**: Standardizes and normalizes output (monitoring adapters)

## Pod Configuration

### Environment Variables

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-pod
spec:
  containers:
  - name: env-container
    image: nginx
    env:
    - name: DB_HOST
      value: "database.example.com"
    - name: DB_PORT
      value: "5432"
```

### ConfigMaps and Secrets

```yaml
# Using ConfigMaps
apiVersion: v1
kind: Pod
metadata:
  name: configmap-pod
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config

# Using Secrets
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
spec:
  containers:
  - name: app
    image: nginx
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: db-password
```

## Pod Resource Management

### Resource Requests and Limits

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-pod
spec:
  containers:
  - name: app
    image: nginx
    resources:
      requests:  # Minimum resources needed
        memory: "64Mi"
        cpu: "250m"  # 250 millicores = 0.25 CPU
      limits:    # Maximum resources allowed
        memory: "128Mi"
        cpu: "500m"  # 500 millicores = 0.5 CPU
```

## Pod Scheduling

### Node Selector

Schedule pods to nodes with specific labels:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: node-selector-pod
spec:
  nodeSelector:
    disktype: ssd  # Will only run on nodes with label disktype=ssd
  containers:
  - name: app
    image: nginx
```

### Affinity and Anti-Affinity

More complex scheduling rules:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: affinity-pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: zone
            operator: In
            values:
            - us-east-1a
            - us-east-1b
  containers:
  - name: app
    image: nginx
```

## Pod Health Checks

Kubernetes provides three types of health checks (probes) to determine the health and availability of containers within pods.

### Liveness Probe

Checks if the container is running properly. If the probe fails, Kubernetes will restart the container:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-probe-pod
spec:
  containers:
  - name: app
    image: nginx
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
      initialDelaySeconds: 15  # Wait before first check
      periodSeconds: 10        # Check interval
      timeoutSeconds: 2        # Timeout for probe
      failureThreshold: 3      # Number of failures before restarting
      successThreshold: 1      # Number of successes to be considered successful
```

### Readiness Probe

Checks if the container is ready to receive traffic. If the probe fails, the pod's IP address will be removed from service endpoints:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: readiness-probe-pod
spec:
  containers:
  - name: app
    image: nginx
    readinessProbe:
      httpGet:
        path: /ready
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 10
```

### Startup Probe

Used for slow-starting containers. Disables liveness and readiness probes until it succeeds:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: startup-probe-pod
spec:
  containers:
  - name: app
    image: nginx
    startupProbe:
      httpGet:
        path: /started
        port: 80
      initialDelaySeconds: 10
      periodSeconds: 5
      failureThreshold: 30  # Allow up to 150s (30 * 5s) for startup
```

### Probe Types

Each probe can use one of these check mechanisms:

```yaml
# HTTP GET request
httpGet:
  path: /healthz
  port: 80
  httpHeaders:
  - name: Custom-Header
    value: Awesome

# TCP socket check
tcpSocket:
  port: 8080

# Command execution
exec:
  command:
  - cat
  - /tmp/healthy
```

## Common Pod Operations

```bash
# Get logs from a pod
kubectl logs nginx-pod

# Get logs from a specific container in a multi-container pod
kubectl logs multi-container-pod -c nginx

# Execute commands in a pod
kubectl exec -it nginx-pod -- /bin/bash

# Port forward to access a pod locally
kubectl port-forward nginx-pod 8080:80

# Copy files to/from a pod
kubectl cp nginx-pod:/etc/nginx/nginx.conf ./nginx.conf
kubectl cp ./config.json nginx-pod:/app/config.json
```

## Advanced Pod Features

### Init Containers

Containers that run and complete before the app containers start:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-container-pod
spec:
  initContainers:
  - name: init-service
    image: busybox
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done;']
  containers:
  - name: app
    image: nginx
```

### Pod Security Context

Configure security settings at the pod or container level:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: app
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
          - ALL
```

### Ephemeral Containers

Temporary containers for debugging:

```bash
# Add an ephemeral container to a running pod
kubectl debug -it my-pod --image=busybox --target=my-container
```

## Troubleshooting Pods

```bash
# Check pod status
kubectl get pod nginx -o wide

# View detailed state information
kubectl describe pod nginx

# Check pod logs
kubectl logs nginx

# Check events related to pods
kubectl get events --field-selector involvedObject.kind=Pod

# Check node conditions if pod is stuck in Pending state
kubectl describe node <node-name>

# Debug with an ephemeral container
kubectl debug -it nginx --image=busybox --target=nginx
```

## Best Practices

1. **Pod Design**:
   - Use labels for organization and selection
   - Keep pods stateless when possible
   - Use appropriate health checks
   - Group containers only when they need to share resources

2. **Resource Management**:
   - Always set resource requests and limits
   - Monitor resource usage to adjust as needed
   - Set appropriate QoS class through resource configuration

3. **Security**:
   - Use Pod Security Contexts to restrict privileges
   - Never run containers as root when possible
   - Use network policies to restrict pod communications
   - Use secrets for sensitive information

4. **Production Readiness**:
   - Always use health checks (probes)
   - Implement proper logging
   - Use namespaces to organize resources
   - Consider using higher-level controllers (Deployments, StatefulSets) instead of bare Pods

## Pod Commands Cheat Sheet

### Basic Pod Operations
```bash
kubectl get pods                          # List all pods in current namespace
kubectl get pods -n <namespace>           # List pods in specific namespace
kubectl describe pod <pod-name>           # Show detailed pod information
kubectl delete pod <pod-name>             # Delete a pod
kubectl logs <pod-name>                   # View pod logs
kubectl exec -it <pod-name> -- /bin/bash  # Get shell access to pod
```

### Creating and Updating Pods
```bash
kubectl run <name> --image=<image>        # Create a pod
kubectl apply -f pod.yaml                 # Create/update from file
kubectl replace -f pod.yaml               # Replace pod from file
kubectl edit pod <pod-name>               # Edit pod configuration
```

### Advanced Pod Commands
```bash
kubectl port-forward <pod-name> 8080:80   # Forward local port to pod port
kubectl attach <pod-name> -c <container>  # Attach to container in pod
kubectl cp <pod-name>:/path /local/path   # Copy files from pod to local
kubectl top pod <pod-name>                # Show pod resource usage
kubectl drain <node>                      # Safely evict all pods from node
```

## References

- [Kubernetes Pod Documentation](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Multi-Container Pods](https://kubernetes.io/docs/concepts/workloads/pods/#using-pods)
- [Pod Quality of Service](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/)
- [Debugging Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
```