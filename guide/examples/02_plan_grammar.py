# SPDX-License-Identifier: Apache-2.0
"""Pro 계획의 기계 문법을 실제 저장소 파서로 읽는 오프라인 실습.

목표: checkbox 상태, 활성 milestone, verify/assert와 연속 루프를 구분한다.
실행: 저장소 루트에서 ``python guide/examples/02_plan_grammar.py``
예상: 첫째 milestone 완료, 둘째 활성, check 3개, 연속 루프 1개.
이유: 장치·LLM을 띄우지 않고 핵심 순수 로직만 로드해 재현성을 확보한다.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[2]
PARSER_PATH = REPO_ROOT / "artemis" / "utils" / "plan_grammar.py"


def load_pure_parser() -> ModuleType:
    """`artemis` 패키지 초기화 없이 독립적인 표준 라이브러리 파서만 로드한다."""
    spec = importlib.util.spec_from_file_location("artemis_learning_plan_grammar", PARSER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"계획 파서를 찾지 못했습니다: {PARSER_PATH}")
    module = importlib.util.module_from_spec(spec)
    # dataclass가 정의 시 모듈 네임스페이스를 조회하므로 먼저 등록한다.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    grammar = load_pure_parser()
    sample = """- [x] 사전 진단
  - verify: Android 기기가 승인 상태다
- [/] 테스트 앱의 읽기 전용 화면 확인
  - assert: 원하는 정보가 화면에 표시된다
- [ ] [Loop:continuous] 명시적 종료 신호까지 관찰
- assert@end: 종료 시 최종 화면의 근거가 있다
"""

    snapshot = grammar.parse_plan(sample)
    active = snapshot.active_milestone()
    continuous = snapshot.continuous_top_level

    # 자료의 의미를 코드로 확인한다. 사소한 출력 차이보다 파서 계약을 검증한다.
    assert len(snapshot.top_level) == 3
    assert active is not None and active.status == "/"
    assert len(snapshot.check_items) == 3
    assert len(continuous) == 1
    assert snapshot.all_top_level_done is False

    print("Top-level 상태:")
    for item in snapshot.top_level:
        print(f"  [{item.status}] {item.text}")
    print(f"활성 milestone: {active.text}")
    print(f"검증/주장 항목: {len(snapshot.check_items)}개")
    print(f"연속 루프: {len(continuous)}개")
    print("전체 완료: 아니요 (대기 중인 milestone이 남아 있음)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
