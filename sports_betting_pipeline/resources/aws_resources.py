# resources/aws_resources.py
from dagster import resource
from sports_betting_pipeline.utils.aws_helpers import get_secret


@resource
def aws_secret_manager_resource(context):
    """
    Dagster resource to wrap the `get_secret` utility function.
    Adds logging and context-specific behavior.
    """

    def wrapped_get_secret(secret_name):
        return get_secret(secret_name)

    # Return the wrapped utility function
    return wrapped_get_secret
