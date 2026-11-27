# Antigravity로 나만의 AI 비서 만들기

고려사이버대학교 소프트웨어학부 세미나 실습 자료

발표 윤지연 · 고려사이버대학교 소프트웨어학부 부회장 · 퓨어프롬프트 AI 개발자

## 자료 받기

- [발표 슬라이드 PDF](https://raw.githubusercontent.com/heznpc/antigravity-assistant-workshop/main/antigravity-assistant-workshop.pdf) · [전체 자료 ZIP](https://github.com/heznpc/antigravity-assistant-workshop/archive/refs/heads/main.zip)
- [앱에서 여는 비서 설정](.agents/agents/workshop-assistant.md) · [SDK 연결](examples/sdk_assistant.py) · [브라우저 예제](examples/web_assistant.py)

## 실습에서 만드는 비서

Antigravity 앱에서 준비된 비서에게 실습 자료 요약이나 체크리스트 작성을 맡겨 봅니다. 로컬 브라우저 예제는 같은 역할 파일의 본문을 읽어 Antigravity SDK에 전달합니다. Python이 브라우저 입력과 README를 SDK에 보내고, 돌려받은 답을 화면에 표시합니다. [커스텀 에이전트](https://antigravity.google/blog/introducing-custom-agents)

### 유사 서비스 소개

발표에서는 여섯 서비스의 공개 화면 캡처로 기능을 소개합니다. 실습은 Antigravity 앱과 SDK로 진행합니다.

| 서비스 | 슬라이드에서 짚는 화면 | 실행 환경 |
| --- | --- | --- |
| [Dots](https://openai.com/index/introducing-dots/) | 왼쪽 ChatGPT 대화에서 일을 맡기고 수정 지시를 보내면, 오른쪽에서 슬라이드 결과를 확인합니다. | Dot 자체 클라우드 컴퓨터를 기본으로 쓰며, 필요할 때 사용자 컴퓨터를 연결할 수 있습니다. [공식 연결 안내](https://learn.chatgpt.com/docs/dots/computers-and-apps) |
| [피클](https://apps.apple.com/kr/app/id6795790129) | ‘둘러보기’의 개인화된 제안을 본 뒤, 예약 채팅에서 ‘브라우저 열기’로 작업 화면을 확인합니다. | 웹 작업은 사용자별 원격 브라우저에서 실행합니다. [공식 실행 환경 설명](https://pickle.com/privacy/isolation) |
| [Meta Muse](https://about.fb.com/ko/news/2026/09/introducing-muse-the-worlds-first-personal-ai-agent-built-for-everyone/amp/) | 대화에서 완성된 PDF를 받고, 구매 시에는 주문 정보와 허용·거부 버튼을 봅니다. [PDF 시연](https://about.fb.com/ko/wp-content/uploads/sites/16/2026/09/Muse_FieldTrip.mp4#t=14.2) · [구매 승인 시연](https://about.fb.com/ko/wp-content/uploads/sites/16/2026/09/Muse_Shopping.mp4#t=17.8) | 연결한 서비스와 Meta가 호스팅하는 실행 환경을 사용합니다. |
| [OpenClaw](https://docs.openclaw.ai/) | 왼쪽 운영 메뉴에서 세션·자동화에 접근하고, 채팅 안에서 명령의 실행 상태와 경과 시간을 봅니다. [공식 저장소의 개발 검증 화면](https://github.com/openclaw/openclaw/blob/6d2cb0379cb66e9fc25584f978b71750e29b916a/.github/pr-proof/working-claw-centering/after-full.png) | 직접 운영하는 게이트웨이로 메신저와 에이전트를 연결합니다. |
| [Grok Bot](https://x.ai/bot) | 예약 가능한 시간 후보를 받아보고, 반복 업무를 정해 둔 일정에 실행하는 루틴을 봅니다. [Grok Bot 앱스토어 화면](https://apps.apple.com/app/id6794501026) | 봇 전용 클라우드 컴퓨터에서 연결한 앱을 사용합니다. [공식 소개](https://x.ai/news/introducing-grok-bot) |
| [Claude Duet](https://claude.com/product/claude-duet) | 먼저 보내는 알림, 주문 승인, 진행 중이거나 대기 중인 작업 목록을 봅니다. [Claude Duet 앱스토어 화면](https://apps.apple.com/us/app/claude-duet-by-anthropic/id6803276000) | 연결한 앱을 사용해 백그라운드에서도 작업합니다. [공식 소개](https://claude.com/resources/articles/claude-duet) |

**사용자가 공개한 일상·업무 사례**

- **아이 일정 · 에밀리의 가족** — 가족이 설정한 OpenClaw가 보육시설 공지에서 행사와 휴원일을 읽어 에밀리의 캘린더에 추가하고 짧은 요약을 보냈습니다. [가족의 사용 기록](https://www.littlemight.com/partner-ai-assistant/#daycare-emails-to-calendar)
- **선물 관리 · 신시아 벨 맥길리스** — Grok Bot에 연말 선물의 배송, 받을 사람, 누적 지출을 기록하도록 맡겼습니다. [사용자 인터뷰](https://www.theatlantic.com/technology/2026/11/ai-agents-holiday-shopping-muse/689587/)
- **영상 수정 · 라일리 브라운** — 휴대폰의 Claude Duet으로 첫 장면과 재생 속도를 바꿔 달라고 요청했습니다. 맥에서 실행 중인 Claude Code가 수정본을 만들었습니다. [직접 시연](https://www.youtube.com/watch?v=zU0jqYKTgMs&t=227s)
- **글감 정리 · 블라드 시필로프** — OpenClaw가 전달받은 기사와 링크를 모아 글감 목록에 추가했습니다. 최종 원고는 본인이 썼습니다. [본인의 사용 기록](https://founderbrain.substack.com/p/how-i-use-openclaw-after-one-month)

## 세미나 실습

### 1. 저장소를 클론하고 앱에서 열기

Git과 Python 3.11 이상을 준비합니다. 학교 계정으로 학생 신분을 확인해 무료로 시작할 수 있다는 점이 이 실습에서 Antigravity를 고른 첫 번째 이유입니다. [Google One 학생 혜택 안내](https://support.google.com/googleone/answer/17422238?hl=ko) · [Antigravity 다운로드](https://antigravity.google/download)

```sh
git clone https://github.com/heznpc/antigravity-assistant-workshop.git
cd antigravity-assistant-workshop
```

Antigravity 앱에서 클론한 폴더를 작업공간으로 열고 에이전트 목록에서 `workshop-assistant`를 선택합니다. “README를 읽고 실습 준비물 3가지를 체크리스트로 만들어 줘”라고 요청해 봅니다. 발표에서는 클론한 [설정 파일](.agents/agents/workshop-assistant.md)을 열어 역할과 도구가 지정된 부분을 살펴봅니다.

### 2. 브라우저에서 실행하기

Python 3.11 이상에서 저장소의 루트 폴더를 열고 실행합니다. Windows에서는 `python3` 대신 `py`를 사용합니다.

```sh
python3 examples/web_assistant.py --demo
```

[실습 준비 비서](http://127.0.0.1:8000)를 열고 **비서에게 요청**을 누릅니다. 예시 모드는 API 키 없이 화면에 안내된 두 요청의 준비된 답을 볼 수 있습니다.

### 3. SDK로 직접 요청 보내기

예시 모드를 실행 중이라면 `Ctrl+C`로 종료합니다. SDK를 설치하고 Gemini API 키를 환경 변수에 설정한 뒤 `--demo` 없이 다시 실행하면 브라우저에서 입력한 요청을 SDK로 보냅니다. SDK 키 발급과 호출 한도는 앱의 학생 혜택과 별도로 확인합니다. [Gemini API 키 안내](https://ai.google.dev/gemini-api/docs/api-key) · [호출 한도](https://ai.google.dev/gemini-api/docs/rate-limits)

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export GEMINI_API_KEY='발급받은-키'
.venv/bin/python examples/web_assistant.py
```

Windows PowerShell에서는 `py -m venv .venv`로 가상환경을 만든 뒤 `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, `$env:GEMINI_API_KEY = '발급받은-키'`, `.\.venv\Scripts\python.exe examples/web_assistant.py`를 순서대로 실행합니다.

### 발표에서 볼 코드

1. [역할 파일](.agents/agents/workshop-assistant.md)의 Markdown 본문이 비서의 역할을 정합니다. YAML의 `tools`는 Antigravity 앱에서 쓰는 도구 설정입니다.
2. [SDK 연결](examples/sdk_assistant.py)이 그 본문을 읽고 `LocalAgentConfig`의 `system_instructions`로 전달합니다.
3. [웹앱](examples/web_assistant.py)이 브라우저 입력에 README를 붙여 `assistant.chat(request)`를 호출하고 화면에 답을 표시합니다. 브라우저 요청은 각각 새 세션에서 실행됩니다.

## 선택 예제 — 캘린더에 일정 저장

```sh
python3 -m examples.calendar.web_assistant --demo
```

[캘린더](http://127.0.0.1:8001)를 열고 기본 요청 “다음 주 수요일 저녁 7시에 스터디 한 시간 넣어 줘”를 보냅니다. 요청에서 얻은 제목, 날짜, 시각, 소요 시간을 로컬 SQLite에 저장하고 주간 화면에 표시합니다. 예시 모드에서는 기본 문장과 같은 순서로 요청을 작성합니다.

SDK로 일정을 해석하려면 위에서 설정한 가상환경과 API 키로 `.venv/bin/python -m examples.calendar.web_assistant`를 실행합니다. Windows PowerShell에서는 `.\.venv\Scripts\python.exe -m examples.calendar.web_assistant`를 실행합니다. 예시 모드와 SDK 모드의 일정은 각각 `.workshop/demo.sqlite3`, `.workshop/calendar.sqlite3`에 저장됩니다. [일정 해석 코드](examples/calendar/calendar_assistant.py) · [아이콘 라이선스](https://github.com/lucide-icons/lucide/blob/main/LICENSE)

## 슬라이드 화면 출처

- 학생 혜택 [Google One 공식 신청 안내](https://support.google.com/googleone/answer/17422238?hl=ko)
- 설치 [Google Antigravity 공식 다운로드](https://antigravity.google/download)
- 앱 [Antigravity 시작하기](https://antigravity.google/docs/getting-started)
- 에이전트 선택 [Google 공식 소개 영상](https://antigravity.google/blog/introducing-custom-agents)
- SDK 코드 [Antigravity SDK 빠른 시작](https://antigravity.google/docs/sdk/overview)
