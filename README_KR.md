<p align="center">
  <img src="./docs/assets/artemis-banner.png?v=7" alt="ARTEMIS 배너" width="100%" />
</p>

<p align="center">
  <strong>AI 어시스턴트와 테스트 도구가 사람처럼 실제 휴대전화를 조작하도록 지원합니다.</strong>
</p>

<p align="center">
  <a href="./README.md">English</a> •
  <a href="./README_CN.md">中文文档</a> •
  <a href="./README_KR.md"><b>한국어</b></a> •
  <a href="#workflow-showcase">작업 흐름</a> •
  <a href="#quick-start">빠른 시작</a> •
  <a href="#mcp-setup">IDE용 MCP</a> •
  <a href="#benchmarks">벤치마크</a> •
  <a href="https://discord.gg/wF2FN4WHGY">Discord 커뮤니티</a>
</p>

<p align="center">
  <a href="./guide/README.md">한국어 학습 가이드</a> •
  <a href="./docs/archify/README.md">코드 아키텍처 분석</a>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.12+-3776AB.svg?logo=python&logoColor=white" alt="Python 3.12 이상"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="Apache-2.0 라이선스"></a>
  <a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/MCP-Native%20Server-8A2BE2.svg" alt="MCP 서버"></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/Multimodal-Gemini%20%7C%20Claude%20%7C%20GPT--4o%20%7C%20Qwen--VL-4285F4.svg" alt="다중 모델 지원"></a>
  <a href="https://github.com/google-research/android_world"><img src="https://img.shields.io/badge/AndroidWorld-99%25%2B%20SOTA-success.svg" alt="AndroidWorld 결과"></a>
</p>

<!-- 시연 화면 -->
<p align="center">
  <img src="./docs/assets/demo.gif" alt="ARTEMIS 실행 모습" width="100%" />
  <br>
  <em>실기기 시연: Google Maps에서 운전 경로와 총 소요 시간을 확인한 다음 YouTube에서 Coldplay 노래를 재생합니다.</em>
</p>

> 이 문서는 [영문 README](./README.md)의 한국어 번역입니다. 기능·벤치마크 수치는 프로젝트가 보고한 값이며, 사용 환경에 따라 달라질 수 있습니다. 설정과 명령은 번역 기준 저장소의 원문을 우선 확인하세요.

## 주요 특징

* **앱 간 자동화**: 자연어 지시로 Android 기기의 테스트 절차와 일상 작업을 수행합니다.
* **멀티모달 대상 지정**: 가능한 경우 요소 인덱스를 사용하고, 맞춤형 UI에는 좌표·시각적 위치 찾기를 대안으로 사용합니다.
* **IDE 진단**: **Model Context Protocol(MCP)** 통합을 통해 **Antigravity, Claude Code, Windsurf** 등이 테스트 기기를 조작하고 **Logcat** 출력과 스크린샷을 수집합니다.
* **Flash 실행**: 비동기 기록 요약을 곁들인 관찰-행동 반응형 루프로, 저장소 설명상 보통 단계당 **3~5초**가 걸립니다.
* **Pro 탐색**: 개별 행동 전에 대상을 확인하고, 막힌 행동은 Operator가 복구하도록 전달합니다. 장시간 탐색·안정성 테스트를 지원합니다.
* **AndroidWorld 결과**: 프로젝트는 Google Research의 **AndroidWorld** 벤치마크(100개 이상의 다단계 과제)에서 **99% 이상의 과제 완료율**을 보고합니다.

<a id="workflow-showcase"></a>
## Antigravity × ARTEMIS: 자율 테스트 작업 흐름

**Antigravity**는 MCP를 통해 **ARTEMIS**를 사용하여 테스트 요청을 계획, 기기 실행, 진단 보고서로 연결합니다.

<table width="100%">
  <tr>
    <td width="50%" align="center">
      <b>1. 프롬프트 입력(작업 전달)</b><br>
      <sub>Antigravity에 테스트 시나리오와 목표 지표를 기술</sub><br><br>
      <img src="./docs/assets/workflow-1-prompt.png" width="100%" alt="1단계: 프롬프트 입력" />
    </td>
    <td width="50%" align="center">
      <b>2. 테스트 계획 생성</b><br>
      <sub>검토할 단계별 테스트 계획과 구조를 작성</sub><br><br>
      <img src="./docs/assets/workflow-2-plan.png" width="100%" alt="2단계: 테스트 계획 생성" />
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <b>3. 자율 테스트 실행</b><br>
      <sub>실기기를 조작하고 UI를 탐색하며 성능을 분석</sub><br><br>
      <img src="./docs/assets/workflow-3-exec.png" width="100%" alt="3단계: 자율 테스트 실행" />
    </td>
    <td width="50%" align="center">
      <b>4. 최종 보고</b><br>
      <sub>구조화된 점검 결과, 지표 표와 원시 데이터를 제공</sub><br><br>
      <img src="./docs/assets/workflow-4-report.png" width="100%" alt="4단계: 최종 보고" />
    </td>
  </tr>
</table>

<a id="quick-start"></a>
## 빠른 시작

이 문서는 `hundong2/artemis` 포크의 사용법입니다. 아래 복제 명령은 이 포크를 가리키며, 원본 개발 저장소는 `google/artemis`입니다.

**USB 디버깅**이 켜진 Android 기기 또는 에뮬레이터가 연결되어 있는지 확인합니다. 원클릭 시작 스크립트는 다음 작업을 수행하도록 설계되어 있습니다.

* **시스템 도구 설치**: ADB, scrcpy, FFmpeg 및 Python 패키지 도구 `uv`와 관련 의존성을 탐지·설치합니다.
* **전역 MCP 서버와 AI 에이전트 규칙 적용**: **Artemis Mobile Testing Mindset**(`rules.md`)과 MCP 설정을 **Antigravity, Cursor, Claude Code, Codex, Windsurf, VS Code, Cline/Roo, OpenClaw**에 설치할지 묻습니다.

### macOS 및 Linux

```bash
# 1. 저장소를 복제하고 디렉터리로 이동
git clone https://github.com/hundong2/artemis.git && cd artemis

# 2. 원클릭 실행
./start.sh
```

### Windows PowerShell

```powershell
# 1. 저장소를 복제하고 디렉터리로 이동
git clone https://github.com/hundong2/artemis.git
cd artemis

# 2. 원클릭 실행
.\start.bat
```

> PowerShell은 기본적으로 현재 디렉터리의 실행 파일을 검색하지 않으므로 `start.bat` 대신 `.\start.bat`을 사용합니다. 끝에 `\`를 덧붙이지 마세요. 명령 프롬프트(CMD)에서는 `start.bat`을 사용합니다.

> **팁**: 기본 브라우저에서 `http://localhost:8000`이 열리며 기기 연결 마법사, 실시간 화면 미러링, 프롬프트 실험 영역, 실행 재생 기능을 제공합니다. CLI에서 직접 실행할 수도 있습니다: `uv run artemis run "Open Settings, find Battery and tell me current level" --profile flash`.

<a id="mcp-setup"></a>
<a id="mcp"></a>
<details>
<summary><b>Codex / Antigravity / Claude Code / Windsurf의 MCP 설정(펼치기)</b></summary>

<br>

ARTEMIS에는 기본 **Model Context Protocol(MCP)** 서버가 포함되어 있어 AI IDE에서 실기기를 연결할 수 있습니다.

### 1. 원클릭 자동 설치(권장)

macOS/Linux의 `./start.sh` 또는 Windows PowerShell의 `.\start.bat`을 실행하면, 감지된 IDE에 전역 MCP 설정과 테스트 규칙을 적용할지 묻습니다. 나중에 아래 명령으로 수동 설치하거나 갱신할 수도 있습니다.

```bash
# Antigravity / Jetski에 MCP 서버와 전역 규칙을 설치
uv run artemis mcp --install antigravity

# Codex를 포함한 지원 IDE 전체에 설치
uv run artemis mcp --install all
```

> **팁**: 최초 설정에서 `uv run artemis init`으로 MCP를 대화형으로 구성할 수도 있습니다. 프로젝트 루트에서 `uv tool install -e .`을 한 번 실행하면 다른 디렉터리에서도 `uv run` 없이 `artemis` 명령을 사용할 수 있습니다.

### 2. 수동 설정(선택 사항)

`uv run artemis mcp --generate-config <client>`를 실행하면 클라이언트에 맞는 TOML 또는 JSON 설정을 출력합니다. 아래 예시의 `/path/to/artemis`를 실제 저장소 경로로 바꾸고 `command`가 해당 저장소 `.venv`의 Python 실행 파일을 가리키도록 합니다. Windows에서는 Python 실행 파일 경로가 일반적으로 `.venv\Scripts\python.exe`입니다.

* **Codex** (`~/.codex/config.toml`):

```toml
[mcp_servers.artemis]
command = "/path/to/artemis/.venv/bin/python"
args = ["-m", "mcp_server"]
cwd = "/path/to/artemis"

[mcp_servers.artemis.env]
PYTHONUNBUFFERED = "1"
PYTHONPATH = "/path/to/artemis"
```

* **Antigravity** (`~/.gemini/jetski/mcp_config.json`):

```json
{
  "mcpServers": {
    "artemis": {
      "command": "/path/to/artemis/.venv/bin/python",
      "args": ["-m", "mcp_server"],
      "cwd": "/path/to/artemis",
      "env": {
        "PYTHONUNBUFFERED": "1"
      },
      "tools": {
        "mobile_run_task": { "eager": true },
        "mobile_manage_task": { "eager": true },
        "mobile_get_device_state": { "eager": true },
        "mobile_inspect_trace": { "eager": true },
        "mobile_diagnose": { "eager": true }
      }
    }
  }
}
```

* **Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "artemis": {
      "command": "/path/to/artemis/.venv/bin/python",
      "args": ["-m", "mcp_server"],
      "cwd": "/path/to/artemis"
    }
  }
}
```

### 3. AI 에이전트의 행동 규칙 적용(권장)

AI 코딩 어시스턴트가 UI 조작을 추측하지 않고 실제 상태를 확인하며 테스트하도록 [`mcp_server/rules.md`](./mcp_server/rules.md)를 제공합니다. 이 파일에는 **코딩 전 능동적 탐색**, **Flash/Pro 경로 선택**, **지연과 타이밍 보정**, **동적 위치 지정 우선·좌표 대체** 전략이 담겨 있습니다.

규칙을 사용하는 IDE의 작업 영역 또는 전역 규칙에 연결하거나 복사할 수 있습니다.

* **Antigravity**: 작업 영역 또는 전역 규칙에 `rules.md` 내용을 추가합니다.
* **Claude Code**: `artemis mcp --install claude`로 `~/.claude/rules/artemis.md`에 설치합니다. `~/.claude/CLAUDE.md`와 `~/.claude/rules/*.md`를 모두 읽으므로 중복 설치는 피하세요.
* **Cursor**: `.cursorrules` 또는 `.cursor/rules/artemis.mdc`를 사용합니다.
* **Codex**: `~/.codex/AGENTS.md` 또는 활성화된 `AGENTS.override.md`에 추가합니다.
* **Windsurf / OpenClaw**: 작업 영역 규칙 또는 전역 시스템 프롬프트에 추가합니다.

MCP 설계와 테스트 규칙의 자세한 내용은 [MCP Server README](./mcp_server/README.md)를 참고하세요.

### 4. IDE 채팅에서 기기 테스트 요청

Codex, Antigravity 또는 Claude Code에서 다음과 같이 요청할 수 있습니다.

> "최신 변경 사항으로 APK를 빌드해 연결된 기기에 설치하고, 테스트 계정으로 로그인 화면을 확인해 주세요. 로그인 뒤 예상치 못한 팝업이 있는지 검사하고 마지막 화면의 스크린샷을 반환해 주세요."

</details>

<a id="python-sdk"></a>
<details>
<summary><b>Python SDK 통합(펼치기)</b></summary>

<br>

개발 장치에는 런타임 의존성이 없는 경량 클라이언트만 설치합니다. ADB, 에이전트, 모델과 영상 처리 작업은 기기 호스트에 남습니다.

```powershell
uv add "artemis-client @ git+https://github.com/hundong2/artemis.git#subdirectory=packages/artemis-client"
```

```python
import asyncio
from artemis_client import ArtemisClient


async def main():
    client = ArtemisClient(
        "http://artemis-host:8000",
        device_serial="emulator-5554",  # 선택: 특정 기기 일련번호 지정
        default_profile="flash",  # 빠른 반응형 실행은 "flash", 심층 추론은 "pro"
    )

    result = await client.run(
        "Open System Settings, go to 'Battery', verify battery percentage is displayed, and check for any crash dialogs.",
    )

    assert result.succeeded, f"테스트 실패: {result.error or result.status}"
    print(f"✅ 테스트 통과! 기기: {result.device_serial} | Trace ID: {result.trace_id}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

## 사용 방식

<p align="center">
  <img src="./docs/assets/artemis-ui-showcase-en.png" alt="ARTEMIS 웹 콘솔" width="100%" />
  <br />
  <sub><b>콘솔 개요</b>: <b>① 화면 전환</b>(Home / Workspace) · <b>② 모델과 재생</b>(Flash/Pro 상태와 동영상 재생) · <b>③ 실시간 에이전트 흐름</b>(행동 인식, 대상 좌표, 구조화된 결과) · <b>④ 프롬프트 입력</b>(자연어 작업 전달) · <b>⑤ 작업 대기열과 대시보드</b>(수명주기와 기록)</sub>
</p>

* **웹 시각화 테스트 콘솔(`uv run artemis ui`)**: 실시간 화면 투사와 상호작용 패널에서 자연어로 테스트를 시작하고 추론 정보, 행동 경로, 실행 재생을 확인합니다. `uv run artemis restart`, `uv run artemis stop`, `uv run artemis status`로 다른 터미널에서도 서버 상태를 관리할 수 있습니다.
* **MCP 서버**: **Antigravity, Claude Code, Windsurf** 등 MCP 클라이언트를 기기에 연결하여 버그 재현과 테스트를 수행합니다.
* **개발자 CLI(`uv run artemis run`)**: 터미널에서 자동화 테스트, 탐색적 안정성 점검, AndroidWorld 벤치마크를 수행하고 구조화된 결과를 확인합니다.
* **Python SDK**: Pydantic 기반의 정형 결과와 단언문을 사용하여 pytest 같은 테스트 도구나 CI/CD 파이프라인에 통합합니다.

<a id="on-device-helper"></a>
## ARTEMIS가 휴대전화에 설치하는 항목

한 기기에서 첫 작업을 시작하면 화면 레이아웃을 읽는 작은 접근성 서비스 **Artemis Accessibility Helper**를 설치합니다. 이 서비스는 UiAutomation 연결을 점유하지 않습니다. UiAutomation을 사용하는 다른 도구가 `FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES`를 활성화하지 않으면 Helper가 일시 중지될 수 있습니다. 휴대전화에 접힌 상태의 "Artemis test helper is running" 알림과 설정 > 접근성의 새 항목이 나타납니다. 둘 다 이 Helper에 해당합니다. 원문 설명에 따르면 Helper는 휴대전화 자체에서만 수신 대기하며 외부로 직접 데이터를 보내지 않습니다.

* 미리 설치해 첫 작업의 약 3초 지연 줄이기: `uv run artemis helper install`
* 상태 확인: `uv run artemis helper status` / `uv run artemis doctor`
* 언제든 제거: `uv run artemis helper uninstall`
* UIAutomator2 사용: `.env`에 `ARTEMIS_HIERARCHY_BACKEND=uiautomator` 설정
* 자동 설치 방지: `.env`에 `ARTEMIS_HELPER_AUTO_INSTALL=false` 설정

작업 중 Helper가 실패하면 ARTEMIS는 UIAutomator2로 전환하고 작업 타임라인, `mobile_manage_task` 상태, 최종 보고서에서 이를 알립니다.

<a id="benchmarks"></a>
## 벤치마크: AndroidWorld(프로젝트 보고치 99% 이상)

프로젝트는 Google Research의 [AndroidWorld](https://github.com/google-research/android_world)에서 **99% 이상의 과제 완료율**을 달성했다고 보고합니다. 원문에 따르면 이 벤치마크에는 20개 이상의 앱과 100개 이상의 다단계 과제가 포함됩니다. 수치는 원본 저장소가 제시한 결과이므로 장비·모델·평가 설정이 다른 환경의 성능으로 일반화하지 마세요.

<p align="center">
  <img src="./docs/assets/androidworld_leaderboard.png?v=2" alt="AndroidWorld 벤치마크 비교" width="100%" />
</p>

## ARTEMIS의 구조

* **실행 전 확인과 연속 행동**: Pro는 개별 행동을 보내기 전에 실시간 UI 트리와 화면 픽셀을 사용해 대상을 확인합니다. 연속 행동은 다음 모델 응답을 기다리기 어려운 일시적 UI를 처리합니다.
* **요소 찾기**: 접근성 계층 구조와 OCR을 결합하고, Canvas·Compose·Flutter 등 맞춤형 화면에는 시각 모델을 활용합니다.
* **공유 기록 압축**: Flash와 Pro는 이전 스크린샷을 시각적 요약으로 바꾸고 완료된 단계를 검색 가능한 기록 조각으로 압축합니다. 컨텍스트 임계값에 따라 원시 기록의 교체 시점이 결정됩니다.

<p align="center">
  <img src="./docs/assets/artemis_architecture_diagram.png" alt="ARTEMIS 시스템 구조도" width="100%" />
</p>

코드 근거, 실행 경로와 신뢰 경계는 [코드 아키텍처 분석](./docs/archify/README.md)에서 자세히 확인할 수 있습니다.

## 실행 프로필: Flash와 Pro

ARTEMIS는 자동화 작업의 성격에 따라 두 실행 프로필을 제공합니다.

* **Flash(`--profile flash`)**: 단일 모델이 화면을 관찰하고 사고·행동하는 반응형 루프입니다. 그래프 오케스트레이션 없이 단계당 약 3~5초라는 원문 기준치를 제시하며, 반복적이고 예측 가능한 UI 작업에 적합합니다. `agent.flash.max_turns=0`이면 기본적으로 단계 수 제한이 없습니다. 기록을 무한정 그대로 보유하는 대신 Pro와 공유하는 세션 기록을 시각 요약과 검색 가능한 이전 단계로 압축합니다. 세션 상대 시간 `T+mm:ss`, `search_history` / `replay_steps`, `video_analyzer`를 활용할 수 있으며, 빨리 사라지는 제어 막대나 토스트는 `click_sequence`로 여러 탭을 이어 처리합니다. **제한**: 작업 계획·메모, 실행 전 Safety Net, 체크포인트 검증, 최종 보고서, ADB 셸을 제공하지 않습니다.
* **Pro(`--profile pro`)**: 원문 기준 단계당 약 15~40초의 계획·검증 중심 다중 에이전트 그래프입니다. **Planner**가 마일스톤과 `verify` / `assert` 항목이 있는 Markdown 계획을 관리하고, **Operator**가 전체 도구로 실행합니다. Explorer의 `flash` / `pro` / `ultra` 수준은 에이전트가 임의 선택하지 않고 `config/artemis.jsonc`의 `pro.explorer.mode` / `flash.explorer_mode` 또는 `--explorer-pro-mode`를 통해 사용자가 프로필별로 지정합니다. 메모, 기록 검색, 영상 분석, ADB 진단도 사용합니다. 각 개별 행동은 XML 우선·픽셀 대체 방식의 **Safety Net**을 통과하며, 빠르게 사라지는 UI는 여러 행동을 연속 실행하는 **fast-action burst**로 처리합니다. 막히거나 실패한 행동은 **execution incident**로 Operator의 컨텍스트에 남고 이후 행동이 성공할 때까지 자체 복구를 시도합니다. 별도의 수리 에이전트는 없습니다. 읽기 전용 **Checker**는 체크포인트와 원래 목표에 대한 종료 검토를 수행합니다. `--verification-level`은 `off` / `final`(기본값) / `checkpoints` / `strict`이며, 계획 마일스톤 수정에는 참고용 검토가 붙습니다. 100단계 이상의 장기 작업, `[Loop:continuous]` 모니터링, 선택적 서면 보고를 지원합니다.

## 로드맵

- [ ] **Android Studio 통합**: IDE 안에서 디버깅, 테스트 기록, 기기 제어를 지원하는 플러그인과 작업 흐름
- [ ] **iOS 확장**: iOS 기기·시뮬레이터로 멀티모달 인식과 자동화 확대
- [ ] **기기 내 경량 VLM**: 낮은 지연과 개인정보 보호를 위한 로컬 에지 시각 모델
- [ ] **실시간 양방향 음성**: 음성 작업 전달과 실행 중 대화·중단 제어

위 항목은 현재 제공 기능이 아니라 원본 README의 계획입니다.

## 커뮤니티와 기여

기여를 환영합니다.

* 저장소에 Star를 눌러 업데이트와 릴리스를 확인할 수 있습니다.
* [Discord 커뮤니티](https://discord.gg/wF2FN4WHGY)에서 기술을 논의할 수 있습니다.
* [Issue](https://github.com/google/artemis/issues)를 등록하거나 [Pull Request](https://github.com/google/artemis/pulls)를 제출할 수 있습니다.

처음 사용한다면 [한국어 학습 가이드](./guide/README.md)에서 설치, 실행, 실습 순서로 진행하세요.

## 라이선스

이 프로젝트는 [Apache License 2.0](LICENSE)으로 배포됩니다. [Minitap, Inc.](https://github.com/minitap-ai/mobile-use)가 개발한 소스 코드가 포함되어 있습니다.
