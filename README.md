# EKS Dashboard Documentation

## Application Overview

EKS Dashboard is a web-based application for monitoring and managing Amazon EKS (Elastic Kubernetes Service) clusters. It provides a simple interface to connect to EKS clusters, discover available clusters in AWS accounts, and view Kubernetes resources like pods, deployments, services, and nodes.

## Architecture

The application follows a client-server architecture with the following components:

### Backend

- **Flask Application**: Python-based web server that handles API requests
- **EKS Connector**: Core component that manages connections to EKS clusters using AWS and Kubernetes APIs
- **API Endpoints**: RESTful endpoints for cluster operations and resource retrieval

### Frontend

- **Dashboard UI**: HTML/CSS/JavaScript-based interface for managing clusters
- **API Test Page**: Utility page for testing API connectivity
- **Bootstrap 5**: Used for responsive UI components

### Technical Stack

- **Backend**:
  - Python 3.x
  - Flask web framework
  - boto3 (AWS SDK for Python)
  - kubernetes-client (Python client for Kubernetes API)
  - YAML and JSON for configuration and data exchange

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript (ES6+)
  - Bootstrap 5.3.0 (for UI components)

## Deployment

### Prerequisites

1. Python 3.6 or higher
2. pip (Python package manager)
3. AWS CLI configured with appropriate permissions
4. Access to AWS EKS clusters
5. kubectl configured (optional, for verification)

### Installation Steps

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd eks-dashboard
   ```

2. **Install backend dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Configure the application**:
   - Ensure AWS credentials are available either through:
     - Environment variables
     - ~/.aws/credentials file
     - IAM roles (if running on EC2)

4. **Run the application**:
   ```
   python app.py
   ```

   The application will start a web server on http://0.0.0.0:8000

### Docker Deployment (Optional)

1. **Build the Docker image**:
   ```
   docker build -t eks-dashboard .
   ```

2. **Run the container**:
   ```
   docker run -p 8000:8000 -v ~/.aws:/root/.aws eks-dashboard
   ```

### AWS ECS/Fargate Deployment (Optional)

For production deployments, consider using Amazon ECS or Fargate:

1. Create an ECR repository
2. Push the Docker image to ECR
3. Create an ECS task definition that includes the AWS credential mounting
4. Configure appropriate IAM roles for the ECS task
5. Deploy as a service with a load balancer

## Usage Guide

### Accessing the Dashboard

1. Open a web browser and navigate to http://localhost:8000 (or your deployment URL)
2. You'll see the main dashboard interface

### Connecting to an EKS Cluster

1. Click the "Add Cluster" button
2. Fill in the cluster details:
   - Cluster name
   - AWS region
   - Authentication method (AWS credentials or AWS profile)
3. Click "Connect"
4. Once connected, the cluster will appear in the dashboard

### Discovering Available Clusters

1. Click the "Discover Clusters" button
2. Select the AWS region where your clusters are located
3. Choose your authentication method
4. Click "Discover Clusters"
5. The available clusters will be listed
6. Click "Connect" on any cluster to add it to your dashboard

### Viewing Cluster Resources

1. From the dashboard, click "View Resources" on any connected cluster
2. Use the tabs to navigate between different resource types:
   - Pods
   - Deployments
   - Services
   - Nodes
3. Each tab shows a table of available resources with relevant details
4. Use the "Refresh" button to update the resource information

### API Testing

1. Navigate to the API Test page at http://localhost:8000/test.html
2. Use the provided buttons to test different API operations:
   - Test Health: Check if the API is running
   - Test List Clusters: List all connected clusters
   - Test Discover Clusters: Discover available clusters in AWS
   - Test Connect to Cluster: Connect to a specific cluster
   - Test List Pods: List all pods in the connected cluster
   - Discover API: Attempt to discover API endpoints

## API Reference

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check API health |
| `/api/clusters` | GET | List all connected clusters |
| `/api/clusters/connect` | POST | Connect to an EKS cluster |
| `/api/clusters/available` | POST | List available EKS clusters |
| `/api/clusters/<connection_id>/disconnect` | POST | Disconnect from a cluster |
| `/api/clusters/<connection_id>/resources/<resource_type>` | GET | Get resources from a cluster |
| `/api/clusters/<connection_id>/pods` | GET | Get pods from a cluster |

### API Request Examples

**Connect to a cluster**:
```json
POST /api/clusters/connect
{
  "cluster_name": "demo-cluster",
  "region": "us-east-1",
  "auth_type": "profile",
  "profile_name": "default"
}
```

**Discover available clusters**:
```json
POST /api/clusters/available
{
  "region": "us-east-1",
  "auth_type": "profile",
  "profile_name": "default"
}
```

## Troubleshooting

### Common Issues

1. **Connection failures**:
   - Verify AWS credentials have EKS permissions
   - Check cluster name and region are correct
   - Ensure network connectivity to AWS APIs

2. **Cannot view resources**:
   - Verify the cluster connection was successful
   - Check AWS IAM permissions for Kubernetes RBAC
   - Restart the application to reinitialize the connector

3. **Clusters not appearing in dashboard**:
   - Ensure the application is running with persistent state
   - Check browser console for JavaScript errors
   - Verify the API responses in the Network tab

### Logs

- Backend logs are printed to the console
- Check browser developer tools for frontend errors
- Set environment variable `FLASK_DEBUG=1` for more detailed logs

## Security Considerations

1. **AWS Credentials**:
   - Use IAM roles instead of access keys when possible
   - Implement least privilege for AWS permissions
   - Consider using temporary credentials with AWS STS

2. **API Security**:
   - Implement proper authentication for the API in production
   - Use HTTPS for all communications
   - Consider adding rate limiting to prevent abuse

3. **Kubernetes RBAC**:
   - Apply appropriate RBAC policies to limit resource access
   - Use read-only permissions when possible
   - Consider namespace restrictions for multi-tenant usage

## Future Enhancements

1. User authentication and multi-user support
2. Persistent storage for cluster connections
3. Advanced filtering and searching for resources
4. Resource editing capabilities
5. Metrics and monitoring integration
6. Enhanced visualization with graphs and charts
7. Support for multiple Kubernetes providers beyond EKS

---

## Implementation Details

### Core Components

#### EKS Connector

The EKS Connector is the heart of the application, responsible for:

1. Discovering EKS clusters in AWS accounts
2. Connecting to clusters using appropriate authentication
3. Retrieving Kubernetes resources from connected clusters
4. Managing cluster connection state

It interfaces with:
- AWS SDK (boto3) for EKS operations
- Kubernetes Python client for K8s API operations
- kubeconfig generation for cluster authentication

#### Flask Application

The Flask application provides the REST API interface and serves the frontend. Key features:

1. Persistent EKS connector instance for state management
2. API endpoints for cluster operations
3. Resource retrieval with proper error handling
4. Static file serving for the frontend assets

#### Frontend UI

The frontend is built with modern web technologies:

1. Bootstrap for responsive layout and components
2. Fetch API for asynchronous communication with backend
3. Modular JavaScript for maintainable code
4. Dynamic content rendering with DOM manipulation
