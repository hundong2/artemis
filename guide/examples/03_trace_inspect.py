# SPDX-License-Identifier: Apache-2.0
"""MCP trace 상태를 읽기 전용·민감정보 비노출 방식으로 점검한다.

목표: status.json의 핵심 상태와 종료 시점을 해석한다.
실행: ``python guide/examples/03_trace_inspect.py``
실제 자료: ``python guide/examples/03_trace_inspect.py --status <status.json 경로>``
예상: 기본 합성 trace는 completed, 소요 3.5초, 결과 존재로 표시된다.
이유: task_desc, error, result, device_serial은 화면 내용이나 개인정보일 수 있어 출력하지 않는다.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


TERMINAL = {"completed", "failed", "cancelled"}
SAMPLE: dict[str, Any] = {
    "trace_id": "sample-offline-trace",
    "task_desc": "합성 읽기 전용 작업",
    "model": "Flash",
    "status": "completed",
    "device_serial": "synthetic-device",
    "start_time": 1000.0,
    "end_time": 1003.5,
    "error": None,
    "result": {"synthetic": True},
}


def summarize(data: dict[str, Any]) -> dict[str, Any]:
    trace_id = data.get("trace_id")
    status = data.get("status")
    if not isinstance(trace_id, str) or not trace_id:
        raise ValueError("trace_id가 없는 상태 파일입니다")
    if not isinstance(status, str) or not status:
        raise ValueError("status가 없는 상태 파일입니다")

    start = data.get("start_time")
    end = data.get("end_time")
    elapsed = None
    if isinstance(start, (int, float)) and isinstance(end, (int, float)):
        if end < start:
            raise ValueError("end_time이 start_time보다 빠릅니다")
        elapsed = round(end - start, 3)

    # 원본의 민감한 문자열을 전달하지 않고, 필드 존재 여부만 요약한다.
    return {
        "trace_id": trace_id,
        "status": status,
        "terminal": status in TERMINAL,
        "duration_seconds": elapsed,
        "has_error": bool(data.get("error")),
        "has_result": data.get("result") is not None,
        "device_assigned": bool(data.get("device_serial")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", type=Path, help="실제 status.json 경로; 생략 시 합성 자료 사용")
    args = parser.parse_args()
    try:
        if args.status is None:
            data = SAMPLE
            print("합성 오프라인 trace를 사용합니다.")
        else:
            # 읽기 전용: trace_store의 쓰기·격리 로직을 호출하지 않는다.
            data = json.loads(args.status.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("최상위 JSON 값은 객체여야 합니다")
        print(json.dumps(summarize(data), ensure_ascii=False, indent=2))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        # 오류 객체를 그대로 출력하면 경로나 본문이 새어 나갈 수 있어 유형만 표시한다.
        print(f"상태 파일을 검사하지 못했습니다: {type(exc).__name__}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
