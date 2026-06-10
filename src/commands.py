"""Command: Entity 호출 절차 — CHECK_ALL_LINE_SUMS / REPORT_FIRST_VIOLATION / REVERIFY_AFTER_EDIT."""

from validate_lines import ValidateResult


def check_all_line_sums(matrix: list[list[int]]) -> ValidateResult:
    """CHECK_ALL_LINE_SUMS — 10선 34 여부, 행→열→대각 순 실행."""
    ...


def report_first_violation(matrix: list[list[int]]) -> ValidateResult:
    """REPORT_FIRST_VIOLATION — 첫 깨진 축(선 라벨 1개)만 보고."""
    ...


def reverify_after_edit(matrix: list[list[int]]) -> ValidateResult:
    """REVERIFY_AFTER_EDIT — 수정 후 전 축 1회 재확인."""
    ...
