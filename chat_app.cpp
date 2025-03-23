#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <mutex>
#include <chrono>
#include <ctime>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <cstring>

// Structure to store message details
struct Message {
    std::string senderID;
    std::string recipientID;
    std::string timestamp;
    std::string content;
};

// User class
class User {
public:
    std::string userID;

    User(const std::string& id) : userID(id) {}

    void sendMessage(const std::string& recipientID, const std::string& content);
};

// Global message history and mutex for concurrency
std::vector<Message> messageHistory;
std::mutex historyMutex;

// Utility to get current timestamp
std::string getCurrentTimestamp() {
    auto now = std::chrono::system_clock::now();
    std::time_t now_time = std::chrono::system_clock::to_time_t(now);
    char buf[100];
    ctime_r(&now_time, buf); // thread-safe
    buf[strcspn(buf, "\n")] = 0; // Remove newline
    return std::string(buf);
}

// Send message implementation
void User::sendMessage(const std::string& recipientID, const std::string& content) {
    Message msg;
    msg.senderID = this->userID;
    msg.recipientID = recipientID;
    msg.timestamp = getCurrentTimestamp();
    msg.content = content;

    std::lock_guard<std::mutex> lock(historyMutex);
    messageHistory.push_back(msg);
    std::cout << "[" << msg.timestamp << "] " << userID << " -> " << recipientID << ": " << content << std::endl;
}

// Display all messages
void displayAllMessages() {
    std::lock_guard<std::mutex> lock(historyMutex);
    std::cout << "\n--- Message History ---\n";
    for (const auto& msg : messageHistory) {
        std::cout << "[" << msg.timestamp << "] " << msg.senderID << " -> " << msg.recipientID << ": " << msg.content << std::endl;
    }
    std::cout << "------------------------\n";
}

// Convert string to lowercase (for case-insensitive search)
std::string toLowerCase(const std::string& str) {
    std::string lowerStr = str;
    std::transform(str.begin(), str.end(), lowerStr.begin(),
                   [](unsigned char c){ return std::tolower(c); });
    return lowerStr;
}

// Search messages by user ID
void searchByUserID(const std::string& userID) {
    std::lock_guard<std::mutex> lock(historyMutex);
    std::cout << "\n--- Messages for User: " << userID << " ---\n";
    for (const auto& msg : messageHistory) {
        if (msg.senderID == userID || msg.recipientID == userID) {
            std::cout << "[" << msg.timestamp << "] " << msg.senderID << " -> " << msg.recipientID << ": " << msg.content << std::endl;
        }
    }
    std::cout << "-----------------------------\n";
}

// Case-insensitive search by keyword
void searchByKeyword(const std::string& keyword) {
    std::string lowerKeyword = toLowerCase(keyword);
    std::lock_guard<std::mutex> lock(historyMutex);
    std::cout << "\n--- Messages containing keyword: \"" << keyword << "\" ---\n";
    for (const auto& msg : messageHistory) {
        if (toLowerCase(msg.content).find(lowerKeyword) != std::string::npos) {
            std::cout << "[" << msg.timestamp << "] " << msg.senderID << " -> " << msg.recipientID << ": " << msg.content << std::endl;
        }
    }
    std::cout << "---------------------------------------------\n";
}

// Simulate user sending messages (threaded)
void simulateUser(User& sender, const std::vector<std::string>& recipients, const std::vector<std::string>& messages) {
    for (size_t i = 0; i < messages.size(); ++i) {
        sender.sendMessage(recipients[i % recipients.size()], messages[i]);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

// Display all user IDs
void displayUserIDs(const std::vector<User>& users) {
    std::cout << "\n--- Available User IDs ---\n";
    for (const auto& user : users) {
        std::cout << user.userID << std::endl;
    }
    std::cout << "---------------------------\n";
}

// Main UI loop
void chatUI(std::vector<User>& users) {
    int choice;
    while (true) {
        std::cout << "\n--- Chat Menu ---\n";
        std::cout << "1. Send Message\n";
        std::cout << "2. Display All Messages\n";
        std::cout << "3. Search by User ID\n";
        std::cout << "4. Search by Keyword\n";
        std::cout << "5. Display All User IDs\n";
        std::cout << "6. Exit\n";
        std::cout << "Enter your choice: ";

        // Validate input
        if (!(std::cin >> choice)) {
            std::cout << "Invalid input. Please enter a number.\n";
            std::cin.clear(); // Clear error flags
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Discard invalid input
            continue;
        }

        std::string senderID, recipientID, content, keyword;

        switch (choice) {
            case 1:
                std::cout << "Enter Sender ID: ";
                std::cin >> senderID;
                std::cout << "Enter Recipient ID: ";
                std::cin >> recipientID;
                std::cin.ignore(); // Clear newline
                std::cout << "Enter Message: ";
                std::getline(std::cin, content);

                {
                    auto it = std::find_if(users.begin(), users.end(), [&](User& u) { return u.userID == senderID; });
                    if (it != users.end()) {
                        it->sendMessage(recipientID, content);
                    } else {
                        std::cout << "Sender not found.\n";
                    }
                }
                break;

            case 2:
                displayAllMessages();
                break;

            case 3:
                std::cout << "Enter User ID to search: ";
                std::cin >> senderID;
                searchByUserID(senderID);
                break;

            case 4:
                std::cout << "Enter keyword to search: ";
                std::cin.ignore();
                std::getline(std::cin, keyword);
                searchByKeyword(keyword);
                break;

            case 5:
                displayUserIDs(users);
                break;

            case 6:
                std::cout << "Exiting chat...\n";
                return;

            default:
                std::cout << "Invalid choice. Try again.\n";
        }
    }
}


int main() {
    // Initialize users
    User user1("Alice");
    User user2("Bob");
    User user3("Charlie");
    User user4("Dave");
    User user5("Eve");

    std::vector<User> users = { user1, user2, user3, user4, user5 };

    // Messages for simulation
    std::vector<std::string> messages1 = { "Hello Bob!", "How are you?", "Let's catch up soon." };
    std::vector<std::string> messages2 = { "Hi Alice!", "I'm good, thanks.", "Sure, sounds great." };
    std::vector<std::string> messages3 = { "Hey Alice and Bob!", "What are you guys up to?", "Join me for a game?" };
    std::vector<std::string> messages4 = { "Dave here!", "Anyone up for coffee?", "Ping me later." };
    std::vector<std::string> messages5 = { "Eve has entered the chat.", "Hi all!", "Nice to meet you!" };

    // Recipients for simulation
    std::vector<std::string> recipients1 = { "Bob", "Bob", "Bob" };
    std::vector<std::string> recipients2 = { "Alice", "Alice", "Alice" };
    std::vector<std::string> recipients3 = { "Alice", "Bob", "Alice" };
    std::vector<std::string> recipients4 = { "Alice", "Charlie", "Eve" };
    std::vector<std::string> recipients5 = { "Dave", "Bob", "Charlie" };

    // Start threads to simulate concurrent messaging
    std::thread t1(simulateUser, std::ref(user1), recipients1, messages1);
    std::thread t2(simulateUser, std::ref(user2), recipients2, messages2);
    std::thread t3(simulateUser, std::ref(user3), recipients3, messages3);
    std::thread t4(simulateUser, std::ref(user4), recipients4, messages4);
    std::thread t5(simulateUser, std::ref(user5), recipients5, messages5);

    t1.join();
    t2.join();
    t3.join();
    t4.join();
    t5.join();

    // Start user interaction
    chatUI(users);

    return 0;
}
