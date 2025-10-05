# Minikube Installation Guide for Ubuntu

This guide provides step-by-step instructions for installing Minikube on Ubuntu Linux systems.

## Prerequisites

Before installing Minikube, ensure your system meets the following requirements:

- Ubuntu 18.04 or later
- 2 CPUs or more
- 2GB of free memory
- 20GB of free disk space
- Internet connection
- Container or virtual machine manager (Docker, VirtualBox, KVM, etc.)

## Installation Methods

### Method 1: Install via Binary Download (Recommended)

1. **Download the latest Minikube binary:**
   ```bash
   curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
   ```

2. **Install Minikube:**
   ```bash
   sudo install minikube-linux-amd64 /usr/local/bin/minikube
   ```

3. **Verify the installation:**
   ```bash
   minikube version
   ```

### Method 2: Install via Package Manager

1. **Update package index:**
   ```bash
   sudo apt update
   ```

2. **Install required packages:**
   ```bash
   sudo apt install -y curl wget apt-transport-https
   ```

3. **Download and install Minikube:**
   ```bash
   wget -q --show-progress --https-only --timestamping \
     https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
   sudo dpkg -i minikube_latest_amd64.deb
   ```

### Method 3: Install via Snap

```bash
sudo snap install minikube
```

## Install Container Runtime

Minikube requires a container runtime. Here are the most common options:

### Option A: Docker (Recommended)

1. **Install Docker:**
   ```bash
   sudo apt update
   sudo apt install -y docker.io
   ```

2. **Start and enable Docker:**
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Add your user to the docker group:**
   ```bash
   sudo usermod -aG docker $USER
   ```

4. **Log out and log back in** for the group changes to take effect.

### Option B: VirtualBox

1. **Install VirtualBox:**
   ```bash
   sudo apt update
   sudo apt install -y virtualbox virtualbox-ext-pack
   ```

## Install kubectl (Optional but Recommended)

kubectl is the Kubernetes command-line tool that allows you to run commands against Kubernetes clusters.

1. **Download kubectl:**
   ```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   ```

2. **Install kubectl:**
   ```bash
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

3. **Verify kubectl installation:**
   ```bash
   kubectl version --client
   ```

## Starting Minikube

1. **Start Minikube with Docker driver:**
   ```bash
   minikube start --driver=docker
   ```

2. **Start Minikube with VirtualBox driver:**
   ```bash
   minikube start --driver=virtualbox
   ```

3. **Set default driver (optional):**
   ```bash
   minikube config set driver docker
   ```

## Verification

1. **Check Minikube status:**
   ```bash
   minikube status
   ```

2. **Check cluster info:**
   ```bash
   kubectl cluster-info
   ```

3. **List nodes:**
   ```bash
   kubectl get nodes
   ```

## Common Commands

### Minikube Management
- `minikube start` - Start the cluster
- `minikube stop` - Stop the cluster
- `minikube delete` - Delete the cluster
- `minikube pause` - Pause the cluster
- `minikube unpause` - Unpause the cluster
- `minikube status` - Check cluster status

### Access Applications
- `minikube dashboard` - Open Kubernetes dashboard
- `minikube service <service-name>` - Access a service
- `minikube tunnel` - Create tunnel for LoadBalancer services

### Resource Management
- `minikube addons list` - List available addons
- `minikube addons enable <addon-name>` - Enable an addon
- `minikube addons disable <addon-name>` - Disable an addon

## Troubleshooting

### Common Issues

1. **Permission denied errors with Docker:**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Insufficient resources:**
   - Increase CPU/Memory allocation:
   ```bash
   minikube start --cpus=4 --memory=4096
   ```

3. **VirtualBox issues:**
   - Enable virtualization in BIOS/UEFI
   - Check if VT-x/AMD-V is enabled:
   ```bash
   egrep -c '(vmx|svm)' /proc/cpuinfo
   ```

4. **Network issues:**
   ```bash
   minikube start --driver=docker --force-systemd=false
   ```

### Logs and Debugging
- `minikube logs` - View Minikube logs
- `minikube ssh` - SSH into the Minikube VM
- `kubectl describe nodes` - Get detailed node information

## Uninstalling Minikube

1. **Stop and delete the cluster:**
   ```bash
   minikube stop
   minikube delete --all
   ```

2. **Remove Minikube binary:**
   ```bash
   sudo rm /usr/local/bin/minikube
   ```

3. **Remove configuration files:**
   ```bash
   rm -rf ~/.minikube
   ```

## Additional Resources

- [Official Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

## Version Information

This guide was last updated for:
- Minikube: Latest stable version
- Ubuntu: 18.04 LTS and later
- Kubernetes: Compatible versions

---

**Note:** Always refer to the official documentation for the most up-to-date installation instructions and troubleshooting tips.