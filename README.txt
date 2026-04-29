# 🏓 Pong LAN Multiplayer

A simple LAN-based multiplayer Pong game developed using Python, sockets, and Pygame.

This project demonstrates real-time communication between multiple devices over a local network, along with basic game synchronization and multiplayer interaction.

---

## 🚀 Features

- Host & Client architecture (TCP socket-based)
- Supports up to **4 players**:
  - 1 Host (Player 1)
  - Up to 3 Clients (Player 2–4)
- Real-time paddle movement and ball synchronization
- Player-specific colors
- Health (lives) system
- Lobby system before game start
- Automatic handling of player disconnects

---

## 🧠 How It Works

- The **Host** acts as the game server.
- Clients connect to the host via IP address.
- The host:
  - Updates the game state (ball, paddles, lives)
  - Sends the current state to all clients
- Clients:
  - Send input (movement keys) to the host
  - Render the game based on received data

---

## 🎮 Controls

### Player 1 (Host)
- `W / S` → Move up/down

### Player 2 (Client)
- `W / S` → Move up/down

### Player 3 (Client)
- `A / D` → Move left/right

### Player 4 (Client)
- `A / D` → Move left/right

---

## 🖥️ How to Run

### 1. Install requirements

```bash
pip install pygame