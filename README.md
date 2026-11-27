# Antigravity로 내 일정을 챙기는 AI 비서 만들기

고려사이버대학교 소프트웨어학부 세미나 실습 자료

발표 윤지연 · 고려사이버대학교 소프트웨어학부 부회장 · 퓨어프롬프트 AI 개발자

## 자료 받기

- [발표 슬라이드 PDF](https://raw.githubusercontent.com/heznpc/antigravity-assistant-workshop/main/antigravity-assistant-workshop.pdf) · [전체 자료 ZIP](https://github.com/heznpc/antigravity-assistant-workshop/archive/refs/heads/main.zip)
- [앱에서 여는 비서 설정](.agents/agents/workshop-assistant.md) · [SDK 일정 해석](examples/calendar_assistant.py) · [캘린더 웹앱](examples/web_assistant.py)

## 실습에서 만드는 비서

브라우저에서 “다음 주 수요일 저녁 7시에 스터디 한 시간 넣어 줘”라고 요청하면 일정이 주간 캘린더에 저장됩니다. Antigravity 앱에서는 커스텀 에이전트의 역할을 확인합니다. 브라우저에서 보낸 요청은 Python 웹앱이 같은 역할 지시와 함께 SDK에 전달합니다. SDK가 해석한 제목, 시작 시각, 소요 시간을 웹앱에서 확인하고 저장합니다. [커스텀 에이전트](https://antigravity.google/blog/introducing-custom-agents) · [SDK 구조화 응답](https://antigravity.google/docs/sdk/structured-output/)

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

Antigravity 앱에서 클론한 폴더를 작업공간으로 열고 에이전트 목록에서 `workshop-assistant`를 선택합니다. [역할 파일](.agents/agents/workshop-assistant.md)에서 앱과 SDK가 읽는 역할 지시를 확인합니다.

### 2. 브라우저에서 일정 맡기기

예시 모드는 Python만 있으면 됩니다. 터미널에서 실행한 뒤 [내 캘린더](http://127.0.0.1:8000)를 열고 **비서에게 요청**을 누릅니다.

```sh
python3 examples/web_assistant.py --demo
```

Windows에서는 `py examples/web_assistant.py --demo`를 실행합니다. 기본 요청을 보내면 다음 주 수요일 19:00–20:00에 스터디가 추가됩니다. 두 번째로 “다음 주 금요일 오후 3시에 과제 회의 30분 넣어 줘.”를 보내고 같은 캘린더에 저장되는지 확인합니다. 예시 모드에서는 날짜, 시작 시간, 제목, 소요 시간을 예시 순서대로 입력합니다.

### 3. SDK로 일정 해석하기

터미널에서 `Ctrl+C`를 눌러 예시 모드를 종료합니다. SDK를 설치하고 발급받은 Gemini API 키를 환경 변수에 설정한 뒤 다시 실행합니다. SDK 키 발급과 호출 한도는 앱의 학생 혜택과 별도로 확인합니다. [Gemini API 키 안내](https://ai.google.dev/gemini-api/docs/api-key) · [호출 한도](https://ai.google.dev/gemini-api/docs/rate-limits)

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export GEMINI_API_KEY='발급받은-키'
.venv/bin/python examples/web_assistant.py
```

Windows PowerShell에서는 `py -m venv .venv`로 가상환경을 만든 뒤 `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, `$env:GEMINI_API_KEY = '발급받은-키'`, `.\.venv\Scripts\python.exe examples/web_assistant.py`를 순서대로 실행합니다.

### 발표에서 볼 코드

1. [역할 파일](.agents/agents/workshop-assistant.md)에 어떤 정보를 일정으로 해석할지 적습니다.
2. [일정 해석 코드](examples/calendar_assistant.py)에서 SDK가 구조화한 제목, 날짜, 시각, 소요 시간을 검증합니다.
3. [웹앱](examples/web_assistant.py)이 일정을 로컬 SQLite에 저장하고 해당 주를 화면에 엽니다.

예시 모드와 SDK 모드의 일정은 각각 `.workshop/demo.sqlite3`, `.workshop/calendar.sqlite3`에 저장됩니다. 캘린더 시간대는 한국 표준시이며 슬라이드 캡처는 예시 모드입니다. [Lucide 아이콘과 라이선스](https://github.com/lucide-icons/lucide/blob/main/LICENSE)

## 슬라이드 화면 출처

- 학생 혜택 [Google One 공식 신청 안내](https://support.google.com/googleone/answer/17422238?hl=ko)
- 설치 [Google Antigravity 공식 다운로드](https://antigravity.google/download)
- 앱 [Antigravity 시작하기](https://antigravity.google/docs/getting-started)
- 에이전트 선택 [Google 공식 소개 영상](https://antigravity.google/blog/introducing-custom-agents)
- SDK 코드 [Antigravity SDK 빠른 시작](https://antigravity.google/docs/sdk/overview)
