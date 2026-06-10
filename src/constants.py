"""도메인 상수 — 4×4 마방진, 10선 라벨, 마법상수."""

GRID_SIZE = 4
MAGIC_SUM = 34
BLANK = 0
VALUE_MIN = 1
VALUE_MAX = 16

# 검사 순서 고정: 행 → 열 → 대각선
LINE_LABELS: tuple[str, ...] = (
    "R1", "R2", "R3", "R4",
    "C1", "C2", "C3", "C4",
    "D1", "D2",
)
