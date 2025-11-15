# Day 14: Affinity

This document explains Kubernetes affinity and anti-affinity primitives, shows common attributes, and gives command examples to add/remove node labels and taints used with affinity rules.

## Affinity Types

- **`nodeAffinity`** — Schedule pods to nodes based on node labels (like nodeSelector but more powerful)
- **`podAffinity`** — Prefer or require pods to be scheduled on the same (or close) topology domain as other pods
- **`podAntiAffinity`** — Prefer or require pods to avoid running on the same topology domain as other pods

Each affinity type supports two modes:

- **`requiredDuringSchedulingIgnoredDuringExecution`** — Hard requirement. If not satisfiable, the pod stays `Pending`. (IgnoredDuringExecution means the rule is only enforced at scheduling time.)
- **`preferredDuringSchedulingIgnoredDuringExecution`** — Soft preference. Scheduler tries to satisfy higher-weight preferences but will still schedule if they can't be met.

---

## Common Attributes

### For Node Affinity

| Attribute | Description | Used In |
|-----------|-------------|---------|
| `nodeSelectorTerms` | Array of node selector requirements | `requiredDuringSchedulingIgnoredDuringExecution` |
| `preference` | Single node selector requirement | `preferredDuringSchedulingIgnoredDuringExecution` |
| `matchExpressions` | List of label selector requirements | Inside `nodeSelectorTerms` or `preference` |
| `weight` | Integer 1-100 indicating preference strength | `preferredDuringSchedulingIgnoredDuringExecution` |

### Match Expressions

Each `matchExpression` contains:

| Field | Description | Example |
|-------|-------------|---------|
| `key` | Node label key | `nodetype`, `disktype`, `region` |
| `operator` | Comparison operator | `In`, `NotIn`, `Exists`, `DoesNotExist`, `Gt`, `Lt` |
| `values` | Array of label values (for In/NotIn) | `["highmem", "highcpu"]` |

### Operators Explained

| Operator | Meaning | Example |
|----------|---------|---------|
| `In` | Label value must be in the list | `nodetype In [highmem, ssd]` |
| `NotIn` | Label value must NOT be in the list | `env NotIn [dev, test]` |
| `Exists` | Label key must exist (any value) | `gpu Exists` |
| `DoesNotExist` | Label key must NOT exist | `spot DoesNotExist` |
| `Gt` | Numeric label value greater than | `noderank Gt 5` |
| `Lt` | Numeric label value less than | `noderank Lt 10` |

### For Pod Affinity/Anti-Affinity

| Attribute | Description |
|-----------|-------------|
| `labelSelector` | Selector for matching pods |
| `topologyKey` | Domain for co-location/separation (e.g., `kubernetes.io/hostname`, `topology.kubernetes.io/zone`) |
| `namespaces` | List of namespaces to match pods from (default: same namespace) |

---

## Examples

### 1) Node Affinity (Required - Hard Rule)

Pod will be **Pending** if no node matches:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-a
spec:
  containers:
  - name: nginx
    image: nginx
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: nodetype
            operator: In
            values:
            - highmem
```

### 2) Node Affinity (Preferred - Soft Rule)

Scheduler prefers matching nodes but will schedule elsewhere if needed:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-ap
spec:
  containers:
  - name: nginx
    image: nginx
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 50
        preference:
          matchExpressions:
          - key: nodetype
            operator: In
            values:
            - ssd
            - nvme
```

### 3) Multiple Preferences with Different Weights

```yaml
affinity:
  nodeAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 80
      preference:
        matchExpressions:
        - key: disktype
          operator: In
          values:
          - ssd
    - weight: 20
      preference:
        matchExpressions:
        - key: region
          operator: In
          values:
          - us-west
```

### 4) Pod Anti-Affinity (Spread Pods)

Prevents multiple pods with `app=web` from running on the same node:

```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - web
      topologyKey: "kubernetes.io/hostname"
```

### 5) Pod Affinity (Co-locate Pods)

Schedule this pod on the same node as pods with `app=cache`:

```yaml
affinity:
  podAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - cache
      topologyKey: "kubernetes.io/hostname"
```

---

## Commands: Labels (Add / Remove)

### Add a Label to a Node

```bash
kubectl label nodes <node-name> <key>=<value>

# Examples:
kubectl label nodes minikube-m02 nodetype=highmem
kubectl label nodes minikube-m02 disktype=ssd region=us-west
```

### View Node Labels

```bash
# Show all labels
kubectl get nodes --show-labels

# Show specific labels as columns
kubectl get nodes -L nodetype,disktype,region

# Describe node (shows labels and more)
kubectl describe node minikube-m02
```

### Update/Overwrite Existing Label

```bash
kubectl label nodes <node-name> <key>=<new-value> --overwrite

# Example:
kubectl label nodes minikube-m02 disktype=nvme --overwrite
```

### Remove a Label

```bash
kubectl label nodes <node-name> <key>-

# Example:
kubectl label nodes minikube-m02 nodetype-
```

---

## Commands: Taints (Add / Remove)

### Add a Taint

```bash
kubectl taint nodes <node-name> <key>=<value>:<effect>

# Examples:
kubectl taint nodes minikube-m02 gpu=true:NoSchedule
kubectl taint nodes minikube-m03 storage=ssd:NoSchedule
kubectl taint nodes worker-1 maintenance=true:NoExecute
```

### View Node Taints

```bash
# Quick view
kubectl describe node <node-name> | grep Taints

# Detailed view
kubectl describe node <node-name> | sed -n '/Taints:/,/Unschedulable:/p'

# All nodes with taints
kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints
```

### Remove a Taint (Note the trailing `-`)

```bash
kubectl taint nodes <node-name> <key>=<value>:<effect>-

# Examples:
kubectl taint nodes minikube-m02 gpu=true:NoSchedule-
kubectl taint nodes worker-1 maintenance=true:NoExecute-
```

### Remove All Taints from a Node

```bash
kubectl patch node <node-name> -p '{"spec":{"taints":null}}' --type=merge

# Example:
kubectl patch node minikube-m02 -p '{"spec":{"taints":null}}' --type=merge
```

⚠️ **Warning:** Be careful removing control-plane taints!

---

## Decision Matrix: When to Use What?

| Scenario | Use | Why |
|----------|-----|-----|
| Pod must run on SSD nodes | `requiredDuringSchedulingIgnoredDuringExecution` | Hard requirement |
| Pod prefers GPU nodes but can run elsewhere | `preferredDuringSchedulingIgnoredDuringExecution` | Soft preference |
| Prevent normal pods from GPU nodes | Taints + Tolerations | Repel unwanted workloads |
| Spread replicas across nodes | `podAntiAffinity` with `hostname` | Avoid single point of failure |
| Co-locate cache with app | `podAffinity` with `hostname` | Reduce latency |
| Spread across zones | `podAntiAffinity` with `zone` topologyKey | High availability |

---

## Testing Tips

### Test Required Affinity (Pod Pending)

1. Create a pod with required affinity for a label that doesn't exist:
```bash
kubectl apply -f affinity.yaml
kubectl get pod nginx-a -o wide
# Should show: Pending
```

2. Check why it's pending:
```bash
kubectl describe pod nginx-a
# Look for: "0/3 nodes are available: 3 node(s) didn't match Pod's node affinity"
```

3. Add the required label:
```bash
kubectl label nodes minikube-m02 nodetype=highmem
```

4. Pod should now schedule:
```bash
kubectl get pod nginx-a -o wide
# Should show: Running on minikube-m02
```

### Test Preferred Affinity (Pod Schedules Anyway)

1. Create pod with preferred affinity (label doesn't exist):
```bash
kubectl apply -f affinity_preferred.yaml
kubectl get pod nginx-ap -o wide
# Should show: Running on any available node
```

2. Add the preferred label to a node:
```bash
kubectl label nodes minikube-m03 nodetype=highmem
```

3. Delete and recreate the pod:
```bash
kubectl delete pod nginx-ap
kubectl apply -f affinity_preferred.yaml
kubectl get pod nginx-ap -o wide
# Should show: Running on minikube-m03 (preferred node)
```

---

## Combining Affinity with Taints/Tolerations

For strict placement (only GPU workloads on GPU nodes):

```bash
# Step 1: Taint the GPU node to repel non-GPU pods
kubectl taint nodes gpu-node gpu=true:NoSchedule

# Step 2: Label the GPU node
kubectl label nodes gpu-node hardware=gpu

# Step 3: Pod with both toleration and affinity
apiVersion: v1
kind: Pod
metadata:
  name: ml-training
spec:
  containers:
  - name: tensorflow
    image: tensorflow/tensorflow:latest-gpu
  tolerations:
  - key: "gpu"
    operator: "Equal"
    value: "true"
    effect: "NoSchedule"
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: hardware
            operator: In
            values:
            - gpu
```

Result:
- Taint blocks all pods without toleration
- Affinity ensures GPU pods only go to GPU nodes
- Perfect isolation!

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Pod stays Pending | No node matches required affinity | Add label to a node or fix affinity rule |
| `unknown field "requiredDuringSchedulingIgnoreDuringExecution"` | Typo: missing 'd' in 'Ignored' | Use `IgnoredDuringExecution` (with 'd') |
| `nodeSelectorTerms` inside preference | Wrong structure for preferred affinity | Use `matchExpressions` directly in `preference` |
| Taint not removed | Wrong syntax | Ensure trailing `-` and exact key=value:effect match |

---

## Files in this Directory

- `affinity.yaml` - Pod with required node affinity
- `affinity_preferred.yaml` - Pod with preferred node affinity