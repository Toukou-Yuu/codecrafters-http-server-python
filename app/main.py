# Uncomment this to pass the first stage
import socket

# RFC9112标准: status-line = HTTP-version SP status-code SP [ reason-phrase ]
HTTP_200 = "HTTP/1.1 200 OK"
HTTP_404 = "HTTP/1.1 404 Not Found"
TEXT_CONTENT = "Content-Type: text/plain"
EMPTY_STR = ""
UTF8 = "utf-8"

# 监听本地4221端口
server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
# accept返回两个元组：
# 1. 第一个元素是表示与客户端通信的套接字对象（通常称为客户端套接字）。
# 2. 第二个元素是客户端的地址信息（例如IP地址和端口号）。
client_socket, client_address = server_socket.accept()

def main():
    print("server starting...")

    # request = request-line + [headers] + [request-body]
    request = client_socket.recv(1024)
    req_segments = request.split(b"\r\n")
    req_line = req_segments[0].decode(UTF8)
    req_headers = read_headers(request.decode(UTF8))
    # RFC9112标准: request-line = method SP request-target SP HTTP-version
    method, path, http_version = req_line.split(" ")
    if path == "/":
        resp = construct_resp(HTTP_200)
    elif match_echo(path):
        # /echo/{echo_str}
        print(f"request-target: {path}\nrequest-headers: {req_headers}")
        resp_body = path[len("/echo/"):]
        resp_length = f"Content-Length: {len(resp_body)}"
        resp_headers = construct_headers(TEXT_CONTENT, resp_length)
        resp = construct_resp(HTTP_200, resp_headers, resp_body)
    elif match_user_agent(path):
        # 读取用户代理
        print(f"request-target: {path}\nrequest-headers: {req_headers}")
        resp_body = read_user_agent(req_headers)
        resp_length = f"Content-Length: {len(resp_body)}"
        resp_headers = construct_headers(TEXT_CONTENT, resp_length)
        resp = construct_resp(HTTP_200, resp_headers, resp_body)
    else:
        resp = construct_resp(HTTP_404)

    client_socket.sendall(resp)
    close_server()

def construct_headers(content_type: str, content_length: str) -> str:
    if content_type == EMPTY_STR and content_length == EMPTY_STR:
        return EMPTY_STR
    elif content_type == EMPTY_STR:
        return f"{content_length}\r\n"
    elif content_length == EMPTY_STR:
        return f"{content_type}\r\n"

    return f"{content_type}\r\n{content_length}\r\n"

def construct_resp(status: str, headers: str = "", body: str = "") -> bytes:
    format_resp = f"{status}\r\n{headers}\r\n{body}"
    return format_resp.encode("utf-8")

def match_echo(path: str) -> bool:
    return path.startswith("/echo")

def match_user_agent(path: str) -> bool:
    return path.startswith("/user-agent")

def read_user_agent(headers: list[str]) -> str:
    for header in headers:
        if header.startswith("User-Agent:"):
            return header.split(":")[1].strip()
    return ""

def read_headers(req: str) -> list[str]:
    # 如果一个请求有请求头，那这个请求一定包含两个CRLF
    end = req.find("\r\n\r\n")
    headers = req[:end].split("\r\n")
    # headers[0]是request-line
    return headers[1:]

def close_server():
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
