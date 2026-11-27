# Antigravity로 나만의 AI 비서 만들기

고려사이버대학교 소프트웨어학부 세미나 실습 자료

발표 윤지연 · 고려사이버대학교 소프트웨어학부 부회장 · 퓨어프롬프트 AI 개발자

## 자료 받기

- [발표 슬라이드 PDF 다운로드](https://raw.githubusercontent.com/heznpc/antigravity-assistant-workshop/main/antigravity-assistant-workshop.pdf) — 공개 배포용 16장
- [전체 자료 ZIP 다운로드](https://github.com/heznpc/antigravity-assistant-workshop/archive/refs/heads/main.zip) — 슬라이드, 커스텀 에이전트, SDK 예제
- [커스텀 에이전트 설정](.agents/agents/workshop-assistant.md) · [SDK 예제](examples/sdk_assistant.py)

## 실습에서 만드는 비서

역할과 작업 규칙을 한 번 정해 두고, 같은 비서에게 그때그때 새 일을 맡깁니다. Antigravity 앱에서 작업 폴더와 에이전트를 열어 파일을 다루는 모습을 확인합니다. SDK에서는 같은 역할 지시를 읽어 Python 프로그램에서 비서를 호출합니다. 앱의 실행 권한과 대화 이력은 별도로 관리되며, SDK에서 세션을 이어 쓰려면 저장과 복원을 구성합니다. [커스텀 에이전트](https://antigravity.google/blog/introducing-custom-agents) · [SDK 빠른 시작](https://antigravity.google/docs/sdk/overview)

### 유사 서비스 화면 둘러보기

| 서비스 | 발표에서 보는 실제 화면 | 실행 환경 |
| --- | --- | --- |
| [Dots](https://openai.com/index/introducing-dots/) | 왼쪽 ChatGPT 대화에서 일을 맡기고 수정 지시를 보내면, 오른쪽에서 슬라이드 결과를 확인합니다. | Dot 자체 클라우드 컴퓨터를 기본으로 쓰며, 필요할 때 사용자 컴퓨터를 연결할 수 있습니다. [공식 연결 안내](https://learn.chatgpt.com/docs/dots/computers-and-apps) |
| [피클](https://apps.apple.com/kr/app/id6795790129) | ‘둘러보기’의 개인화된 제안을 본 뒤, 예약 채팅에서 ‘브라우저 열기’로 작업 화면을 확인합니다. | 웹 작업은 사용자별 원격 브라우저에서 실행합니다. [공식 실행 환경 설명](https://pickle.com/privacy/isolation) |
| [Meta Muse](https://about.fb.com/ko/news/2026/09/introducing-muse-the-worlds-first-personal-ai-agent-built-for-everyone/amp/) | 대화에서 완성된 PDF를 받고, 구매 시에는 주문 정보와 허용·거부 버튼을 봅니다. [PDF 시연](https://about.fb.com/ko/wp-content/uploads/sites/16/2026/09/Muse_FieldTrip.mp4#t=14.2) · [구매 승인 시연](https://about.fb.com/ko/wp-content/uploads/sites/16/2026/09/Muse_Shopping.mp4#t=17.8) | 연결한 서비스와 Meta가 호스팅하는 실행 환경을 사용합니다. |
| [OpenClaw](https://docs.openclaw.ai/) | 왼쪽 운영 메뉴에서 세션·자동화에 접근하고, 채팅 안에서 명령의 실행 상태와 경과 시간을 봅니다. [공식 저장소의 개발 검증 화면](https://github.com/openclaw/openclaw/blob/6d2cb0379cb66e9fc25584f978b71750e29b916a/.github/pr-proof/working-claw-centering/after-full.png) | 직접 운영하는 게이트웨이로 메신저와 에이전트를 연결합니다. |

[Antigravity 앱](https://antigravity.google/docs/getting-started)에서는 작업 폴더에 커스텀 에이전트를 띄우고, [SDK](https://antigravity.google/docs/sdk/overview)에서는 같은 역할 지시를 Python에서 읽고 실행합니다.

## 따라 하기

1. [Google 학생 혜택 신청 페이지](https://one.google.com/ai-student)에서 개인 Google 계정으로 로그인합니다. Google AI Plus 학생 혜택을 선택하고 SheerID로 학생 신분을 확인합니다. 신청 화면에 표시되는 기간과 이후 가격을 확인합니다. [Google One 공식 신청 안내](https://support.google.com/googleone/answer/17422238?hl=ko)
2. [Antigravity 다운로드](https://antigravity.google/download)에서 운영체제에 맞는 **Antigravity App**을 설치합니다. 같은 Google 계정으로 로그인한 뒤 내려받은 자료 폴더를 작업공간으로 엽니다.
3. 앱의 에이전트 목록에서 `workshop-assistant`를 선택합니다. [커스텀 에이전트 설정 파일](.agents/agents/workshop-assistant.md)의 Markdown 본문이 역할 지시이고, YAML의 `tools`가 이 예제에서 지정한 도구입니다.
4. SDK 실습은 Python 가상환경에서 시작합니다. [Gemini API 키 발급 안내](https://ai.google.dev/gemini-api/docs/api-key)와 [Gemini API 제한](https://ai.google.dev/gemini-api/docs/rate-limits)은 앱 구독과 별도로 확인합니다.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install google-antigravity
export GEMINI_API_KEY='발급받은-키'
python examples/sdk_assistant.py "README를 읽고 실습 준비물 세 가지를 뽑아 줘."
```

Windows PowerShell에서는 `python -m venv .venv` 다음에 `.\.venv\Scripts\Activate.ps1`로 가상환경을 활성화하고, `$env:GEMINI_API_KEY = '발급받은-키'`로 설정합니다. 키는 로컬 환경 변수에만 둡니다.

같은 실행에서 이어서 요청하려면 명령 끝에 새 요청을 따옴표로 하나 더 붙입니다. 예를 들어 첫 요청으로 준비물을 뽑고, 두 번째 요청으로 실습이 끝난 뒤 확인할 체크리스트를 받을 수 있습니다.

## 슬라이드 화면 출처

- 학생 혜택 [Google One 공식 신청 안내](https://support.google.com/googleone/answer/17422238?hl=ko)
- 설치 [Google Antigravity 공식 다운로드](https://antigravity.google/download)
- 앱 [Antigravity 시작하기](https://antigravity.google/docs/getting-started)
- 에이전트 선택 [Google 공식 소개 영상](https://antigravity.google/blog/introducing-custom-agents)
- SDK 코드 [Antigravity SDK 빠른 시작](https://antigravity.google/docs/sdk/overview)
