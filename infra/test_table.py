import pytest
from botocore.exceptions import ClientError
from infra.table_repository import CalculatorRepository

def test_should_set_table_when_initialized():
#   mock_get_dynamo_resource.return_value = get_localstack_dynamo_resource
    repo = CalculatorRepository()
    response = repo.table.meta.client.describe_table(TableName="calculator")
    assert response["Table"]["TableName"] == "calculator"