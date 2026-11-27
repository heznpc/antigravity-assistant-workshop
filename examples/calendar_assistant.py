"""자연어 일정 요청을 캘린더에 저장할 한 건의 일정으로 해석합니다."""

import asyncio
import re
from dataclasses import dataclass
from datetime import date, timedelta

from sdk_assistant import create_assistant

DEFAULT_PROMPT = "다음 주 수요일 저녁 7시에 스터디 한 시간 넣어 줘."
WEEKDAYS = "월화수목금토일"
EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "date": {"type": "string"},
        "time": {"type": "string"},
        "duration_minutes": {"type": "integer"},
        "question": {"type": "string"},
    },
    "required": ["title", "date", "time", "duration_minutes", "question"],
}


@dataclass(frozen=True)
class Event:
    title: str
    date: date
    time: str
    duration_minutes: int

    @property
    def start_minutes(self) -> int:
        hour, minute = map(int, self.time.split(":"))
        return hour * 60 + minute

    @property
    def time_range(self) -> str:
        hour, minute = divmod(self.start_minutes + self.duration_minutes, 60)
        return f"{self.time}–{hour:02d}:{minute:02d}"


def monday(day: date) -> date:
    return day - timedelta(days=day.weekday())


def validate_event(payload: object) -> Event:
    if not isinstance(payload, dict):
        raise ValueError("받은 일정 정보를 읽을 수 없습니다.")
    question = payload.get("question")
    if isinstance(question, str) and question.strip():
        raise ValueError(question.strip()[:240])
    title = payload.get("title")
    time = payload.get("time")
    duration = payload.get("duration_minutes")
    try:
        day = date.fromisoformat(payload.get("date", ""))
    except (TypeError, ValueError) as error:
        raise ValueError("일정의 날짜를 확인해 주세요.") from error
    if not isinstance(title, str) or not 0 < len(title.strip()) <= 80:
        raise ValueError("일정 제목을 1자 이상 80자 이하로 알려 주세요.")
    if not isinstance(time, str) or not re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", time):
        raise ValueError("일정의 시작 시각을 확인해 주세요.")
    if type(duration) is not int or not 1 <= duration <= 1440:
        raise ValueError("일정의 소요 시간을 알려 주세요.")
    event = Event(title.strip(), day, time, duration)
    if event.start_minutes + event.duration_minutes > 1440:
        raise ValueError("자정을 넘는 일정은 날짜별로 나눠 주세요.")
    if not date(1900, 1, 1) <= day <= date(2099, 12, 31):
        raise ValueError("1900년부터 2099년 사이의 날짜를 입력해 주세요.")
    return event


def demo_event(prompt: str, today: date) -> Event:
    match = re.fullmatch(
        r"(이번|다음)\s*주\s*([월화수목금토일])요일\s*"
        r"(?:(오전|오후|저녁)\s*)?(\d{1,2})시\s*(?:(\d{1,2})분\s*)?에\s*"
        r"(.+?)\s+(한\s*시간|\d{1,3}\s*(?:시간|분))\s+(?:넣어|추가해)\s*줘[.!]?",
        prompt,
    )
    if not match:
        raise ValueError("날짜, 시작 시간, 제목, 소요 시간을 기본 예시와 같은 순서로 적어 주세요.")
    week, weekday, period, hour_text, minute_text, title, length = match.groups()
    hour = int(hour_text)
    if period:
        if not 1 <= hour <= 12:
            raise ValueError("오전 또는 오후 시각을 1시부터 12시 사이로 알려 주세요.")
        hour = hour % 12 + 12 * (period in {"오후", "저녁"})
    day = monday(today) + timedelta(days=7 * (week == "다음") + WEEKDAYS.index(weekday))
    amount = 1 if length.startswith("한") else int(length.split()[0].rstrip("시간분"))
    return validate_event({
        "title": title,
        "date": day.isoformat(),
        "time": f"{hour:02d}:{int(minute_text or 0):02d}",
        "duration_minutes": amount * (60 if length.endswith("시간") else 1),
    })


async def interpret(prompt: str, today: date) -> Event:
    request = (
        f"오늘은 한국 시간 {today.isoformat()} {WEEKDAYS[today.weekday()]}요일입니다.\n"
        "캘린더에 추가하라는 요청에서 일정 한 건을 해석하세요. date는 YYYY-MM-DD, "
        "time은 24시간제 HH:MM, duration_minutes는 정수 분으로 답하세요. "
        "제목은 요청에 적힌 이름만 사용하세요. 저장 가능한 요청이면 question은 빈 문자열입니다. "
        "정보가 부족하거나 일정을 추가하라는 요청이 아니면 question에 안내를 적고 "
        "나머지는 빈 문자열과 0으로 두세요.\n\n"
        f"사용자 요청\n{prompt}"
    )
    async with asyncio.timeout(35):
        async with create_assistant(EVENT_SCHEMA) as assistant:
            response = await assistant.chat(request)
            payload = await response.structured_output()
    return validate_event(payload)
