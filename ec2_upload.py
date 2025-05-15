import boto3
import os
import time
from botocore.exceptions import ClientError

# Configuration
KEY_NAME = "MyPokemonKeyPair"
PEM_FILE_PATH = os.path.expanduser(f"~/Desktop/{KEY_NAME}.pem")
SECURITY_GROUP_NAME = "MyPokemonSecurityGroup"
INSTANCE_NAME = "MyPokemonInstance"
REGION = "us-west-2"
AMI_ID = "ami-04999cd8f2624f834"
INSTANCE_TYPE = "t2.micro"

ec2 = boto3.client("ec2", region_name=REGION)

# 1. Create key pair
try:
    print(f"Creating key pair '{KEY_NAME}'...")
    key_pair = ec2.create_key_pair(KeyName=KEY_NAME)
    private_key = key_pair['KeyMaterial']
    with open(PEM_FILE_PATH, 'w') as file:
        file.write(private_key)
    os.chmod(PEM_FILE_PATH, 0o400)
    print(f"Saved key to {PEM_FILE_PATH}")
except ClientError as e:
    if 'InvalidKeyPair.Duplicate' in str(e):
        print(f"Key pair '{KEY_NAME}' already exists. Skipping key creation.")
    else:
        raise

# 2. Create security group
try:
    print(f"Creating security group '{SECURITY_GROUP_NAME}'...")
    vpc_id = ec2.describe_vpcs()['Vpcs'][0]['VpcId']
    response = ec2.create_security_group(
        GroupName=SECURITY_GROUP_NAME,
        Description='Security group for SSH access',
        VpcId=vpc_id
    )
    sg_id = response['GroupId']
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )
    print(f"Security group created: {sg_id}")
except ClientError as e:
    if 'InvalidGroup.Duplicate' in str(e):
        sg_id = ec2.describe_security_groups(
            Filters=[{'Name': 'group-name', 'Values': [SECURITY_GROUP_NAME]}]
        )['SecurityGroups'][0]['GroupId']
        print(f"Security group already exists. Using: {sg_id}")
    else:
        raise

# 3. User data script
user_data_script = '''#!/bin/bash
yum update -y
yum install -y git python3
cd /home/ec2-user
git clone https://github.com/zivorimon/pokeapi.2025.git
'''

# 4. Launch instance
print("Launching EC2 instance...")
instances = ec2.run_instances(
    ImageId=AMI_ID,
    InstanceType=INSTANCE_TYPE,
    KeyName=KEY_NAME,
    MaxCount=1,
    MinCount=1,
    SecurityGroupIds=[sg_id],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}]
        }
    ],
    UserData=user_data_script
)

instance_id = instances['Instances'][0]['InstanceId']
print(f"Instance created with ID: {instance_id}")

# 5. Wait and get public IP
ec2_resource = boto3.resource("ec2", region_name=REGION)
instance = ec2_resource.Instance(instance_id)
print("Waiting for instance to be running...")
instance.wait_until_running()
instance.reload()
public_ip = instance.public_ip_address
print(f"Public IP: {public_ip}")
