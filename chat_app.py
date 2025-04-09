import threading
import time
from datetime import datetime

# Message structure
class Message:
    def __init__(self, sender_id, recipient_id, content):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.content = content

# User class
class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def send_message(self, recipient_id, content, message_history, history_lock):
        msg = Message(self.user_id, recipient_id, content)
        with history_lock:
            message_history.append(msg)
            print(f"[{msg.timestamp}] {self.user_id} -> {recipient_id}: {content}")

# Initialize global data
message_history = []
history_lock = threading.Lock()

# Display all messages
def display_all_messages():
    with history_lock:
        print("\n--- Message History ---")
        for msg in message_history:
            print(f"[{msg.timestamp}] {msg.sender_id} -> {msg.recipient_id}: {msg.content}")
        print("------------------------")

# Search messages by user ID
def search_by_user_id(user_id):
    with history_lock:
        print(f"\n--- Messages for User: {user_id} ---")
        for msg in message_history:
            if msg.sender_id == user_id or msg.recipient_id == user_id:
                print(f"[{msg.timestamp}] {msg.sender_id} -> {msg.recipient_id}: {msg.content}")
        print("-----------------------------")

# Case-insensitive keyword search
def search_by_keyword(keyword):
    keyword_lower = keyword.lower()
    with history_lock:
        print(f"\n--- Messages containing keyword: \"{keyword}\" ---")
        for msg in message_history:
            if keyword_lower in msg.content.lower():
                print(f"[{msg.timestamp}] {msg.sender_id} -> {msg.recipient_id}: {msg.content}")
        print("---------------------------------------------")

# Display all user IDs
def display_user_ids(users):
    print("\n--- Available User IDs ---")
    for user in users:
        print(user.user_id)
    print("---------------------------")

# Simulate threaded user messaging
def simulate_user(user, recipients, messages):
    for i, content in enumerate(messages):
        recipient = recipients[i % len(recipients)]
        user.send_message(recipient, content, message_history, history_lock)
        time.sleep(0.1)

# Main UI loop
def chat_ui(users):
    while True:
        print("\n--- Chat Menu ---")
        print("1. Send Message")
        print("2. Display All Messages")
        print("3. Search by User ID")
        print("4. Search by Keyword")
        print("5. Display All User IDs")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        choice = int(choice)

        if choice == 1:
            sender_id = input("Enter Sender ID: ")
            recipient_id = input("Enter Recipient ID: ")
            content = input("Enter Message: ")

            sender = next((u for u in users if u.user_id == sender_id), None)
            if sender:
                sender.send_message(recipient_id, content, message_history, history_lock)
            else:
                print("Sender not found.")

        elif choice == 2:
            display_all_messages()

        elif choice == 3:
            user_id = input("Enter User ID to search: ")
            search_by_user_id(user_id)

        elif choice == 4:
            keyword = input("Enter keyword to search: ")
            search_by_keyword(keyword)

        elif choice == 5:
            display_user_ids(users)

        elif choice == 6:
            print("Exiting chat...")
            break

        else:
            print("Invalid choice. Try again.")


    
