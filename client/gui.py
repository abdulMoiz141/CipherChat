# client/gui.py
import customtkinter as ctk
import threading
from datetime import datetime
import sys
import os

# Add parent dir to path to import local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from network import NetworkClient
from encryption import EncryptionManager
from common.constants import FORMAT

# Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CipherChat - Secure E2EE Messenger")
        self.geometry("500x650")
        
        self.network = NetworkClient()
        self.encryption = None
        self.username = ""
        
        # --- UI FRAMES ---
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # 1. Login Screen
        self.login_frame = ctk.CTkFrame(self.container)
        self.create_login_screen()

        # 2. Chat Screen (Hidden initially)
        self.chat_frame = ctk.CTkFrame(self.container)
        self.create_chat_screen()

        self.show_frame(self.login_frame)

    def show_frame(self, frame):
        frame.pack(fill="both", expand=True)
        frame.tkraise()

    def create_login_screen(self):
        # Title
        label = ctk.CTkLabel(self.login_frame, text="CipherChat Login", font=("Roboto", 24, "bold"))
        label.pack(pady=40)

        # Inputs
        self.ip_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Server IP Address", width=300)
        self.ip_entry.pack(pady=10)
        self.ip_entry.insert(0, "127.0.0.1") # Default for testing

        self.user_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=300)
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Room Password (Secret Key)", show="*", width=300)
        self.pass_entry.pack(pady=10)

        # Connect Button
        self.connect_btn = ctk.CTkButton(self.login_frame, text="Connect securely", command=self.start_connection)
        self.connect_btn.pack(pady=30)
        
        # Info
        info_lbl = ctk.CTkLabel(self.login_frame, text="Encryption: AES-256 (Fernet)\nIntegrity: HMAC-SHA256", text_color="gray")
        info_lbl.pack(side="bottom", pady=20)

    def create_chat_screen(self):
        # Header
        self.header_frame = ctk.CTkFrame(self.chat_frame, height=50)
        self.header_frame.pack(fill="x", padx=10, pady=10)
        
        self.status_lbl = ctk.CTkLabel(self.header_frame, text="Status: Connected", text_color="#00FF00")
        self.status_lbl.pack(side="left", padx=10)

        # Hacker View Toggle
        self.hacker_view_var = ctk.StringVar(value="off")
        self.hacker_switch = ctk.CTkSwitch(self.header_frame, text="Show Encrypted Stream", 
                                           command=self.toggle_hacker_view, variable=self.hacker_view_var, onvalue="on", offvalue="off")
        self.hacker_switch.pack(side="right", padx=10)

        # Chat Area
        self.chat_box = ctk.CTkTextbox(self.chat_frame, width=450, height=450, state="disabled")
        self.chat_box.pack(pady=10, padx=10)

        # Input Area
        self.input_frame = ctk.CTkFrame(self.chat_frame)
        self.input_frame.pack(fill="x", padx=10, pady=10, side="bottom")

        self.msg_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Type your secure message...", width=350)
        self.msg_entry.pack(side="left", padx=10)
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=80, command=self.send_message)
        self.send_btn.pack(side="right", padx=10)

    def start_connection(self):
        ip = self.ip_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()

        if not ip or not user or not password:
            return

        # 1. Initialize Encryption
        self.encryption = EncryptionManager(password)
        self.username = user

        # 2. Connect Network
        if self.network.connect(ip):
            self.login_frame.pack_forget()
            self.show_frame(self.chat_frame)
            
            # Start listening thread
            recv_thread = threading.Thread(target=self.network.receive_loop, args=(self.on_receive_message,))
            recv_thread.daemon = True
            recv_thread.start()
        else:
            self.connect_btn.configure(text="Connection Failed!", fg_color="red")

    def send_message(self):
        msg = self.msg_entry.get()
        if not msg: return

        # Display locally
        self.display_message(f"You: {msg}", "white")

        # Encrypt and Send
        try:
            full_msg = f"{self.username}: {msg}"
            encrypted_bytes = self.encryption.encrypt_message(full_msg)
            self.network.send_raw(encrypted_bytes)
            self.msg_entry.delete(0, "end")
        except Exception as e:
            self.display_message(f"[Error sending: {e}]", "red")

    def on_receive_message(self, raw_bytes):
        """Callback when network receives data"""
        
        # Check if it's a System Command (like ALIAS_REQ)
        try:
            decoded_chk = raw_bytes.decode(FORMAT)
            if decoded_chk == "ALIAS_REQ":
                self.network.send_raw(self.username.encode(FORMAT))
                return
            elif decoded_chk.startswith("System:"):
                self.display_message(decoded_chk, "#FFFF00") # Yellow for system
                return
        except:
            pass # It's likely encrypted data if decode fails
        
        # Handle User Messages
        if self.hacker_view_var.get() == "on":
            # HACKER VIEW: Show Raw Ciphertext
            self.display_message(f"[ENCRYPTED]: {raw_bytes}", "#FF5555") # Red/Pink for hacking
        else:
            # NORMAL VIEW: Decrypt it
            decrypted_text = self.encryption.decrypt_message(raw_bytes)
            self.display_message(decrypted_text, "white")

    def display_message(self, text, color):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", text + "\n", ("color_tag"))
        self.chat_box.tag_config("color_tag", foreground=color)
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def toggle_hacker_view(self):
        state = self.hacker_view_var.get()
        if state == "on":
            self.display_message("--- [HACKER MODE ENABLED] Showing Raw Stream ---", "gray")
        else:
            self.display_message("--- [SECURE MODE ENABLED] Decrypting Stream ---", "gray")