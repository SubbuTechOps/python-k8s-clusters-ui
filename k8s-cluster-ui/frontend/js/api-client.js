/**
 * K8s Cluster API Client
 * 
 * A simple JavaScript client for interacting with the K8s Cluster Management API.
 * This base class provides common functionality for both GKE and EKS clients.
 */
class K8sClusterAPI {
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
export default K8sClusterAPI;