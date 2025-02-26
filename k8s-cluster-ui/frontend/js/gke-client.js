import K8sClusterAPI from './api-client.js';

/**
 * GKE Cluster API Client
 * 
 * A JavaScript client for interacting with GKE clusters.
 */
class GKEClusterAPI extends K8sClusterAPI {
    /**
     * Connect to a GKE cluster using a service account key
     * @param {string} clusterName - Name of the GKE cluster
     * @param {string} projectId - Google Cloud project ID
     * @param {string} zone - Zone where the cluster is located
     * @param {string} serviceAccountKey - Service account key JSON string
     * @returns {Promise<object>} - Connection result
     */
    async connectCluster(clusterName, projectId, zone, serviceAccountKey) {
        return this._request('/clusters/connect', 'POST', {
            cluster_name: clusterName,
            project_id: projectId,
            zone: zone,
            auth_type: 'service_account',
            service_account_key: serviceAccountKey
        });
    }
    
    /**
     * Connect to a GKE cluster using gcloud credentials
     * @param {string} clusterName - Name of the GKE cluster
     * @param {string} projectId - Google Cloud project ID
     * @param {string} zone - Zone where the cluster is located
     * @returns {Promise<object>} - Connection result
     */
    async connectWithGcloudCredentials(clusterName, projectId, zone) {
        return this._request('/clusters/connect', 'POST', {
            cluster_name: clusterName,
            project_id: projectId,
            zone: zone,
            auth_type: 'gcloud'
        });
    }
    
    /**
     * List available projects
     * @returns {Promise<object>} - List of available GCP projects
     */
    async listProjects() {
        return this._request('/projects', 'GET');
    }
    
    /**
     * List available zones for a project
     * @param {string} projectId - Google Cloud project ID
     * @returns {Promise<object>} - List of available zones
     */
    async listZones(projectId) {
        return this._request(`/projects/${projectId}/zones`, 'GET');
    }
    
    /**
     * List available clusters in a project and zone
     * @param {string} projectId - Google Cloud project ID
     * @param {string} zone - Zone to check for clusters
     * @param {string} serviceAccountKey - Service account key JSON string (optional)
     * @returns {Promise<object>} - List of available clusters
     */
    async listAvailableClusters(projectId, zone, serviceAccountKey = null) {
        const requestData = {
            project_id: projectId,
            zone: zone
        };
        
        if (serviceAccountKey) {
            requestData.auth_type = 'service_account';
            requestData.service_account_key = serviceAccountKey;
        } else {
            requestData.auth_type = 'gcloud';
        }
        
        return this._request('/clusters/available', 'POST', requestData);
    }
}

// Initialize the API client
const gkeClient = new GKEClusterAPI();

// Make it available globally
window.gkeClient = gkeClient;

// Export the API client
export default GKEClusterAPI;