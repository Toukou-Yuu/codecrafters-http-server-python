
class Response:
    def __init__(self) -> None:
        self.status_line: str = ""
        self.header_list: list = []
        self.header_str: str = ""
        self.body: str|bytes = ""

    # RFC9112标准: status-line = HTTP-version SP status-code SP [ reason-phrase ]
    def add_status(self, status: str) -> None:
        self.status_line = status
    
    def add_header(self, header: str) -> None:
        if header != "":
            self.header_str += (header + "\r\n")
            self.header_list.append(header + "\r\n")

    def add_headers(self, headers: list[str]) -> None:
        for header in headers:
            if header != "":
                self.header_str += (header + "\r\n")
                self.header_list.append(header + "\r\n")

    def add_body(self, body: str | bytes) -> None:
        self.body = body
            

    def get_header(self, target: str) -> str:
        for header in self.header_list:
            if header.__eq__(target):
                return header
        return ""

    def get_headers(self) -> list[str]:
        return self.header_list

    def construct_utf8(self) -> bytes:
        if isinstance(self.body, str):
            body_str = f"{self.status_line}\r\n{self.header_str}\r\n{self.body}"
            return body_str.encode("utf8")
        body_bytes = f"{self.status_line}\r\n{self.header_str}\r\n".encode() + self.body
        return body_bytes