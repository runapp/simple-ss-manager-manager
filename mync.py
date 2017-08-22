#!/usr/bin/python3
import socket
import os
import readline
import sys
import time

base_port = 2000


def connect():
    sockfile = "/tmp/tmp.sock"
    if os.path.exists(sockfile):
        os.remove(sockfile)
    client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    client.bind(sockfile)
    client.connect("/tmp/m.sock")
    client.settimeout(1)
    return client


def close(client):
    sockfile = "/tmp/tmp.sock"
    client.close()
    os.remove(sockfile)


def getparam(str):
    global base_port
    charlist = "0123456789 "
    i = 1
    while str[i] in charlist:
        i += 1
    return (int(str[1:i].strip()) + base_port, str[i:])


def main():
    client = connect()
    while True:
        try:
            y = input('>')
            if y == '' or y[0] == 'p':
                x = 'ping'
            elif y[0] == 'a':
                port, pwd = getparam(y)
                x = 'add: {{"server_port":{},"password":"{}"}}'.format(
                    port, pwd)
            elif y[0] == 'r':
                x = 'remove: {{"server_port":{}}}'.format(port)
            elif y[0] == 'q':
                break
            else:
                continue
            client.send((x).encode('utf8'))
            print(x)
            print(client.recv(2048).decode('utf8'))
        except KeyboardInterrupt:
            break
    close(client)


def init():
    os.system('ss-manager -s \'::\' -s 0.0.0.0 -u -m chacha20-ietf-poly1305 -f /tmp/ss-manager.pid --manager-address /tmp/m.sock')
    time.sleep(5)
    client = connect()
    os.chdir('/root/.shadowsocks')
    for i in os.listdir():
        x = 'add: {}'.format(open(i).read().replace("\n", '').replace(
            'port":"', 'port":').replace('","pass', ',"pass').replace(',}', '}'))
        print(x)
        client.send((x).encode('utf8'))
        print(client.recv(2048).decode('utf8'))
    close(client)


def install():
    f = open('/usr/lib/systemd/system/ss-manager.service', 'w')
    f.write(
        r'''[Unit]
Description=ss-manager daemon
Documentation=man:ss-manager
After=network.target

[Service]
Type=forking
LimitNOFILE=32768
ExecStart=''' + os.path.realpath(__file__) + r''' init

[Install]
WantedBy=multi-user.target
''')
    f.close()


if len(sys.argv) > 1:
    if sys.argv[1] == 'init':
        init()
    elif sys.argv[1] == 'install':
        install()
    else:
        main()
else:
    main()
