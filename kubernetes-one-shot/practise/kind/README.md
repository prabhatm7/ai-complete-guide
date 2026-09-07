# Kind Cluster Guide

This folder contains a local Kubernetes cluster setup using `kind`.

## Files

- `config.yaml`: the cluster definition used by `kind`

## What This Cluster Creates

This configuration creates:

- 1 control-plane node
- 3 worker nodes
- port mapping from host `80` to container `80`
- port mapping from host `443` to container `443`

## Start Kind After Installation

After `kind` is installed, move into this folder and run:

```bash
kind create cluster --name practise --config ./config.yaml
```

## Verify The Cluster

```bash
kubectl cluster-info --context kind-practise
kubectl get nodes --context kind-practise
```

You should see 4 nodes total:

- 1 control-plane
- 3 workers

## Use The Cluster

Switch to the `kind` context:

```bash
kubectl config use-context kind-practise
```

If both `kind` and `minikube` clusters are running, you can switch between them with:

```bash
kubectl config use-context kind-practise
kubectl config use-context minikube
```

Whichever context you choose with `kubectl config use-context ...` becomes the default context for all `kubectl` commands.

Check the current default context:

```bash
kubectl config current-context
```

Useful commands:

```bash
kubectl get nodes
kubectl get pods -A
kubectl get deployments -A
kubectl get svc -A
kubectl describe node practise-control-plane
kubectl get events --sort-by=.metadata.creationTimestamp
```

## Deploy Something Simple

```bash
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=ClusterIP
kubectl get deploy,pods,svc
kubectl port-forward svc/nginx 8080:80
```

Then open `http://localhost:8080`.

## Delete And Recreate

Delete the cluster:

```bash
kind delete cluster --name practise
```

Create it again:

```bash
kind create cluster --name practise --config ./config.yaml
```

## Why Use Kind?

- you can keep cluster setup in YAML
- multi-node clusters are easy to reproduce
- it is good for learning cluster structure locally