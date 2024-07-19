# RFC9112标准: status-line = HTTP-version SP status-code SP [ reason-phrase ]
# status
HTTP_OK: str = "HTTP/1.1 200 OK"
HTTP_NOT_FOUND: str = "HTTP/1.1 404 Not Found"
HTTP_CREATED: str = "HTTP/1.1 201 Created"
# methods
GET: str = "GET"
POST: str = "POST"
# headers
USER_AGENT: str = "User-Agent"
CONTENT_TYPE: str = "Content-Type"
CONTENT_LENGTH: str = "Content-Length"
CONTENT_ENCODING: str = "Content-Encoding"
ACCEPT_ENCODING: str = "Accept-Encoding"
# headers with value
CONTENT_TEXT_PLAIN: str = "Content-Type: text/plain"
CONTENT_FILE: str = "Content-Type: application/octet-stream"
CONTENT_GZIP: str = "Content-Encoding: gzip"
CONTENT_LENGTH_ZERO: str = "Content-Length: 0"
# others
EMPTY_STR: str = ""
UTF8: str = "utf-8"
RECV_BUFFER: int = 1024
VALID_ENDPOINT: list[str] = ["/", "/echo", "/user-agent", "/files"]
# split
CRLF: str = "\r\n"
SP: str = " "

__all__ = [
    # status
    "HTTP_OK", "HTTP_NOT_FOUND", "HTTP_CREATED",
    # methods
    "GET", "POST",
    # headers
    "USER_AGENT", "CONTENT_TYPE", "CONTENT_LENGTH", "CONTENT_ENCODING", "ACCEPT_ENCODING",
    # headers with value
    "CONTENT_TEXT_PLAIN", "CONTENT_FILE", "CONTENT_GZIP", "CONTENT_LENGTH_ZERO",
    # others
    "EMPTY_STR", "UTF8", "RECV_BUFFER", "VALID_ENDPOINT",
    # split
    "CRLF", "SP"
]