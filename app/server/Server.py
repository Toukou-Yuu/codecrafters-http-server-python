import socket
import threading
from app.server.Request import Request
from app.server.Response import Response

# RFC9112标准: status-line = HTTP-version SP status-code SP [ reason-phrase ]
HTTP_200 = "HTTP/1.1 200 OK"
HTTP_404 = "HTTP/1.1 404 Not Found"
TEXT_PLAIN = "Content-Type: text/plain"
EMPTY_STR = ""
UTF8 = "utf-8"
VALID_ENDPOINT = ["/", "/echo", "/user-agent"]

class Server:
    def link_start(self) -> None:
        self.SERVER_SOCKET = socket.create_server(("localhost", 4221), reuse_port=True)
        while True:
            print("listening port: 4221")
            client_socket, client_addr = self.SERVER_SOCKET.accept()
            print("accept request, creating threading to handle it......")
            threading.Thread(target=self.handle_req, args=(client_socket, client_addr)).start()

    def close(self, client_socket) -> None:
        self.SERVER_SOCKET.close()
        client_socket.close()

    def handle_req(self, client_socket, client_addr) -> None:
        self.req = Request(client_socket.recv(1024).decode("utf8"))
        print(f"handling request: {self.req.path}")
        if self.req.full_match_endpoint("/"):
            self.handle_root(client_socket)
        elif self.req.match_endpoint("/echo"):
            # 读取echo_str：/echo/{echo_str}
            self.handle_echo(client_socket)
        elif self.req.full_match_endpoint("/user-agent"):
            # 读取用户代理
            self.handle_user_agent(client_socket)
        else:
            self.handle_404(client_socket)
        # self.close()


    def handle_root(self, client_socket) -> None:
        print("-----------handle root request-----------")
        resp = Response()
        resp.add_status(HTTP_200)
        resp.add_header(TEXT_PLAIN)
        resp.add_header("Content-Length: 0")
        constructed = resp.construct_utf8()
        print(f"response: {constructed}")
        client_socket.sendall(constructed)

    def handle_echo(self, client_socket) -> None:
        # 读取echo字符串：/echo/{echo_str}
        print("-----------handle echo request-----------")
        req_target = self.req.read_req_target()
        body = req_target[len("/echo/"):]
        resp = Response()
        resp.add_status(HTTP_200)
        resp.add_body(body)
        resp.add_header(TEXT_PLAIN)
        resp.add_header(f"Content-Length: {len(body)}")
        constructed = resp.construct_utf8()
        print(f"response: {constructed}")
        client_socket.sendall(resp.construct_utf8())

    def handle_user_agent(self, client_socket) -> None:
        # 读取用户代理
        print("-----------handle user-agent-----------")
        resp = Response()
        body = self.req.read_user_agent()
        resp.add_status(HTTP_200)
        resp.add_body(body)
        resp.add_header(TEXT_PLAIN)
        resp.add_header(f"Content-Length: {len(body)}") 
        constructed = resp.construct_utf8()
        print(f"response: {constructed}")
        client_socket.sendall(resp.construct_utf8())

    def handle_404(self, client_socket) -> None:
        print("-----------handle 404-----------")
        resp = Response()
        resp.add_status(HTTP_404)
        resp.add_header("Content-Length: 0")
        constructed = resp.construct_utf8()
        print(f"response: {constructed}")
        client_socket.sendall(resp.construct_utf8())
