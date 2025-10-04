# create_tables.py
import boto3
import time

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://dynamodb:8000",
    region_name="us-west-2",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

def create_tables():
    print (dynamodb.meta.client.list_tables())
    existing = [c for c in dynamodb.meta.client.list_tables()["TableNames"]]
    # ChatSessions table: единствен chat_id
    if "ChatSessions" not in existing:
        print("Creating ChatSessions table...")
        table = dynamodb.create_table(
            TableName="ChatSessions",
            KeySchema=[{"AttributeName": "chat_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "chat_id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.wait_until_exists()

    # Messages table: partition by chat_id, sort by created_at (timestamp)
    if "Messages" not in existing:
        print("Creating Messages table...")
        table2 = dynamodb.create_table(
            TableName="Messages",
            KeySchema=[
                {"AttributeName": "chat_id", "KeyType": "HASH"},
                {"AttributeName": "created_at", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "chat_id", "AttributeType": "S"},
                {"AttributeName": "created_at", "AttributeType": "N"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table2.wait_until_exists()

    print("Tables ready.")

if __name__ == "__main__":
    create_tables()
