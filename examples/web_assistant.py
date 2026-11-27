"""로컬 브라우저에서 README에 관한 요청을 실습 비서에게 보낸다."""

import asyncio
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from string import Template
from urllib.parse import parse_qs

from sdk_assistant import create_assistant

HOST = "127.0.0.1"
PORT = 8000
ORIGIN = f"http://{HOST}:{PORT}"
DEFAULT_PROMPT = "README를 읽고 실습 준비물 3가지를 체크리스트로 만들어 줘."
README = Path(__file__).resolve().parents[1] / "README.md"
PAGE = Path(__file__).with_name("web_assistant.html")


async def ask(prompt: str) -> str:
    readme = README.read_text(encoding="utf-8")
    request = (
        f"아래 자료를 참고해 사용자의 요청에 한국어로 답해 주세요.\n\n"
        f"요청\n{prompt}\n\n자료\n{readme}"
    )
    async with create_assistant() as assistant:
        response = await assistant.chat(request)
        return await response.text()


class WorkshopHandler(BaseHTTPRequestHandler):
    def render(self, prompt=DEFAULT_PROMPT, result="", error="", status=HTTPStatus.OK):
        page = Template(PAGE.read_text(encoding="utf-8")).substitute(
            result_hidden="" if result else "hidden",
            error_hidden="" if error else "hidden",
            prompt=escape(prompt),
            result=escape(result),
            error=escape(error),
        )
        body = page.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/" or self.headers.get("Host") != f"{HOST}:{PORT}":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self.render()

    def do_POST(self):
        if self.path != "/":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if self.headers.get("Host") != f"{HOST}:{PORT}" or self.headers.get("Origin") != ORIGIN:
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        if self.headers.get_content_type() != "application/x-www-form-urlencoded":
            self.send_error(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 8192:
                raise ValueError
            fields = parse_qs(self.rfile.read(size).decode("utf-8"), max_num_fields=1)
            prompt = fields.get("prompt", [""])[0].strip()
            if not 0 < len(prompt) <= 500:
                raise ValueError
        except (UnicodeError, ValueError):
            self.render(error="요청을 1자 이상, 500자 이하로 입력해 주세요.", status=HTTPStatus.BAD_REQUEST)
            return

        try:
            result = asyncio.run(ask(prompt))
        except Exception as error:
            self.log_error("비서 호출 실패 (%s)", type(error).__name__)
            self.render(
                prompt,
                error="비서 호출에 실패했습니다. SDK 설치와 Gemini API 키를 확인해 주세요.",
                status=HTTPStatus.BAD_GATEWAY,
            )
            return
        self.render(prompt, result=result)


if __name__ == "__main__":
    with ThreadingHTTPServer((HOST, PORT), WorkshopHandler) as server:
        print(f"브라우저에서 {ORIGIN}을 여세요.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
