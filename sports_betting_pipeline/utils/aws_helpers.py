import boto3
import json

def get_secret(secret_name:str, region_name='us-east-1') -> dict:
    """Retrieves a secret from AWS Secrets Manager

    Args:
        secret_name (str): The secret name
        region_name (str, optional): The AWS region where the secret is stored. Defaults to 'us-east-1'.
    
    Returns:
        dict: The parsed JSON secret
    """

    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        
        if "SecretString" in response:
            return json.loads(response['SecretString'])
        else:
            raise ValueError("SecretBinary format not supported")
    except Exception as e:
        raise RuntimeError(f"Failed to retreive secret '{secret_name}': {e}")
        