# -*- coding: utf-8 -*-
"""
Test encryption - Kiem tra module ma hoa
"""

import sys
import os

# Them duong dan de import
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'client'))

from encryption import CryptoManager


def test_key_generation():
    """Test tao cap khoa RSA"""
    print("\n" + "="*60)
    print("TEST 1: Tao cap khoa RSA")
    print("="*60)
    
    try:
        crypto = CryptoManager()
        
        # Kiem tra key pair da duoc tao
        assert crypto.key_pair is not None, "Key pair khong duoc tao"
        assert crypto.private_key is not None, "Private key khong duoc tao"
        assert crypto.public_key is not None, "Public key khong duoc tao"
        
        # Kiem tra kich thuoc key
        assert crypto.key_pair.size_in_bits() == 2048, "Key size khong dung (phai la 2048-bit)"
        
        # Kiem tra export public key
        public_key_str = crypto.get_public_key_string()
        assert public_key_str is not None, "Khong the export public key"
        assert len(public_key_str) > 0, "Public key string rong"
        
        print("[PASS] Tao cap khoa RSA thanh cong")
        print(f"[INFO] Key size: {crypto.key_pair.size_in_bits()} bits")
        print(f"[INFO] Public key length: {len(public_key_str)} characters")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def test_encryption_decryption():
    """Test ma hoa va giai ma"""
    print("\n" + "="*60)
    print("TEST 2: Ma hoa va giai ma")
    print("="*60)
    
    try:
        # Tao 2 clients
        alice = CryptoManager()
        bob = CryptoManager()
        
        # Tin nhan test
        message = "Day la tin nhan test cho do an Mang May Tinh!"
        print(f"[INFO] Tin nhan goc: '{message}'")
        
        # Alice ma hoa tin nhan cho Bob
        bob_public_key = bob.get_public_key_string()
        encrypted_data = alice.encrypt_message(message, bob_public_key)
        
        assert encrypted_data is not None, "Ma hoa that bai"
        assert 'encrypted_aes_key' in encrypted_data, "Thieu encrypted_aes_key"
        assert 'ciphertext' in encrypted_data, "Thieu ciphertext"
        assert 'signature' in encrypted_data, "Thieu signature"
        assert 'nonce' in encrypted_data, "Thieu nonce"
        assert 'tag' in encrypted_data, "Thieu tag"
        
        print("[INFO] Da ma hoa thanh cong")
        print(f"[INFO] Ciphertext: {encrypted_data['ciphertext'][:50]}...")
        
        # Bob giai ma tin nhan
        alice_public_key = alice.get_public_key_string()
        plaintext, verified = bob.decrypt_message(encrypted_data, alice_public_key)
        
        assert plaintext is not None, "Giai ma that bai"
        assert plaintext == message, f"Tin nhan khong khop: '{plaintext}' != '{message}'"
        assert verified == True, "Chu ky khong hop le"
        
        print(f"[INFO] Da giai ma: '{plaintext}'")
        print(f"[INFO] Chu ky hop le: {verified}")
        print("[PASS] Ma hoa va giai ma thanh cong")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def test_signature_verification():
    """Test xac thuc chu ky so"""
    print("\n" + "="*60)
    print("TEST 3: Xac thuc chu ky so")
    print("="*60)
    
    try:
        # Tao 3 clients
        alice = CryptoManager()
        bob = CryptoManager()
        charlie = CryptoManager()
        
        message = "Tin nhan co chu ky"
        
        # Alice ma hoa cho Bob
        bob_public_key = bob.get_public_key_string()
        encrypted_data = alice.encrypt_message(message, bob_public_key)
        
        # Bob giai ma voi public key dung (Alice)
        alice_public_key = alice.get_public_key_string()
        plaintext1, verified1 = bob.decrypt_message(encrypted_data, alice_public_key)
        
        assert verified1 == True, "Chu ky hop le bi tu choi"
        print("[INFO] Chu ky hop le duoc xac thuc dung")
        
        # Bob thu giai ma voi public key SAI (Charlie)
        charlie_public_key = charlie.get_public_key_string()
        plaintext2, verified2 = bob.decrypt_message(encrypted_data, charlie_public_key)
        
        # Van giai ma duoc nhung chu ky khong hop le
        assert plaintext2 == message, "Khong giai ma duoc tin nhan"
        assert verified2 == False, "Chu ky sai van duoc chap nhan"
        print("[INFO] Chu ky khong hop le duoc phat hien dung")
        
        print("[PASS] Xac thuc chu ky so thanh cong")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def test_multiple_messages():
    """Test ma hoa nhieu tin nhan"""
    print("\n" + "="*60)
    print("TEST 4: Ma hoa nhieu tin nhan")
    print("="*60)
    
    try:
        alice = CryptoManager()
        bob = CryptoManager()
        
        messages = [
            "Tin nhan 1",
            "Tin nhan 2 dai hon mot chut",
            "Tin nhan 3 voi ki tu dac biet: @#$%^&*()",
            "Tin nhan 4 co chu so: 123456789",
            "Tin nhan 5 rat rat rat dai " * 10
        ]
        
        bob_public_key = bob.get_public_key_string()
        alice_public_key = alice.get_public_key_string()
        
        for i, msg in enumerate(messages):
            # Ma hoa
            encrypted = alice.encrypt_message(msg, bob_public_key)
            assert encrypted is not None, f"Ma hoa tin nhan {i+1} that bai"
            
            # Giai ma
            plaintext, verified = bob.decrypt_message(encrypted, alice_public_key)
            assert plaintext == msg, f"Tin nhan {i+1} khong khop"
            assert verified == True, f"Chu ky tin nhan {i+1} khong hop le"
            
            print(f"[INFO] Tin nhan {i+1}: PASS (length: {len(msg)})")
        
        print("[PASS] Ma hoa nhieu tin nhan thanh cong")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def run_all_tests():
    """Chay tat ca cac test"""
    print("\n" + "="*60)
    print("TEST ENCRYPTION MODULE")
    print("="*60)
    
    results = []
    
    results.append(("Test Key Generation", test_key_generation()))
    results.append(("Test Encryption/Decryption", test_encryption_decryption()))
    results.append(("Test Signature Verification", test_signature_verification()))
    results.append(("Test Multiple Messages", test_multiple_messages()))
    
    # Ket qua tong
    print("\n" + "="*60)
    print("KET QUA TEST")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")
    
    print("="*60)
    print(f"Tong: {passed}/{total} tests passed")
    
    if passed == total:
        print("TAT CA TESTS PASS!")
    else:
        print(f"CO {total - passed} TESTS FAIL!")
    
    print("="*60 + "\n")
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
