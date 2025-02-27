# SubbuK8sConsole Documentation

## Application Overview

SubbuK8sConsole is a powerful web-based application designed to simplify Kubernetes cluster management across multiple cloud providers. It provides a unified interface to connect to and monitor clusters from Amazon EKS (Elastic Kubernetes Service) and Google Kubernetes Engine (GKE), offering comprehensive insights into your Kubernetes infrastructure.

## Key Features 🌟

- **Multi-Cloud Support**: Seamlessly manage and monitor AWS EKS and GKE clusters from a single dashboard
- **Comprehensive Cluster Insights**: 
  - Real-time visibility into nodes, pods, deployments, and services
  - Detailed resource information across different Kubernetes environments
- **Secure & Scalable Authentication**: 
  - Supports multiple authentication methods
  - Leverages Kubeconfig, AWS Boto3, and Google Cloud SDK
- **User-Friendly Interface**: 
  - Responsive design built with Bootstrap
  - Intuitive navigation and resource management
- **Powerful API-Driven Architecture**:
  - Efficient interaction with cloud provider and Kubernetes APIs
  - Robust backend for retrieving and displaying cluster data

## Architecture

The application follows a modern client-server architecture with robust, scalable components:

### Backend

- **Flask Microservices**: Python-based web server handling API requests
- **Multi-Cloud Connectors**: 
  - EKS Connector for AWS clusters
  - GKE Connector for Google Cloud clusters
- **RESTful API Endpoints**: Comprehensive cluster and resource management operations

### Frontend

- **Dynamic Dashboard UI**: 
  - HTML5, CSS3, and JavaScript-powered interface
  - Bootstrap 5 for responsive design
- **API Integration Page**: Utility for testing and exploring API capabilities

### Technical Stack

- **Backend**:
  - Python 3.x
  - Flask web framework
  - boto3 (AWS SDK)
  - google-cloud-kubernetes-client
  - kubernetes-client (Python Kubernetes API)
  - YAML and JSON for configuration

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript (ES6+)
  - Bootstrap 5.3.0

## Deployment

### Prerequisites

1. Python 3.6+
2. pip (Python package manager)
3. AWS CLI and Google Cloud SDK
4. Configured cloud provider credentials
5. kubectl (optional, for verification)

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/SubbuK8sConsole.git
   cd SubbuK8sConsole
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Cloud Credentials**:
   - AWS: Configure using AWS CLI or environment variables
   - Google Cloud: Set up Google Cloud authentication
   - Ensure appropriate IAM permissions for cluster access

4. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will start on http://0.0.0.0:8000

### Docker Deployment

1. **Build Docker Image**:
   ```bash
   docker build -t subbu-k8s-console .
   ```

2. **Run Container**:
   ```bash
   docker run -p 8000:8000 \
     -v ~/.aws:/root/.aws \
     -v ~/.config/gcloud:/root/.config/gcloud \
     subbu-k8s-console
   ```

## Usage Guide

### Dashboard Navigation

1. Open the web interface at http://localhost:8000
2. Use the intuitive dashboard to:
   - Add new clusters
   - Discover available clusters
   - View detailed resource information

### Connecting Clusters

1. Click "Add Cluster"
2. Select cloud provider (AWS or GKE)
3. Enter cluster details:
   - Cluster name
   - Region
   - Authentication method
4. Connect and start exploring!

## API Reference

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check application status |
| `/api/clusters` | GET | List connected clusters |
| `/api/clusters/connect` | POST | Connect to a new cluster |
| `/api/clusters/available` | POST | Discover available clusters |
| `/api/clusters/<id>/resources` | GET | Retrieve cluster resources |

## Troubleshooting

### Common Issues

1. **Connection Problems**:
   - Verify cloud provider credentials
   - Check network connectivity
   - Ensure proper IAM permissions

2. **Resource Visibility**:
   - Confirm cluster connection
   - Validate Kubernetes RBAC settings
   - Check authentication configuration

## Security Considerations

1. **Cloud Provider Security**:
   - Use IAM roles with least privilege
   - Implement temporary credentials
   - Secure kubeconfig management

2. **Application Security**:
   - Use HTTPS for all communications
   - Implement authentication
   - Apply rate limiting

## Future Roadmap

- Advanced multi-cluster management
- Enhanced monitoring and metrics
- User authentication system
- More cloud provider integrations
- Advanced resource editing capabilities

## Contributing

Contributions are welcome! Please check our GitHub repository for guidelines on:
- Reporting issues
- Submitting pull requests
- Development setup

## License

[Specify your project's license]

---

**Built with ❤️ for Kubernetes Enthusiasts**
