# 03. 고급 활용: 검증, 진단, 성능, 보안

## 학습 목표

테스트의 성공 조건을 먼저 정의하고, Flash/Pro를 목적에 맞게 선택하며, trace와 코드 근거로 실패를 진단한다. 실제 장치가 없어도 계획 문법과 상태 기록을 재현할 수 있다.

## 1. 작업을 검증 가능한 테스트로 바꾸기

“앱이 잘 동작하는지 봐줘”는 종료 기준이 없다. 테스트를 설계할 때 대상 앱 패키지, 시작 상태, 허용 행동, 기대 결과, 금지 행동, 최대 대기 시간, 기록할 증거를 먼저 정한다. 실제 실행 목표에는 테스트 계정·가짜 데이터와 `--locked-app` 같은 범위 제한을 고려한다. `locked_app_package`의 의미는 [`run.py`](../artemis/interfaces/cli/commands/run.py)와 [`mcp_server/tools/task_runner.py`](../mcp_server/tools/task_runner.py)에서 확인할 수 있다.

Pro 계획의 예시는 다음과 같다. 이것은 실행 명령이 아니라 파서가 읽는 형식을 이해하기 위한 문서다.

```md
- [ ] 테스트 앱을 연다
  - verify: 로그인 화면이 보인다
- [/] 읽기 전용 정보 화면을 확인한다
  - assert: 배터리 수치가 표시된다
- [ ] 결과와 근거를 기록한다
  - assert@end: 최종 화면 스크린샷이 있다
```

`verify`는 다음 단계로 갈 수 있는지 확인하는 수용 기준이고, `assert`는 테스트 결과의 주장이다. `[Loop:continuous]`는 정상 종료 조건을 별도로 설계해야 하므로 일반 단발 테스트에 습관적으로 넣지 않는다. [오프라인 실습](examples/02_plan_grammar.py)에서 실제 파서가 인식한 구조를 본다.

## 2. 실패 분석 순서

1. `uv run artemis doctor` 또는 MCP의 `mobile_diagnose`로 환경·장치·자격 증명부터 분리한다.
2. `adb devices -l`로 대상 기기와 승인 상태를 확인한다. 여러 기기라면 사용자가 지정한 serial을 보존한다.
3. CLI나 MCP가 반환한 `trace_id`와 상태를 기록하고, `status.json`, `stdout.log`, `stderr.log`를 읽는다. 로그는 기기 내용과 키가 섞일 수 있으므로 외부 공유 전에 가린다.
4. 장치 연결은 정상인데 행동이 실패했다면 hierarchy, OCR, 좌표 공간, 타임아웃, 화면 전환 시점으로 가설을 좁힌다. 좌표 하드코딩은 최후 수단이다.
5. 버그 보고에는 재현 절차, 기기/에뮬레이터 버전, 앱 버전, 프로파일, 기대·실제 결과를 포함하되 비밀값과 개인 데이터는 제거한다.

[`trace_store.py`](../artemis/runtime/trace_store.py)는 손상된 `status.json`을 격리하고, 여러 프로세스의 상태 갱신에 잠금을 사용한다. 따라서 상태 파일을 직접 수정해 결과를 “고치는” 방식은 피한다. [읽기 전용 trace 검사 예제](examples/03_trace_inspect.py)를 사용하면 합성 레코드 또는 이미 생성된 `status.json`의 형식만 살펴볼 수 있다.

## 3. 성능과 비용을 볼 때

자동화의 전체 지연을 `모델 추론 + 화면 캡처/전송 + 탐색 + ADB/기기 실행 + 검증`으로 나누어 본다. Flash와 Pro의 시간 차이를 곧바로 모델 성능 차이로 해석하지 않는다. 같은 앱 상태, 같은 장치, 같은 목표, 같은 모델 설정에서 여러 번 측정해야 한다. API 호출 수·토큰 비용, 실패율, 확인 가능한 최종 결과, 실행 시간이 함께 지표가 된다.

비결정적인 화면(애니메이션·토스트·네트워크 로딩)에는 고정 `sleep`보다 상태 기반 대기와 명시적 타임아웃을 우선한다. 단, 상태 기반 대기 역시 accessibility 정보가 빠진 앱에서는 OCR·영상 관찰로 보완해야 한다. Flash에서 계획·체크포인트가 필요한 상황이면 단순히 재시도를 늘리기보다 Pro로 전환하고 수용 기준을 작성한다.

## 4. 보안·프라이버시 경계

- `.env`의 API 키와 로그인 비밀은 Git에 넣지 않는다. 진단 결과를 붙여넣을 때도 실제 값을 제거한다.
- MCP의 `mobile_run_task`는 기기 조작 권한을 IDE 에이전트에 연결한다. 신뢰할 수 있는 클라이언트에만 노출하고, 대상 앱·기기 범위를 제한한다.
- 기본 MCP stdio는 로컬 IDE 연결에 적합하다. 원격 전송(`sse`)을 사용할 때는 [`mcp.py`](../artemis/interfaces/cli/commands/mcp.py)의 기본 바인딩 주소 `127.0.0.1`을 변경하기 전에 인증·네트워크 접근 제어를 설계한다. 단순 포트 개방을 배포 절차로 간주하지 않는다.
- Accessibility Helper는 기기에 설치될 수 있다. 공유·개인 장치에서 자동 설치를 끄거나 제거하는 방법은 [시작하기](01_getting_started.md#5-기기에-설치되는-accessibility-helper)를 따른다.
- trace와 스크린샷에는 개인 데이터가 남을 수 있다. 테스트 전용 계정과 데이터 보존·삭제 정책을 준비한다.

## 5. 코드 기여·배포 전 검증

`CONTRIBUTING.md`는 기본 `make test`를 장치·키가 필요 없는 결정적 테스트로 정의한다. `pyproject.toml`의 pytest 기본 마커도 `integration`, `e2e`, `cloud`, `manual`, `android`를 제외한다. 새 기능은 가능한 한 이 기본 테스트에 순수 로직을 분리하고, 장치가 필요한 테스트에 정확한 마커를 붙인다.

```powershell
uv run pytest
uv run ruff format --check guide/examples
uv run ruff check guide/examples
uv run pyright --project pyright-core.json
```

`uv run pytest`는 프로젝트 전체의 기본 테스트다. 장치·모델 실험은 필요한 환경을 갖춘 별도 단계에서 [`Makefile`](../Makefile)의 `test-integration` / `test-device` 정의를 보고 수행한다. 문서와 오프라인 예제만 작업한다면 예제 세 개를 Python으로 직접 실행하고 lint를 확인하는 것으로도 독립 검증이 가능하다.

프로덕션에 연결되는 MCP 도구를 새로 만들 때는 [`mcp_server/base.py`](../mcp_server/base.py)의 도구 등록, 입력 검증, 시간 초과와 취소, trace 상태 갱신, 민감정보 차단, 재시도·중복 실행 위험을 함께 살핀다. CLI 옵션을 바꾸면 `--help`와 문서·테스트를 동기화한다. 변경 이력과 코드 근거를 공유할 때는 [Archify 분석](../docs/archify/README.md)을 참조하되, 그림이 테스트 증거를 대체하지는 않는다.

## 다음 학습 경로

1. [계획 파서](examples/02_plan_grammar.py)의 입력을 바꿔 완료·차단·연속 루프 상태를 비교한다.
2. [trace 검사](examples/03_trace_inspect.py)에 `--status`를 제공해 실제 작업의 상태 파일을 읽되 결과 본문은 출력하지 않는다.
3. `tests/unit`의 관련 테스트를 읽고 순수 파서나 상태 로직에 대한 실패 케이스를 추가한다.
4. 승인된 에뮬레이터에서 작은 목표를 실행하고, 예상 결과와 실제 trace를 대조한다.
