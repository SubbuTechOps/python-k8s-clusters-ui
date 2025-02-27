# EKS Cluster Management API Flow Documentation

## Overview

This document describes the flow of operations in the EKS Cluster Management API, a Flask-based application that facilitates the connection to and management of Amazon EKS (Elastic Kubernetes Service) clusters. The application provides a seamless interface between users and their Kubernetes resources hosted on AWS.

## System Components

1. **Frontend**: HTML/CSS/JavaScript application served by Flask
2. **Backend API**: Flask application with RESTful endpoints
3. **EKSConnector**: Core class managing connections to EKS clusters
4. **AWS Services**: Interaction with AWS EKS via boto3
5. **Kubernetes API**: Interaction with Kubernetes resources via kubernetes-client

## Initialization Flow

When the application starts:

1. Flask application initializes
2. A persistent `EKSConnector` instance is created at module level
3. Static files directory is configured for serving the frontend
4. Application begins listening for HTTP requests

## Connection Flow

### User Initiates Connection

1. User fills connection form in the frontend with:
   - Cluster name
   - AWS region
   - Authentication method (AWS credentials or profile)
   - Required authentication details

2. Frontend sends a POST request to `/api/clusters/connect` with JSON payload containing connection parameters

### Backend Processes Connection Request

1. Flask routes the request to the `connect_cluster` handler
2. Request parameters are validated:
   - Cluster name and region are required
   - Authentication details are checked based on auth type

3. Based on the authentication type:
   - For `credentials`: `connect_with_aws_credentials` is called with the provided AWS keys
   - For `profile`: `connect_with_aws_profile` is called with the profile name

### AWS Authentication Process

1. A boto3 session is created with the provided credentials or profile
2. EKS client is initialized with the session
3. The EKS client calls `describe_cluster` to fetch details about the specified cluster

### Kubernetes Configuration Generation

1. Cluster information is retrieved from the EKS API
2. A kubeconfig is dynamically generated containing:
   - Cluster endpoint
   - Certificate authority data
   - AWS command for token generation
   - Profile information (if applicable)

3. The kubeconfig is written to a temporary file
4. Kubernetes configuration is loaded from the temporary file
5. The temporary file is deleted after loading

### Connection Validation and Storage

1. Kubernetes API client is initialized
2. A test connection is made by listing namespaces
3. On successful connection:
   - A connection ID is generated in the format `{region}_{cluster_name}`
   - The API client and cluster information are stored in the `connected_clusters` dictionary
   - Success response with connection ID is returned to the frontend

4. On failure:
   - Error details are captured
   - Error response is returned to the frontend

## Resource Retrieval Flow

### User Requests Resources

1. User selects a connected cluster from the frontend
2. User selects a resource type (pods, deployments, services, nodes)
3. Frontend sends a GET request to `/api/clusters/{connection_id}/resources/{resource_type}`

### Backend Processes Resource Request

1. Flask routes the request to the `get_resources` handler
2. The connection ID is validated against stored connections
3. The resource type is validated against supported types
4. The stored API client for the connection is retrieved

### Kubernetes API Interaction

1. Based on the resource type, the appropriate Kubernetes API is used:
   - For pods and services: `CoreV1Api`
   - For deployments: `AppsV1Api`
   - For nodes: `CoreV1Api`

2. The appropriate API method is called to list resources:
   - `list_pod_for_all_namespaces()`
   - `list_deployment_for_all_namespaces()`
   - `list_service_for_all_namespaces()`
   - `list_node()`

3. Resource data is formatted into a standardized structure with relevant fields for each resource type

### Resource Response

1. Formatted resource data is returned as a JSON response
2. Frontend displays the resources to the user in an appropriate format

## Cluster Discovery Flow

### User Requests Available Clusters

1. User provides AWS region and authentication details
2. Frontend sends a POST request to `/api/clusters/available`

### Backend Lists Clusters

1. Flask routes the request to the `list_available_clusters` handler
2. Request parameters are validated
3. A boto3 session is created with the provided credentials or profile
4. EKS client is initialized with the session
5. The EKS client calls `list_clusters` to get a list of cluster names in the region
6. For each cluster, `describe_cluster` is called to get detailed information

### Cluster Response

1. List of available clusters with details (name, status, version, endpoint, creation time) is returned
2. Frontend displays the list to the user

## Disconnection Flow

### User Initiates Disconnect

1. User selects a connected cluster to disconnect
2. Frontend sends a POST request to `/api/clusters/{connection_id}/disconnect`

### Backend Processes Disconnect

1. Flask routes the request to the `disconnect_cluster` handler
2. The connection ID is validated against stored connections
3. The connection is removed from the `connected_clusters` dictionary
4. Success response is returned to the frontend

## Error Handling Flow

### AWS Client Errors

1. AWS API calls are wrapped in try-except blocks to catch `ClientError`
2. Error codes and messages are extracted from the response
3. Formatted error responses with specific AWS error details are returned

### Kubernetes API Errors

1. Kubernetes API calls are wrapped in try-except blocks
2. Error messages are captured and formatted
3. Error responses are returned to the frontend

### General Exception Handling

1. General exceptions are caught at function level
2. Errors are logged with detailed messages
3. Generic error responses are returned to the frontend

## Connection Management

The application maintains connections to multiple clusters simultaneously:

1. Each connection is stored with a unique connection ID (region_clustername)
2. For each connection, the following is stored:
   - Kubernetes API client
   - Cluster information (name, region, version, status, endpoint)

3. The `list_connected_clusters` method provides an overview of all active connections

## Resource Formatting

Each resource type has a specialized formatting function:

1. **Pods**: Name, namespace, status, containers, node, creation time
2. **Deployments**: Name, namespace, replicas, available replicas, creation time
3. **Services**: Name, namespace, type, cluster IP, ports, creation time
4. **Nodes**: Name, status, roles, instance type, zone, kubelet version, creation time

## Security Considerations

1. AWS credentials are never stored on disk
2. Kubeconfig files are created as temporary files and deleted after use
3. AWS credential validation happens before attempting to connect
4. All API endpoints validate parameters before processing

## Flow Diagram

```
┌─────────────┐          ┌───────────────┐          ┌───────────────┐
│   Frontend  │          │  Flask API    │          │ EKSConnector  │
└──────┬──────┘          └───────┬───────┘          └───────┬───────┘
       │                         │                          │
       │  1. Request Connection  │                          │
       │────────────────────────>                           │
       │                         │                          │
       │                         │  2. Connect to Cluster   │
       │                         │─────────────────────────>│
       │                         │                          │
       │                         │                          │──┐
       │                         │                          │  │ 3. Create AWS Session
       │                         │                          │<─┘
       │                         │                          │
       │                         │                          │──┐
       │                         │                          │  │ 4. Access EKS API
       │                         │                          │<─┘
       │                         │                          │
       │                         │                          │──┐
       │                         │                          │  │ 5. Generate Kubeconfig
       │                         │                          │<─┘
       │                         │                          │
       │                         │                          │──┐
       │                         │                          │  │ 6. Initialize K8s Client
       │                         │                          │<─┘
       │                         │                          │
       │                         │  7. Return Connection ID │
       │                         │<─────────────────────────│
       │                         │                          │
       │  8. Connection Response │                          │
       │<────────────────────────                           │
       │                         │                          │
       │  9. Request Resources   │                          │
       │────────────────────────>                           │
       │                         │                          │
       │                         │  10. Get Resources       │
       │                         │─────────────────────────>│
       │                         │                          │
       │                         │                          │──┐
       │                         │                          │  │ 11. Call K8s API
       │                         │                          │<─┘
       │                         │                          │
       │                         │  12. Return Resources    │
       │                         │<─────────────────────────│
       │                         │                          │
       │  13. Resource Response  │                          │
       │<────────────────────────                           │
       │                         │                          │
```

## Conclusion

The EKS Cluster Management API provides a comprehensive interface for connecting to and interacting with EKS clusters. By understanding this flow, developers and operators can effectively utilize the API to manage their Kubernetes resources on AWS.
