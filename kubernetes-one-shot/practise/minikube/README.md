# Minikube Cluster Guide

This folder documents a local Kubernetes cluster setup using `minikube`.

## Start Minikube After Installation

If you want a simple single-node local cluster:

```bash
minikube start
```

If you want a multi-node cluster similar to the `kind` example:

```bash
minikube start -p practise --nodes 4 --kubernetes-version=v1.31.2
```

Notes:

- `-p practise` creates a profile named `practise`
- `--nodes 4` creates 1 control-plane node and 3 worker nodes
- this is similar to the `kind` setup, but it is not driven by the same YAML file

## Verify The Cluster

For the default profile:

```bash
kubectl config use-context minikube
kubectl get nodes
kubectl cluster-info
```

For the `practise` profile:

```bash
minikube profile practise
kubectl config current-context
kubectl get nodes
```

You can also list all profiles:

```bash
minikube profile list
```

If both `minikube` and `kind` clusters are running, switch the active `kubectl` context with:

```bash
kubectl config use-context minikube
kubectl config use-context kind-practise
```

The selected context becomes the default cluster context for `kubectl` until you switch again.

Check which cluster is currently the default:

```bash
kubectl config current-context
```

## Useful Minikube Commands

```bash
minikube status
minikube ip
minikube dashboard
minikube addons list
minikube addons enable ingress
minikube service list
```

## Useful kubectl Commands

Once the cluster is running:

```bash
kubectl get nodes
kubectl get pods -A
kubectl get deployments -A
kubectl get svc -A
kubectl describe node minikube
kubectl get events --sort-by=.metadata.creationTimestamp
```

## Deploy Something Simple

```bash
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=NodePort
kubectl get deploy,pods,svc
minikube service nginx
```

## Stop Or Delete Minikube

Stop the default cluster:

```bash
minikube stop
```

Stop a specific profile:

```bash
minikube stop -p practise
```

Delete the default cluster:

```bash
minikube delete
```

Delete the `practise` profile:

```bash
minikube delete -p practise
```

## Why Use Minikube?

- it is easy to start with one command
- it is beginner-friendly for learning Kubernetes basics
- it includes useful addons and helper commands