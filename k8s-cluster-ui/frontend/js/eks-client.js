/**
 * K8s Cluster API Client for AWS EKS
 * 
 * A simple JavaScript client for interacting with the K8s Cluster Management API.
 * This can be included in your frontend application.
 */
class EKSClusterAPI {
    /**
     * Initialize the API client
     * @param {string} baseUrl - Base URL for the API
     */
    constructor(baseUrl = '/api') {  // Changed from 'http://localhost:5000/api'
        this.baseUrl = baseUrl;
    }

    /**
     * Make an API request
     * @param {string} endpoint - API endpoint
     * @param {string} method - HTTP method
     * @param {object} data - Request data (for POST requests)
     * @returns {Promise<object>} - Response data
     */
    async _request(endpoint, method = 'GET', data = null) {
        const url = `${this.baseUrl}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (data && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            const responseData = await response.json();

            if (!response.ok) {
                throw new Error(responseData.message || 'API request failed');
            }

            return responseData;
        } catch (error) {
            console.error(`API Error (${method} ${endpoint}):`, error);
            throw error;
        }
    }

    /**
     * Connect to an EKS cluster using AWS credentials
     * @param {object} clusterConfig - Cluster configuration with AWS credentials
     * @returns {Promise<object>} - Connection result
     */
    async connectClusterWithCredentials(clusterName, region, accessKeyId, secretAccessKey, sessionToken = null) {
        const config = {
            cluster_name: clusterName,
            region: region,
            auth_type: 'credentials',
            aws_access_key_id: accessKeyId,
            aws_secret_access_key: secretAccessKey
        };
        
        if (sessionToken) {
            config.aws_session_token = sessionToken;
        }
        
        return this._request('/clusters/connect', 'POST', config);
    }
    
    /**
     * Connect to an EKS cluster using AWS profile
     * @param {string} clusterName - Name of the EKS cluster
     * @param {string} region - AWS region
     * @param {string} profileName - AWS profile name
     * @returns {Promise<object>} - Connection result
     */
    async connectClusterWithProfile(clusterName, region, profileName = 'default') {
        return this._request('/clusters/connect', 'POST', {
            cluster_name: clusterName,
            region: region,
            auth_type: 'profile',
            profile_name: profileName
        });
    }
    
    /**
     * List available EKS clusters in a region using AWS credentials
     * @param {string} region - AWS region
     * @param {string} accessKeyId - AWS access key ID
     * @param {string} secretAccessKey - AWS secret access key
     * @param {string} sessionToken - AWS session token (optional)
     * @returns {Promise<object>} - List of available clusters
     */
    async listAvailableClustersWithCredentials(region, accessKeyId, secretAccessKey, sessionToken = null) {
        const config = {
            region: region,
            auth_type: 'credentials',
            aws_access_key_id: accessKeyId,
            aws_secret_access_key: secretAccessKey
        };
        
        if (sessionToken) {
            config.aws_session_token = sessionToken;
        }
        
        return this._request('/clusters/available', 'POST', config);
    }
    
    /**
     * List available EKS clusters in a region using AWS profile
     * @param {string} region - AWS region
     * @param {string} profileName - AWS profile name
     * @returns {Promise<object>} - List of available clusters
     */
    async listAvailableClustersWithProfile(region, profileName = 'default') {
        return this._request('/clusters/available', 'POST', {
            region: region,
            auth_type: 'profile',
            profile_name: profileName
        });
    }

    /**
     * List connected clusters
     * @returns {Promise<object>} - List of connected clusters
     */
    async listClusters() {
        return this._request('/clusters');
    }

    /**
     * Disconnect from a cluster
     * @param {string} connectionId - Connection ID
     * @returns {Promise<object>} - Disconnection result
     */
    async disconnectCluster(connectionId) {
        return this._request(`/clusters/${connectionId}/disconnect`, 'POST');
    }

    /**
     * Get resources from a cluster
     * @param {string} connectionId - Connection ID
     * @param {string} resourceType - Resource type (pods, deployments, services, nodes)
     * @returns {Promise<object>} - Resources data
     */
    async getResources(connectionId, resourceType) {
        return this._request(`/clusters/${connectionId}/resources/${resourceType}`);
    }

    /**
     * Check API health
     * @returns {Promise<object>} - Health status
     */
    async checkHealth() {
        return this._request('/health');
    }
}

// Export the API client
export default EKSClusterAPI;