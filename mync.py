#!/usr/bin/python3
import socket
import os
import readline
import sys
import time

LOCAL_SOCK = "/var/run/ss-manager-temp-" + str(os.getpid()) + ".sock"
SERVER_SOCK = "/var/run/m.sock"
CMD_LINE = 'ss-manager -s "::" -s 0.0.0.0 -u -m aes-256-gcm -f /var/run/ss-manager.pid --manager-address ' + SERVER_SOCK
conf_dir = '/root/.shadowsocks'
base_port = 2000


def connect():
    if os.path.exists(LOCAL_SOCK):
        os.remove(LOCAL_SOCK)
    client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    client.bind(LOCAL_SOCK)
    client.connect(SERVER_SOCK)
    client.settimeout(1)
    return client


def close(client):
    client.close()
    os.remove(LOCAL_SOCK)


def getparam(s: str):
    global base_port
    s = s.strip()
    charlist = "0123456789"
    i = 1
    while s[i] in charlist:
        i += 1
    return (int(s[1:i]) + base_port, s[i:].strip() if i < len(s) else '')


def main():
    client = connect()
    while True:
        try:
            y = input('>')
            if y == '' or y[0] == 'p':
                x = 'ping'
            elif y[0] == 'a':
                port, pwd = getparam(y)
                x = 'add: {{"server_port":{},"password":"{}"}}'.format(port, pwd)
            elif y[0] == 'r':
                port, _ = getparam(y)
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
    import json
    os.system(CMD_LINE)
    time.sleep(2)
    client = connect()
    os.chdir(conf_dir)
    for i in os.listdir():
        if not i.endswith('.conf'):
            continue
        with open(i) as f:
            c = json.load(f)
            x = 'add: {{"server_port":{},"password":"{}"}}'.format(c['server_port'], c['password'])
            print('Sending:\n%s\n' % x)
            client.send((x).encode('utf8'))
            print('Received:\n%s\n' % client.recv(2048).decode('utf8'))
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
        base_port = int(sys.argv[1])
        main()
else:
    main()
