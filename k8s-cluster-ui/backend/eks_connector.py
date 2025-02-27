import boto3
from kubernetes import client, config
import os
import yaml
import base64
import tempfile
import json
from botocore.exceptions import ClientError

class EKSConnector:
    def __init__(self):
        self.connected_clusters = {}
        print("EKSConnector initialized")
        
    def connect_with_aws_credentials(self, cluster_name, region, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None):
        """
        Connect to an EKS cluster using AWS credentials.
        
        Args:
            cluster_name (str): Name of the EKS cluster
            region (str): AWS region where the cluster is located
            aws_access_key_id (str, optional): AWS access key ID
            aws_secret_access_key (str, optional): AWS secret access key
            aws_session_token (str, optional): AWS session token (for temporary credentials)
            
        Returns:
            dict: Connection result with success status and message
        """
        print(f"Attempting to connect to cluster '{cluster_name}' in region '{region}'")
        try:
            # Initialize AWS session
            session_kwargs = {
                'region_name': region
            }
            
            # Add credentials if provided
            if aws_access_key_id and aws_secret_access_key:
                session_kwargs['aws_access_key_id'] = aws_access_key_id
                session_kwargs['aws_secret_access_key'] = aws_secret_access_key
                if aws_session_token:
                    session_kwargs['aws_session_token'] = aws_session_token
                print(f"Using provided AWS credentials (Access Key ID: {aws_access_key_id[:4]}...)")
            else:
                print("No AWS credentials provided")
            
            # Create boto3 session
            print("Creating boto3 session...")
            session = boto3.Session(**session_kwargs)
            
            # Create EKS client
            print("Creating EKS client...")
            eks_client = session.client('eks')
            
            # Get cluster info
            print(f"Retrieving cluster info for '{cluster_name}'...")
            cluster = eks_client.describe_cluster(name=cluster_name)
            cluster_info = cluster['cluster']
            print(f"Cluster info retrieved successfully. Version: {cluster_info.get('version')}, Status: {cluster_info.get('status')}")
            
            # Generate kubeconfig for the cluster
            print("Generating kubeconfig...")
            kubeconfig = self._generate_kubeconfig(cluster_info, session)
            
            # Load the kubeconfig
            print("Loading kubeconfig...")
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(yaml.dump(kubeconfig).encode())
                temp_file_path = temp_file.name
            
            # Load the configuration
            config.load_kube_config(config_file=temp_file_path)
            os.unlink(temp_file_path)
            
            # Initialize the API client
            print("Initializing Kubernetes API client...")
            api_client = client.ApiClient()
            
            # Test connection by listing namespaces
            print("Testing connection by listing namespaces...")
            v1 = client.CoreV1Api(api_client)
            namespaces = v1.list_namespace()
            print(f"Connection successful. Found {len(namespaces.items)} namespaces.")
            
            # Store the client for later use
            connection_id = f"{region}_{cluster_name}"
            self.connected_clusters[connection_id] = {
                "api_client": api_client,
                "cluster_info": {
                    "name": cluster_name,
                    "region": region,
                    "version": cluster_info.get('version'),
                    "status": cluster_info.get('status'),
                    "endpoint": cluster_info.get('endpoint')
                }
            }
            
            return {
                "success": True,
                "message": f"Successfully connected to cluster {cluster_name}",
                "connection_id": connection_id
            }
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            print(f"AWS ClientError: {error_code} - {error_message}")
            return {
                "success": False,
                "message": f"AWS Error ({error_code}): {error_message}"
            }
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to connect to cluster: {str(e)}"
            }
            
    def connect_with_aws_profile(self, cluster_name, region, profile_name="default"):
        """
        Connect to an EKS cluster using an AWS profile.
        
        Args:
            cluster_name (str): Name of the EKS cluster
            region (str): AWS region where the cluster is located
            profile_name (str, optional): AWS profile name in ~/.aws/credentials
            
        Returns:
            dict: Connection result with success status and message
        """
        print(f"Attempting to connect to cluster '{cluster_name}' in region '{region}' using profile '{profile_name}'")
        try:
            # Create boto3 session with profile
            print(f"Creating boto3 session with profile '{profile_name}'...")
            session = boto3.Session(profile_name=profile_name, region_name=region)
            
            # Create EKS client
            print("Creating EKS client...")
            eks_client = session.client('eks')
            
            # Get cluster info
            print(f"Retrieving cluster info for '{cluster_name}'...")
            cluster = eks_client.describe_cluster(name=cluster_name)
            cluster_info = cluster['cluster']
            print(f"Cluster info retrieved successfully. Version: {cluster_info.get('version')}, Status: {cluster_info.get('status')}")
            
            # Generate kubeconfig for the cluster
            print("Generating kubeconfig...")
            kubeconfig = self._generate_kubeconfig(cluster_info, session)
            
            # Load the kubeconfig
            print("Loading kubeconfig...")
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(yaml.dump(kubeconfig).encode())
                temp_file_path = temp_file.name
            
            # Load the configuration
            config.load_kube_config(config_file=temp_file_path)
            os.unlink(temp_file_path)
            
            # Initialize the API client
            print("Initializing Kubernetes API client...")
            api_client = client.ApiClient()
            
            # Test connection by listing namespaces
            print("Testing connection by listing namespaces...")
            v1 = client.CoreV1Api(api_client)
            namespaces = v1.list_namespace()
            print(f"Connection successful. Found {len(namespaces.items)} namespaces.")
            
            # Store the client for later use
            connection_id = f"{region}_{cluster_name}"
            self.connected_clusters[connection_id] = {
                "api_client": api_client,
                "cluster_info": {
                    "name": cluster_name,
                    "region": region,
                    "version": cluster_info.get('version'),
                    "status": cluster_info.get('status'),
                    "endpoint": cluster_info.get('endpoint')
                }
            }
            
            return {
                "success": True,
                "message": f"Successfully connected to cluster {cluster_name}",
                "connection_id": connection_id
            }
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            print(f"AWS ClientError: {error_code} - {error_message}")
            return {
                "success": False,
                "message": f"AWS Error ({error_code}): {error_message}"
            }
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to connect to cluster: {str(e)}"
            }
    
    def list_available_clusters(self, region, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, profile_name=None):
        """
        List available EKS clusters in the specified region.
        
        Args:
            region (str): AWS region
            aws_access_key_id (str, optional): AWS access key ID
            aws_secret_access_key (str, optional): AWS secret access key
            aws_session_token (str, optional): AWS session token
            profile_name (str, optional): AWS profile name
            
        Returns:
            dict: List of available clusters
        """
        print(f"Attempting to list clusters in region '{region}'")
        try:
            # Initialize AWS session
            session_kwargs = {
                'region_name': region
            }
            
            # Add credentials if provided
            if profile_name:
                session_kwargs['profile_name'] = profile_name
                print(f"Using AWS profile: {profile_name}")
            elif aws_access_key_id and aws_secret_access_key:
                session_kwargs['aws_access_key_id'] = aws_access_key_id
                session_kwargs['aws_secret_access_key'] = aws_secret_access_key
                if aws_session_token:
                    session_kwargs['aws_session_token'] = aws_session_token
                print(f"Using AWS credentials (Access Key ID: {aws_access_key_id[:4]}...)")
            else:
                print("No AWS credentials or profile provided, using instance role or environment variables")
            
            # Create boto3 session
            print("Creating boto3 session...")
            session = boto3.Session(**session_kwargs)
            
            # Create EKS client
            print("Creating EKS client...")
            eks_client = session.client('eks')
            
            # List clusters
            print("Calling list_clusters API...")
            clusters = eks_client.list_clusters()
            cluster_names = clusters['clusters']
            print(f"Found {len(cluster_names)} clusters: {cluster_names}")
            
            # Get details for each cluster
            cluster_details = []
            for cluster_name in cluster_names:
                try:
                    print(f"Getting details for cluster '{cluster_name}'...")
                    cluster_info = eks_client.describe_cluster(name=cluster_name)['cluster']
                    created_at = cluster_info.get('createdAt')
                    created_at_str = created_at.isoformat() if created_at else None
                    
                    cluster_details.append({
                        "name": cluster_name,
                        "status": cluster_info.get('status'),
                        "version": cluster_info.get('version'),
                        "endpoint": cluster_info.get('endpoint'),
                        "created_at": created_at_str
                    })
                    print(f"Successfully retrieved details for cluster '{cluster_name}'")
                except Exception as e:
                    print(f"Error getting details for cluster '{cluster_name}': {str(e)}")
                    # Skip clusters that we can't get details for
                    continue
            
            print(f"Returning details for {len(cluster_details)} clusters")
            return {
                "success": True,
                "region": region,
                "clusters": cluster_details,
                "count": len(cluster_details)
            }
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            print(f"AWS ClientError when listing clusters: {error_code} - {error_message}")
            return {
                "success": False,
                "message": f"AWS Error ({error_code}): {error_message}"
            }
        except Exception as e:
            print(f"Unexpected error when listing clusters: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "message": f"Failed to list clusters: {str(e)}"
            }
    
    def get_resources(self, connection_id, resource_type):
        """
        Get resources of specified type from the connected cluster.
        
        Args:
            connection_id (str): ID of the connected cluster
            resource_type (str): Type of the resource (pods, deployments, services, nodes)
            
        Returns:
            dict: Resources data or error message
        """
        print(f"Getting resources of type '{resource_type}' for connection '{connection_id}'")
        if connection_id not in self.connected_clusters:
            print(f"Connection '{connection_id}' not found")
            return {
                "success": False,
                "message": "Cluster not connected"
            }
        
        try:
            api_client = self.connected_clusters[connection_id]["api_client"]
            
            if resource_type == "pods":
                print("Listing pods...")
                api = client.CoreV1Api(api_client)
                resources = api.list_pod_for_all_namespaces()
                print(f"Found {len(resources.items)} pods")
                return self._format_resources(resources.items, resource_type)
            
            elif resource_type == "deployments":
                print("Listing deployments...")
                api = client.AppsV1Api(api_client)
                resources = api.list_deployment_for_all_namespaces()
                print(f"Found {len(resources.items)} deployments")
                return self._format_resources(resources.items, resource_type)
            
            elif resource_type == "services":
                print("Listing services...")
                api = client.CoreV1Api(api_client)
                resources = api.list_service_for_all_namespaces()
                print(f"Found {len(resources.items)} services")
                return self._format_resources(resources.items, resource_type)
            
            elif resource_type == "nodes":
                print("Listing nodes...")
                api = client.CoreV1Api(api_client)
                resources = api.list_node()
                print(f"Found {len(resources.items)} nodes")
                return self._format_resources(resources.items, resource_type)
            
            else:
                print(f"Unsupported resource type: {resource_type}")
                return {
                    "success": False,
                    "message": f"Unsupported resource type: {resource_type}"
                }
                
        except Exception as e:
            print(f"Error getting resources: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to get resources: {str(e)}"
            }
    
    def disconnect(self, connection_id):
        """
        Disconnect from a cluster.
        
        Args:
            connection_id (str): ID of the connected cluster
            
        Returns:
            dict: Disconnection result with success status and message
        """
        print(f"Disconnecting from cluster with connection ID '{connection_id}'")
        if connection_id in self.connected_clusters:
            cluster_info = self.connected_clusters[connection_id]["cluster_info"]
            del self.connected_clusters[connection_id]
            print(f"Successfully disconnected from cluster '{cluster_info['name']}'")
            return {
                "success": True,
                "message": f"Disconnected from cluster {cluster_info['name']}"
            }
        else:
            print(f"Connection '{connection_id}' not found")
            return {
                "success": False,
                "message": "Cluster not connected"
            }
    
    def list_connected_clusters(self):
        """
        List all connected clusters.
        
        Returns:
            list: List of connected clusters with their information
        """
        print(f"Listing connected clusters. Currently connected to {len(self.connected_clusters)} clusters")
        return [
            {
                "connection_id": conn_id,
                "cluster_info": cluster_data["cluster_info"]
            }
            for conn_id, cluster_data in self.connected_clusters.items()
        ]
    
    def _generate_kubeconfig(self, cluster_info, aws_session):
        """
        Generate a kubeconfig for connecting to the EKS cluster.
        
        Args:
            cluster_info: EKS cluster info
            aws_session: boto3 session
            
        Returns:
            dict: Kubeconfig data
        """
        cluster_name = cluster_info['name']
        cluster_endpoint = cluster_info['endpoint']
        cluster_ca = cluster_info['certificateAuthority']['data']
        cluster_arn = cluster_info['arn']
        region = cluster_arn.split(':')[3]
        
        print(f"Generating kubeconfig for cluster '{cluster_name}' in region '{region}'")
        
        # Create a kubeconfig
        kubeconfig = {
            "apiVersion": "v1",
            "kind": "Config",
            "current-context": cluster_name,
            "clusters": [
                {
                    "name": cluster_name,
                    "cluster": {
                        "server": cluster_endpoint,
                        "certificate-authority-data": cluster_ca
                    }
                }
            ],
            "contexts": [
                {
                    "name": cluster_name,
                    "context": {
                        "cluster": cluster_name,
                        "user": "aws"
                    }
                }
            ],
            "users": [
                {
                    "name": "aws",
                    "user": {
                        "exec": {
                            "apiVersion": "client.authentication.k8s.io/v1beta1",
                            "command": "aws",
                            "args": [
                                "eks",
                                "get-token",
                                "--cluster-name",
                                cluster_name,
                                "--region",
                                region
                            ]
                        }
                    }
                }
            ]
        }
        
        # Add profile if it exists - safely check for profile_name
        try:
            profile_name = None
            # Try to get profile name safely
            if hasattr(aws_session, '_session'):
                if hasattr(aws_session._session, 'profile_name'):
                    profile_name = aws_session._session.profile_name
            
            # Alternative method to get profile name if above doesn't work
            if profile_name is None and hasattr(aws_session, 'profile_name'):
                profile_name = aws_session.profile_name
                
            if profile_name:
                print(f"Adding profile '{profile_name}' to kubeconfig")
                kubeconfig["users"][0]["user"]["exec"]["args"].extend(["--profile", profile_name])
        except Exception as e:
            print(f"Warning: Couldn't add profile to kubeconfig: {str(e)}")
            # Continue without profile - will use default credentials
        
        return kubeconfig
    
    def _format_resources(self, items, resource_type):
        """
        Format resources for API response.
        
        Args:
            items: List of resource items
            resource_type: Type of the resource
            
        Returns:
            dict: Formatted resources
        """
        formatted_items = []
        
        for item in items:
            if resource_type == "pods":
                formatted_items.append({
                    "name": item.metadata.name,
                    "namespace": item.metadata.namespace,
                    "status": item.status.phase,
                    "containers": [cont.name for cont in item.spec.containers],
                    "node": item.spec.node_name if item.spec.node_name else "Not scheduled",
                    "created_at": item.metadata.creation_timestamp.isoformat() if item.metadata.creation_timestamp else None
                })
            
            elif resource_type == "deployments":
                formatted_items.append({
                    "name": item.metadata.name,
                    "namespace": item.metadata.namespace,
                    "replicas": item.spec.replicas,
                    "available_replicas": item.status.available_replicas if item.status.available_replicas else 0,
                    "created_at": item.metadata.creation_timestamp.isoformat() if item.metadata.creation_timestamp else None
                })
            
            elif resource_type == "services":
                formatted_items.append({
                    "name": item.metadata.name,
                    "namespace": item.metadata.namespace,
                    "type": item.spec.type,
                    "cluster_ip": item.spec.cluster_ip,
                    "ports": [{"port": port.port, "target_port": port.target_port, "protocol": port.protocol} for port in item.spec.ports],
                    "created_at": item.metadata.creation_timestamp.isoformat() if item.metadata.creation_timestamp else None
                })
            
            elif resource_type == "nodes":
                conditions = {cond.type: cond.status for cond in item.status.conditions}
                formatted_items.append({
                    "name": item.metadata.name,
                    "status": "Ready" if conditions.get("Ready") == "True" else "NotReady",
                    "roles": [label.split("node-role.kubernetes.io/")[1] for label in item.metadata.labels.keys() if "node-role.kubernetes.io/" in label] if item.metadata.labels else [],
                    "instance_type": item.metadata.labels.get("node.kubernetes.io/instance-type", "Unknown"),
                    "zone": item.metadata.labels.get("topology.kubernetes.io/zone", "Unknown"),
                    "kubelet_version": item.status.node_info.kubelet_version,
                    "created_at": item.metadata.creation_timestamp.isoformat() if item.metadata.creation_timestamp else None
                })
        
        return {
            "success": True,
            "resource_type": resource_type,
            "count": len(formatted_items),
            "items": formatted_items
        }