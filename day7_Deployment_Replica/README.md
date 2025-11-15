# Day 7: Deployment, ReplicaSet, and ReplicationController

## Overview

This module covers the core Kubernetes controllers for managing pod replicas and deployments:
- **ReplicationController (RC)**: Legacy controller for maintaining pod replicas
- **ReplicaSet (RS)**: Modern replacement for ReplicationController with advanced selector support
- **Deployment**: High-level controller that manages ReplicaSets and provides declarative updates

## Key Concepts

### ReplicationController (Legacy)
- Ensures a specified number of pod replicas are running
- Uses equality-based selectors only
- **Not recommended for new deployments**
- Replaced by ReplicaSets

### ReplicaSet
- Next-generation ReplicationController
- Supports set-based selectors (In, NotIn, Exists)
- Usually managed by Deployments
- Provides better label matching capabilities

### Deployment
- **Recommended approach** for stateless applications
- Manages ReplicaSets automatically
- Provides rolling updates and rollbacks
- Declarative updates for pods and ReplicaSets
- Supports scaling, pausing, and resuming

## Files in This Directory

- `rc.yaml` - ReplicationController example (legacy)
- `rs.yaml` - ReplicaSet example
- `deployment.yaml` - Deployment example (recommended)
- `pod_creation.yaml` - Standalone pod example

## Common Commands

### ReplicaSet Operations

```bash
# Create ReplicaSet
kubectl apply -f rs.yaml

# Get ReplicaSets
kubectl get rs
kubectl get replicaset

# View ReplicaSet details
kubectl describe rs demoapp-rs

# Edit ReplicaSet (not recommended for replicas)
kubectl edit rs demoapp-rs

# Scale ReplicaSet
kubectl scale --replicas=10 rs/demoapp-rs
kubectl scale --replicas=5 rs/demoapp-rs

# Delete ReplicaSet
kubectl delete rs demoapp-rs

# Delete ReplicaSet but keep pods
kubectl delete rs demoapp-rs --cascade=orphan
```

### Deployment Operations

```bash
# Create Deployment
kubectl apply -f deployment.yaml

# Get Deployments
kubectl get deployments
kubectl get deploy

# View Deployment details
kubectl describe deployment demoapp-deployment

# Scale Deployment
kubectl scale --replicas=5 deployment/demoapp-deployment

# Update Deployment image
kubectl set image deployment/demoapp-deployment demoapp-container=nginx:1.19

# View Deployment rollout status
kubectl rollout status deployment/demoapp-deployment

# View Deployment history
kubectl rollout history deployment/demoapp-deployment

# Rollback to previous version
kubectl rollout undo deployment/demoapp-deployment

# Rollback to specific revision
kubectl rollout undo deployment/demoapp-deployment --to-revision=2

# Pause Deployment (prevent updates)
kubectl rollout pause deployment/demoapp-deployment

# Resume Deployment
kubectl rollout resume deployment/demoapp-deployment

# Edit Deployment
kubectl edit deployment demoapp-deployment

# Delete Deployment
kubectl delete deployment demoapp-deployment
```

### ReplicationController Operations

```bash
# Create ReplicationController
kubectl apply -f rc.yaml

# Get ReplicationControllers
kubectl get rc
kubectl get replicationcontroller

# Scale ReplicationController
kubectl scale --replicas=5 rc/demoapp-rc

# Delete ReplicationController
kubectl delete rc demoapp-rc
```

### Monitoring and Debugging

```bash
# Watch resources in real-time
kubectl get pods --watch
kubectl get rs --watch
kubectl get deploy --watch

# View pod distribution across nodes
kubectl get pods -o wide

# Get labels for all pods
kubectl get pods --show-labels

# Filter pods by label
kubectl get pods -l app=demoapp-rs
kubectl get pods -l env=dev

# View events
kubectl get events --sort-by=.metadata.creationTimestamp

# Get YAML output
kubectl get deployment demoapp-deployment -o yaml
kubectl get rs demoapp-rs -o yaml

# Get JSON output for specific field
kubectl get deployment demoapp-deployment -o jsonpath='{.spec.replicas}'
```

## Practical Examples

### Scaling Workflow

```bash
# Start with 3 replicas
kubectl apply -f deployment.yaml

# Scale up to 10 replicas
kubectl scale --replicas=10 deployment/demoapp-deployment

# Verify scaling
kubectl get pods -l app=demoapp-deployment
kubectl get deployment demoapp-deployment

# Scale down to 2 replicas
kubectl scale --replicas=2 deployment/demoapp-deployment
```

### Rolling Update Workflow

```bash
# Create deployment with nginx:1.19
kubectl apply -f deployment.yaml

# Update to nginx:1.20
kubectl set image deployment/demoapp-deployment demoapp-container=nginx:1.20

# Watch the rollout
kubectl rollout status deployment/demoapp-deployment

# Check rollout history
kubectl rollout history deployment/demoapp-deployment

# Rollback if needed
kubectl rollout undo deployment/demoapp-deployment
```

### Label Selection Examples

```bash
# ReplicaSet uses matchLabels
kubectl get rs demoapp-rs -o yaml | grep -A 5 selector

# Get pods matching specific labels
kubectl get pods -l env=dev
kubectl get pods -l 'env in (dev,prod)'
kubectl get pods -l type=frontend
```

## Key Differences

### ReplicationController vs ReplicaSet

| Feature | ReplicationController | ReplicaSet |
|---------|----------------------|------------|
| Selector Type | Equality-based only | Set-based and Equality-based |
| API Version | v1 | apps/v1 |
| Recommended | ❌ No (Legacy) | ⚠️ Only via Deployment |
| Examples | `env: dev` | `env in (dev, prod)` |

### ReplicaSet vs Deployment

| Feature | ReplicaSet | Deployment |
|---------|-----------|------------|
| Rolling Updates | ❌ Manual | ✅ Automatic |
| Rollback | ❌ Not supported | ✅ Built-in |
| Versioning | ❌ No | ✅ Yes |
| Recommended | ⚠️ Only via Deployment | ✅ Yes |
| Use Case | Direct pod management | Application deployment |

## Best Practices

1. **Use Deployments**: Always use Deployments instead of directly creating ReplicaSets
2. **Define Resource Limits**: Set CPU and memory limits for containers
3. **Use Labels**: Properly label resources for organization and selection
4. **Health Checks**: Add liveness and readiness probes
5. **Rolling Updates**: Configure update strategy for zero-downtime deployments
6. **History Limit**: Set `revisionHistoryLimit` to control history retention

## Troubleshooting

### Pods Not Starting
```bash
# Check ReplicaSet/Deployment status
kubectl describe rs <name>
kubectl describe deployment <name>

# Check pod details
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Scaling Issues
```bash
# Verify current replica count
kubectl get deployment <name> -o jsonpath='{.spec.replicas}'

# Check for resource constraints
kubectl describe nodes
kubectl top nodes
```

### Update Failures
```bash
# Check rollout status
kubectl rollout status deployment/<name>

# View rollout history
kubectl rollout history deployment/<name>

# Rollback if needed
kubectl rollout undo deployment/<name>
```

## CKA Exam Tips

1. Know how to quickly scale deployments
2. Understand the difference between RC, RS, and Deployments
3. Practice rollout and rollback commands
4. Be familiar with label selectors
5. Know how to troubleshoot failed deployments
6. Understand pod lifecycle and states
7. Practice editing resources with `kubectl edit`

## References

- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [ReplicaSets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
- [ReplicationController](https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/)
