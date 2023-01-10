import socket

## NOTE : there is a timeout of 15 seconds

def main():
    # create a socket
    s = socket.socket()
    s.settimeout(15)

    # bind the socket
    s.bind(('localhost', 8001))

    # listen for connections
    s.listen()

    # accept a connection
    c, addr = s.accept()

    timeout = False

    while not timeout:

        # run while active
        while True:
            try:
                r = c.recv(1024)
                if not r:
                    continue
                c.send(r)
            except socket.timeout:
                timeout = True
                break

    # close the connection
    c.close()


if __name__ == '__main__':
    main()


