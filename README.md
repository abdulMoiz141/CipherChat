# 🛡️ CipherChat (SecureConnect)

> **A Secure, Multi-Client, End-to-End Encrypted Communication System.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Security](https://img.shields.io/badge/Security-AES--256-green)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-orange)

## 📖 Overview
**CipherChat** is a desktop messaging application designed to demonstrate the principles of **Network Security** and **Cryptography**. Unlike traditional chat apps where the server can read your messages, CipherChat employs a **Zero-Knowledge Architecture**.

Messages are encrypted on your device (Client) using **AES-256** and are only decrypted on the receiver's device. The central server acts merely as a postman and cannot read any content, ensuring total privacy.

---

## 🚀 Key Features

### 🔒 Security Features
* **End-to-End Encryption (E2EE):** Uses **AES (Fernet)** to encrypt messages before they leave the device.
* **Data Integrity:** Implements **HMAC-SHA256** signatures to detect tampering during transit.
* **Secure Authentication:** Uses **PBKDF2** (Password-Based Key Derivation) to generate strong 32-byte keys from a simple Room Password.
* **Zero-Knowledge Server:** The server routes encrypted bytes without access to decryption keys.

### 💻 Application Features
* **Multi-Client Support:** Real-time group chatting over Local Area Network (LAN).
* **Modern GUI:** Built with **CustomTkinter** for a professional Dark Mode experience.
* **Hacker View / Developer Mode:** A dedicated toggle switch that reveals the raw **Ciphertext** (e.g., `gAAAA...`) to visually prove encryption is active.
* **Live Status Indicators:** Visual feedback for connection status (Connected/Disconnected).

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core Application Logic |
| **GUI Framework** | CustomTkinter | Modern User Interface |
| **Networking** | Python `socket` (TCP) | Reliable Data Transmission |
| **Concurrency** | `threading` | Handling UI and Network simultaneously |
| **Cryptography** | `cryptography.fernet` | Symmetric Encryption (AES) |
| **Key Derivation** | `PBKDF2HMAC` | Generating Keys from Passwords |

---

## 📂 Project Structure

```text
CipherChat/
│
├── server/
│   ├── server.py           # The Central Hub (Run this first)
│   └── server_config.py    # IP/Port Configuration
│
├── client/
│   ├── client.py           # Entry point for the User App
│   ├── gui.py              # User Interface Logic
│   ├── encryption.py       # AES & Key Management Logic
│   └── network.py          # Socket Communication Handler
│
├── common/
│   ├── constants.py        # Shared Settings (Port, Headers)
│   └── crypto_utils.py     # Shared Math (Key Generation)
│
├── requirements.txt        # List of dependencies
└── README.md               # Documentation
