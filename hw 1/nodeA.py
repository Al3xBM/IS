from Crypto import Random
from Crypto.Cipher import AES
import socket
import sys

class nodeA:
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

  def enc(self, block):
    block = '{}'.format(block).encode()
    if self.mode == b'cbc':
      cript = int.from_bytes(self.operator, byteorder="big") ^ int.from_bytes(block, byteorder="big")
      cript = cript ^ int.from_bytes(self.privKey, byteorder="big")
      cript = cript.to_bytes(max(len(self.operator), len(block)), byteorder="big")
      self.setOperator(cript)
    else:
      cript = int.from_bytes(self.privKey, byteorder="big") ^ int.from_bytes(self.operator, byteorder="big")
      mx = max(len(self.privKey), len(self.operator))
      self.setOperator(cript.to_bytes(mx, byteorder="big"))
      cript = cript ^ int.from_bytes(block, byteorder="big")
      cript = cript.to_bytes(max(mx, len(block)), byteorder="big")
    return cript



HOST = '127.0.0.1'
PORT = 65432
PORT2 = 54321

def main():
  global nA
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Provide public key')
    data = s.recv(1024)
    print('Received: ',data)
    nA = nodeA(data)
    print('How do you wish to communicate? Choose CBC or OFB')
    print('If a proper mode is not selected, it will be defaulted to CBC')
    askComm = input()
    if askComm.lower() == "ofb":
      s.sendall(b'ofb')
      nA.setCommMode(b'ofb')
    else:
      s.sendall(b'cbc')
      nA.setCommMode(b'cbc')
    data = s.recv(1024)
    print('Received: ',data)
    encKey = data
    nA.setPrivKey(data)
    s.shutdown(socket.SHUT_RDWR)
    s.close()
  
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT2))
    s.listen()
    conn, addr = s.accept()
    with conn:
      print('Connected by ', addr)
      data = conn.recv(1024)
      print("Received: ", data)
      conn.sendall(encKey)
      conn.sendall(nA.getCommMode())
      data = conn.recv(1024)
      print("Received: ", data)
      file = open('text.txt')
      nA.setOperator(b'1234567890123456')
      while True:
        block = file.read(16)
        if not block:
          break
        print('Read from file: ', block)
        cript = nA.enc(block)
        print('Encrypted as: ', cript)
        conn.sendall(cript)


      

main()