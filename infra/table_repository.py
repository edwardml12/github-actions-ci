import boto3
from botocore.exceptions import ClientError
import os

class CalculatorRepository():
    def __init__(self):
        dynamo =  boto3.resource(
            "dynamodb",
            endpoint_url="http://localhost:4566",
            region_name=os.getenv("AWS_REGION", "sa-east-1")
        )
        self.table = dynamo.Table("calculator")

    def table_exists(self, table_name: str) -> bool:
        # dynamodb = boto3.client("dynamodb", region_name="us-east-1")
        try:
            print("_________________self.table_________________")
            print(self.table)
            self.table.describe_table(TableName=table_name)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                return False
            raise  # unexpected error