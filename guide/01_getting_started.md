# 01. 설치부터 첫 작업까지

## 학습 목표

ARTEMIS가 해결하는 문제, 실행에 필요한 구성 요소, CLI·MCP·Python SDK의 차이를 알고 **실제 기기를 조작하기 전에** 진단을 끝낸다. AndroidWorld 성능 수치나 README의 실행 화면은 재현을 보장하지 않는다. 사용자 기기·앱·모델 설정에 따라 결과가 달라진다.

## 1. 기본 개념

- **ADB(Android Debug Bridge)**: PC에서 Android 기기와 통신하는 도구다. USB 디버깅과 기기 승인 상태가 핵심이다.
- **LLM 공급자**: 화면을 해석하고 다음 행동을 선택하는 모델 서비스다. 모델 호출에는 자격 증명과 비용이 들 수 있다.
- **프로파일**: `flash`는 빠른 반응형 루프, `pro`는 계획·검증에 무게를 둔 실행 경로다. 둘 다 실제 기기를 조작한다.
- **trace**: 작업의 상태·로그·행동 증거를 보존하는 기록이다. UI에 보이는 성공 문구만으로 검증을 끝내지 않는다.
- **MCP(Model Context Protocol)**: IDE의 AI 에이전트가 ARTEMIS의 모바일 도구를 호출하게 하는 연결 방식이다.

## 2. 설치와 환경 설정

저장소는 Python 3.12 이상과 `uv`를 요구한다([`pyproject.toml`](../pyproject.toml)). Windows PowerShell에서는 저장소 루트에서 다음처럼 시작한다.

```powershell
uv sync --dev
Copy-Item .env.example .env
uv run artemis doctor
adb devices -l
```

macOS/Linux에서는 `cp .env.example .env`와 동일한 `uv` 명령을 사용한다. `uv sync --dev`는 패키지를 설치하지만, 장치 연결이나 모델 자격 증명까지 해결하지 않는다. `start.sh`와 `start.bat`는 일부 시스템 도구 설치 및 글로벌 IDE 설정을 제안하므로, 내용을 확인하고 원하는 경우에만 실행한다.

`.env`에는 실제 사용할 모델의 키만 넣는다. 기본 [`config/artemis.jsonc`](../config/artemis.jsonc)는 Google 모델을 지정하며 [`artemis/config/llm.py`](../artemis/config/llm.py)는 공급자별 키를 검사한다. 따라서 기본 구성을 유지한다면 `GOOGLE_API_KEY`를 설정해야 한다. 다른 공급자를 쓰면 모델 설정과 대응하는 환경변수를 함께 바꾼다. 키를 문서·예제·로그·버전 관리에 넣지 않는다. `OCR_API_KEY`는 선택적인 OCR 구성이다.

기기가 없다면 여기서 멈추지 않아도 된다. [환경 사전점검](examples/01_preflight.py), [계획 파서](examples/02_plan_grammar.py), [trace 검사](examples/03_trace_inspect.py)는 오프라인에서 실행한다.

## 3. 첫 실행: 진단 → 읽기 전용 목표

1. `uv run artemis doctor`에서 Python, 설정, ADB, 연결 기기 문제를 확인한다.
2. `adb devices -l`에서 원하는 기기가 `device` 상태인지 확인한다. `unauthorized`이면 기기 화면의 디버깅 승인 대화상자를 직접 확인한다.
3. 여러 기기가 연결되어 있으면 실행 대상을 명시한다. CLI의 정확한 장치 옵션은 `uv run artemis run --help`에서 확인한다.
4. 테스트용 에뮬레이터에서 **설정 화면을 열고 표시된 정보 읽기**처럼 변경이 적은 목표로 시작한다.

```powershell
uv run artemis run "Open Settings and report the displayed battery level without changing settings" --profile flash
```

이 명령은 실제 Android 화면을 조작하고 모델 API를 호출한다. 개인 휴대전화에 곧바로 실행하지 말고 테스트 계정과 에뮬레이터를 먼저 사용한다. 더 복잡한 목표나 검증 항목이 필요하면 `--profile pro`와 `--verification-level`을 검토한다. [`run.py`](../artemis/interfaces/cli/commands/run.py)에서 프로파일·옵션의 실제 정의를 확인할 수 있다.

## 4. UI, MCP, SDK 중 무엇을 쓸까?

| 방식 | 적합한 상황 | 진입점 |
| --- | --- | --- |
| CLI | 단일 작업을 터미널에서 재현·디버깅 | `uv run artemis run "..." --profile flash` |
| 웹 UI | 화면 미러링, 작업 상태와 replay를 시각적으로 확인 | `uv run artemis ui` |
| MCP | IDE 대화에서 모바일 테스트 도구를 호출 | `uv run artemis mcp --generate-config codex`로 설정 형식 확인 |
| Python SDK | pytest·자동화 코드에서 프로그램 방식으로 실행 | [원본 SDK 예제](../README.md#python-sdk)와 [`artemis/interfaces/sdk`](../artemis/interfaces/sdk) |

`mcp --generate-config codex`는 설정 스니펫을 출력한다. 반면 `mcp --install codex`는 사용자 홈의 글로벌 IDE 설정·규칙을 실제로 바꾼다. 적용 범위를 확인한 뒤 실행하고 IDE를 재시작한다. 직접 서버를 실행하는 `uv run artemis mcp`는 stdio 프로세스로서 IDE 클라이언트가 연결해 사용할 때 의미가 있다. MCP 도구 이름과 의미는 [`mcp_server/README.md`](../mcp_server/README.md)에 정리돼 있다.

## 5. 기기에 설치되는 Accessibility Helper

기본 hierarchy backend는 `auto`이며, 첫 작업이 기기에 Artemis Accessibility Helper를 설치·사용할 수 있다([원본 README](../README.md#on-device-helper)). 공유 기기나 개인 기기에서는 사전에 동의를 받고, 자동 설치를 원하지 않으면 `.env`에 `ARTEMIS_HELPER_AUTO_INSTALL=false`를 설정한다. 선택적으로 `ARTEMIS_HIERARCHY_BACKEND=uiautomator`를 사용할 수 있다. 설치 상태·제거는 `uv run artemis helper status` / `uv run artemis helper uninstall`로 확인한다.

## 6. 가장 흔한 실패

- **`adb devices`가 비어 있음**: 케이블·에뮬레이터 실행·ADB 서버·USB 디버깅을 확인한다.
- **`unauthorized`**: 기기의 RSA 승인 안내를 확인한다. 무작정 재실행하지 않는다.
- **자격 증명 오류**: `.env` 존재만으로 충분하지 않다. 현재 모델 공급자와 해당 키 이름이 일치해야 한다.
- **화면 인식 오류**: `doctor`, hierarchy backend, 접근성 권한, 로그와 trace를 확인한다. 바로 좌표를 하드코딩하지 않는다.
- **느린 실행**: LLM 추론, 화면 캡처, ADB 지연을 분리해 본다. Flash/Pro 선택은 속도와 검증 요구 사이의 선택이지 성공 보장이 아니다.

다음은 [핵심 개념](02_core_concepts.md)에서 한 작업이 코드 안에서 어떻게 흘러가는지 살펴본다.
