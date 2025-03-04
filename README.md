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
```mermaid
graph TD
    %% Client Components
    HTML[HTML/CSS UI]
    JS[JavaScript]
    BOOTSTRAP[Bootstrap Framework]
    
    %% Server Components
    FLASK[Flask Web Server]
    EKSCONN[EKS Connector]
    GKECONN[GKE Connector]
    K8SCLIENT[Kubernetes Client]
    BOTO3[boto3 AWS SDK]
    GOOGLEAPI[Google Cloud SDK]
    KUBECONFIG[Kubeconfig Generator]
    
    %% API Routes
    HEALTH[Health API]
    CLUSTERS[Clusters API]
    CONNECT[Connect API]
    AVAILABLE[Available API]
    RESOURCES[Resources API]
    
    %% External Services
    AWS_API[AWS EKS API]
    GCP_API[Google Cloud GKE API]
    K8S_API[Kubernetes API]
    
    %% Client Relationships
    JS --> HTML
    BOOTSTRAP --> HTML
    
    %% Server Relationships
    FLASK --> HEALTH
    FLASK --> CLUSTERS
    FLASK --> CONNECT
    FLASK --> AVAILABLE
    FLASK --> RESOURCES
    
    CONNECT --> EKSCONN
    CONNECT --> GKECONN
    AVAILABLE --> EKSCONN
    AVAILABLE --> GKECONN
    RESOURCES --> EKSCONN
    RESOURCES --> GKECONN
    
    EKSCONN --> BOTO3
    EKSCONN --> K8SCLIENT
    EKSCONN --> KUBECONFIG
    
    GKECONN --> GOOGLEAPI
    GKECONN --> K8SCLIENT
    
    BOTO3 --> AWS_API
    GOOGLEAPI --> GCP_API
    K8SCLIENT --> K8S_API
    
    %% Client-Server Relationship
    HTML --> FLASK
    FLASK --> HTML
    
    %% Styling
    classDef client fill:#f9f9f9,stroke:#333
    classDef server fill:#e6f3ff,stroke:#333
    classDef eks fill:#ffe6cc,stroke:#333
    classDef gke fill:#d9ead3,stroke:#333
    classDef api fill:#fff2cc,stroke:#333
    classDef external fill:#f5f5f5,stroke:#333
    
    class HTML,JS,BOOTSTRAP client
    class FLASK,K8SCLIENT server
    class EKSCONN,BOTO3,KUBECONFIG eks
    class GKECONN,GOOGLEAPI gke
    class HEALTH,CLUSTERS,CONNECT,AVAILABLE,RESOURCES api
    class AWS_API,GCP_API,K8S_API external
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

## Deployment Steps

### Prerequisites
- Python 3.6+
- Git
- pip (Python package manager)

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SubbuTechOps/python-k8s-console-ui.git
   cd python-k8s-console-ui
   ```

2. **Create Virtual Environment**
   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Application**
   ```bash
   cd ./backend
   python app.py
   ```

5. **Access the Console**
   - Open your browser and navigate to `http://localhost:8000`
---

## 📸 Screenshots

### Home Page
![Home Dashboard](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/Homepage.png)
![Home Dashboard](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/Homepage-2.png)

### EKS Dashboard - No Clusters
![EKS Dashboard](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/AWS%20Dashboard.png)

### EKS Cluster Discovery
![EKS Cluster Discovery](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/Discover%20EKS%20Cluster.png)

### EKS Cluster View
![EKS Cluster View](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/AWS%20Dashboard-3.png)

### Pod Management
![Pod Management](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/AWS%20Dashboard-4.png)
![Pod Management](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/AWS%20Dashboard-5.png)
![Pod Management](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/AWS%20Dashboard-6.png)

### Deployment View
![Deployment View](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/AWS%20Dashboard-Deployments.png)

### Service Management
![Service Management](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/AWS%20Dashboard-Services.png)
![Service Management](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/AWS%20Dashboard-Services2.png)

### Node Information
![Node Information](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/AWS%20Dashboard-Nodes.png)

### GKE Dashboard (Coming Soon)
![GKE Dashboard](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/GKE-Dashboard.png)

### API Test Console
![API Test Console](https://github.com/SubbuTechOps/python-k8s-clusters-ui/raw/master/k8s-cluster-ui/screenshots/API%20Test%20Console.png)

---
## Getting Started

1. Configure AWS credentials
2. Install dependencies
3. Start the application
4. Discover and connect to clusters
5. Explore Kubernetes resources

## 🔍 Troubleshooting

Common issues and solutions:

- **Port already in use**: Change the port in `app.py` or set `FLASK_RUN_PORT` environment variable
- **Kubernetes connection issues**: Ensure your kubeconfig is properly set up
- **Missing dependencies**: Verify virtual environment is activated before installing requirements

## 🚢 Deploying to Production

For production environments:

1. **Use a WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set up a Reverse Proxy**
   - Configure Nginx or Apache as a reverse proxy
   - Enable HTTPS with Let's Encrypt certificates

3. **Set Environment Variables**
   ```bash
   export FLASK_ENV=production
   export FLASK_DEBUG=0
   ```

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

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License 
---

**Built with ❤️ for Kubernetes Administrators**
