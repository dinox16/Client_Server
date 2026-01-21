# -*- coding: utf-8 -*-
"""
Test blockchain - Kiem tra module blockchain
"""

import sys
import os
import time

# Them duong dan de import
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'client'))

from blockchain import Block, MessageBlockchain


def test_block_creation():
    """Test tao block"""
    print("\n" + "="*60)
    print("TEST 1: Tao block")
    print("="*60)
    
    try:
        # Tao block
        timestamp = str(time.time())
        data = {
            'from': 'Alice',
            'to': 'Bob',
            'message': 'Xin chao',
            'timestamp': timestamp
        }
        
        block = Block(1, timestamp, data, '0')
        
        # Kiem tra thuoc tinh
        assert block.index == 1, "Index khong dung"
        assert block.timestamp == timestamp, "Timestamp khong dung"
        assert block.data == data, "Data khong dung"
        assert block.previous_hash == '0', "Previous hash khong dung"
        assert block.hash is not None, "Hash khong duoc tao"
        assert len(block.hash) == 64, "Hash length khong dung (phai la 64 hex chars)"
        
        print(f"[INFO] Block index: {block.index}")
        print(f"[INFO] Block hash: {block.hash[:16]}...")
        print("[PASS] Tao block thanh cong")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def test_block_mining():
    """Test mining Proof of Work"""
    print("\n" + "="*60)
    print("TEST 2: Mining Proof of Work")
    print("="*60)
    
    try:
        timestamp = str(time.time())
        data = {'from': 'Alice', 'to': 'Bob', 'message': 'Test', 'timestamp': timestamp}
        block = Block(1, timestamp, data, '0')
        
        # Mining voi difficulty = 2
        difficulty = 2
        block.mine_block(difficulty)
        
        # Kiem tra hash bat dau bang '00'
        assert block.hash.startswith('0' * difficulty), f"Hash khong bat dau bang {'0' * difficulty}"
        assert block.nonce > 0, "Nonce phai > 0 sau khi mining"
        
        print(f"[INFO] Mining xong voi nonce: {block.nonce}")
        print(f"[INFO] Hash: {block.hash}")
        print("[PASS] Mining Proof of Work thanh cong")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def test_blockchain_initialization():
    """Test khoi tao blockchain"""
    print("\n" + "="*60)
    print("TEST 3: Khoi tao blockchain")
    print("="*60)
    
    try:
        blockchain = MessageBlockchain()
        
        # Kiem tra genesis block
        assert len(blockchain.chain) == 1, "Chain phai co 1 genesis block"
        assert blockchain.chain[0].index == 0, "Genesis block phai co index 0"
        assert blockchain.chain[0].previous_hash == '0', "Genesis block phai co previous_hash = '0'"
        
        print(f"[INFO] Chain length: {len(blockchain.chain)}")
        print(f"[INFO] Genesis block hash: {blockchain.chain[0].hash[:16]}...")
        print("[PASS] Khoi tao blockchain thanh cong")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def test_add_message():
    """Test them tin nhan vao blockchain"""
    print("\n" + "="*60)
    print("TEST 4: Them tin nhan vao blockchain")
    print("="*60)
    
    try:
        blockchain = MessageBlockchain()
        
        # Them nhieu tin nhan
        messages = [
            ('Alice', 'Bob', 'Tin nhan 1'),
            ('Bob', 'Alice', 'Tin nhan 2'),
            ('Alice', 'Charlie', 'Tin nhan 3')
        ]
        
        for sender, recipient, message in messages:
            blockchain.add_message(sender, recipient, message)
        
        # Kiem tra so luong block
        expected_length = 1 + len(messages)  # genesis + messages
        assert len(blockchain.chain) == expected_length, f"Chain length sai: {len(blockchain.chain)} != {expected_length}"
        
        # Kiem tra lien ket giua cac block
        for i in range(1, len(blockchain.chain)):
            current = blockchain.chain[i]
            previous = blockchain.chain[i - 1]
            assert current.previous_hash == previous.hash, f"Block {i} khong lien ket dung voi block truoc"
        
        print(f"[INFO] Da them {len(messages)} tin nhan")
        print(f"[INFO] Chain length: {len(blockchain.chain)}")
        print("[PASS] Them tin nhan thanh cong")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def test_chain_validation():
    """Test xac thuc blockchain"""
    print("\n" + "="*60)
    print("TEST 5: Xac thuc blockchain")
    print("="*60)
    
    try:
        blockchain = MessageBlockchain()
        
        # Them tin nhan
        blockchain.add_message('Alice', 'Bob', 'Test 1')
        blockchain.add_message('Bob', 'Alice', 'Test 2')
        
        # Kiem tra chain hop le
        is_valid = blockchain.is_chain_valid()
        assert is_valid == True, "Chain hop le bi tu choi"
        
        print("[INFO] Blockchain hop le")
        print("[PASS] Xac thuc blockchain thanh cong")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def test_tampering_detection():
    """Test phat hien thay doi du lieu"""
    print("\n" + "="*60)
    print("TEST 6: Phat hien tampering")
    print("="*60)
    
    try:
        blockchain = MessageBlockchain()
        
        # Them tin nhan
        blockchain.add_message('Alice', 'Bob', 'Tin nhan goc')
        blockchain.add_message('Bob', 'Alice', 'Tin nhan 2')
        
        # Kiem tra truoc khi thay doi
        assert blockchain.is_chain_valid() == True, "Chain nen hop le truoc khi thay doi"
        print("[INFO] Blockchain hop le truoc khi thay doi")
        
        # Thay doi du lieu trong block
        print("[INFO] Dang thay doi du lieu trong block 1...")
        blockchain.chain[1].data['message'] = 'Tin nhan da bi hack!'
        
        # Kiem tra sau khi thay doi
        is_valid = blockchain.is_chain_valid()
        assert is_valid == False, "Blockchain van hop le sau khi bi thay doi (khong phat hien ra tampering)"
        
        print("[INFO] Blockchain KHONG hop le sau khi thay doi")
        print("[PASS] Phat hien tampering thanh cong")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def test_message_history():
    """Test lay lich su tin nhan"""
    print("\n" + "="*60)
    print("TEST 7: Lay lich su tin nhan")
    print("="*60)
    
    try:
        blockchain = MessageBlockchain()
        
        # Them tin nhan
        messages = [
            ('Alice', 'Bob', 'Xin chao'),
            ('Bob', 'Alice', 'Chao ban'),
            ('Alice', 'Bob', 'Ban khoe khong?')
        ]
        
        for sender, recipient, message in messages:
            blockchain.add_message(sender, recipient, message)
        
        # Lay lich su
        history = blockchain.get_message_history()
        
        assert len(history) == len(messages), f"So tin nhan khong dung: {len(history)} != {len(messages)}"
        
        # Kiem tra noi dung
        for i, (sender, recipient, message) in enumerate(messages):
            assert history[i]['from'] == sender, f"Sender khong dung o tin nhan {i}"
            assert history[i]['to'] == recipient, f"Recipient khong dung o tin nhan {i}"
            assert history[i]['message'] == message, f"Message khong dung o tin nhan {i}"
        
        print(f"[INFO] Da lay {len(history)} tin nhan tu blockchain")
        print("[PASS] Lay lich su tin nhan thanh cong")
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
    print("TEST BLOCKCHAIN MODULE")
    print("="*60)
    
    results = []
    
    results.append(("Test Block Creation", test_block_creation()))
    results.append(("Test Block Mining", test_block_mining()))
    results.append(("Test Blockchain Initialization", test_blockchain_initialization()))
    results.append(("Test Add Message", test_add_message()))
    results.append(("Test Chain Validation", test_chain_validation()))
    results.append(("Test Tampering Detection", test_tampering_detection()))
    results.append(("Test Message History", test_message_history()))
    
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
