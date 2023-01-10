#!/usr/bin/env python3
import socket, sys
import time

#define address & buffer size
HOST = ""
PORT = 8002
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ins:

        #QUESTION 3
        ins.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #bind socket to address
        ins.bind((HOST, PORT))

        #set to listening mode
        ins.listen(2)

        #continuously listen for connections
        while True:
            conn, addr = ins.accept()
            print("Connected by", addr)

            try:
                #define address info, payload, and buffer size
                host = 'www.google.com'
                port = 80
                payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
                buffer_size = 4096

                #make the socket, get the ip, and connect
                outs = create_tcp_socket()

                remote_ip = get_remote_ip(host)

                outs.connect((remote_ip , port))
                print (f'Socket Connected to {host} on ip {remote_ip}')

                #send the data and shutdown

                full_data = conn.recv(BUFFER_SIZE)
                send_data(outs, full_data.decode())
                outs.shutdown(socket.SHUT_WR)

                #continue accepting data until no more left
                full_data = b""
                while True:
                    data = outs.recv(buffer_size)
                    if not data:
                        break
                    full_data += data
                conn.sendall(full_data)
            except Exception as e:
                print(e)
            finally:
                #always close at the end!
                outs.close()
                conn.close()


if __name__ == "__main__":
    main()
