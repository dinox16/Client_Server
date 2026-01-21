# -*- coding: utf-8 -*-
"""
Module Blockchain - Luu lich su tin nhan bat bien
Cung cap chuc nang luu tru tin nhan voi Proof of Work
"""

import hashlib
import json
from datetime import datetime


class Block:
    """
    Block trong blockchain
    Moi block chua 1 tin nhan va duoc lien ket voi block truoc
    """
    
    def __init__(self, index, timestamp, data, previous_hash):
        """
        Khoi tao block moi
        
        Args:
            index: Vi tri cua block trong chain
            timestamp: Thoi gian tao block
            data: Du lieu (tin nhan)
            previous_hash: Hash cua block truoc do
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Tinh SHA-256 hash cua block
        
        Returns:
            str: Hash hex string
        """
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty=2):
        """
        Proof of Work mining
        Tim nonce sao cho hash bat dau bang '00...'
        
        Args:
            difficulty: So luong so 0 o dau hash
        """
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"[BLOCKCHAIN] Block {self.index} da duoc mine: {self.hash[:16]}... (nonce: {self.nonce})")


class MessageBlockchain:
    """
    Blockchain luu tru lich su tin nhan
    Moi tin nhan la 1 block moi
    """
    
    def __init__(self):
        """Khoi tao blockchain voi genesis block"""
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        print("[BLOCKCHAIN] Da khoi tao voi genesis block")
    
    def create_genesis_block(self):
        """
        Tao block dau tien trong chain
        
        Returns:
            Block: Genesis block
        """
        return Block(0, str(datetime.now()), {
            'from': 'SYSTEM',
            'to': 'SYSTEM',
            'message': 'Genesis Block',
            'timestamp': str(datetime.now())
        }, '0')
    
    def get_latest_block(self):
        """
        Lay block cuoi cung trong chain
        
        Returns:
            Block: Block cuoi cung
        """
        return self.chain[-1]
    
    def add_message(self, sender, recipient, message):
        """
        Them tin nhan moi vao blockchain
        
        Args:
            sender: Nguoi gui
            recipient: Nguoi nhan
            message: Noi dung tin nhan
        """
        try:
            previous_block = self.get_latest_block()
            new_index = previous_block.index + 1
            timestamp = str(datetime.now())
            
            block_data = {
                'from': sender,
                'to': recipient,
                'message': message,
                'timestamp': timestamp
            }
            
            new_block = Block(new_index, timestamp, block_data, previous_block.hash)
            new_block.mine_block(self.difficulty)
            self.chain.append(new_block)
            
            print(f"[BLOCKCHAIN] Da them tin nhan tu {sender} den {recipient}")
        except Exception as e:
            print(f"[ERROR] Loi khi them vao blockchain: {e}")
    
    def is_chain_valid(self):
        """
        Kiem tra tinh toan ven cua blockchain
        
        Returns:
            bool: True neu chain hop le, False neu khong
        """
        try:
            for i in range(1, len(self.chain)):
                current_block = self.chain[i]
                previous_block = self.chain[i - 1]
                
                # Kiem tra hash cua block hien tai
                if current_block.hash != current_block.calculate_hash():
                    print(f"[ERROR] Block {i} co hash khong hop le")
                    return False
                
                # Kiem tra lien ket voi block truoc
                if current_block.previous_hash != previous_block.hash:
                    print(f"[ERROR] Block {i} khong lien ket dung voi block truoc")
                    return False
                
                # Kiem tra Proof of Work
                if not current_block.hash.startswith('0' * self.difficulty):
                    print(f"[ERROR] Block {i} khong thoa man Proof of Work")
                    return False
            
            return True
        except Exception as e:
            print(f"[ERROR] Loi khi xac thuc blockchain: {e}")
            return False
    
    def print_chain(self):
        """In lich su tin nhan trong blockchain"""
        print("\n" + "="*60)
        print("LICH SU TIN NHAN TRONG BLOCKCHAIN")
        print("="*60)
        
        for block in self.chain:
            print(f"\nBlock {block.index}:")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Data: {json.dumps(block.data, indent=4, ensure_ascii=False)}")
            print(f"  Previous Hash: {block.previous_hash[:16]}...")
            print(f"  Hash: {block.hash[:16]}...")
            print(f"  Nonce: {block.nonce}")
        
        print("\n" + "="*60)
        print(f"Tong so block: {len(self.chain)}")
        print(f"Blockchain hop le: {self.is_chain_valid()}")
        print("="*60 + "\n")
    
    def get_message_history(self):
        """
        Lay lich su tin nhan
        
        Returns:
            list: Danh sach cac tin nhan
        """
        messages = []
        for block in self.chain[1:]:  # Bo qua genesis block
            messages.append(block.data)
        return messages
