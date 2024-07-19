import socket
from socket import socket as type_socket
import threading
import sys
import gzip
from app.server.Request import Request
from app.server.Response import Response
from app.Constants import *
class Aincrad_Server:
    def link_start(self) -> None:
        self.SERVER_SOCKET = socket.create_server(("localhost", 4221), reuse_port=True)
        while True:
            print("listening port: 4221")
            client_socket, client_addr = self.SERVER_SOCKET.accept()
            print("accept request, creating threading to handle it......")
            threading.Thread(target=self._handle_req, args=(client_socket, client_addr)).start()

    def _handle_req(self, client_socket: type_socket, client_addr: type_socket) -> None:
        self.req = Request(client_socket.recv(1024).decode(UTF8))
        print(f"handling request: {self.req.read_req_target()}")
        if self.req.full_match_endpoint("/"):
            resp = self._handle_root()
        elif self.req.match_endpoint("/echo"):
            # 读取echo_str：/echo/{echo_str}
            resp = self._handle_echo()
        elif self.req.full_match_endpoint("/user-agent"):
            # 读取用户代理
            resp = self._handle_user_agent()
        elif self.req.match_endpoint("/files"):
            resp = self._handle_file()
        else:
            resp = self._handle_404()
        client_socket.sendall(resp)

    def _handle_root(self) -> bytes:
        print("-----------handle root request-----------")
        resp = Response()
        resp.add_status_line(HTTP_OK)
        resp.add_header(CONTENT_TEXT_PLAIN)
        resp.add_header(CONTENT_LENGTH_ZERO)
        constructed = resp.construct_utf8()
        print(f"response: {constructed}")
        return constructed

    def _handle_echo(self) -> bytes:
        # 读取echo字符串：/echo/{echo_str}
        print("-----------handle echo request-----------")
        resp = Response()
        encodings = self.req.read_header(ACCEPT_ENCODING)
        req_target = self.req.read_req_target()
        body = req_target[len("/echo/"):]
        if "gzip" in encodings:
            print("client accept gzip")
            resp.add_header(CONTENT_GZIP)
            body = gzip.compress(body.encode(UTF8))
        resp.add_status_line(HTTP_OK)
        resp.add_body(body)
        resp.add_header(CONTENT_TEXT_PLAIN)
        resp.add_header(f"{CONTENT_LENGTH}: {len(body)}")
        constructed = resp.construct_utf8()
        print(f"response: {constructed}")
        return constructed

    def _handle_user_agent(self) -> bytes:
        # 读取用户代理
        print("-----------handle user-agent-----------")
        resp = Response()
        body = self.req.read_header(USER_AGENT)
        resp.add_status_line(HTTP_OK)
        resp.add_body(body)
        resp.add_header(CONTENT_TEXT_PLAIN)
        resp.add_header(f"{CONTENT_LENGTH}: {len(body)}") 
        constructed = resp.construct_utf8()
        print(f"response: {constructed}")
        return constructed

    def _handle_file(self) -> bytes:
        # ./your_program.sh --directory /tmp/
        # path = /files/{filename}
        directory = sys.argv[2]
        filename = self.req.read_req_target()[7:]
        print(f"dir: {directory}\nfilename: {filename}")
        resp = Response()

        try:
            if self.req._method == POST:
                body = self.req.read_body()
                with open(f"/{directory}/{filename}", "w") as file:
                    file.write(body)
                resp.add_status_line(HTTP_CREATED)
            elif self.req._method == GET:
                with open(f"/{directory}/{filename}", "r") as file:
                    body = file.read()
                resp.add_status_line(HTTP_OK)
                resp.add_header(CONTENT_FILE)
                resp.add_header(f"{CONTENT_LENGTH}: {len(body)}")
                resp.add_body(body)
        except Exception as e:
            resp.add_status_line(HTTP_NOT_FOUND)
        return resp.construct_utf8()

    def _handle_404(self) -> bytes:
        print("-----------handle 404-----------")
        resp = Response()
        resp.add_status_line(HTTP_NOT_FOUND)
        resp.add_header(CONTENT_LENGTH_ZERO)
        constructed = resp.construct_utf8()
        print(f"response: {constructed}")
        return constructed
