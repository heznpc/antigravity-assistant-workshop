"""커스텀 에이전트의 역할 지시를 SDK로 읽어 요청을 실행한다."""

import argparse
import asyncio
from pathlib import Path

ROLE_FILE = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "agents"
    / "workshop-assistant.md"
)


def create_assistant():
    from google.antigravity import Agent, LocalAgentConfig

    role_file = ROLE_FILE.read_text(encoding="utf-8")
    instructions = role_file.split("---", maxsplit=2)[2].strip()
    return Agent(LocalAgentConfig(system_instructions=instructions))


async def run(prompts: list[str]) -> None:
    async with create_assistant() as assistant:
        for prompt in prompts:
            response = await assistant.chat(prompt)
            print(await response.text())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompts", nargs="+", metavar="요청")
    asyncio.run(run(parser.parse_args().prompts))
