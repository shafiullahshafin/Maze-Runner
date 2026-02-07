# Maze Runner

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**Maze Runner** is a modern, cross-platform desktop recreation of the classic Snake game. Built with Python and Pygame, it features a robust leaderboard system, smooth gameplay mechanics, and secure database integration.

---

## Features

*   **Classic Gameplay**: Navigate the snake, eat food, and grow longer.
*   **Wall Wrapping**: Walls wrap around (Nokia style) - going through a wall makes you appear on the other side!
*   **Difficulty Levels**: Choose between Easy, Medium, and Hard modes.
*   **Lives System**: Start with 3 lives.
*   **Global Leaderboard**: Compete for the top spot! Scores are saved to a **PostgreSQL** database.
*   **Pause & Resume**: Pause the game anytime with P or TAB.
*   **Cross-Platform**: Optimized for macOS, Windows, and Linux.

---

## Prerequisites

*   **Active Internet Connection**: Required to connect to the global leaderboard database.
*   **Operating System**: Windows, macOS, or Linux.

---

## Installation

### Option 1: Download the App (Recommended)
Download the latest release for your operating system from the **Releases** page.

### Option 2: Run from Source
If you are a developer and want to run the code directly:

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/maze-runner.git
    cd maze-runner
    ```
2.  Set up a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    # Activate:
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate   # Windows
    
    pip install -r requirements.txt
    ```
3.  Run the game:
    ```bash
    python main.py
    ```

---

## Building the App

To create a standalone executable for your operating system:

1.  **Activate your virtual environment**.
2.  Run the build script:
    ```bash
    python3 build_app.py
    ```
    *   On **Windows**, you can also simply run `build_windows.bat`.
    *   On **Linux**, you can run `build_linux.sh`.

3.  The executable/app will be generated in the `dist/` folder.

---

## How to Play

1.  Start the game.
2.  The app will check for database connection.
3.  Enter your **username** at the login screen.
4.  Use the **Main Menu** to start a new game or view the leaderboard.

### Controls

| Key | Action |
| :--- | :--- |
| **Arrow Keys** | Move Snake / Navigate Menu |
| **P** / **TAB** | Pause / Resume Game |
| **ESC** | Return to Menu / Quit |
| **ENTER** | Confirm Selection |

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
