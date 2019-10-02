import sys, socket, os
from threading import Thread

class CustomUploader(Thread):
  def __init__(self, sock: socket.socket, address):
    super().__init__(daemon=True)
    self.sock = sock
    self.address = address
    self.resolve_filename = lambda file, i: (file + (('_copy' + str(i)) if i != -1 else '')) \
                   if list(filter(lambda a: a == (file + (('_copy' + str(i)) if i != -1 else '')), \
                   os.listdir())) == [] else self.resolve_filename(file, i + 1)
  def _close(self):
    self.sock.close()

  def run(self):
    len_filename = int(self.sock.recv(2).decode('ascii'))
    file_name = self.sock.recv(len_filename).decode('ascii')

    file = self.resolve_filename(file_name, -1)

    with open(file, 'wb') as f:
      buff = self.sock.recv(1024)
      while buff:
        f.write(buff)
        buff = self.sock.recv(1024)

    print('\"' + file_name + '\"', 'accepted as', '\"' + file + '\"')
    self._close()
    return

sock = socket.socket()

sock.bind(("0.0.0.0", 8800))

sock.listen(5)

while True:
   CustomUploader(*sock.accept()).start()

sock.close()