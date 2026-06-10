# PRD — MagicSquare_xx (4×4, two missing numbers)

**작성일**: 2026-06-10  
**프로젝트명**: **MagicSquare_xx** (MagicSquare_1004)  
**도메인**: **4×4 Magic Square completion (two missing numbers)**  
**주 언어**: **Python 3.10+**  
**Mom Test 근거**: [`Report/01.MagicSquare_xx_STEP1_Mom_Test_Interview_Report.md`](../Report/01.MagicSquare_xx_STEP1_Mom_Test_Interview_Report.md)  
**세션 3 워크북**: [`Report/03.MagicSquare_xx_Session3_Workbook_Report.md`](../Report/03.MagicSquare_xx_Session3_Workbook_Report.md)

---

## 1. 제품 개요

### 1.1 문제 정의(요약)

- 본 제품은 4×4 격자에서 **합의된 값 집합(1~16)** 과 **규칙(불변식)** 을 만족하는 **완성된 배치**를 산출하거나, 그러한 배치의 **존재 여부를 판정**하는 문제를 다룬다.
- 빈칸은 **`0`이 정확히 2개**이며, 완성 시 **10개 합**(행 4 + 열 4 + 대각선 2)은 모두 **34**이다.
- “마방진 앱을 만든다”가 아니라, Mom Test에서 확인된 **검증 비용·첫 위반 국소화**를 **입력/출력 계약**과 **검증 가능한 불변식**으로 고정하고 **TDD**로 보호하는 학습용 시스템이다.

### 1.2 Mom Test → 제품 연결(요약)

| 관찰(과거 사실) | 제품 요구로의 번역 |
|:---|:---|
| 대각선 검사 누락·10선 확인에 **약 20분** 소모 | **행→열→대각** 고정 검사 순서 (R-05) |
| 같은 줄만 수정·어디가 틀린지 모름 | 실패 시 **첫 위반 1개**만 반환 (R-06) |
| 맞춘 뒤 **1분** 재확인·닫음·재연습 없음 | 회귀 테스트로 절차 고정 (Test Loop RED-1~3) |

### 1.3 현재 구현 범위 (세션 3)

| 포함 | 보류 |
|:---|:---|
| Rule R-01~R-06 (문서·테스트) | Solver·자동 완성 |
| Entity `validate_lines` (10선 판정) | Boundary/UI |
| Command 스켈레톤 3개 | `int[6]` 출력·조합 시도 |
| Test Loop RED-1~RED-3 | GREEN/REFACTOR 일부 |

---

## 2. 목표 / 비목표

### 2.1 목표(Goals)

- **Clean ECB layering** (boundary / control / entity)
- **TDD-first** (테스트 = 사양, 회귀 보호)
- **결정적 동작** (동일 입력 → 동일 출력)
- **10선 검증 명시** (행·열·두 대각선, 상수 34)

### 2.2 비목표(Non-goals)

- UI 스타일링·PyQt 앱
- 성능 최적화 선제 도입
- 모든 해 열거
- 퍼즐 풀이법 튜토리얼
- Mom Test **표면 문제**: “자동 완성만 있으면 된다”

---

## 3. 사용자(페르소나) 및 사용 시나리오

### 3.1 페르소나

4×4·빈칸 2·1~16·**합 34(10선)** 를 손/코드로 다루는 **소프트웨어 개발 학습자**. TDD·ECB 훈련 중.

### 3.2 핵심 사용자 여정(Journey)

1. **Mom Test** — 과거 행동·검증 비용 수집
2. **계약 정의** — 입력/출력/10선 검증 순서 확정
3. **Domain 분리** — 빈칸·누락 수·마방진 판정 분리
4. **Dual-Track TDD** — UI / Logic 병렬 RED→GREEN→REFACTOR
5. **회귀 보호** — 대각선 누락·첫 위반 시나리오 테스트 고정

---

## 4. Dual-Track TDD · Contract

### 4.1 Dual-Track 원리

| Track | Layer | 역할 |
|:---|:---|:---|
| **Logic** | entity, control | 10선 판정·조합·불변식 |
| **UI** | boundary | `message`·스키마·첫 위반 노출 |

- UI 테스트는 도메인 내부에 의존하지 않음.
- Logic 테스트는 UI를 모름.

### 4.2 UX Contract 언어 (boundary — 보류)

- 표준 `message`·`code`, **첫 위반 1개**만 노출

### 4.3 Logic Rule 언어 (control/entity)

- 허용/거부 (I-01~I-04)
- 10선 합 판정 (`validate_lines`)
- 반환/차단 (성공 `int[6]` vs `UI_UNSOLVABLE` — 후속 세션)

---

## 5. 스코프(기능 요구사항)

### 5.1 입력 계약 — 고정

- **4×4** 정수 행렬
- 셀 값: **`0` 또는 `1~16`**
- **`0` = 빈칸, 정확히 2개** (부분 입력 시)
- **`0` 제외 중복 없음**

### 5.2 출력 계약 — 고정(성공 시, 후속 세션)

- **길이 6** 정수 배열: `[r1, c1, n1, r2, c2, n2]`
- 좌표 **1-index** (1..4), **row-major** 스캔
- `n1,n2`: 누락된 두 숫자, 결정적 배정 순서 (I-10)

### 5.3 에러 계약 — 고정(실패 시, boundary — 보류)

- `error`: `{ code, message, details? }`
- **첫 위반 1개만** 반환
- **우선순위**: Shape → EmptyCount → Range → Duplicate → Unsolvable

| code | message (완전 일치) |
|:---|:---|
| `UI_INVALID_SHAPE` | `Matrix must be 4x4.` |
| `UI_INVALID_EMPTY_COUNT` | `Matrix must contain exactly 2 empty cells (0).` |
| `UI_OUT_OF_RANGE` | `Cell values must be 0 or 1..16.` |
| `UI_DUPLICATE_NON_ZERO` | `Non-zero values must be unique.` |
| `UI_UNSOLVABLE` | `No magic square completion exists for this input.` |

**Entity 주의**: entity 레이어는 E001~E005 **`code`/`message` emit 금지** — dict·bool·좌표 등 순수 계약만.

### 5.4 10선 검증 — 고정

- 완성 보드: **4행 + 4열 + 2대각선 = 10선**, 각 합 = **34**
- **검사 순서 고정**: 행(R1~R4) → 열(C1~C4) → 대각(D1↘, D2↙)
- **불일치 시 첫 위반 선 1개만** 보고 (R-06)
- **미완성**(`0` 존재): 10선 판정 **중단** → `incomplete` (§5.5)

### 5.5 Entity API — `validate_lines` (세션 3 SSOT)

**FR-VAL-01** · 구현: `src/validate_lines.py`

```python
validate_lines(grid: list[list[int]]) -> ValidateResult

ValidateResult = {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": list[str],  # 10선 라벨만
}
```

| status | 조건 | failed_lines |
|:---|:---|:---|
| `pass` | 빈칸(`0`) 없음, 10선 합 모두 34 | `[]` |
| `fail` | 빈칸 없음, 첫 위반 선 1개 | `["D1"]` 등 **1개** |
| `incomplete` | 빈칸(`0`) **1개 이상** | `[]` *(판정 중단)* |

**10선 라벨** (검사 순서 = 아래 순서):

`R1` `R2` `R3` `R4` → `C1` `C2` `C3` `C4` → `D1` `D2`

상수 SSOT: `src/constants.py` — `GRID_SIZE=4`, `MAGIC_SUM=34`, `VALUE_MIN=1`, `VALUE_MAX=16`, `LINE_LABELS`.

---

## 6. 도메인 불변식(Invariants)

### 6.1 Rule (워크북 R-01~R-06)

| ID | 내용 |
|:---|:---|
| **R-01** | Shape: 4×4 |
| **R-02** | `0` 정확히 2개 *(부분 입력)* |
| **R-03** | 값 `0` 또는 `1..16`, `0` 제외 유일 |
| **R-04** | 완성 시 10선 합 = 34 |
| **R-05** | 검사 순서: **행 → 열 → 대각선** |
| **R-06** | 불일치 시 **첫 위반 1개만** |

### 6.2 입력(Preconditions) — I-xx

| ID | 내용 |
|:---|:---|
| **I-01** | Shape: 4×4 |
| **I-02** | EmptyCount: `0` 정확히 2개 |
| **I-03** | Range: `0` 또는 `1..16` |
| **I-04** | UniqNonZero: 0 제외 중복 없음 |
| **I-05** | MissingExactly2: 누락 값 2개 (도출) |
| **I-06** | MagicConstant: 34 |
| **I-07~I-09** | RowSum / ColSum / DiagSum |
| **I-10** | DeterministicOrderRule (출력·배정) |

---

## 7. 기능 요구(FR) · Test Loop 추적

| FR ID | 요약 | Story | Test ID (세션 3) | entity 함수 |
|:---|:---|:---:|:---|:---|
| **FR-VAL-01** | 10선 검증·순서·첫 위반·incomplete | §9.4 | **RED-1**~**RED-3** | `validate_lines` |
| **FR-LOC-01** | 빈칸 2좌표 row-major 1-index | §9.2 | *(후속)* D-LOC-01 | `find_blank_coords` |
| **FR-NUM-01** | 누락 수 2개 1..16 | §9.3 | *(후속)* | `find_not_exist_nums` |
| **FR-CMD-01** | CHECK_ALL_LINE_SUMS | Command | *(후속)* | `check_all_line_sums` |
| **FR-CMD-02** | REPORT_FIRST_VIOLATION | Command | *(후속)* | `report_first_violation` |
| **FR-CMD-03** | REVERIFY_AFTER_EDIT | Command | *(후속)* | `reverify_after_edit` |

### 7.1 Test Loop RED (FR-VAL-01)

| Test ID | 시나리오 | Then (계약) |
|:---|:---|:---|
| **RED-1** | 완성 격자, **한 대각선만** 틀림 | `fail`, `failed_lines==["D1"]` 또는 `["D2"]` |
| **RED-2** | 행·열 34, 대각만 틀림 | 검사 순서상 **대각선**이 첫 위반 |
| **RED-3** | 검사 순서 변경 | 회귀 테스트 **의도적 실패** *(GREEN 이후)* |

---

## 8. 아키텍처 (ECB)

### 8.1 레이어 (현재 · 목표)

| 계층 | 현재 (`src/`) | 역할 |
|:---|:---|:---|
| **entity** | `validate_lines.py`, `constants.py` | 순수 판정·상수. I/O·print 없음 |
| **control** | `commands.py` *(스켈레톤)* | Entity 호출 순서 고정 |
| **boundary** | *(보류)* | CLI/UI — 10선·34 **중복 구현 금지** |

### 8.2 의존성

- 허용: boundary → control → entity
- 금지: entity → control/boundary

### 8.3 Command (워크북)

| Command | 전제 | 결과 |
|:---|:---|:---|
| `CHECK_ALL_LINE_SUMS` | 4×4 격자 | 10선 34 여부, 행→열→대각 순 |
| `REPORT_FIRST_VIOLATION` | 동일 | 첫 깨진 축(선 라벨 1개) |
| `REVERIFY_AFTER_EDIT` | 수정 후 | 전 축 1회 재확인 |

---

## 9. 사용자 스토리 및 AC(요약)

### 9.1 Story 1 — 입력 검증

- Logic: I-01~I-04 위반 시 거부
- UI: §5.3 `message` 완전 일치, 첫 위반 1개

### 9.2 Story 2 — 빈칸 탐색 (FR-LOC-01)

- Logic: **row-major**, **정확히 2좌표**, **1-index**

### 9.3 Story 3 — 누락 숫자

- Logic: 1..16 중 2개

### 9.4 Story 4 — 마방진 판정 (FR-VAL-01)

- Logic: **10선** 합 34, 검사 순서 **행→열→대각** 고정
- Entity: `validate_lines` — `pass` / `fail` / `incomplete`

### 9.5 Story 5 — 두 조합 시도·출력

- Logic: small/large 배정 → reverse → `int[6]` 또는 unsolvable
- *(후속 세션)*

---

## 10. 검증 계획(요약)

### 10.1 통합 시나리오(필수)

- **Mom Test 회귀**: 대각선만 틀린 완성 보드 (RED-1)
- **순서 회귀**: R-05 변경 시 테스트 실패 (RED-3)
- **incomplete**: 빈칸 존재 시 `failed_lines==[]`

### 10.2 Traceability (C2C)

- FR-VAL-01 → RED-1~RED-3
- R-05, R-06 → `validate_lines` assert
- I-06 → `MAGIC_SUM` (`constants.py`)

### 10.3 테스트 픽스처 (Given)

| ID | 설명 |
|:---|:---|
| **G0** | 완성 마방진 (`0` 없음, 10선=34) |
| **G1** | 부분 입력 (`0`×2, row-major 빈칸 (2,2)·(3,3) 1-index) |
| **G0-D1-bad** | G0에서 D1만 깨짐 (RED-1용) |

---

## 11. 비기능 요구사항(NFR)

| ID | 내용 |
|:---|:---|
| **NFR-01** | 결정성: 동일 입력 → 동일 출력 |
| **NFR-02** | 회귀: §5.4·§5.5·R-05·R-06 변경 시 테스트 실패 |
| **NFR-03** | entity E001~E005 emit 금지 |

---

## 12. 가정 / 리스크

### 12.1 가정

- 값 집합 **1..16**, 빈칸 **`0`×2**
- `pythonpath = ["src"]` (`pyproject.toml`)

### 12.2 리스크

- 10선 중 **대각선만** 테스트하지 않으면 Mom Test 사례 재발
- Boundary에 10선 판정 중복 시 ECB·회귀 붕괴

---

## 13. 문서 추적

| 문서 | 역할 |
|:---|:---|
| `docs/PRD.md` | **본 문서** — 기술 SSOT |
| `.cursorrules` | TDD·ECB·AI 작업 규칙 |
| `Report/03.MagicSquare_xx_Session3_Workbook_Report.md` | 세션 3 Rule·Command·RED |
| `docs/RED_TODO.md` | *(예정)* Dual-Track RED 체크리스트 |

---

*본 PRD는 Mom Test·세션 3 워크북·현재 `src/` 스켈레톤을 반영한 SSOT이다. RED 상세 진행은 `/red-test-plan` → `/red-skeleton` 파이프라인을 따른다.*
