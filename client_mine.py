import socket

def main():
    # connect to google.com using sockets
    c = socket.socket()
    c.settimeout(5)

    c.connect(('google.com', 80))

    # send a GET request
    c.send(b'GET /teapot HTTP/1.1\r\nHost: www.google.com\r\n\r\n')

    # receive the response
    response = b""

    timeout = False

    while not timeout:
        try:
            curr = c.recv(1024)
            response = response + curr
            if not curr or len(curr) < 1024:
                break
        except socket.timeout:
            timeout = True
            break

    # print the response
    print(response.decode())

    # close
    c.close()


if __name__ == '__main__':
    main()