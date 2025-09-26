# test_dynamo.py
from dynamo_helpers import create_chat, add_message, get_messages, list_chats

chat_id = create_chat("Test chat")
print("chat_id:", chat_id)
add_message(chat_id, "user", "Hello, this is a test")
add_message(chat_id, "assistant", "Hi — I am a test reply")
print("messages:", get_messages(chat_id))
print("all chats:", list_chats())
