# SubbuK8sConsole Documentation

## Application Overview

SubbuK8sConsole is a powerful web-based application designed to simplify Kubernetes cluster management across multiple cloud providers. It provides a unified interface to connect to and monitor clusters from Amazon EKS (Elastic Kubernetes Service), offering comprehensive insights into your Kubernetes infrastructure.

## Architecture
```mermaid
flowchart TD
    subgraph "Frontend"
        UI[Web UI Interface]
        UI_EKS[EKS Dashboard]
        UI_GKE[GKE Dashboard]
        UI_TEST[API Test Page]
        UI --> UI_EKS
        UI --> UI_GKE
        UI --> UI_TEST
    end

    subgraph "Backend Server"
        FLASK[Flask Web Server]
        PERSIST[Persistent EKS/GKE Connector]
        API[REST API Endpoints]
        
        FLASK --> API
        API <--> PERSIST
    end

    subgraph "Cloud Providers"
        AWS[AWS APIs]
        GCP[Google Cloud APIs]
        
        subgraph "Kubernetes APIs"
            K8S_API[Kubernetes API]
            PODS[Pods]
            DEPLOY[Deployments]
            SVC[Services]
            NODES[Nodes]
            
            K8S_API --> PODS
            K8S_API --> DEPLOY
            K8S_API --> SVC
            K8S_API --> NODES
        end
        
        AWS --> K8S_API
        GCP --> K8S_API
    end

    UI_EKS <--> API
    UI_GKE <--> API
    UI_TEST <--> API
    
    PERSIST <--> AWS
    PERSIST <--> GCP
    
    classDef frontend fill:#f9f9f9,stroke:#333,stroke-width:2px
    classDef backend fill:#e6f3ff,stroke:#333,stroke-width:2px
    classDef cloud fill:#f5f5f5,stroke:#333,stroke-width:2px
    classDef k8s fill:#e7f2e7,stroke:#333,stroke-width:2px
    
    class UI,UI_EKS,UI_GKE,UI_TEST frontend
    class FLASK,PERSIST,API backend
    class AWS,GCP cloud
    class K8S_API,PODS,DEPLOY,SVC,NODES k8s
```

```
+-------------------+        +-------------------+        +-------------------+
|   Frontend Layer  |        |   API Layer       |        |   Cloud Provider  |
|   (HTML/JS/CSS)  | <----> |   (Flask Backend) | <----> |   (AWS/GCP)       |
+-------------------+        +-------------------+        +-------------------+
        |                            |                            |
        |                            |                            |
+-------------------+        +-------------------+        +-------------------+
| Browser Interface |        | EKS Connector     |        | Kubernetes Cluster|
| (User Interaction)|        | (Resource Manager)|        | (EKS/GKE)         |
+-------------------+        +-------------------+        +-------------------+
```

### Component Breakdown

1. **Frontend Layer**
   - Built with HTML5, CSS3, JavaScript
   - Responsive design using Bootstrap
   - Handles user interactions
   - Sends API requests to backend
   - Renders cluster and resource information

2. **API Layer (Backend)**
   - Flask-based Python web server
   - Manages API endpoints
   - Handles authentication and resource retrieval
   - Interfaces with cloud providers
   - Provides RESTful API for cluster management

3. **Cloud Provider Connector**
   - Uses boto3 for AWS interactions
   - Manages cluster connections
   - Retrieves cluster metadata
   - Generates dynamic kubeconfig
   - Handles authentication methods

## API Workflow and Interaction Patterns

### Cluster Discovery Workflow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant AWS
    
    User->>Frontend: Select region and auth method
    Frontend->>Backend: POST /api/clusters/available
    Backend->>AWS: List EKS Clusters
    AWS-->>Backend: Return cluster list
    Backend-->>Frontend: Clusters JSON
    Frontend->>User: Display Available Clusters
```

### Cluster Connection Workflow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant AWS
    participant K8s
    
    User->>Frontend: Provide cluster details
    Frontend->>Backend: POST /api/clusters/connect
    Backend->>AWS: Authenticate and Retrieve Cluster Info
    AWS-->>Backend: Cluster Credentials
    Backend->>K8s: Generate Kubeconfig
    K8s-->>Backend: Connection Established
    Backend-->>Frontend: Connection ID
    Frontend->>User: Cluster Connected
```

### Resource Retrieval Workflow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant K8s
    
    User->>Frontend: Request Resource View
    Frontend->>Backend: GET /api/clusters/{connection_id}/resources/{type}
    Backend->>K8s: List Resources
    K8s-->>Backend: Resource Details
    Backend-->>Frontend: Formatted Resources
    Frontend->>User: Display Resources
```

## API Endpoints Overview

### Authentication and Cluster Management

| Endpoint | Method | Description | Authentication Required |
|----------|--------|-------------|-------------------------|
| `/api/clusters/connect` | POST | Connect to an EKS cluster | AWS Credentials/Profile |
| `/api/clusters/available` | POST | Discover available clusters | AWS Credentials/Profile |
| `/api/clusters` | GET | List connected clusters | None |
| `/api/clusters/<connection_id>/disconnect` | POST | Disconnect from a cluster | Connection ID |

### Resource Retrieval

| Endpoint | Method | Description | Authentication Required |
|----------|--------|-------------|-------------------------|
| `/api/clusters/<connection_id>/resources/<type>` | GET | Get cluster resources | Connection ID |
| `/api/clusters/<connection_id>/pods` | GET | Get pod information | Connection ID |

### Utility

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check API status |

## Authentication Methods

### 1. AWS Credentials Authentication
- Direct AWS access key authentication
- Supports temporary session tokens
- Provides granular access control

### 2. AWS Profile Authentication
- Uses pre-configured AWS profiles
- Simplifies credential management
- Default profile support

## Error Handling

The API provides comprehensive error responses:
- Detailed error messages
- Appropriate HTTP status codes
- Logging for backend diagnostics

## Security Considerations

1. **Credential Management**
   - Supports multiple authentication methods
   - Temporary credential support
   - No long-term credential storage

2. **API Security**
   - CORS support
   - Minimal persistent state
   - Stateless resource retrieval

## Deployment Considerations

- Supports containerized deployment
- Compatible with various hosting environments
- Minimal infrastructure requirements

## Future Enhancements

- Multi-cloud support expansion
- Enhanced authentication mechanisms
- Advanced resource management features
- Persistent cluster connection state
- Real-time cluster monitoring

## Getting Started

1. Configure AWS credentials
2. Install dependencies
3. Start the application
4. Discover and connect to clusters
5. Explore Kubernetes resources

## Troubleshooting

- Verify AWS credentials
- Check network connectivity
- Review application logs
- Ensure proper IAM permissions

---

**Built with ❤️ for Kubernetes Administrators**
