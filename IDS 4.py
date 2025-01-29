import json
import base64
from datetime import datetime
from hedera import (
    Client, 
    TopicCreateTransaction, 
    TopicMessageSubmitTransaction, 
    TopicMessageQuery, 
    Hbar, 
    PrivateKey, 
    AccountId
)
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    return key

def encrypt_message(key, message):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(key, encrypted_message):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

def initialize_client():
    client = Client.for_testnet()
    client.set_operator(AccountId("your-account-id"), PrivateKey.fromString("your-private-key"))
    return client

# Create a new Hedera Topic
def create_topic(client):
    transaction = TopicCreateTransaction().set_max_transaction_fee(Hbar(2))
    response = transaction.execute(client)
    receipt = response.get_receipt(client)
    topic_id = receipt.topic_id
    print(f"Topic Created: {topic_id}")
    return topic_id

# Send message to a Hedera Topic
def send_message(client, topic_id, message, key):
    encrypted_message = encrypt_message(key, message)
    transaction = TopicMessageSubmitTransaction() \
        .set_topic_id(topic_id) \
        .set_message(base64.b64encode(encrypted_message).decode())
    response = transaction.execute(client)
    print(f"Message Sent: '{message}' at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Retrieve messages from a Hedera Topic
def retrieve_messages(client, topic_id, key):
    query = TopicMessageQuery().set_topic_id(topic_id).set_start_time(datetime(2024, 12, 27, 10, 0, 0))
    messages = query.execute(client)
    print("Messages Received:")
    for message in messages:
        encrypted_message = base64.b64decode(message.message)
        decrypted_message = decrypt_message(key, encrypted_message)
        timestamp = message.consensus_timestamp.to_string()
        print(f"{decrypted_message} at {timestamp}")

def filter_messages(messages, keyword):
    filtered_messages = [msg for msg in messages if keyword.lower() in msg.lower()]
    return filtered_messages

def main():
    client = initialize_client()
    topic_id = create_topic(client)
    
    encryption_key = generate_key()

    send_message(client, topic_id, "Hello, Hedera!", encryption_key)
    send_message(client, topic_id, "Learning HCS", encryption_key)
    send_message(client, topic_id, "Message 3", encryption_key)

    messages = retrieve_messages(client, topic_id, encryption_key)

    filtered_messages = filter_messages(messages, "Hedera")
    print("\nFiltered Messages:")
    for msg in filtered_messages:
        print(msg)

if __name__ == "__main__":
    main()
