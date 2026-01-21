# -*- coding: utf-8 -*-
"""
Client chat bao mat - Secure Chat Client
Client chat voi ma hoa E2EE va blockchain
"""

import socket
import threading
import json
import sys
import os

# Them duong dan de import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from encryption import CryptoManager
from blockchain import MessageBlockchain


class SecureChatClient:
    """
    Client chat bao mat
    - Ket noi den server
    - Ma hoa E2EE cho tin nhan
    - Luu lich su vao blockchain
    """
    
    def __init__(self, username):
        """
        Khoi tao client
        
        Args:
            username: Ten nguoi dung
        """
        self.username = username
        self.crypto = CryptoManager()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peers = {}  # {username: public_key}
        self.blockchain = MessageBlockchain()
        self.connected = False
        self.receive_thread = None
        
        print(f"[{self.username}] Client da duoc khoi tao")
    
    def connect(self, server_ip='127.0.0.1', server_port=5555):
        """
        Ket noi den server
        
        Args:
            server_ip: Dia chi IP cua server
            server_port: Cong cua server
        """
        try:
            self.socket.connect((server_ip, server_port))
            print(f"[{self.username}] Da ket noi den server {server_ip}:{server_port}")
            
            # Gui thong tin dang ky
            registration = {
                'username': self.username,
                'public_key': self.crypto.get_public_key_string()
            }
            self.socket.send(json.dumps(registration).encode('utf-8'))
            
            self.connected = True
            
            # Bat dau thread nhan tin nhan
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
        except Exception as e:
            print(f"[ERROR] Khong the ket noi: {e}")
            self.connected = False
    
    def receive_messages(self):
        """Thread nhan tin nhan tu server"""
        while self.connected:
            try:
                data = self.socket.recv(8192).decode('utf-8')
                if not data:
                    break
                
                packet = json.loads(data)
                
                # Xu ly cac loai goi tin
                if packet.get('type') == 'user_list':
                    self.handle_user_list(packet['users'])
                elif packet.get('type') == 'message':
                    self.handle_message(packet)
                    
            except Exception as e:
                if self.connected:
                    print(f"[ERROR] Loi nhan tin nhan: {e}")
                break
        
        self.connected = False
    
    def handle_user_list(self, users):
        """
        Xu ly danh sach users tu server
        
        Args:
            users: Dict {username: public_key}
        """
        self.peers = users
        # Bo minh ra khoi danh sach
        if self.username in self.peers:
            del self.peers[self.username]
        
        usernames = list(self.peers.keys())
        print(f"[{self.username}] Danh sach users online: {usernames}")
    
    def handle_message(self, packet):
        """
        Xu ly tin nhan nhan duoc
        
        Args:
            packet: Goi tin nhan da ma hoa
        """
        try:
            sender = packet['from']
            encrypted_data = packet['encrypted_data']
            
            # Lay public key cua nguoi gui
            sender_public_key = self.peers.get(sender)
            if not sender_public_key:
                print(f"[WARNING] Khong tim thay public key cua {sender}")
                return
            
            # Giai ma tin nhan
            plaintext, verified = self.crypto.decrypt_message(encrypted_data, sender_public_key)
            
            if plaintext:
                # Hien thi tin nhan
                if verified:
                    print(f"[{sender}]: {plaintext}")
                else:
                    print(f"[{sender}] (CHU KY KHONG HOP LE): {plaintext}")
                
                # Luu vao blockchain
                self.blockchain.add_message(sender, self.username, plaintext)
            else:
                print(f"[ERROR] Khong the giai ma tin nhan tu {sender}")
                
        except Exception as e:
            print(f"[ERROR] Loi xu ly tin nhan: {e}")
    
    def send_message(self, recipient, message):
        """
        Gui tin nhan da ma hoa
        
        Args:
            recipient: Ten nguoi nhan
            message: Noi dung tin nhan
        """
        try:
            if not self.connected:
                print(f"[ERROR] Chua ket noi den server")
                return
            
            # Kiem tra nguoi nhan co online khong
            if recipient not in self.peers:
                print(f"[ERROR] {recipient} khong online")
                return
            
            # Lay public key cua nguoi nhan
            recipient_public_key = self.peers[recipient]
            
            # Ma hoa tin nhan
            encrypted_data = self.crypto.encrypt_message(message, recipient_public_key)
            if not encrypted_data:
                print(f"[ERROR] Khong the ma hoa tin nhan")
                return
            
            # Tao goi tin
            packet = {
                'type': 'message',
                'from': self.username,
                'to': recipient,
                'encrypted_data': encrypted_data
            }
            
            # Gui qua server
            self.socket.send(json.dumps(packet).encode('utf-8'))
            print(f"[{self.username}] Da gui tin nhan den {recipient}")
            
            # Luu vao blockchain
            self.blockchain.add_message(self.username, recipient, message)
            
        except Exception as e:
            print(f"[ERROR] Loi gui tin nhan: {e}")
    
    def disconnect(self):
        """Ngat ket noi khoi server"""
        self.connected = False
        try:
            self.socket.close()
        except:
            pass
        print(f"[{self.username}] Da ngat ket noi")
    
    def print_blockchain(self):
        """In blockchain"""
        self.blockchain.print_chain()
    
    def verify_blockchain(self):
        """
        Kiem tra blockchain
        
        Returns:
            bool: True neu hop le
        """
        is_valid = self.blockchain.is_chain_valid()
        if is_valid:
            print(f"[{self.username}] Blockchain hop le")
        else:
            print(f"[{self.username}] Blockchain KHONG hop le!")
        return is_valid


def main():
    """Ham main de test client"""
    import time
    
    print("="*60)
    print("SECURE CHAT CLIENT - Mang May Tinh")
    print("="*60)
    
    username = input("Nhap username cua ban: ").strip()
    if not username:
        print("[ERROR] Username khong duoc de trong")
        return
    
    client = SecureChatClient(username)
    
    server_ip = input("Nhap IP server (Enter de dung 127.0.0.1): ").strip()
    if not server_ip:
        server_ip = '127.0.0.1'
    
    client.connect(server_ip, 5555)
    
    if not client.connected:
        print("[ERROR] Khong the ket noi den server")
        return
    
    # Doi de nhan user list
    time.sleep(1)
    
    print("\n" + "="*60)
    print("HUONG DAN:")
    print("- Gui tin nhan: send <username> <message>")
    print("- Xem blockchain: blockchain")
    print("- Xem danh sach users: users")
    print("- Thoat: quit")
    print("="*60 + "\n")
    
    try:
        while client.connected:
            command = input(f"{username}> ").strip()
            
            if not command:
                continue
            
            if command.lower() == 'quit':
                break
            elif command.lower() == 'blockchain':
                client.print_blockchain()
            elif command.lower() == 'users':
                print(f"Users online: {list(client.peers.keys())}")
            elif command.startswith('send '):
                parts = command.split(' ', 2)
                if len(parts) < 3:
                    print("Format: send <username> <message>")
                else:
                    recipient = parts[1]
                    message = parts[2]
                    client.send_message(recipient, message)
            else:
                print("Lenh khong hop le. Nhap 'send', 'blockchain', 'users' hoac 'quit'")
                
    except KeyboardInterrupt:
        print("\n")
    finally:
        client.disconnect()


if __name__ == '__main__':
    main()
