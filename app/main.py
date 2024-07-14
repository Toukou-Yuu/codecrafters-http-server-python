# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    # 监听本地4221端口
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # 'b' 表示这是一个字节字符串，而不是普通的Unicode字符串
    # accept返回两个元组：
    # 1. 第一个元素是表示与客户端通信的套接字对象（通常称为客户端套接字）。
    # 2. 第二个元素是客户端的地址信息（例如IP地址和端口号）。
    server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
