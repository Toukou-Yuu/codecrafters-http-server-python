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
        while True:
            self.SERVER_SOCKET = socket.create_server(("localhost", 4221), reuse_port=True)
            self.CLIENT_SOCKET, self.CLIENT_ADDR = self.SERVER_SOCKET.accept()
            threading.Thread(target=self.handle_req).start()

    def close(self) -> None:
        self.SERVER_SOCKET.close()
        self.CLIENT_SOCKET.close()

    def handle_req(self) -> None:
        self.req = Request(self.CLIENT_SOCKET.recv(1024).decode("utf8"))
        if self.req.full_match_endpoint("/"):
            self.handle_root()
        elif self.req.match_endpoint("/echo"):
            # 读取echo_str：/echo/{echo_str}
            self.handle_echo()
        elif self.req.full_match_endpoint("/user-agent"):
            # 读取用户代理
            self.handle_user_agent()
        else:
            self.handle_404()
        # self.close()


    def handle_root(self) -> None:
        print("-----------handle root request-----------")
        resp = Response()
        resp.add_status(HTTP_200)
        resp.add_header(TEXT_PLAIN)
        resp.add_header("Content-Length: 0")
        constructed = resp.construct_utf8()
        print(f"response: {constructed}")
        self.CLIENT_SOCKET.sendall(constructed)

    def handle_echo(self) -> None:
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
        self.CLIENT_SOCKET.sendall(resp.construct_utf8())

    def handle_user_agent(self) -> None:
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
        self.CLIENT_SOCKET.sendall(resp.construct_utf8())

    def handle_404(self) -> None:
        print("-----------handle 404-----------")
        resp = Response()
        resp.add_status(HTTP_404)
        resp.add_header("Content-Length: 0")
        constructed = resp.construct_utf8()
        print(f"response: {constructed}")
        self.CLIENT_SOCKET.sendall(resp.construct_utf8())
