from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

user = 'root'
passwd = 'root'
ip = '172.18.10.12'
port = 21

authorizer = DummyAuthorizer()
authorizer.add_user(user, passwd, "/", perm="elradfmw")
authorizer.add_anonymous("/")

handler = FTPHandler
handler.authorizer = authorizer
server = FTPServer((ip, port), handler)
server.serve_forever()
