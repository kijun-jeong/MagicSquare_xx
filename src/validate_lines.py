"""Entity: 10선 합 검증. 격자만 받고 dict 반환 (I/O·UI 없음)."""

from typing import Literal, TypedDict


class ValidateResult(TypedDict):
    status: Literal["pass", "fail", "incomplete"]
    failed_lines: list[str]


def validate_lines(grid: list[list[int]]) -> ValidateResult:
    """4×4 격자의 10선(행→열→대각) 합을 검사한다.

    - pass: 빈칸 없음, 10선 합 모두 34
    - fail: 빈칸 없음, 첫 위반 선 1개를 failed_lines에 담음 (예: ["D1"])
    - incomplete: 빈칸(0) 존재, failed_lines는 []
    """
    ...
