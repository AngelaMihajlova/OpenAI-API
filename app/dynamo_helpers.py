# dynamo_helpers.py
import boto3
import time
import uuid
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://dynamodb:8000",
    region_name="us-west-2",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

CHAT_TABLE = dynamodb.Table("ChatSessions")
MSG_TABLE  = dynamodb.Table("Messages")

def create_chat(title: str = "New chat") -> str:
    chat_id = str(uuid.uuid4())
    now = int(time.time())
    CHAT_TABLE.put_item(Item={
        "chat_id": chat_id,
        "title": title,
        "created_at": now
    })
    return chat_id

def list_chats(limit: int = 50):
    resp = CHAT_TABLE.scan(Limit=limit)
    return resp.get("Items", [])

def add_message(chat_id: str, role: str, content):
    """
    Додава порака во DynamoDB.
    content може да биде string, dict или list.
    """
    created_at = int(time.time() * 1000)
    # Ако content е dict или list, ќе се претвори во JSON string
    if isinstance(content, (dict, list)):
        content = json.dumps(content)
    MSG_TABLE.put_item(Item={
        "chat_id": chat_id,
        "created_at": created_at,
        "role": role,
        "content": content
    })

def get_messages(chat_id: str, limit: int = 100):
    resp = MSG_TABLE.query(
        KeyConditionExpression=Key("chat_id").eq(chat_id),
        ScanIndexForward=True,   # ascending by created_at
        Limit=limit
    )
    # Ако сакаш, можеме автоматски да го конвертираме JSON string назад во dict/list
    for item in resp.get("Items", []):
        try:
            item["content"] = json.loads(item["content"])
        except (json.JSONDecodeError, TypeError):
            pass
    return resp.get("Items", [])

def delete_chat(chat_id: str):
    """
    Брише chat и сите пораки поврзани со него.
    """
    # прво бриши пораки
    msgs = get_messages(chat_id)
    for msg in msgs:
        MSG_TABLE.delete_item(
            Key={
                "chat_id": msg["chat_id"],
                "created_at": msg["created_at"]
            }
        )
    # потоа бриши сам chat
    CHAT_TABLE.delete_item(
        Key={"chat_id": chat_id}
    )
