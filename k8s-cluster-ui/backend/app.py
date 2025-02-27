from flask import Flask, jsonify, request, send_from_directory, g
from flask_cors import CORS
import os
import time

# Create a persistent EKS connector that lives outside request context
from eks_connector import EKSConnector
# Create it once at module level instead of per request
persistent_eks_connector = EKSConnector()
print("Created persistent EKS connector")

# Debug print to verify static folder path
static_folder_path = os.path.abspath("../frontend")
print(f"Looking for static files in: {static_folder_path}")

# Initialize Flask app and CORS
app = Flask(__name__, static_folder=static_folder_path, static_url_path="/")
CORS(app, resources={r"/api/*": {"origins": "*"}})  

# Use the persistent connector instead of creating one per request
def get_eks_connector():
    return persistent_eks_connector

# ---------------- FRONTEND ROUTES ----------------
@app.route('/')
def serve_frontend():
    """Serve the main HTML page."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static frontend assets (CSS, JS, images)."""
    return send_from_directory(app.static_folder, path)

# ---------------- API ROUTES ----------------
@app.route('/api/clusters/connect', methods=['POST'])
def connect_cluster():
    """Connect to an EKS cluster using provided credentials"""
    eks_connector = get_eks_connector()
    data = request.json

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    # Required parameters
    cluster_name = data.get('cluster_name')
    region = data.get('region')
    auth_type = data.get('auth_type', 'credentials')

    if not all([cluster_name, region]):
        return jsonify({"success": False, "message": "cluster_name and region are required."}), 400

    if auth_type == 'credentials':
        aws_access_key_id = data.get('aws_access_key_id')
        aws_secret_access_key = data.get('aws_secret_access_key')
        aws_session_token = data.get('aws_session_token')

        if not all([aws_access_key_id, aws_secret_access_key]):
            return jsonify({"success": False, "message": "AWS credentials required."}), 400

        result = eks_connector.connect_with_aws_credentials(cluster_name, region, aws_access_key_id, aws_secret_access_key, aws_session_token)

    elif auth_type == 'profile':
        profile_name = data.get('profile_name', 'default')
        result = eks_connector.connect_with_aws_profile(cluster_name, region, profile_name)

    else:
        return jsonify({"success": False, "message": f"Unsupported auth type: {auth_type}."}), 400

    return jsonify(result), 200 if result["success"] else 500

@app.route('/api/clusters/available', methods=['POST'])
def list_available_clusters():
    """List available EKS clusters in a region"""
    eks_connector = get_eks_connector()
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    region = data.get('region')
    auth_type = data.get('auth_type', 'credentials')

    if not region:
        return jsonify({"success": False, "message": "Region is required."}), 400

    if auth_type == 'credentials':
        aws_access_key_id = data.get('aws_access_key_id')
        aws_secret_access_key = data.get('aws_secret_access_key')
        aws_session_token = data.get('aws_session_token')

        if not all([aws_access_key_id, aws_secret_access_key]):
            return jsonify({"success": False, "message": "AWS credentials required."}), 400

        result = eks_connector.list_available_clusters(region, aws_access_key_id, aws_secret_access_key, aws_session_token)

    elif auth_type == 'profile':
        profile_name = data.get('profile_name', 'default')
        result = eks_connector.list_available_clusters(region, profile_name=profile_name)

    else:
        return jsonify({"success": False, "message": f"Unsupported auth type: {auth_type}."}), 400

    return jsonify(result), 200 if result["success"] else 500

@app.route('/api/clusters', methods=['GET'])
def list_clusters():
    """List all connected clusters"""
    eks_connector = get_eks_connector()
    clusters = eks_connector.list_connected_clusters()
    return jsonify({"success": True, "clusters": clusters}), 200

@app.route('/api/clusters/<connection_id>/disconnect', methods=['POST'])
def disconnect_cluster(connection_id):
    """Disconnect from a cluster"""
    eks_connector = get_eks_connector()
    result = eks_connector.disconnect(connection_id)
    return jsonify(result), 200 if result["success"] else 404

@app.route('/api/clusters/<connection_id>/resources/<resource_type>', methods=['GET'])
def get_resources(connection_id, resource_type):
    """Get resources of a specific type from a connected cluster"""
    eks_connector = get_eks_connector()
    valid_resource_types = ['pods', 'deployments', 'services', 'nodes']
    
    # Debug log
    print(f"Attempting to get {resource_type} for connection {connection_id}")
    print(f"Available connections: {list(eks_connector.connected_clusters.keys())}")
    
    if resource_type not in valid_resource_types:
        return jsonify({"success": False, "message": f"Invalid resource type. Supported: {', '.join(valid_resource_types)}"}), 400

    result = eks_connector.get_resources(connection_id, resource_type)
    return jsonify(result), 200 if result.get("success", False) else 500

# Add this convenience endpoint for pods specifically to match the test.html expectations
@app.route('/api/clusters/<connection_id>/pods', methods=['GET'])
def get_pods(connection_id):
    """Get pods from a connected cluster - convenience endpoint"""
    eks_connector = get_eks_connector()
    result = eks_connector.get_resources(connection_id, 'pods')
    return jsonify(result), 200 if result.get("success", False) else 500

# Add this for testing EKS connectivity
@app.route('/api/test-eks-list', methods=['GET'])
def test_eks_list():
    eks_connector = get_eks_connector()
    result = eks_connector.list_available_clusters(
        region='us-east-1'
        # Using environment credentials
    )
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    response = jsonify({"status": "ok", "message": "API is running"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response, 200

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, threaded=True)