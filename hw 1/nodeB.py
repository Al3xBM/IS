from Crypto import Random
from Crypto.Cipher import AES
import socket
import time

class nodeB:
  def __init__(self, k):
    self.publicKey = k

  def setCommMode(self, m):
    self.mode = m

  def setPrivKey(self, k):
    cipher = AES.new(self.publicKey, AES.MODE_CBC, b'1234567890123456')
    self.privKey = cipher.decrypt(k)
    print('decripted key is: ', self.privKey)

  def getPrivKey(self):
    return self.privKey

  def getCommMode(self):
    return self.mode

  def getPublicKey(self):
    return self.publicKey

  def setOperator(self, op):
    self.operator = op

  def decr(self, block):
    if self.mode == b'cbc':
      plain = int.from_bytes(self.privKey, byteorder="big") ^ int.from_bytes(block, byteorder="big")
      plain = plain ^ int.from_bytes(self.operator, byteorder="big") 
      plain = plain.to_bytes(max(len(self.operator), len(block)), byteorder="big")
      self.setOperator(block)
    else:
      plain = int.from_bytes(self.privKey, byteorder="big") ^ int.from_bytes(self.operator, byteorder="big")
      mx = max(len(self.privKey), len(self.operator))
      self.setOperator(plain.to_bytes(mx, byteorder="big"))
      plain = plain ^ int.from_bytes(block, byteorder="big")
      plain = plain.to_bytes(max(mx, len(block)), byteorder="big")
    return plain

HOST = '127.0.0.1'
PORT = 65432
PORT2 = 54321

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Provide public key')
    data = s.recv(1024)
    print('Received: ',data)
    nB = nodeB(data)
    s.shutdown(socket.SHUT_RDWR)
    s.close()


  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
    time.sleep(7)
    s2.connect((HOST, PORT2))
    s2.sendall(b'Please provide the cripted key and the comm mode')
    data = s2.recv(1024)
    print('Received: ',data)
    nB.setPrivKey(data)
    data = s2.recv(1024)
    print('Received: ',data)
    nB.setCommMode(data)
    s2.sendall(b'You can now send the message')
    nB.setOperator(b'1234567890123456')
    while True:
      data = s2.recv(1024)
      if not data:
        break
      print(nB.decr(data))


main()