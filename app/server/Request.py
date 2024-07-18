
class Request:
    # request = request-line + [headers] + [request-body]
    def __init__(self, request: str) -> None:
        self.request = request
        self.req_line = self.request.split("\r\n")[0]
        self.method, self.path, self.http_version = self.req_line.split(" ")
        self.headers = self.read_headers()
        self.body = self.request.split("\r\n")[-1]

    # RFC9112标准: request-line = method SP request-target SP HTTP-version
    def read_req_line(self) -> str:
        return self.req_line
    
    def read_req_target(self) -> str:
        return self.path

    def read_header(self, target: str) -> str:
        for header in self.headers:
            if header.startswith(target):
                return header.split(target)[1].strip()
        return ""

    def read_headers(self) -> list[str]:
        # 如果一个请求有请求头，那这个请求一定包含两个CRLF
        end = self.request.find("\r\n\r\n")
        headers = self.request[:end].split("\r\n")
        # headers[0]是request-line
        return headers[1:]
    
    def read_body(self) -> str:
        return self.body

    def read_user_agent(self) -> str:
        for header in self.read_headers():
            if header.startswith("User-Agent:"):
                return header.split(":")[1].strip()
        return ""
    
    def full_match_endpoint(self, target: str) -> bool:
        return self.path.__eq__(target)

    def match_endpoint(self, target: str) -> bool:
        return self.path.startswith(target)

