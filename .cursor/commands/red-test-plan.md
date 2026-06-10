# RED Test Plan — ARRR A단계 (Ask = RED ③)

**C2C 설계표·테스트 플랜만** 작성하는 커맨드.  
`tests/`·`src/` **파일을 생성·수정하지 않는다.**  
다음 단계: [`/red-skeleton`](red-skeleton.md) — RED 스켈레톤·픽스처 작성.

**SSOT (반드시 먼저 읽기)**

| 문서 | 용도 |
|:---|:---|
| [`.cursorrules`](../../.cursorrules) | 도메인·10선·34·ECB·TDD 금지 |
| [`docs/PRD.md`](../../docs/PRD.md) | FR·입출력·에러·ECB 계약 |
| [`docs/RED_TODO.md`](../../docs/RED_TODO.md) | *(있으면)* D-*/U-* 진행·픽스처 G0~G8 |
| [`Report/03.MagicSquare_xx_Session3_Workbook_Report.md`](../../Report/03.MagicSquare_xx_Session3_Workbook_Report.md) | 세션 주제·Rule·RED 시나리오 |
| 채팅 맥락 | 이번 RED 묶음·Test ID·Layer 힌트 |

---

## 트리거

사용자가 **`/red-test-plan`만** 입력해도 동작한다.  
추가 인자가 없으면 아래를 **자동 추출**한다.

| 추출 항목 | 우선순위 |
|:---|:---|
| **세션 주제** | 채팅 최근 턴 → 워크북 Report → PRD §1·§9 |
| **RED 묶음 / Test ID** | 채팅 명시 → `RED_TODO` 체크 항목 → PRD FR 매핑 |
| **Layer** | 채팅 `entity`/`boundary` → 없으면 **entity** (Logic Track 기본) |
| **Track** | Layer=entity → **Logic** · Layer=boundary → **UI** |

명시적 오버라이드 예: `Phase: red | Layer: entity | Track: Logic` · `이번 RED 묶음: D-LOC-01 (FR-LOC-01)`

---

## Phase 선언

응답 **첫 줄**에 반드시 쓴다:

```
Phase: red | Layer: {entity|boundary} | Track: {Logic|UI}
```

이어서 **이번 RED 묶음**을 한 줄로 적는다 (예: `RED 묶음: RED-1~RED-3 — validate_lines 대각선 첫 위반`).

---

## 역할 (ARRR · A단계)

| 항목 | 내용 |
|:---|:---|
| **ARRR** | **A**sk — RED ③ (설계·플랜만, 코드 없음) |
| **산출** | C2C 추적표 · Track 설계표 · 테스트 플랜 · ECB·Mock 점검 |
| **다음** | `/red-skeleton` — `tests/` 스켈레톤·conftest만 |

---

## C2C Rule 1~3 (고정)

| Rule | 내용 |
|:---|:---|
| **Rule 1** | PRD **FR**마다 최소 **1개 Test ID** (또는 RED 묶음 1건) |
| **Rule 2** | assert·Then은 **계약만** — 구현 세부·E00x `message`·UI 문구 금지 |
| **Rule 3** | 설계표·플랜에 **FR ID**와 **Test ID**를 명시해 추적 가능하게 |

---

## 출력 4블록 (표 형식 필수)

아래 **4개 섹션을 순서대로** 표로 작성한다. 파일 생성 없이 **채팅 응답만**.

### 블록 1 — C2C (Rule 1~3)

1. **PRD FR 인용** — `docs/PRD.md`에서 해당 FR 문장·§번호 인용 (없으면 §합성 근거 표기)
2. **To-Do 1개** — 판단이 필요한 항목만 (`[ ]` 체크박스 1행)
3. **Test ID → Given / When / Then** 표

### 블록 2 — Track 설계표

**Logic Track (Layer: entity)** — Track B:

| Test ID | 대상 함수 | Given→Then | Invariant | Expected RED Failure |
|:---|:---|:---|:---|:---|

**UI Track (Layer: boundary)** — Track A:  
동일 커맨드에서 **Layer만 `boundary`로 바꾸면 재사용**한다.

### 블록 3 — 테스트 플랜

| 항목 | 내용 |
|:---|:---|
| **파일 경로** | 예: `tests/test_validate_lines.py` |
| **test 함수명 후보** | RED 묶음당 1함수 권장 |
| **conftest 픽스처** | G0~G8 또는 `grid_g1` 등 — **데이터만** |
| **pytest 명령** | 노드 1개 지정 |
| **RED 묶음 범위** | 이번 턴 Test ID 목록 |

### 블록 4 — ECB·Mock 점검

Logic Track: Domain Mock **금지**, entity E001~E005 emit **금지**.

---

## MagicSquare_xx 기본 맥락 (자동 추출 실패 시 폴백)

| 항목 | 기본값 |
|:---|:---|
| Entity API | `validate_lines(grid) -> {"status", "failed_lines"}` |
| 10선 순서 | R1~R4 → C1~C4 → D1·D2 |
| 마법상수 | 34 |
| RED 우선 | 완성 격자·대각선만 틀림 → `failed_lines` 첫 위반 `D1`/`D2` |
| incomplete | `0` 존재 → `status=="incomplete"`, `failed_lines==[]` |

---

## 금지

`src/` 수정 · `tests/` 생성 · GREEN/REFACTOR · skip/xfail

---

## 완료 보고

```
/red-skeleton 으로 넘길 준비됐다
```

---

## 파이프라인 위치

```
/red-test-plan  →  /red-skeleton  →  /green-minimal  →  (REFACTOR)
   RED ③ Ask          RED ④            GREEN
```
