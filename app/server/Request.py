from app.Constants import CRLF, EMPTY_STR, SP
class Request:
    # request = request-line + [headers] + [request-body]
    def __init__(self, request: str) -> None:
        self._request = request
        lines = self._request.split(CRLF)
        self._req_line = lines[0]
        self._body = lines[-1]
        # RFC9112: request-line = method SP request-target SP HTTP-version
        self._method, self._path, self._http_version = self._req_line.split(SP)
        self._headers = self.read_headers()
    def read_req_line(self) -> str:
        return self._req_line
    
    def read_method(self) -> str:
        return self._method

    def read_req_target(self) -> str:
        return self._path
    
    def read_http_version(self) -> str:
        return self._http_version

    def read_header(self, target: str) -> str:
        for header in self._headers:
            if header.startswith(target):
                # key: value
                return header.split(":")[1].strip()
        return EMPTY_STR

    def read_headers(self) -> list[str]:
        # 如果一个请求有请求头，那这个请求一定包含两个CRLF
        end = self._request.find(f"{CRLF}{CRLF}")
        headers = self._request[:end].split(CRLF)
        # headers[0]是request-line
        return headers[1:]
    
    def read_body(self) -> str:
        return self._body
    
    def full_match_endpoint(self, target: str) -> bool:
        return target == self.read_req_target()

    def match_endpoint(self, target: str) -> bool:
        return self.read_req_target().startswith(target)

