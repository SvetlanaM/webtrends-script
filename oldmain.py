import socket, pip
from urllib.request import urlopen

pip.main(['install', 'PySocks'])

import socks

socks.set_default_proxy(socks.SOCKS5, "localhost", 9999)
socket.socket = socks.socksocket

html = urlopen("../find-ip-address")
print(html.read())