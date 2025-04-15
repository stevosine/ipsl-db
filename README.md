

This is a postgreSQL replcation and load balancer deployment on kubernetes using minikube helm chart with the following key outcomes.

      •	Primary Pod as statefulset handles all write and read operations by default( bitnami helm chart).
      •	Data replicated to stateful read only replicas using streaming replication and synced to primary.
      •	Load balancer kubernetes service routes traffic to the appropriate pod.
      •	Each pod has its own PVC for data persistence.
      • A schema with 2 tables with data loaded using faker library
