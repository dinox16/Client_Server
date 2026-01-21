# Do An Mang May Tinh - Chat Client Server

He thong chat LAN voi ma hoa End-to-End va Blockchain

## Tinh nang

- Chat giua nhieu client qua server hub
- Ma hoa E2EE (RSA + AES hybrid)
- Chu ky so xac thuc nguoi gui
- Blockchain luu lich su tin nhan
- Mo phong tan cong malware
- Co che bao ve chong doc trom du lieu

## Cai dat

```bash
pip install pycryptodome
```

## Cach chay

### 1. Khoi dong Server
```bash
cd server
python server.py
```

### 2. Khoi dong Client
```bash
cd client
python
>>> from client import SecureChatClient
>>> alice = SecureChatClient("Alice")
>>> alice.connect("127.0.0.1", 5555)
>>> alice.send_message("Bob", "Xin chao!")
```

### 3. Demo tu dong
```bash
python demo/run_demo.py
```

### 4. Demo tan cong
```bash
python demo/attack_scenario.py
```

## Tai lieu

Xem chi tiet trong file `HUONG_DAN_THUC_HIEN.txt`

## Kien truc

```
Client A <--E2EE--> Server <--E2EE--> Client B
             |
         Blockchain
```

## Bao mat

- End-to-End Encryption
- Digital Signatures  
- Blockchain Integrity
- Malware Resistance
