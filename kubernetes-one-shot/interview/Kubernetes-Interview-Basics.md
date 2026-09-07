# Kubernetes — Basics + Intermediate Interview Review

## 1. Kubernetes Basics

- Kubernetes = container orchestration platform.
- Main goals:
  - Deploy containers.
  - Scale applications.
  - Self-heal workloads.
  - Perform rolling updates/rollbacks.
  - Provide networking and service discovery.
  - Manage configuration and secrets.
- Cluster:
  - Control plane.
  - Worker nodes.
- Control plane:
  - API Server -> front door for the Kubernetes API.
  - etcd -> distributed key-value store containing cluster state.
  - Scheduler -> chooses a node for unscheduled Pods.
  - Controller Manager -> runs controllers that reconcile desired and actual state.
- Worker node:
  - kubelet -> manages Pods assigned to the node.
  - Container runtime -> runs containers, commonly containerd.
  - kube-proxy -> Service networking component; exact implementation can vary.

## 2. Declarative Model

- Kubernetes is declarative.
- YAML describes desired state.
- Kubernetes continuously compares:
  - Desired state.
  - Actual state.
- Controllers reconcile differences.
- Example:
  - Desired replicas = 3.
  - One Pod crashes.
  - Actual replicas = 2.
  - ReplicaSet creates another Pod.
  - State returns to 3.

## 3. Core Resources

### Namespace

- Logical isolation/grouping boundary.
- Useful for:
  - Teams.
  - Environments.
  - RBAC.
  - Resource quotas.
- Not a separate cluster.
- Namespace alone does not provide network isolation.
- NetworkPolicy can provide network-level restrictions.

### Pod

- Smallest deployable unit.
- Usually one main application container.
- Multiple containers can share:
  - Network namespace.
  - Pod IP.
  - Volumes.
- Containers in one Pod can communicate using `localhost`.
- Pods are ephemeral.
- Production workloads are normally managed by controllers.

### Deployment

- Manages stateless application Pods.
- Usually the preferred resource for APIs/web apps.
- Manages ReplicaSets.
- Supports:
  - Scaling.
  - Rolling updates.
  - Rollbacks.
  - Self-healing.
- Hierarchy:
  - Deployment -> ReplicaSet -> Pods -> Containers.

### ReplicaSet

- Maintains the desired number of matching Pods.
- Example:
  - `replicas: 3` -> keeps 3 matching Pods.
- Deployment normally creates/manages ReplicaSets.
- Direct ReplicaSet management is less common.

### DaemonSet

- Runs a Pod on every eligible node.
- Typical use:
  - Log collectors.
  - Monitoring agents.
  - Security agents.
  - Node-level networking agents.
- New eligible nodes get a Pod automatically.
- It is node-oriented, not replica-count-oriented.

### Job

- Runs a finite task until it successfully completes.
- Typical use:
  - Database migration.
  - Data processing.
  - One-time batch task.
- Expected to finish.
- Common restart policy:
  - `OnFailure`
  - `Never`

### CronJob

- Creates Jobs on a schedule.
- Typical use:
  - Nightly backup.
  - Cleanup.
  - Reports.
  - Scheduled batch processing.
- Hierarchy:
  - CronJob -> Job -> Pod -> Container.

## 4. YAML Structure

- Common top-level fields:
  - `apiVersion`
  - `kind`
  - `metadata`
  - `spec`
- `apiVersion`:
  - API group/version.
  - Examples:
    - `v1`
    - `apps/v1`
    - `batch/v1`
- `kind`:
  - Resource type.
  - Examples:
    - Deployment
    - Service
    - Job
    - CronJob
- `metadata`:
  - Name.
  - Namespace.
  - Labels.
  - Annotations.
- `spec`:
  - Desired configuration.
- `status`:
  - Observed/current state, normally maintained by Kubernetes.

## 5. Labels vs Selectors

### Labels

- Key-value metadata.
- Example:
  - `app: nginx`
  - `environment: production`

### Selectors

- Find resources using labels.
- Example:
  - `matchLabels: app: nginx`
- Critical rule:
  - Controller selectors must correctly match Pod template labels.
- Service selectors determine which Pods receive Service traffic.

## 6. Deployment Flow

- `kubectl apply -f deployment.yaml`
- kubectl sends the desired object to API Server.
- API Server validates/authenticates/authorizes the request.
- Desired state is stored in etcd.
- Deployment controller creates/updates a ReplicaSet.
- ReplicaSet creates Pods.
- Scheduler selects nodes.
- Kubelet starts containers through the runtime.
- Kubelet reports status.
- If a Pod dies, the controller creates a replacement.

## 7. Deployment Rolling Update

- Deployment creates a new ReplicaSet for the new Pod template.
- New Pods are gradually created.
- Old Pods are gradually removed.
- `maxUnavailable`:
  - Maximum unavailable Pods during update.
- `maxSurge`:
  - Maximum extra Pods above desired replica count.
- Readiness probes help prevent unready Pods from receiving Service traffic.
- Rollback:
  - `kubectl rollout undo deployment/<name>`

## 8. Scaling

- Manual:
  - `kubectl scale deployment <name> --replicas=5`
- HPA:
  - Horizontal Pod Autoscaler.
  - Automatically changes Pod replica count based on metrics.
- VPA:
  - Vertical Pod Autoscaler.
  - Can recommend/adjust resource requests depending on configuration.
- Cluster Autoscaler:
  - Adds/removes nodes based on scheduling demand where supported.
- Interview distinction:
  - HPA -> Pods.
  - Cluster Autoscaler -> Nodes.

## 9. Service

- Pods are ephemeral.
- Pod IPs can change.
- Service provides a stable virtual endpoint.
- Service selects Pods using labels.
- Typical flow:
  - Client -> Service -> selected Pods.

### Service types

- ClusterIP:
  - Default.
  - Internal cluster access.
- NodePort:
  - Exposes a port on nodes.
- LoadBalancer:
  - Integrates with an external load balancer when supported.
- ExternalName:
  - Maps a Service name to an external DNS name.

## 10. Service Discovery

- Kubernetes provides DNS-based service discovery.
- Inside the same namespace:
  - `service-name`
- Fully qualified form:
  - `service-name.namespace.svc.cluster.local`

## 11. ConfigMap vs Secret

### ConfigMap

- Non-sensitive configuration.
- Examples:
  - Feature flags.
  - Environment settings.
  - Application configuration.

### Secret

- Intended for sensitive configuration.
- Examples:
  - Passwords.
  - API keys.
  - Tokens.
- Base64 encoding is not encryption.
- Encryption at rest can be configured.
- Avoid committing real credentials to Git.

## 12. Requests vs Limits

### Requests

- Resource amount used for scheduling decisions.
- Example:
  - CPU `100m`.
  - Memory `128Mi`.

### Limits

- Maximum configured container resource usage.
- CPU can be throttled at the limit.
- Memory overuse can result in OOM kill.

### Remember

- Requests -> scheduling.
- Limits -> runtime constraint.

## 13. Probes

### Readiness

- Question:
  - "Can this Pod receive traffic?"
- Failed readiness:
  - Container can keep running.
  - Pod is removed from Service endpoints.

### Liveness

- Question:
  - "Is this container still healthy?"
- Repeated failure can cause container restart.

### Startup

- Useful for slow-starting applications.
- Allows startup time before liveness/readiness behavior becomes decisive.

## 14. Jobs

- `completions`:
  - Number of successful completions required.
- `parallelism`:
  - Maximum concurrent Pods.
- `backoffLimit`:
  - Retry limit for failed Pods before Job failure.
- `ttlSecondsAfterFinished`:
  - Automatically cleans up a completed Job after a delay.
- Job:
  - One finite task.
- CronJob:
  - Scheduled creator of Jobs.

## 15. Scheduling

### Scheduler

- Chooses a suitable node for an unscheduled Pod.

### nodeSelector

- Simple node label matching.
- Example:
  - Run only on nodes labeled `disk: ssd`.

### Node Affinity

- More expressive node selection.
- Can be:
  - Required.
  - Preferred.

### Taints and Tolerations

- Taint:
  - Repels Pods from a node unless tolerated.
- Toleration:
  - Allows a Pod to run on a tainted node.
- Common for:
  - Dedicated nodes.
  - GPU/special hardware.
  - Isolation.

### Pod Affinity / Anti-Affinity

- Affinity:
  - Place Pods near matching Pods.
- Anti-affinity:
  - Separate Pods from matching Pods.
- Useful for availability and topology decisions.

## 16. StatefulSet

- Used for stateful workloads.
- Provides:
  - Stable Pod identity.
  - Stable network identity.
  - Persistent storage association.
  - Ordered operations when configured.
- Example:
  - Database.
  - Stateful distributed system.
- Contrast:
  - Deployment -> interchangeable Pods.
  - StatefulSet -> stable identity.

## 17. StatefulSet vs Deployment

- Deployment:
  - Usually stateless.
  - Pods are interchangeable.
  - Easy horizontal scaling.
- StatefulSet:
  - Stateful.
  - Stable names such as `app-0`, `app-1`.
  - Stable storage/network identity.
  - Supports ordered behavior.

## 18. Deployment vs DaemonSet

- Deployment:
  - Run N replicas across suitable nodes.
- DaemonSet:
  - Run one Pod per eligible node.
- API server -> Deployment.
- Node log collector -> DaemonSet.

## 19. Job vs Deployment

- Deployment:
  - Long-running application.
  - Keeps Pods running.
- Job:
  - Finite task.
  - Completes and stops.
- REST API -> Deployment.
- DB migration -> Job.

## 20. Job vs CronJob

- Job:
  - Run task once.
- CronJob:
  - Run Jobs according to a schedule.
- Migration -> Job.
- Nightly backup -> CronJob.

## 21. ReplicaSet vs Deployment

- ReplicaSet:
  - Maintains Pod count.
- Deployment:
  - Higher-level controller.
  - Manages ReplicaSets.
  - Provides rollout/rollback functionality.
- Interview answer:
  - "I generally use Deployment instead of directly managing a ReplicaSet for stateless applications."

## 22. Ingress

- Ingress provides HTTP/HTTPS routing into Services.
- Routing can be based on:
  - Host.
  - Path.
- Requires an Ingress Controller.
- Example:
  - `api.example.com` -> API Service.
  - `/users` -> Users Service.
- Gateway API is another modern option for traffic management.

## 23. Networking

- Pods generally receive their own IP.
- Pod-to-Pod networking is provided by the cluster networking implementation.
- Service provides a stable virtual endpoint.
- CNI:
  - Container Network Interface.
  - Provides/configures cluster networking.
- NetworkPolicy:
  - Controls allowed network traffic according to the cluster/CNI capabilities.

## 24. Storage

### PV

- PersistentVolume.
- Cluster-level storage resource.

### PVC

- PersistentVolumeClaim.
- Workload's request for storage.

### StorageClass

- Defines dynamic storage provisioning behavior.

### Typical flow

- Pod -> PVC -> PV -> Storage backend.

## 25. RBAC

- RBAC = Role-Based Access Control.
- Controls:
  - Who.
  - Can perform which actions.
  - On which resources.
- Role:
  - Permissions within a namespace.
- ClusterRole:
  - Cluster-scoped/reusable permissions.
- RoleBinding:
  - Binds permissions to users/groups/ServiceAccounts within a namespace.
- ClusterRoleBinding:
  - Binds a ClusterRole at cluster scope.
- ServiceAccount:
  - Identity used by workloads.
- Principle of least privilege:
  - Grant only required permissions.

## 26. ResourceQuota vs LimitRange

### ResourceQuota

- Controls total resource/object consumption in a namespace.
- Examples:
  - Maximum CPU.
  - Maximum memory.
  - Maximum Pods.

### LimitRange

- Defines default/min/max resource constraints for individual containers/Pods.

## 27. Init Containers

- Run before application containers.
- Useful for:
  - Initialization.
  - Dependency checks.
  - Preparing files.
  - Setup work.
- Main containers start after init containers complete successfully.

## 28. Sidecar

- Additional container in the same Pod as the main application.
- Containers share:
  - Network namespace.
  - Pod IP.
  - Can share volumes.
- Examples:
  - Proxy.
  - Telemetry helper.
  - Log/config agent.
- Adds complexity and resource consumption.

## 29. PodDisruptionBudget

- Helps maintain availability during voluntary disruptions.
- Examples:
  - Node drain.
  - Maintenance.
- Controls voluntary Pod disruption.
- Does not guarantee availability during every failure.

## 30. Useful kubectl Commands

### Inspect

- `kubectl cluster-info`
- `kubectl get nodes`
- `kubectl get ns`
- `kubectl get pods`
- `kubectl get pods -A`
- `kubectl get deployments`
- `kubectl get rs`
- `kubectl get daemonsets`
- `kubectl get jobs`
- `kubectl get cronjobs`
- `kubectl get svc`

### Details

- `kubectl describe pod <pod>`
- `kubectl describe deployment <deployment>`
- `kubectl get pod <pod> -o yaml`

### Apply/delete

- `kubectl apply -f file.yaml`
- `kubectl delete -f file.yaml`

### Logs/debug

- `kubectl logs <pod>`
- `kubectl logs -f <pod>`
- `kubectl exec -it <pod> -- /bin/sh`

### Rollouts

- `kubectl rollout status deployment/<name>`
- `kubectl rollout history deployment/<name>`
- `kubectl rollout undo deployment/<name>`
- `kubectl rollout restart deployment/<name>`

### Scaling

- `kubectl scale deployment <name> --replicas=5`

## 31. Common Interview Questions

### What happens after `kubectl apply`?

- kubectl -> API Server.
- API Server validates/authenticates/authorizes.
- Desired state is persisted in etcd.
- Controller observes the resource.
- Deployment controller -> ReplicaSet.
- ReplicaSet -> Pods.
- Scheduler -> node selection.
- Kubelet -> starts containers.
- Status is continuously reported.

### What happens when a Pod dies?

- Controller detects fewer replicas than desired.
- Replacement Pod is created.
- Scheduler chooses a node.
- Kubelet starts it.

### What happens when a node dies?

- Node becomes unhealthy/unreachable.
- Kubernetes detects node conditions.
- Controllers can recreate/reschedule managed workloads onto healthy nodes.
- Exact timing depends on failure detection and controller behavior.

### Why do we need a Service?

- Pod IPs are ephemeral.
- Service provides a stable endpoint.
- Service selects Pods using labels.
- Traffic goes to eligible endpoints.

### What is etcd?

- Distributed key-value store.
- Stores Kubernetes cluster state.
- Critical control-plane component.
- Backups are important.

### What is kubelet?

- Node agent.
- Ensures assigned Pods/containers are running.
- Reports node and Pod status.

### What is a namespace?

- Logical isolation/grouping mechanism.
- Useful for organization, RBAC, quotas and policies.
- Not a separate cluster.

### What is reconciliation?

- Controller observes desired state.
- Compares it with actual state.
- Takes corrective action.
- Repeats continuously.

## 32. YAML Interview Traps

- `metadata.name` identifies the resource.
- `metadata.namespace` selects the namespace for namespaced resources.
- Controller selectors must correctly match Pod template labels.
- `containerPort` does NOT expose a Pod outside the cluster by itself.
- A Service provides stable networking to Pods.
- `replicas` belongs to controllers such as Deployment/ReplicaSet, not a normal Pod.
- Jobs normally use `OnFailure` or `Never`.
- CronJob creates Jobs; it does not directly manage Pods.
- Deployment manages ReplicaSets; ReplicaSets manage Pods.
- DaemonSet targets eligible nodes rather than a fixed global replica count.
- Secret base64 is encoding, not encryption.

## 33. Resource Hierarchy

- Deployment -> ReplicaSet -> Pods -> Containers.
- CronJob -> Job -> Pods -> Containers.
- DaemonSet -> Pods -> Containers.
- StatefulSet -> Pods -> Containers.
- Service -> selects Pods using labels.
- Ingress -> routes HTTP/HTTPS traffic to Services.

## 34. Mental Model

- API Server -> "Front door."
- etcd -> "Cluster state database."
- Scheduler -> "Chooses the node."
- Kubelet -> "Runs/maintains Pods on a node."
- Controller -> "Keeps actual state aligned with desired state."
- Deployment -> "Manages application versions and ReplicaSets."
- ReplicaSet -> "Keeps the right number of Pods."
- Pod -> "Runs containers."
- Service -> "Stable network endpoint for Pods."
- Ingress -> "HTTP/HTTPS routing into Services."
- Job -> "Run a finite task."
- CronJob -> "Run Jobs on a schedule."
- DaemonSet -> "Run a Pod on every eligible node."
- StatefulSet -> "Run stateful Pods with stable identity."

## 35. Final 10-Point Interview Checklist

- Kubernetes is declarative and reconciliation-based.
- Pod is the smallest deployable unit.
- Deployment -> ReplicaSet -> Pods.
- CronJob -> Job -> Pods.
- Deployment is generally for stateless applications.
- StatefulSet is for stateful workloads.
- DaemonSet is for node-level workloads.
- Service provides stable networking for Pods.
- Requests affect scheduling; limits constrain runtime resources.
- Readiness controls traffic eligibility; liveness can trigger restarts.
