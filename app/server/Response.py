from app.Constants import CRLF, EMPTY_STR
class Response:
    def __init__(self) -> None:
        self._status_line: str = ""
        self._header_list: list = []
        self._header_str: str = ""
        self._body: str | bytes

    # RFC9112: status-line = HTTP-version SP status-code SP [ reason-phrase ]
    def add_status_line(self, status_line: str) -> None:
        self._status_line = status_line
    
    def add_header(self, header: str) -> None:
        if header != EMPTY_STR:
            self._header_str += f"{header}{CRLF}"
            self._header_list.append(f"{header}{CRLF}")

    def add_headers(self, headers: list[str]) -> None:
        for header in headers:
            if header != EMPTY_STR:
                self._header_str += f"{header}{CRLF}"
                self._header_list.append(f"{header}{CRLF}")

    def add_body(self, body: str | bytes) -> None:
        self._body = body

    def construct_utf8(self) -> bytes:
        if isinstance(self._body, str):
            self._body = self._body.encode()
        response = f"{self._status_line}{CRLF}{self._header_str}{CRLF}".encode() + self._body
        return response