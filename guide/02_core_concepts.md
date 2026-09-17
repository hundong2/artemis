# 02. 핵심 개념과 코드 흐름

## 학습 목표

ARTEMIS의 사용자가 입력한 목표가 어디로 들어가고, 어떤 경로에서 화면을 관찰·조작하며, 실패 증거가 어디에 남는지 설명할 수 있다. 이 문서는 README 그림만 해석한 자료가 아니라 아래 소스 파일의 호출·등록 관계를 기준으로 한다.

## 1. 한 작업의 실행 흐름

```text
CLI run 또는 MCP mobile_run_task
  → 설정·기기 선택 / 비동기 작업 등록
  → Agent 초기화와 DeviceExecutionLock
  → FlashRunner 또는 Pro graph
  → 화면 계층·스크린샷 관찰 → 행동 실행 → 재관찰
  → trace/status.json, 로그, 결과 기록
```

[`artemis/interfaces/cli/main.py`](../artemis/interfaces/cli/main.py)는 Typer 명령을 등록한다. [`commands/run.py`](../artemis/interfaces/cli/commands/run.py)의 `execute_task`는 LLM 설정과 장치 선택을 수행하고 `Agent`를 초기화한다. [`artemis/sdk/agent.py`](../artemis/sdk/agent.py)의 `run_task`는 `flash` 요청이면 `FlashRunner`, 그렇지 않으면 Pro graph 경로를 사용한다. [`mcp_server/tools/task_runner.py`](../mcp_server/tools/task_runner.py)의 `mobile_run_task`는 같은 종류의 모바일 작업을 비동기로 제출하고 `trace_id`를 반환한다. 이를 받은 클라이언트는 [`mobile_manage_task`](../mcp_server/tools/task_manager.py)로 상태를 확인한다.

이 흐름은 구조적 요약이다. 실제 실행에서는 daemon·worker subprocess·UI 콘솔이 끼어들 수 있다. 프로세스 경계나 상태 소유권을 더 정확히 보려면 [Archify 분석](../docs/archify/README.md)의 코드 근거를 함께 확인한다.

## 2. Flash와 Pro의 역할

| 항목 | Flash | Pro |
| --- | --- | --- |
| 기본 목적 | 분명하고 짧은 UI 경로를 반응형으로 실행 | 복잡한 탐색, 계획, 단계별 검증 |
| 핵심 코드 | [`agents/flash/runner.py`](../artemis/agents/flash/runner.py) | [`graph/graph.py`](../artemis/graph/graph.py), [`utils/plan_grammar.py`](../artemis/utils/plan_grammar.py) |
| 계획·체크 | 지속적 계획서 없음 | top-level milestone, `verify`, `assert` 등 기계 판독 문법 |
| 비용·시간 | 보통 낮지만 모델·기기 상태에 따라 달라짐 | 일반적으로 더 많은 추론·검증 비용 |

Flash는 단순히 “정확도가 낮은 모드”가 아니다. 상태가 명확한 빠른 반복 작업에 적합하다. Pro는 계획과 체크를 둘 수 있지만, 체크 실패가 자동으로 외부 제품의 버그를 확정하지는 않는다. UI 관찰 자료와 로그를 사람이 재검토해야 한다.

## 3. UI 관찰, locator, 좌표

ARTEMIS는 Accessibility Helper 또는 UIAutomator2에서 UI hierarchy를 얻고, 필요한 경우 OCR·이미지 관찰을 결합한다([`screen_client_factory.py`](../artemis/clients/screen_client_factory.py), [`ui_hierarchy.py`](../artemis/utils/ui_hierarchy.py)). 가능하면 resource ID, 텍스트, 접근성 속성 같은 동적 locator를 먼저 사용하고, 위치가 불명확할 때만 좌표를 쓴다. 레이아웃이나 해상도가 바뀌면 절대 좌표는 쉽게 깨진다.

[`coordinates.py`](../artemis/utils/coordinates.py)는 픽셀 좌표와 0–1000 정규화 좌표를 변환한다. 기록을 분석할 때 두 공간을 혼동하지 않는 것이 중요하다. 특히 Pro는 물리 픽셀, Flash는 정규화 좌표를 기록하는 경로가 있으므로 `coordinate_space` 표지를 확인하고 이중 변환하지 않는다. 스와이프 방향은 손가락 이동 방향이다. 예를 들어 `up` 스와이프는 화면의 더 아래쪽 콘텐츠가 보이도록 하는 동작이다.

## 4. Pro 계획 문법이 왜 별도 코드인가?

[`plan_grammar.py`](../artemis/utils/plan_grammar.py)는 계획 문서를 두 채널로 구분한다.

- **기계 채널**: `- [ ]`, `- [/]`, `- [x]`, `- [!]` 같은 체크박스와 `[Loop]`, `[Loop:continuous]`, `verify:`, `assert:`.
- **의미 채널**: 작업 설명의 자유 문장. 사람이 읽거나 모델이 해석하지만, 실행 하네스는 자유 문장 표현을 제어 조건으로 삼지 않는다.

따라서 “완료”라고 자유 문장에 적는 것만으로 top-level milestone이 완료되지 않는다. 반대로 `verify`는 완료 수용 기준, `assert`는 테스트 주장을 뜻하므로 실패 처리도 다르다. [실제 파서 실습](examples/02_plan_grammar.py)은 키·장치 없이 이 차이를 보여준다.

## 5. trace와 상태의 책임

MCP 작업의 `trace_id`는 이후 상태 조회와 기록 탐색의 손잡이다. [`trace_store.py`](../artemis/runtime/trace_store.py)는 `<trace_id>/status.json`을 원자적으로 기록하고 잠금으로 동시 갱신을 조정한다. 최초 필드는 `trace_id`, `task_desc`, `model`, `status`, `device_serial`, `start_time`, `end_time`, `error`, `result` 등을 포함한다. 종료 상태는 `completed`, `failed`, `cancelled`로 정규화된다.

`status.json`만으로 테스트 품질을 확정하면 안 된다. `completed`는 프로세스 완료와 결과 기록을 뜻할 수 있지만, 목표의 정확성은 결과·스크린샷·행동 로그·필요한 검증 항목과 함께 판단해야 한다. trace에는 화면 내용, 앱 데이터, 기기 식별자, 사용자 입력 등이 포함될 수 있다. 공유·업로드 전에 민감정보를 점검한다. [trace 검사 예제](examples/03_trace_inspect.py)는 이런 이유로 작업 설명·결과 본문을 출력하지 않는다.

## 6. 디렉터리 지도와 확장 지점

| 디렉터리 | 하는 일 | 확장 시 주의 |
| --- | --- | --- |
| [`artemis/interfaces/cli`](../artemis/interfaces/cli) | 사용자 명령과 옵션 | CLI 도움말·입력 검증·호환성 테스트 |
| [`artemis/sdk`](../artemis/sdk) | Agent, builders, 타입 | 공개 SDK 계약을 깨지 않기 |
| [`artemis/agents`](../artemis/agents) / [`artemis/graph`](../artemis/graph) | Flash/Pro 행동·계획 | 비용·재시도·중단 조건의 회귀 테스트 |
| [`artemis/clients`](../artemis/clients) / [`artemis/controllers`](../artemis/controllers) | 화면·ADB·기기 접점 | 기기 권한, timeout, 플랫폼 차이 |
| [`mcp_server`](../mcp_server) | IDE 연결과 비동기 도구 | 외부 입력, 상태 조회, 알림 실패 |
| [`artemis/runtime`](../artemis/runtime) / [`artemis/telemetry`](../artemis/telemetry) | 장치 잠금·trace·관측 | 여러 프로세스 동시성·민감정보 보존 |
| [`apps/admin_console`](../apps/admin_console) | 웹 대시보드·작업 큐 | 서비스 시작/중지와 접근 제어 |

다음 단계는 [고급 활용](03_advanced.md)에서 실패를 추적하고 안전하게 기여하는 방법을 익히는 것이다.
