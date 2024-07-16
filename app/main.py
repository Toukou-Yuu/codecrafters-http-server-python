# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("server starting...")

    # Uncomment this to pass the first stage
    # 监听本地4221端口
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # accept返回两个元组：
    # 1. 第一个元素是表示与客户端通信的套接字对象（通常称为客户端套接字）。
    # 2. 第二个元素是客户端的地址信息（例如IP地址和端口号）。
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024)

    # 'b' 表示这是一个字节字符串，而不是普通的Unicode字符串
    # 在网络编程中，recv() 方法返回的数据是字节串（bytes），而不是普通的字符串（str）。
    req_lines = request.split(b"\r\n")
    # method, request target(path), http version
    req_line = req_lines[0].decode("utf-8")
    method, path, _ = req_line.split(" ")
    if path == "/":
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/echo"):
        # /echo/{echo_str}
        echo_str = path[len("/echo/"):]
        status = "HTTP/1.1 200 OK"
        content_type = "Content-Type: text/plain"
        content_length = f"Content-Length: {len(echo_str)}"
        format_response = f"{status}\r\n{content_type}\r\n{content_length}\r\n\r\n{echo_str}"
        response = format_response.encode("utf-8")
        print(f"read: {echo_str}")
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    client_socket.sendall(response)
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
