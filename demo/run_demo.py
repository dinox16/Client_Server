# -*- coding: utf-8 -*-
"""
Demo day du - Full Demo
Chay demo day du voi 3 clients va server
"""

import sys
import os
import time
import threading

# Them duong dan de import
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'client'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'server'))

from client import SecureChatClient


def run_full_demo():
    """
    Chay demo day du:
    1. Khoi dong server (can chay rieng trong terminal khac)
    2. Ket noi 3 clients
    3. Gui tin nhan qua lai
    4. Hien thi blockchain
    5. Kiem tra integrity
    """
    print("\n" + "="*60)
    print("DEMO DAY DU - Chat Client-Server voi E2EE")
    print("="*60 + "\n")
    
    print("[HUONG DAN]")
    print("1. Mo terminal rieng va chay server:")
    print("   cd server")
    print("   python server.py")
    print()
    print("2. Sau khi server chay, nhan Enter de tiep tuc demo...")
    input()
    
    print("\n[INFO] Bat dau demo voi 3 clients: Alice, Bob, Charlie")
    print()
    
    # Khoi tao 3 clients
    print("[STEP 1] Khoi tao clients...")
    alice = SecureChatClient("Alice")
    bob = SecureChatClient("Bob")
    charlie = SecureChatClient("Charlie")
    print()
    
    time.sleep(1)
    
    # Ket noi den server
    print("[STEP 2] Ket noi den server...")
    alice.connect('127.0.0.1', 5555)
    time.sleep(0.5)
    bob.connect('127.0.0.1', 5555)
    time.sleep(0.5)
    charlie.connect('127.0.0.1', 5555)
    time.sleep(2)  # Doi de nhan user list
    print()
    
    # Gui tin nhan
    print("[STEP 3] Gui tin nhan...")
    print()
    
    print("Alice gui tin nhan cho Bob:")
    alice.send_message("Bob", "Xin chao Bob! Ban khoe khong?")
    time.sleep(1)
    
    print("\nBob tra loi Alice:")
    bob.send_message("Alice", "Chao Alice! Minh khoe, cam on ban!")
    time.sleep(1)
    
    print("\nCharlie gui tin nhan cho Alice:")
    charlie.send_message("Alice", "Hey Alice, chieu nay di ca phe khong?")
    time.sleep(1)
    
    print("\nAlice tra loi Charlie:")
    alice.send_message("Charlie", "OK, 5 gio gap nhau nhe!")
    time.sleep(1)
    
    print("\nBob gui tin nhan cho Charlie:")
    bob.send_message("Charlie", "Charlie, ban co tai lieu mon Mang May Tinh khong?")
    time.sleep(1)
    
    print("\nCharlie tra loi Bob:")
    charlie.send_message("Bob", "Co, minh gui cho ban qua email nhe!")
    time.sleep(2)
    
    # Hien thi blockchain
    print("\n" + "="*60)
    print("[STEP 4] Hien thi blockchain cua Alice")
    print("="*60)
    alice.print_blockchain()
    
    time.sleep(1)
    
    print("\n" + "="*60)
    print("[STEP 5] Hien thi blockchain cua Bob")
    print("="*60)
    bob.print_blockchain()
    
    time.sleep(1)
    
    print("\n" + "="*60)
    print("[STEP 6] Hien thi blockchain cua Charlie")
    print("="*60)
    charlie.print_blockchain()
    
    # Kiem tra integrity
    print("\n" + "="*60)
    print("[STEP 7] Kiem tra integrity cua blockchain")
    print("="*60)
    alice.verify_blockchain()
    bob.verify_blockchain()
    charlie.verify_blockchain()
    print()
    
    time.sleep(1)
    
    # Ngat ket noi
    print("[STEP 8] Ngat ket noi...")
    alice.disconnect()
    bob.disconnect()
    charlie.disconnect()
    print()
    
    # Ket luan
    print("="*60)
    print("DEMO HOAN TAT!")
    print("="*60)
    print("Da chung minh:")
    print("1. Chat E2EE giua nhieu clients")
    print("2. Server relay tin nhan ma hoa")
    print("3. Blockchain luu lich su tin nhan")
    print("4. Xac thuc chu ky so")
    print("5. Bao mat du lieu end-to-end")
    print("="*60 + "\n")


def interactive_demo():
    """Demo tuong tac cho nguoi dung"""
    print("\n" + "="*60)
    print("DEMO TUONG TAC")
    print("="*60 + "\n")
    
    username = input("Nhap username cua ban: ").strip()
    if not username:
        print("[ERROR] Username khong duoc de trong")
        return
    
    client = SecureChatClient(username)
    
    print("\n[INFO] Ket noi den server tai 127.0.0.1:5555...")
    client.connect('127.0.0.1', 5555)
    
    if not client.connected:
        print("[ERROR] Khong the ket noi den server")
        print("[INFO] Dam bao server dang chay: python server/server.py")
        return
    
    time.sleep(1)
    
    print("\n" + "="*60)
    print("HUONG DAN:")
    print("- Gui tin nhan: send <username> <message>")
    print("- Xem blockchain: blockchain")
    print("- Xem users: users")
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
                print("Lenh khong hop le")
                
    except KeyboardInterrupt:
        print("\n")
    finally:
        client.disconnect()


def main():
    """Ham main"""
    print("\n" + "="*60)
    print("DEMO SCRIPTS - Do An Mang May Tinh")
    print("="*60)
    print("\n1. Demo day du (tu dong)")
    print("2. Demo tuong tac")
    print()
    
    choice = input("Chon demo (1/2): ").strip()
    
    if choice == '1':
        run_full_demo()
    elif choice == '2':
        interactive_demo()
    else:
        print("[ERROR] Lua chon khong hop le")


if __name__ == '__main__':
    main()
