# -*- coding: utf-8 -*-
"""
Kich ban tan cong - Attack Scenario
Demo Alice bi malware, Bob gui tin nhan nhay cam
"""

import sys
import os
import time
import threading
import json

# Them duong dan de import
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'client'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'security'))

from client import SecureChatClient
from malware_simulation import CompromisedClient


def attack_scenario():
    """
    Kich ban tan cong chi tiet:
    1. Alice va Bob ket noi
    2. Malware chiem quyen may Alice
    3. Bob gui tin nhan nhay cam
    4. Malware intercept nhung KHONG doc duoc
    5. Alice van doc duoc binh thuong
    """
    print("\n" + "="*60)
    print("KICH BAN TAN CONG - MALWARE VA E2EE")
    print("="*60 + "\n")
    
    print("[CANH BAO] Demo nay mo phong tan cong malware!")
    print("[INFO] Muc dich: Chung minh E2EE bao ve tin nhan du client bi hack")
    print()
    print("[YEU CAU] Server phai dang chay tai 127.0.0.1:5555")
    print()
    input("Nhan Enter de tiep tuc...")
    print()
    
    # Buoc 1: Alice va Bob ket noi
    print("="*60)
    print("[BUOC 1] Alice va Bob ket noi den server")
    print("="*60)
    
    alice = SecureChatClient("Alice")
    bob = SecureChatClient("Bob")
    
    alice.connect('127.0.0.1', 5555)
    time.sleep(0.5)
    bob.connect('127.0.0.1', 5555)
    time.sleep(2)  # Doi de nhan user list
    
    if not alice.connected or not bob.connected:
        print("[ERROR] Khong the ket noi den server!")
        print("[INFO] Chay server truoc: python server/server.py")
        return
    
    print("[INFO] Alice va Bob da online\n")
    time.sleep(1)
    
    # Buoc 2: Malware chiem quyen Alice
    print("="*60)
    print("[BUOC 2] Hacker cai malware vao may Alice")
    print("="*60)
    
    malware = CompromisedClient("Alice")
    print("[HACKER] Da xam nhap thanh cong!")
    print("[HACKER] Dang lang nghe tat ca traffic...\n")
    time.sleep(2)
    
    # Buoc 3: Bob gui tin nhan nhay cam
    print("="*60)
    print("[BUOC 3] Bob gui tin nhan nhay cam cho Alice")
    print("="*60)
    
    sensitive_message = "Mat khau ngan hang cua minh la: 123456789"
    print(f"[BOB] Tin nhan goc: '{sensitive_message}'")
    print("[BOB] Dang ma hoa bang public key cua Alice...")
    
    # Tao goi tin ma hoa (gia lap)
    recipient_public_key = alice.crypto.get_public_key_string()
    encrypted_data = bob.crypto.encrypt_message(sensitive_message, recipient_public_key)
    
    if not encrypted_data:
        print("[ERROR] Loi ma hoa tin nhan")
        return
    
    packet = {
        'type': 'message',
        'from': 'Bob',
        'to': 'Alice',
        'encrypted_data': encrypted_data
    }
    
    print("[BOB] Da ma hoa xong!")
    print("[BOB] Dang gui qua server...\n")
    time.sleep(1)
    
    # Buoc 4: Malware intercept
    print("="*60)
    print("[BUOC 4] Malware bat duoc packet")
    print("="*60)
    
    malware.intercept_traffic(packet)
    time.sleep(2)
    
    # Buoc 5: Alice nhan va giai ma
    print("="*60)
    print("[BUOC 5] Alice nhan va giai ma tin nhan")
    print("="*60)
    
    print("[ALICE] Dang giai ma bang private key cua minh...")
    sender_public_key = bob.crypto.get_public_key_string()
    plaintext, verified = alice.crypto.decrypt_message(encrypted_data, sender_public_key)
    
    if plaintext:
        print(f"[ALICE] Tin nhan da giai ma: '{plaintext}'")
        if verified:
            print("[ALICE] Chu ky HOP LE - Xac nhan tu Bob")
        else:
            print("[ALICE] CHU KY KHONG HOP LE!")
        
        # Luu vao blockchain
        alice.blockchain.add_message("Bob", "Alice", plaintext)
        print("[ALICE] Da luu vao blockchain\n")
    else:
        print("[ERROR] Khong the giai ma tin nhan\n")
    
    time.sleep(2)
    
    # Ket luan
    print("="*60)
    print("KET LUAN")
    print("="*60)
    print()
    print("TINH HUONG:")
    print("- Alice bi malware chiem quyen")
    print("- Malware bat duoc TAT CA traffic mang")
    print("- Bob gui tin nhan nhay cam: Mat khau ngan hang")
    print()
    print("KET QUA:")
    print("- Malware CHI THAY duoc ciphertext (du lieu ma hoa)")
    print("- Malware KHONG THE doc duoc plaintext (noi dung goc)")
    print("- Alice van nhan va doc duoc tin nhan BINH THUONG")
    print()
    print("LY DO:")
    print("- E2EE: Tin nhan duoc ma hoa TRUOC KHI gui")
    print("- Private key: Chi co Alice moi giai ma duoc")
    print("- Hybrid encryption: RSA + AES bao mat 2 lop")
    print("- Digital signature: Xac thuc nguoi gui")
    print()
    print("="*60)
    print("E2EE DA BAO VE THANH CONG DU LIEU!")
    print("="*60 + "\n")
    
    # Hien thi blockchain cua Alice
    print("[BONUS] Lich su tin nhan cua Alice trong blockchain:")
    alice.print_blockchain()
    
    # Ngat ket noi
    print("[INFO] Ngat ket noi...")
    alice.disconnect()
    bob.disconnect()
    print("[INFO] Demo hoan tat!\n")


def main():
    """Ham main"""
    attack_scenario()


if __name__ == '__main__':
    main()
