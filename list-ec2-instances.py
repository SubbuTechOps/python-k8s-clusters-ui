import boto3

def list_running_ec2_instances():
    # Create EC2 client
    ec2 = boto3.client('ec2')
    
    # Get instances with running state
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    
    # Process the response
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}")
            print(f"Instance Type: {instance['InstanceType']}")
            print(f"Launch Time: {instance['LaunchTime']}")
            
            # Get instance name if it exists
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        print(f"Name: {tag['Value']}")
            
            print(f"Public IP: {instance.get('PublicIpAddress', 'N/A')}")
            print(f"Private IP: {instance['PrivateIpAddress']}")
            print("-" * 50)

if __name__ == "__main__":
    try:
        list_running_ec2_instances()
    except Exception as e:
        print(f"Error: {str(e)}")
