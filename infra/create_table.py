import boto3

def create_table(endpoint_url="http://localhost:4566", table_name="calculator"):
    dynamodb = boto3.client(
        "dynamodb",
        region_name="sa-east-1",
        endpoint_url=endpoint_url
    )

    try:
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        print(f"Tabela '{table_name}' criada com sucesso!")
    except Exception as e:
        print(e)
