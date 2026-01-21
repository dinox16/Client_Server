# -*- coding: utf-8 -*-
"""
Module ma hoa - Encryption Module
Cung cap chuc nang ma hoa E2EE voi RSA + AES hybrid va chu ky so
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64
import json


class CryptoManager:
    """
    Quan ly ma hoa va giai ma
    - Tao cap khoa RSA 2048-bit
    - Ma hoa hybrid (RSA + AES)
    - Chu ky so
    """
    
    def __init__(self):
        """Khoi tao va tao cap khoa RSA"""
        print("[CRYPTO] Dang tao cap khoa RSA 2048-bit...")
        self.key_pair = RSA.generate(2048)
        self.private_key = self.key_pair
        self.public_key = self.key_pair.publickey()
        print("[CRYPTO] Da tao cap khoa thanh cong")
    
    def get_public_key_string(self):
        """
        Export public key thanh base64 string
        Returns:
            str: Public key da encode base64
        """
        public_key_bytes = self.public_key.export_key()
        return base64.b64encode(public_key_bytes).decode('utf-8')
    
    def import_public_key(self, public_key_str):
        """
        Import public key tu base64 string
        Args:
            public_key_str: Public key string da encode base64
        Returns:
            RSA key object
        """
        try:
            public_key_bytes = base64.b64decode(public_key_str.encode('utf-8'))
            return RSA.import_key(public_key_bytes)
        except Exception as e:
            print(f"[ERROR] Khong the import public key: {e}")
            return None
    
    def encrypt_message(self, message, recipient_public_key_str):
        """
        Ma hoa tin nhan bang hybrid encryption (RSA + AES)
        
        Args:
            message: Tin nhan plaintext
            recipient_public_key_str: Public key cua nguoi nhan (base64 string)
        
        Returns:
            dict: {
                'encrypted_aes_key': AES key da ma hoa bang RSA,
                'nonce': Nonce cho AES-EAX,
                'tag': Authentication tag,
                'ciphertext': Tin nhan da ma hoa,
                'signature': Chu ky so
            }
        """
        try:
            # 1. Tao AES-256 key ngau nhien
            aes_key = get_random_bytes(32)  # 256-bit
            
            # 2. Ma hoa message bang AES-EAX
            cipher_aes = AES.new(aes_key, AES.MODE_EAX)
            nonce = cipher_aes.nonce
            ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode('utf-8'))
            
            # 3. Ma hoa AES key bang RSA public key cua nguoi nhan
            recipient_public_key = self.import_public_key(recipient_public_key_str)
            cipher_rsa = PKCS1_OAEP.new(recipient_public_key)
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)
            
            # 4. Ky message hash bang private key cua minh
            message_hash = SHA256.new(message.encode('utf-8'))
            signature = pkcs1_15.new(self.private_key).sign(message_hash)
            
            # Return tat ca thanh phan da ma hoa
            return {
                'encrypted_aes_key': base64.b64encode(encrypted_aes_key).decode('utf-8'),
                'nonce': base64.b64encode(nonce).decode('utf-8'),
                'tag': base64.b64encode(tag).decode('utf-8'),
                'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
                'signature': base64.b64encode(signature).decode('utf-8')
            }
        except Exception as e:
            print(f"[ERROR] Loi khi ma hoa tin nhan: {e}")
            return None
    
    def decrypt_message(self, encrypted_data, sender_public_key_str):
        """
        Giai ma tin nhan va xac thuc chu ky
        
        Args:
            encrypted_data: Dict chua cac thanh phan da ma hoa
            sender_public_key_str: Public key cua nguoi gui (base64 string)
        
        Returns:
            tuple: (plaintext, verified)
                - plaintext: Tin nhan goc
                - verified: True neu chu ky hop le, False neu khong
        """
        try:
            # 1. Giai ma AES key bang RSA private key cua minh
            encrypted_aes_key = base64.b64decode(encrypted_data['encrypted_aes_key'].encode('utf-8'))
            cipher_rsa = PKCS1_OAEP.new(self.private_key)
            aes_key = cipher_rsa.decrypt(encrypted_aes_key)
            
            # 2. Giai ma message bang AES key
            nonce = base64.b64decode(encrypted_data['nonce'].encode('utf-8'))
            tag = base64.b64decode(encrypted_data['tag'].encode('utf-8'))
            ciphertext = base64.b64decode(encrypted_data['ciphertext'].encode('utf-8'))
            
            cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher_aes.decrypt_and_verify(ciphertext, tag).decode('utf-8')
            
            # 3. Xac thuc chu ky cua nguoi gui
            signature = base64.b64decode(encrypted_data['signature'].encode('utf-8'))
            sender_public_key = self.import_public_key(sender_public_key_str)
            message_hash = SHA256.new(plaintext.encode('utf-8'))
            
            verified = False
            try:
                pkcs1_15.new(sender_public_key).verify(message_hash, signature)
                verified = True
            except (ValueError, TypeError):
                print("[WARNING] Chu ky khong hop le!")
                verified = False
            
            return (plaintext, verified)
            
        except Exception as e:
            print(f"[ERROR] Loi khi giai ma tin nhan: {e}")
            return (None, False)
