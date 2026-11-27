"""로컬 브라우저에서 일정 요청을 받아 주간 캘린더에 저장합니다."""

import argparse
import asyncio
import os
import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta, timezone
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from string import Template
from urllib.parse import parse_qs, urlsplit

from .calendar_assistant import DEFAULT_PROMPT, WEEKDAYS, Event, demo_event, interpret, monday

HOST = "127.0.0.1"
PORT = 8001
ORIGIN = f"http://{HOST}:{PORT}"
KST = timezone(timedelta(hours=9))
PAGE = Path(__file__).with_name("web_assistant.html")
DATA_DIR = Path(__file__).resolve().parents[2] / ".workshop"


def today_in_korea() -> date:
    return datetime.now(KST).date()


def open_calendar(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            UNIQUE (title, day, start_time, duration)
        )
    """)
    return db


def save_event(path: Path, event: Event) -> int:
    record = (event.title, event.date.isoformat(), event.time, event.duration_minutes)
    with closing(open_calendar(path)) as db, db:
        db.execute("INSERT OR IGNORE INTO events (title, day, start_time, duration) VALUES (?, ?, ?, ?)", record)
        return db.execute(
            "SELECT id FROM events WHERE title = ? AND day = ? AND start_time = ? AND duration = ?",
            record,
        ).fetchone()[0]


def read_week(path: Path, week: date) -> list[tuple[int, Event]]:
    with closing(open_calendar(path)) as db:
        rows = db.execute(
            "SELECT id, title, day, start_time, duration FROM events "
            "WHERE day BETWEEN ? AND ? ORDER BY start_time, id",
            (week.isoformat(), (week + timedelta(days=6)).isoformat()),
        ).fetchall()
    return [(row[0], Event(row[1], date.fromisoformat(row[2]), row[3], row[4])) for row in rows]


def render_week(week: date, events: list[tuple[int, Event]], today: date, saved_id: int) -> str:
    columns = []
    for offset, weekday in enumerate(WEEKDAYS):
        day = week + timedelta(days=offset)
        cards = []
        for event_id, event in events:
            if event.date == day:
                selected = " new" if event_id == saved_id else ""
                cards.append(
                    f'<li class="event{selected}"><time>{event.time_range}</time>'
                    f'<strong>{escape(event.title)}</strong></li>'
                )
        current = ' class="today"' if day == today else ""
        columns.append(
            f'<section{current}><h3><span>{weekday}요일</span> '
            f'<time datetime="{day.isoformat()}">{day.day:02d}</time></h3>'
            f'<ul>{"".join(cards)}</ul></section>'
        )
    return "".join(columns)


class CalendarServer(ThreadingHTTPServer):
    def __init__(self, demo: bool):
        self.demo = demo
        DATA_DIR.mkdir(exist_ok=True)
        self.db_path = DATA_DIR / ("demo.sqlite3" if demo else "calendar.sqlite3")
        super().__init__((HOST, PORT), CalendarHandler)


class CalendarHandler(BaseHTTPRequestHandler):
    server: CalendarServer

    def week_from_query(self) -> date:
        try:
            value = parse_qs(urlsplit(self.path).query).get("week", [""])[0]
            day = date.fromisoformat(value)
            if date(1900, 1, 1) <= day <= date(2099, 12, 31):
                return monday(day)
        except ValueError:
            pass
        return monday(today_in_korea())

    def render(self, prompt=DEFAULT_PROMPT, error="", status=HTTPStatus.OK):
        week = self.week_from_query()
        raw_id = parse_qs(urlsplit(self.path).query).get("saved", [""])[0]
        saved_id = int(raw_id) if raw_id.isascii() and raw_id.isdigit() and len(raw_id) <= 18 else 0
        events = read_week(self.server.db_path, week)
        saved = next((event for event_id, event in events if event_id == saved_id), None)
        success = f"{saved.date.month}월 {saved.date.day}일 {saved.time_range} · {saved.title} 저장됨" if saved else ""
        end = week + timedelta(days=6)
        page = Template(PAGE.read_text(encoding="utf-8")).substitute(
            mode="예시 모드" if self.server.demo else "SDK 모드",
            week=week.isoformat(),
            week_label=f"{week.year}년 {week.month}월 {week.day}일 – {end.month}월 {end.day}일",
            previous=(week - timedelta(days=7)).isoformat(),
            following=(week + timedelta(days=7)).isoformat(),
            columns=render_week(week, events, today_in_korea(), saved_id),
            prompt=escape(prompt),
            error=escape(error),
            error_hidden="" if error else "hidden",
            success=escape(success),
            success_hidden="" if success else "hidden",
        )
        body = page.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlsplit(self.path).path != "/" or self.headers.get("Host") != f"{HOST}:{PORT}":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self.render()

    def do_POST(self):
        if urlsplit(self.path).path != "/":
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
        except ValueError:
            self.render(error="요청을 1자 이상, 500자 이하로 입력해 주세요.", status=HTTPStatus.BAD_REQUEST)
            return

        try:
            today = today_in_korea()
            event = demo_event(prompt, today) if self.server.demo else asyncio.run(interpret(prompt, today))
            event_id = save_event(self.server.db_path, event)
        except ValueError as error:
            self.render(prompt, error=str(error), status=HTTPStatus.UNPROCESSABLE_ENTITY)
            return
        except Exception as error:
            self.log_error("일정 요청 실패 (%s)", type(error).__name__)
            self.render(
                prompt,
                error="일정 처리에 실패했습니다. API 키를 확인하거나 예시 모드로 다시 실행해 주세요.",
                status=HTTPStatus.BAD_GATEWAY,
            )
            return

        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", f"/?week={monday(event.date).isoformat()}&saved={event_id}")
        self.send_header("Content-Length", "0")
        self.end_headers()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="API 키 없이 예시 모드로 실행")
    args = parser.parse_args()
    if not args.demo and not os.environ.get("GEMINI_API_KEY"):
        parser.exit(2, "GEMINI_API_KEY를 설정하거나 --demo로 실행해 주세요.\n")
    with CalendarServer(args.demo) as server:
        print(f"브라우저에서 {ORIGIN}을 여세요.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
