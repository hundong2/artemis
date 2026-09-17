# ARTEMIS 코드 아키텍처: Pro 작업의 실행 경로

분석일: 2026-09-17

- 원격 저장소: [hundong2/artemis](https://github.com/hundong2/artemis)
- 분석 기준 commit: `371aa6df56880643da57b30da936e9812fb0ec66`
- 탐색형 결과: [architecture.html](architecture.html) · [Archify 원본 명세](architecture.json)
- [가이드로 돌아가기](../../guide/README.md)

## 범위와 읽는 순서

이 그림은 `artemis run`의 **Pro 프로필**을 대표 실행 경로로 잡는다. 상단에는 AI 코딩 도구가 외부 FastMCP 작업 도구를 호출하는 별도 진입 경로와 Planner·Operator가 이용하는 모델 제공자를, 하단에는 실행 trace를 보관하는 DataEngine을 둔다. 실행 코드를 직접 확인한 흐름만 그렸고, 저장소의 모든 UI·클라우드·비디오 분석 기능을 하나의 그림에 억지로 넣지 않았다.

1. Typer CLI가 실행 목표와 설정을 받아 `Agent`를 초기화한다.
2. `Agent.run_task()`가 장치 컨텍스트와 작업 요청을 만들고, Pro 실행에서는 LangGraph의 Planner→Operator→Validator·Checker 계열 루프를 호출한다. Flash는 별도 `FlashRunner` 분기다.
3. Validator는 현재 화면의 전제조건을 확인한 뒤 프로세스 **내부** `ActionSession`으로 행동을 보낸다. 이 세션은 외부 IDE용 FastMCP 서버와 별개이며 메모리상의 MCP client/server 쌍이다.
4. `AdbActuator`·`UnifiedMobileController`·`AndroidAdbDriver`가 ADB와 화면 계층/스크린샷을 통해 기기와 통신한다. `DataEngine`은 세션·step·trace를 로컬 SQLite 및 파일 경로에 기록한다.

## 구성요소와 코드 근거

다음 경로는 이 commit에서 확인한 저장소 상대 경로다. 세부 번호는 [명세의 `sources`](architecture.json)에도 기록했다.

| 그림의 구성요소 | 확인한 근거 | 역할 |
| --- | --- | --- |
| 사용자·Typer CLI | `artemis/interfaces/cli/main.py:41`, `artemis/interfaces/cli/commands/run.py:44` | `run` 명령 등록과 작업 요청 접수. |
| Agent SDK | `artemis/sdk/agent.py:132`, `:517`, `:685`, `:727` | 장치 컨텍스트, 작업 수명주기, Flash/Pro 분기. |
| Pro 실행 그래프 | `artemis/graph/graph.py:965`, `:980`, `:1033`, `:1034`, `:1043` | Planner, Operator, Validator 및 후속 노드의 등록·전이. |
| 기기 제어 경계 | `artemis/agents/validator/validator.py:65`, `artemis/mcp/action_session.py:66`, `artemis/mcp/actuators/adb.py:101` | 전제조건 검사, 단일 owner 작업의 in-memory MCP 호출, ADB 제어. |
| Android 기기 | `artemis/controllers/unified_controller.py:64`, `artemis/drivers/factory.py:75`, `artemis/drivers/android/adb_driver.py:73`, `:122` | 플랫폼 드라이버 선택과 화면/입력 동작. |
| AI 코딩 도구·FastMCP | `mcp_server/server.py:82`, `mcp_server/base.py:33`, `mcp_server/tools/task_runner.py:204`, `mcp_server/background/task_runner.py:166`, `:231` | 외부 MCP 도구를 등록하고 작업을 Agent 실행으로 연결. |
| 모델 제공자 | `artemis/agents/planner/planner.py:311`, `artemis/agents/operator/operator.py:936`, `artemis/services/llm.py` | Planner·Operator의 모델 호출 경계. 특정 공급자를 고정하지 않는다. |
| DataEngine | `artemis/sdk/agent.py:1139`, `artemis/data_engine/engine.py:392`, `:407`, `artemis/data_engine/storage.py:64`, `:94` | 실행 세션과 단계 기록을 로컬 SQLite로 저장. |

## 신뢰 경계와 제한 사항

- **외부 IDE → MCP 서버:** 별도의 외부 도구 진입점이다. `mcp_server/server.py`와 `mcp_server/tools/task_runner.py`가 등록·작업 제출을 담당한다. 그림의 외부 FastMCP와 내부 `ActionSession`을 같은 프로세스/전송으로 해석하면 안 된다. MCP 작업은 환경에 따라 daemon queue 또는 독립 background runner로 갈 수 있다.
- **Agent → 모델 제공자:** 추론 서비스로 프롬프트와 관측 자료가 전달될 수 있다. 모델 키는 `artemis/config/settings.py`의 설정 대상으로, 배포별 네트워크·데이터 보존 정책은 이 그림만으로 단정하지 않는다. 선택적 OCR도 별도 외부 경계이지만 그림에서는 제외했다.
- **로컬 호스트 → Android:** ADB와 화면 관측/입력은 실제 장치 상태를 변경할 수 있다. 모의 드라이버와 클라우드 원격 드라이버도 있지만 대표 경로는 기본 Android ADB 드라이버다 (`artemis/drivers/factory.py:34`). 실제 실습에는 사용자 소유 기기, USB 디버깅, 승인된 테스트 앱이 필요하다.
- **실행 기록:** `DataEngine`은 로컬 SQLite와 이미지/trace 파일을 사용한다. 화면 및 로그에 민감정보가 들어갈 수 있으므로 공유 전에 점검한다.
- **제외 범위:** Angular Showcase UI→FastAPI→작업 큐·별도 프로세스 경로, FlashRunner의 반응형 루프, optional OCR, cloud virtualization, 기능별 agent 내부 상세, 프로덕션 배포 토폴로지는 그림에 포함하지 않았다. 이들은 `apps/admin_console/server.py`, `apps/admin_console/services/task_queue_service.py`, `artemis/agents/flash/runner.py` 등에서 별도로 확인할 수 있다. 그림은 배포 환경·인증 체계·포트를 추정하지 않는다.
- **언어:** 작성한 제목·구성요소·설명은 한국어다. Archify Viewer가 한국어 locale을 지원하지 않으므로 `meta.locale`을 생략했으며, 고정 Viewer UI와 생성된 `<html lang>`은 영어로 fallback한다.

## 검증 증거

- Archify 유형: `architecture`, 품질: `showcase`.
- 명세 검사: **9/9 artifact checks, composition error 0, warning 0**. 실행한 명령: `validate architecture architecture.json --repo-root <이 저장소> --quality showcase --json`.
- 최종 전달: `deliver architecture architecture.json architecture.html --repo-root <이 저장소> --quality showcase --json` 종료 코드 0. 고정 명세의 SHA-256 `b950209e93d4b8989f233df49f3f45f185849753496b3f6544cddea0542796aa` (4,392 bytes), 결과 HTML의 SHA-256 `4f38adf101e4fc30858e05b3ba0144893049bb7b0678bd38aee153c9c4ab9dd1` (717,494 bytes). 코드 근거 참조 23개를 검사했다.
- 브라우저 자동 증거: [visual-check receipt](architecture.visual-check.json) **passed**; 현재 HTML의 SHA-256에 연결되어 있다. 1440×900, 1600×1000, 1920×1080, 2048×1320의 밝은 테마에서 가로·세로 넘침 없음, 두 끝 크기의 밝은/어두운 스크린샷을 수집했다. [contact sheet](architecture.visual-check.html) · [1440 밝음](architecture.visual-check.1440x900.light.png) · [1440 어두움](architecture.visual-check.1440x900.dark.png) · [2048 밝음](architecture.visual-check.2048x1320.light.png) · [2048 어두움](architecture.visual-check.2048x1320.dark.png).
- 별도 시각 검토: 네 장의 실제 이미지를 열어 두 테마의 노드·카드 잘림, 라벨 충돌, 관계선 교차와 큰 화면의 하단 균형을 확인했고 눈에 띄는 결함을 발견하지 못했다. 이는 자동 브라우저 증거와 다른 **이미지 기반 인지 검토**다. 시각 검토 이후 명세 수정은 없었다.
- 후보 단계에서는 라벨 위치 충돌 두 건과 작은 화면의 글자 크기 문제를 검증 결과에 따라 고쳤다. 최종 전달 이후 **시각 수정 회차는 0회**다.

```text
diagram_type: architecture
output: D:\workspace\laboratory\artemis\docs\archify\architecture.html
specification_sha256: b950209e93d4b8989f233df49f3f45f185849753496b3f6544cddea0542796aa
artifact_sha256: 4f38adf101e4fc30858e05b3ba0144893049bb7b0678bd38aee153c9c4ab9dd1
validation: 9/9 showcase, 0 errors, 0 warnings
browser_evidence: passed
visual_review: passed
correction_rounds: 0
```
