# Day 5: Multi-Node Kubernetes Cluster with Specialized Node Types

## Overview

This section covers how to set up a multi-node Kubernetes cluster using Minikube with specialized node types. This configuration simulates a real-world production environment with dedicated nodes for different workloads: frontend applications, background worker processes, and database services.

## Objectives

- Set up a multi-node cluster with Minikube (3 nodes)
- Configure specialized node types using labels
- Deploy workloads to specific node types
- Understand node affinity and workload isolation
- Practice resource allocation across different node types

## Prerequisites

- Minikube installed (see [Minikube Installation Guide](../minikube-ubuntu-installation.md))
- kubectl installed and configured
- Sufficient system resources for a 3-node cluster:
  - Minimum 6GB RAM total (2GB per node)
  - At least 6 CPU cores total (2 per node)
  - At least 20GB free disk space

## Node Types Architecture

Our cluster will consist of three specialized node types:

1. **Frontend Node** (control-plane): Hosts customer-facing applications with moderate resource requirements
2. **Worker Node**: Hosts background processing workloads
3. **Database Node**: Hosts data storage services with higher resource allocations

## Setup Instructions

### 1. Start Minikube with 3 Nodes

To start a multi-node Minikube cluster with our specialized configuration, use the following command:

```bash
minikube start --nodes 3 --kubernetes-version=v1.28.0 --driver=docker --memory=2048m --cpus=2
```

This command:
- Creates a cluster with 3 nodes (1 control-plane + 2 workers)
- Uses Kubernetes version 1.28.0
- Uses Docker as the driver
- Allocates 2GB RAM and 2 CPU cores per node

**Note:** For convenience, use the `setup_multinode.sh` script included in this directory.

### 2. Verify Cluster Status

Check that all nodes are running properly:

```bash
kubectl get nodes
```

Expected output:
```
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   2m30s   v1.28.0
minikube-m02   Ready    <none>          96s     v1.28.0
minikube-m03   Ready    <none>          96s     v1.28.0
```

### 3. Configure Node Labels for Specialization

Add specific labels to each node to designate its specialized role:

```bash
kubectl label node minikube node-type=frontend
kubectl label node minikube-m02 node-type=worker
kubectl label node minikube-m03 node-type=db
```

### 4. Verify Node Labels

Confirm that the labels are properly applied:

```bash
kubectl get nodes --show-labels | grep node-type
```

## Deploying to Specialized Nodes

When you're ready to create your own applications, you can deploy them to specific nodes using nodeSelector.

### 1. Example Deployment with NodeSelector

Here's an example of how to create a deployment that targets a specific node:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend-app
  template:
    metadata:
      labels:
        app: frontend-app
    spec:
      nodeSelector:
        node-type: frontend    # This will place pods only on nodes with this label
      containers:
      - name: frontend-app
        image: nginx:latest
```

Save a file like this and apply it:

```bash
kubectl apply -f your-deployment.yaml
```

### 2. Verify Workload Distribution

After creating deployments, check that pods are deployed on their designated nodes:

```bash
kubectl get pods -o wide
```

### 5. Understanding the Deployment Files

### Common Deployment Patterns for Different Node Types

When designing your deployments for specialized nodes, consider these patterns:

#### 1. Frontend Applications
- Place customer-facing applications on nodes with good network connectivity
- Consider using higher replica counts for high availability
- Typically use lighter resource requirements but may need to scale horizontally
- Example resource settings:
  ```yaml
  resources:
    requests:
      memory: "128Mi"
      cpu: "200m"
    limits:
      memory: "256Mi"
      cpu: "500m"
  ```

#### 2. Worker Applications
- Background processing tasks on dedicated nodes
- Can use batch processing or queue-based workloads
- Often need fewer resources per pod but may need many pods
- Example resource settings:
  ```yaml
  resources:
    requests:
      memory: "64Mi"
      cpu: "100m"
    limits:
      memory: "128Mi"
      cpu: "200m"
  ```

#### 3. Database Applications
- Stateful applications with persistence requirements
- Usually need dedicated nodes with higher resources
- Often use StatefulSets instead of Deployments
- Consider using persistent volumes
- Example resource settings:
  ```yaml
  resources:
    requests:
      memory: "256Mi"
      cpu: "500m"
    limits:
      memory: "512Mi"
      cpu: "1000m"
  ```

## Advanced Node Management

### Using Taints for Enhanced Isolation

For stricter workload isolation, consider adding taints:

```bash
# Taint the DB node to only accept database workloads
kubectl taint node minikube-m03 workload=database:NoSchedule
```

Add corresponding tolerations to your database deployment:

```yaml
tolerations:
- key: "workload"
  operator: "Equal"
  value: "database"
  effect: "NoSchedule"
```

## Cleanup

To delete the multi-node cluster:

```bash
minikube delete
```

## Troubleshooting

1. **Node resource constraints**: Adjust resource requests/limits in deployment files
2. **Pod scheduling issues**: Check node labels and selectors match
3. **Database performance issues**: Consider persistent volumes for database storage

## Benefits of Specialized Node Types

1. **Resource Optimization**: Match workloads with appropriate hardware
2. **Improved Security**: Isolate sensitive database workloads
3. **Better Performance**: Reduce resource contention between workload types
4. **Cost Efficiency**: Allocate resources according to specific needs
5. **Easier Maintenance**: Schedule maintenance on specific node types without affecting others

## References

- [Minikube Multi-Node Documentation](https://minikube.sigs.k8s.io/docs/tutorials/multi_node/)
- [Kubernetes: Node Selectors](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
- [Kubernetes: Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
- [Kubernetes: Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Kubernetes: Node Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity)