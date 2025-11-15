# Day 13: Taints, Tolerations & Node Selectors

## Taints and Tolerations

### Taint
- **Configured on:** Node
- **Purpose:** Prevent pods from scheduling on nodes unless they tolerate the taint
- **Syntax:**
  ```bash
  kubectl taint nodes <node-name> <key>=<value>:<effect>
  ```

### Toleration
- **Configured on:** Pod (in pod spec)
- **Purpose:** Allow pods to schedule on tainted nodes
- **Effects:**
  - `NoSchedule`: Prevents new pods without toleration from scheduling (existing pods remain)
  - `NoExecute`: Evicts existing pods AND prevents new pods without toleration
  - `PreferNoSchedule`: Soft preference - scheduler tries to avoid but no guarantee

### Taint Effects Comparison

| Effect | New Pods | Existing Pods | Use Case |
|--------|----------|---------------|----------|
| **NoSchedule** | ❌ Blocked | ✅ Remain | Standard node isolation |
| **NoExecute** | ❌ Blocked | ❌ Evicted | Node maintenance, urgent isolation |
| **PreferNoSchedule** | ⚠️ Avoided (best effort) | ✅ Remain | Soft preferences |

---

## Commands

### Taints

**Add a taint:**
```bash
kubectl taint nodes <node-name> <key>=<value>:<effect>

# Examples:
kubectl taint nodes minikube-m02 gpu=true:NoSchedule
kubectl taint nodes minikube-m03 storage=ssd:NoSchedule
kubectl taint nodes worker-1 maintenance=true:NoExecute
```

**View taints:**
```bash
kubectl describe node <node-name> | grep Taints
```

**Remove a taint:**
```bash
kubectl taint nodes <node-name> <key>=<value>:<effect>-

# Example:
kubectl taint nodes minikube-m02 gpu=true:NoSchedule-
```

### Tolerations (in Pod YAML)

**Basic toleration:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  containers:
  - name: nginx
    image: nginx
  tolerations:
  - key: "gpu"
    operator: "Equal"
    value: "true"
    effect: "NoSchedule"
```

**Tolerate all taints with specific key:**
```yaml
tolerations:
- key: "gpu"
  operator: "Exists"
  effect: "NoSchedule"
```

**Tolerate all taints (use with caution):**
```yaml
tolerations:
- operator: "Exists"
```

**Toleration with time limit (NoExecute only):**
```yaml
tolerations:
- key: "maintenance"
  operator: "Equal"
  value: "true"
  effect: "NoExecute"
  tolerationSeconds: 3600  # Pod will be evicted after 1 hour
```

---

## Node Selectors & Labels

### Labels

**Add label to node:**
```bash
kubectl label nodes <node-name> <key>=<value>

# Examples:
kubectl label nodes minikube-m02 disktype=ssd
kubectl label nodes minikube-m02 gpu=true region=us-west
```

**View labels:**
```bash
kubectl get nodes --show-labels
kubectl get nodes -L disktype,gpu,region
```

**Update label:**
```bash
kubectl label nodes <node-name> <key>=<value> --overwrite
```

**Remove label:**
```bash
kubectl label nodes <node-name> <key>-
```

### NodeSelector (in Pod YAML)

**Schedule pod on node with specific label:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-ssd
spec:
  containers:
  - name: nginx
    image: nginx
  nodeSelector:
    disktype: ssd
```

---

## Difference between Taint/Toleration and NodeSelector

| Feature | Taint/Toleration | NodeSelector |
|---------|------------------|--------------|
| **Direction** | Node **repels** pods (unless tolerated) | Pod **selects** node |
| **Purpose** | Prevent unwanted pods | Schedule pods on specific nodes |
| **Configured on** | Taint on node, Toleration on pod | Label on node, NodeSelector on pod |
| **Flexibility** | More control (NoExecute can evict) | Simple label matching only |
| **Use Case** | Isolation, dedicated nodes, maintenance | Simple node selection |
| **Default behavior** | Pods blocked unless tolerated | Pods can go anywhere unless nodeSelector set |

### Analogy for Better Understanding

Think of it like a **nightclub**:

- **Taints/Tolerations = Bouncer at the door** 🚫
  - Node says: "I don't want random pods, only special ones!"
  - Bouncer (taint) blocks everyone EXCEPT those with VIP pass (toleration)
  - **Push away** unwanted pods
  
- **NodeSelector = Guest choosing venue** 🎯
  - Pod says: "I only want to run on nodes with SSD!"
  - Pod actively **seeks out** matching nodes
  - **Pull toward** desired nodes

### Visual Comparison

```
TAINT/TOLERATION (Defense - Node protects itself)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Node (GPU)                        Pods
  ╔═══════════╗                       
  ║  gpu=true ║  ← Taint          ❌ Regular Pod → BLOCKED
  ║ :NoSchedule║                   ❌ DB Pod → BLOCKED  
  ╚═══════════╝                     ✅ ML Pod (with toleration) → ALLOWED
       ↑
   Protects node from unwanted pods


NODE SELECTOR (Offense - Pod chooses node)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Node (SSD)        Node (HDD)
 ╔══════════╗      ╔══════════╗
 ║disktype: ║      ║disktype: ║
 ║   ssd    ║      ║   hdd    ║
 ╚══════════╝      ╚══════════╝
      ↑                 ↓
      └─────✅──────────┘
            │
      Pod with nodeSelector:
        disktype: ssd
      (Pod actively seeks SSD node)
```

### Real-World Examples

#### Example 1: Only Taints (Keep pods OUT)
```bash
# Scenario: Node under maintenance - don't schedule new pods
kubectl taint nodes worker-1 maintenance=true:NoSchedule

Result: 
- New pods → blocked from worker-1
- Existing pods → remain (NoSchedule doesn't evict)
- Pod doesn't need to know anything
```

#### Example 2: Only NodeSelector (Pull pods IN)
```bash
# Scenario: Database needs SSD storage
kubectl label nodes node-1 disktype=ssd

# Pod YAML:
nodeSelector:
  disktype: ssd

Result:
- DB pod → only schedules on nodes with disktype=ssd
- Other nodes → can still accept other pods
- Node doesn't block anything
```

#### Example 3: BOTH (Strict control)
```bash
# Scenario: Expensive GPU node - ONLY for ML workloads

# Step 1: Taint to repel non-ML pods
kubectl taint nodes gpu-node gpu=true:NoSchedule

# Step 2: Label for ML pods to find it
kubectl label nodes gpu-node hardware=gpu

# ML Pod YAML:
tolerations:
- key: gpu
  value: "true"
  effect: NoSchedule
nodeSelector:
  hardware: gpu

Result:
- Taint blocks all pods without toleration
- NodeSelector ensures ML pods go to GPU node
- Perfect isolation!
```

### Decision Tree: Which to Use?

```
Do you want to PREVENT pods from scheduling on a node?
│
├─ YES → Use TAINTS
│   │
│   └─ Do existing pods need to be evicted immediately?
│       ├─ YES → NoExecute
│       └─ NO  → NoSchedule
│
└─ NO → Do you want pods to PREFER specific nodes?
    │
    ├─ MUST run on specific nodes → NodeSelector
    ├─ PREFER but not required → Use Node Affinity (advanced)
    └─ STRICT (only certain workloads on certain nodes) → BOTH Taints + NodeSelector
```

### Key Differences Summary

| Aspect | Taint/Toleration | NodeSelector |
|--------|------------------|--------------|
| **Who decides?** | Node (defensive) | Pod (offensive) |
| **Mental model** | "Keep OUT unless allowed" | "Go HERE if available" |
| **What if no match?** | Pod stays Pending (no toleration) | Pod stays Pending (no matching label) |
| **Can evict pods?** | ✅ Yes (NoExecute) | ❌ No |
| **Complexity** | More complex (3 effects) | Simple (label matching) |
| **Best for** | Isolation, exclusion | Selection, attraction |

### When to use what?

- **Taints/Tolerations:** When you want to **keep pods away** from certain nodes (e.g., GPU nodes, maintenance mode)
  - ✅ Node maintenance
  - ✅ Dedicated hardware (GPU, high-memory)
  - ✅ Security isolation
  - ✅ Emergency evictions

- **NodeSelector:** When you want to **attract specific pods** to certain nodes (e.g., run database on SSD nodes)
  - ✅ Hardware requirements (SSD, CPU type)
  - ✅ Geographic placement (region=us-west)
  - ✅ Environment separation (env=production)
  - ✅ Cost optimization (instance-type=spot)

- **Both together:** For strict placement (e.g., only GPU workloads on GPU nodes)
  - ✅ Dedicated + Exclusive workloads
  - ✅ Compliance requirements
  - ✅ Resource isolation
  - ✅ Multi-tenant clusters

---

## Example Scenarios

### Scenario 1: Dedicated GPU Node
```bash
# Taint the GPU node to repel non-GPU workloads
kubectl taint nodes gpu-node gpu=true:NoSchedule

# Label the GPU node
kubectl label nodes gpu-node hardware=gpu

# Pod YAML for GPU workload
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
  nodeSelector:
    hardware: gpu
```

### Scenario 2: Node Maintenance
```bash
# Mark node for maintenance (evicts non-tolerant pods)
kubectl taint nodes worker-1 maintenance=true:NoExecute

# Critical pods that should remain during maintenance
tolerations:
- key: "maintenance"
  operator: "Equal"
  value: "true"
  effect: "NoExecute"
  tolerationSeconds: 7200  # Stay for 2 hours max
```

### Scenario 3: Control Plane Protection
```bash
# Control plane nodes typically have this taint by default
kubectl describe node minikube | grep Taints
# Taints: node-role.kubernetes.io/control-plane:NoSchedule

# Only pods with this toleration can schedule on control-plane
tolerations:
- key: "node-role.kubernetes.io/control-plane"
  operator: "Exists"
  effect: "NoSchedule"
```

---

## Testing Your Setup

**1. Test that taint blocks pods:**
```bash
# Create test pod without toleration
kubectl run test-pod --image=nginx

# Check where it scheduled (should avoid tainted nodes)
kubectl get pod test-pod -o wide
```

**2. Test that toleration allows scheduling:**
```bash
# Apply pod with toleration
kubectl apply -f gpu-pod.yaml

# Verify it can run on tainted node
kubectl get pod gpu-pod -o wide
```

**3. View current cluster taints:**
```bash
kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints
```

---

## Files in this Directory

- `gpu-pod.yaml` - Pod with GPU toleration
- `storage-pod.yaml` - Pod with storage toleration  
- `nginx.yaml` - Basic pod without tolerations
- `newnginx.yaml` - Pod with specific node requirements