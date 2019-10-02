import sys, socket, os

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print('usage: \"python3', sys.argv[0], '<file> <host> <port>\"')
    sys.exit(-1)
  if list(filter(lambda a: a == sys.argv[1], os.listdir())) == []:
    print('no such file \"' + sys.argv[1] + '\"')
    sys.exit(-2)

  sock = socket.socket()
  sock.connect((sys.argv[2], int(sys.argv[3])))

  sock.send(str(len(sys.argv[1].encode('ascii'))).encode('ascii'))
  
  sock.send(sys.argv[1].encode('ascii'))
  
  with open(sys.argv[1], 'rb') as f:
    transf = 0
    buff = f.read(1024)
    while buff:
      sock.send(buff)
      transf += 1024
      print(str(os.path.getsize(sys.argv[1]) - transf) if (os.path.getsize(sys.argv[1]) - transf) > 0 else '0', 'bytes left')
      buff = f.read(1024)

  sock.close()