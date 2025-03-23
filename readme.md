# Chat App

## Overview

This is a multi-threaded chat application implemented in C++ and in Python. The program allows users to send and receive messages, display message history, and perform searches based on user ID and keywords. The application utilizes threads for concurrent messaging and a mutex to handle shared message history.

## Features

-   **Send and receive messages between users:** Enables real-time communication.
-   **Display all messages:** Shows the complete message history.
-   **Search messages by user ID:** Filters messages by a specific user.
-   **Search messages by keyword (case-insensitive):** Filters messages containing a specified word.
-   **Display all available user IDs:** Lists all users who have sent messages.
-   **Multi-threaded messaging simulation:** Simulates concurrent messaging using threads.

## Requirements

### C++ Segment

-   g++ compiler
-   C++11 or later

### Python Segment

-   Python 3.x

## Installation and Execution

### Running the C++ Program

#### Ubuntu

1.  Install g++ if not already installed:

    ```bash
    sudo apt update && sudo apt install g++
    ```

2.  Compile the program:

    ```bash
    g++ -std=c++11 chat_app.cpp -o chat_app -pthread
    ```

3.  Run the program:

    ```bash
    ./chat_app
    ```

#### Windows

1.  Install MinGW and add it to the system PATH.
2.  Open the terminal and compile the program:

    ```bash
    g++ -std=c++11 chat_app.cpp -o chat_app.exe -pthread
    ```

3.  Run the program:

    ```bash
    chat_app.exe
    ```

#### macOS

1.  Install Xcode command-line tools:

    ```bash
    xcode-select --install
    ```

2.  Compile the program:

    ```bash
    g++ -std=c++11 chat_app.cpp -o chat_app -pthread
    ```

3.  Run the program:

    ```bash
    ./chat_app
    ```

### Running the Python Program

#### Ubuntu

1.  Ensure Python 3 is installed:

    ```bash
    python3 --version
    ```

2.  Run the Python script:

    ```bash
    python3 chat_app.py
    ```

#### Windows

1.  Ensure Python 3 is installed:

    ```bash
    python --version
    ```

2.  Run the Python script:

    ```bash
    python chat_app.py
    ```

#### macOS

1.  Ensure Python 3 is installed:

    ```bash
    python3 --version
    ```

2.  Run the Python script:

    ```bash
    python3 chat_app.py
    ```

## Screenshots

### 1. Send Message
![Send Message](Screenshots/Send%20Message.png)

### 2. Display All Messages
![Display All Messages](Screenshots/Display%20All%20Messages.png)

### 3. Display All User IDs
![Display All User IDs](Screenshots/Display%20All%20User%20IDs.png)

### 4. Search By User ID
![Search By User ID](Screenshots/Search%20By%20User%20ID.png)

### 5. Search By Keyword
![Search By Keyword](Screenshots/Search%20By%20Keyword.png)
