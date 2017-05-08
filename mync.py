#!/usr/bin/python3
import socket,os,readline,sys,time

def connect():
    sockfile="/tmp/tmp.sock"
    if os.path.exists(sockfile):
        os.remove(sockfile)
    client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    client.bind(sockfile)
    client.connect("/tmp/m.sock")
    client.settimeout(1)
    return client

def close(client):
    sockfile="/tmp/tmp.sock"
    client.close()
    os.remove(sockfile)

def main():
    base_port=2000
    client=connect()
    while True:
        try:
            y=input('>')
            if y=='' or y[0]=='p':
                x='ping'
            elif y[0]=='a':
                x='add: {{"server_port":{},"password":"{}"}}'.format(int(y[1])+base_port,y[2:])
            elif y[0]=='r':
                x='remove: {{"server_port":{}}}'.format(int(y[1])+base_port,y[2:])
            else:
                continue
            client.send((x).encode('utf8'))
            print(client.recv(2048).decode('utf8'))
        except KeyboardInterrupt:
            break
    close(client)

def init():
    os.system('ss-manager -s \'::\' -s 0.0.0.0 -u -m chacha20 -f /tmp/ss-manager.pid --manager-address /tmp/m.sock')
    time.sleep(5)
    client=connect()
    os.chdir('/root/.shadowsocks')
    for i in os.listdir():
        x='add: {}'.format(open(i).read().replace("\n",'').replace('port":"','port":').replace('","pass',',"pass').replace(',}','}'))
        print(x)
        client.send((x).encode('utf8'))
        print(client.recv(2048).decode('utf8'))
    close(client)

if len(sys.argv)>1:
    if sys.argv[1]=='init':
        init()
        exit(0)
main()
