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

# Entry point of the program
if __name__ == "__main__":
    # Create users
    user1 = User("Alice")
    user2 = User("Bob")
    user3 = User("Charlie")
    user4 = User("Dave")
    user5 = User("Eve")

    users = [user1, user2, user3, user4, user5]

    # Predefined messages
    messages1 = ["Hello Bob!", "How are you?", "Let's catch up soon."]
    messages2 = ["Hi Alice!", "I'm good, thanks.", "Sure, sounds great."]
    messages3 = ["Hey Alice and Bob!", "What are you guys up to?", "Join me for a game?"]
    messages4 = ["Dave here!", "Anyone up for coffee?", "Ping me later."]
    messages5 = ["Eve has entered the chat.", "Hi all!", "Nice to meet you!"]

    # Recipients for each user
    recipients1 = ["Bob"]
    recipients2 = ["Alice"]
    recipients3 = ["Alice", "Bob"]
    recipients4 = ["Alice", "Charlie", "Eve"]
    recipients5 = ["Dave", "Bob", "Charlie"]

    # Start threads for simulation
    threads = [
        threading.Thread(target=simulate_user, args=(user1, recipients1, messages1)),
        threading.Thread(target=simulate_user, args=(user2, recipients2, messages2)),
        threading.Thread(target=simulate_user, args=(user3, recipients3, messages3)),
        threading.Thread(target=simulate_user, args=(user4, recipients4, messages4)),
        threading.Thread(target=simulate_user, args=(user5, recipients5, messages5))
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Start user interaction
    chat_ui(users)
