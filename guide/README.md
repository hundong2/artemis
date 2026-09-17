# ARTEMIS 한국어 학습 가이드

작성일: 2026-09-17

코드 확인 기준: 이 저장소의 `371aa6df56880643da57b30da936e9812fb0ec66` 커밋

ARTEMIS는 자연어 목표를 Android 기기·에뮬레이터에서 실행하고, 화면 관찰과 조작 과정을 기록하는 모바일 자동화·테스트 프레임워크다. 이 가이드는 [원본 README](../README.md)를 출발점으로 삼되, 실제 코드의 진입점과 안전한 실습 경계를 함께 설명한다. 프로젝트 전체의 시각적 구조는 [Archify 코드 아키텍처 분석](../docs/archify/README.md)을 참고한다.

## 학습 순서

| 단계 | 자료 | 학습 목표 | 장치·API 키 |
| --- | --- | --- | --- |
| 0 | [환경 사전점검 예제](examples/01_preflight.py) | Python, `uv`, ADB, 설정 파일의 존재를 확인하되 비밀값을 출력하지 않기 | 불필요 |
| 1 | [시작하기](01_getting_started.md) | 설치, 설정, `doctor`, 첫 CLI 실행, MCP 연결 | 실제 실행 때 필요 |
| 2 | [핵심 개념](02_core_concepts.md) | CLI→Agent→Flash/Pro→기기 제어→trace 흐름 읽기 | 불필요 |
| 3 | [계획 문법 예제](examples/02_plan_grammar.py) | 실제 Pro 계획 파서의 상태·검증 항목을 오프라인에서 관찰하기 | 불필요 |
| 4 | [고급 활용](03_advanced.md) | 테스트 설계, trace 디버깅, 성능·보안, 코드 확장 | 선택 |
| 5 | [trace 검사 예제](examples/03_trace_inspect.py) | 기록 상태의 핵심 필드와 완료 조건을 민감정보 노출 없이 검토하기 | 불필요 |

Python 예제는 저장소 루트에서 실행한다. 최소 Python 버전은 `pyproject.toml` 기준 3.12다. 오프라인 예제는 의도적으로 실제 장치나 LLM을 호출하지 않으며, ARTEMIS의 대형 런타임 의존성을 설치하기 전에도 실행할 수 있다.

```powershell
python guide/examples/01_preflight.py
python guide/examples/02_plan_grammar.py
python guide/examples/03_trace_inspect.py
```

`02_plan_grammar.py`는 저장소의 실제 `artemis/utils/plan_grammar.py` 파일만 별도 로드한다. 따라서 일반 `artemis` 패키지의 장치·모델 관련 초기화를 수행하지 않는다. `03_trace_inspect.py`는 기본적으로 메모리상의 합성 자료를 검사하고, `--status <path>`를 지정한 경우에만 실제 `status.json`을 **읽기 전용**으로 검사한다. 합성 자료나 오프라인 예제의 성공은 Android 자동화의 성공을 의미하지 않는다.

## 실사용에 필요한 것

- Python 3.12 이상, `uv`, Android SDK의 `adb`, 승인된 Android 기기 또는 에뮬레이터.
- 화면 기록·분석에 필요한 FFmpeg와 선택적인 scrcpy. `uv run artemis doctor`로 현재 환경의 요구 사항을 확인한다.
- `config/artemis.jsonc`에서 선택한 모델 공급자에 대응하는 자격 증명. 기본 설정은 Google 공급자를 사용하므로 `.env`의 `GOOGLE_API_KEY`가 필요할 수 있다. 다른 공급자는 설정과 키를 함께 바꾼다.
- 실기기 실행 전, 자동 조작 대상·앱·계정을 확인한다. 개인 기기·실서비스의 변경 작업에는 테스트 계정을 사용한다.

## 코드에서 확인한 진입점

- [CLI 명령 등록](../artemis/interfaces/cli/main.py): `init`, `doctor`, `run`, `ui`, `mcp`, `trace`, `helper`.
- [실행 명령](../artemis/interfaces/cli/commands/run.py): 설정 로드, 장치 선택, `Agent` 생성·실행.
- [에이전트 실행](../artemis/sdk/agent.py): Flash runner 또는 Pro graph로 분기하고 장치·기록을 관리.
- [MCP 작업 시작](../mcp_server/tools/task_runner.py): 비동기 작업과 `trace_id`를 제공.
- [trace 저장](../artemis/runtime/trace_store.py): `status.json`의 원자적 기록 및 상태 갱신.

문서의 명령과 옵션은 위 확인 기준의 코드에 맞췄다. 이후 upstream 버전에서 인터페이스가 바뀌면 `uv run artemis --help`와 하위 명령의 `--help`를 우선 확인한다.

## 다음 단계

오프라인 예제를 먼저 실행해 용어와 자료 구조를 익힌 뒤, [시작하기](01_getting_started.md)의 사전 진단을 통과하면 테스트용 에뮬레이터에서 간단한 읽기 작업부터 시작한다. 자동화가 실패하면 [고급 활용](03_advanced.md)의 trace·로그 점검 순서로 원인을 좁힌다.
