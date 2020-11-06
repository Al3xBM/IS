from Crypto import Random
from Crypto.Cipher import AES
import socket

class keyManager:
  @staticmethod
  def gen_K1(key):
    k = Random.get_random_bytes(16)
    print('Key is: ', k)
    cipher = AES.new(key, AES.MODE_CBC, b'1234567890123456')
    encK = cipher.encrypt(k)
    return encK

  @staticmethod
  def gen_K3():
    return Random.get_random_bytes(16)



HOST = '127.0.0.1'
PORT = 65432

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    connB, addrB = s.accept()
    connA, addrA = s.accept()

    pubKey = keyManager.gen_K3()
    print('pub key is: ', pubKey)

    with connB:
        print('Connected by', addrB)
        while True:
            data = connB.recv(1024)
            print("Received: ", data)
            if not data:
                break
            connB.sendall(pubKey)

    with connA:
      print('Connected by', addrA)
      while True:
          data = connA.recv(1024)
          print("Received: ", data)
          if data == b'cbc' or data == b'ofb':
            toSend = keyManager.gen_K1(pubKey)
            print('enc key is: ', toSend)
          else:
            toSend = pubKey
          if not data:
              break
          connA.sendall(toSend)

main()