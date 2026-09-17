# SPDX-License-Identifier: Apache-2.0
"""ARTEMIS 설치 전 읽기 전용 진단: 키 값이나 장치 내용을 출력하지 않는다.

목표: 실행에 필요한 파일, Python 버전, 외부 명령의 준비 여부를 구분한다.
실행: 저장소 루트에서 ``python guide/examples/01_preflight.py``
예상: 필수 코드와 Python 3.12+가 있으면 종료 코드 0; 장치 도구의 부재는 경고만 표시.
이유: 오프라인 학습 단계에서는 ADB나 API 키가 없어도 소스 구조를 살펴볼 수 있다.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
REQUIRED_FILES = (
    "pyproject.toml",
    "config/artemis.jsonc",
    "artemis/interfaces/cli/main.py",
    "mcp_server/server.py",
)
PROVIDER_KEY_NAMES = (
    "GOOGLE_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "OPEN_ROUTER_API_KEY",
    "XAI_API_KEY",
)


def main() -> int:
    python_ready = sys.version_info >= (3, 12)
    missing_files = [name for name in REQUIRED_FILES if not (REPO_ROOT / name).is_file()]

    print(f"저장소: {REPO_ROOT}")
    print(f"Python 3.12 이상: {'예' if python_ready else '아니요'}")
    print(
        f"필수 소스 파일: {'모두 있음' if not missing_files else '누락: ' + ', '.join(missing_files)}"
    )

    # 명령의 존재만 검사하고 실제로 ADB·서버·기기를 시작하지 않는다.
    for name in ("uv", "adb", "ffmpeg", "scrcpy"):
        state = "발견" if shutil.which(name) else "미발견"
        print(f"{name}: {state}")

    env_file = REPO_ROOT / ".env"
    print(f".env 파일: {'있음' if env_file.is_file() else '없음'}")
    # 현재 프로세스의 환경변수 이름만 검사한다. 값, 길이, 일부 문자열도 출력하지 않는다.
    configured = [name for name in PROVIDER_KEY_NAMES if os.environ.get(name)]
    print(f"현재 셸의 모델 키 변수: {len(configured)}개 설정됨")
    print("참고: .env 파일 내용과 API 키의 유효성은 이 예제가 검사하지 않습니다.")
    print("실제 장치 준비 여부는 설치 후 `uv run artemis doctor`로 확인하세요.")

    return 0 if python_ready and not missing_files else 1


if __name__ == "__main__":
    raise SystemExit(main())
