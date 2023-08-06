import logging
import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError, WaiterError
from botocore.waiter import Waiter


class AwsHelper:
    _logger = logging.getLogger(__name__)

    def __init__(self):
        pass
