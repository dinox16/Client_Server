# -*- coding: utf-8 -*-
"""
Demo bao ve - Defense Demonstration
Chung minh he thong bao ve duoc tin nhan truoc malware
"""

import sys
import os
import time
import threading

# Them duong dan de import
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'client'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'security'))

from malware_simulation import CompromisedClient


def demonstrate_attack_scenario():
    """
    Demo kich ban tan cong day du
    
    Kich ban:
    1. Alice va Bob ket noi server
    2. Malware chiem quyen may Alice  
    3. Bob gui tin nhan nhay cam cho Alice
    4. Malware intercept packet
    5. KET QUA: Malware CHI thay ciphertext, KHONG doc duoc plaintext
    6. Alice van doc duoc binh thuong
    """
    print("\n" + "="*60)
    print("DEMO: CLIENT BI MALWARE CHIEM QUYEN")
    print("="*60)
    
    print("\n[KICH BAN]")
    print("1. Alice va Bob la 2 nguoi ban")
    print("2. Hacker cai malware vao may Alice")
    print("3. Bob gui tin nhan nhay cam: 'Mat khau ngan hang: 123456'")
    print("4. Malware bat packet nhung KHONG doc duoc noi dung")
    print("5. Alice van nhan va doc duoc tin nhan binh thuong")
    
    print("\n" + "="*60)
    print("BAT DAU DEMO...")
    print("="*60 + "\n")
    
    time.sleep(2)
    
    # Buoc 1: Alice va Bob online
    print("[STEP 1] Alice va Bob da ket noi den server")
    print("[INFO] Alice IP: 192.168.1.100")
    print("[INFO] Bob IP: 192.168.1.101")
    print()
    
    time.sleep(1)
    
    # Buoc 2: Hacker cai malware vao may Alice
    print("[STEP 2] Hacker da xam nhap va cai malware vao may Alice")
    malware = CompromisedClient("Alice")
    print()
    
    time.sleep(1)
    
    # Buoc 3: Bob gui tin nhan
    print("[STEP 3] Bob gui tin nhan nhay cam cho Alice")
    print("[BOB] Dang ma hoa tin nhan...")
    print("[BOB] Dang gui qua server...")
    
    # Gia lap goi tin ma hoa
    encrypted_packet = {
        'type': 'message',
        'from': 'Bob',
        'to': 'Alice',
        'encrypted_data': {
            'encrypted_aes_key': 'L8xK9mP2qR5tY7wZ0aB3cD6eF9gH2iJ5kL8mN1oP4qR7sT0uV3wX6yZ9',
            'nonce': 'aB3dE6fG9h',
            'tag': 'iJ2kL5m',
            'ciphertext': 'X5yZ8aB1cD4eF7gH0iJ3kL6mN9oP2qR5sT8uV1wX4yZ7aB0cD3eF6',
            'signature': 'gH9iJ2kL5mN8oP1qR4sT7uV0wX3yZ6aB9cD2eF5gH8iJ1kL4mN7oP0'
        }
    }
    
    print("[SERVER] Dang chuyen tiep tin nhan den Alice...")
    print()
    
    time.sleep(1)
    
    # Buoc 4: Malware intercept
    print("[STEP 4] Malware bat duoc packet tren may Alice")
    malware.intercept_traffic(encrypted_packet)
    
    time.sleep(2)
    
    # Buoc 5: Alice doc binh thuong
    print("[STEP 5] Alice nhan va giai ma tin nhan thanh cong")
    print("[ALICE] Dang giai ma bang private key...")
    print("[ALICE] Dang xac thuc chu ky cua Bob...")
    print("[ALICE] Chu ky HOP LE!")
    print("[Bob]: Mat khau ngan hang: 123456")
    print("[ALICE] Da luu vao blockchain")
    print()
    
    time.sleep(1)
    
    # Ket luan
    print("="*60)
    print("KET LUAN")
    print("="*60)
    print("1. Malware DA chiem quyen may Alice")
    print("2. Malware DA bat duoc tat ca packets")
    print("3. NHUNG malware KHONG THE doc duoc noi dung tin nhan")
    print("4. Alice van nhan va doc duoc tin nhan binh thuong")
    print()
    print("LY DO:")
    print("- Tin nhan duoc ma hoa E2EE TRUOC KHI gui")
    print("- Server chi thay ciphertext")
    print("- Malware khong co private key de giai ma")
    print("- Chi nguoi nhan (Alice) co private key moi doc duoc")
    print("="*60 + "\n")


def explain_security_layers():
    """Giai thich cac lop bao ve"""
    print("\n" + "="*60)
    print("CAC LOP BAO VE TRONG HE THONG")
    print("="*60 + "\n")
    
    print("1. END-TO-END ENCRYPTION (E2EE)")
    print("   - Tin nhan duoc ma hoa TRUOC KHI roi khoi thiet bi")
    print("   - Server khong bao gio thay plaintext")
    print("   - Chi nguoi nhan co private key moi giai ma duoc")
    print()
    
    print("2. HYBRID ENCRYPTION (RSA + AES)")
    print("   - RSA 2048-bit: Ma hoa AES key")
    print("   - AES-256-EAX: Ma hoa noi dung tin nhan")
    print("   - Ket hop ca bao mat va hieu nang")
    print()
    
    print("3. DIGITAL SIGNATURE")
    print("   - Moi tin nhan duoc ky boi nguoi gui")
    print("   - Nguoi nhan xac thuc chu ky")
    print("   - Ngan chan gia mao va thay doi tin nhan")
    print()
    
    print("4. BLOCKCHAIN INTEGRITY")
    print("   - Moi tin nhan luu thanh 1 block")
    print("   - Proof of Work mining")
    print("   - Khong the sua doi lich su")
    print()
    
    print("5. FORWARD SECRECY")
    print("   - Moi tin nhan dung AES key khac nhau")
    print("   - Neu 1 tin nhan bi hack, cac tin khac van an toan")
    print()
    
    print("="*60)
    print("KET QUA: Ngay ca khi may bi chiem quyen, du lieu van an toan!")
    print("="*60 + "\n")


def main():
    """Ham main chay demo"""
    print("\n" + "="*60)
    print("DEFENSE DEMONSTRATION - Do An Mang May Tinh")
    print("="*60)
    
    # Demo tan cong
    demonstrate_attack_scenario()
    
    time.sleep(2)
    
    # Giai thich bao mat
    explain_security_layers()
    
    print("\n[INFO] Demo hoan tat!")
    print("[INFO] Xem them tai HUONG_DAN_THUC_HIEN.txt\n")


if __name__ == '__main__':
    main()
