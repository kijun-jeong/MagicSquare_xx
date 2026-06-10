# TDD RED — validate_lines

`validate_lines` Entity의 **RED 단계 전용** 커맨드.  
`tests/`만 수정한다. `src/`는 건드리지 않는다.

---

## Phase 선언

응답 **첫 줄**에 반드시 쓴다:

```
Phase: RED
```

이어서 이번 RED가 다루는 시나리오를 한 줄로 적는다 (예: `RED-1: 완성 격자, D1만 틀림`).

---

## 대상

| 항목 | 내용 |
|:---|:---|
| **함수** | `validate_lines(grid) -> ValidateResult` |
| **파일** | `tests/test_validate_lines.py` *(필요 시 `tests/` 보조 모듈)* |
| **API** | `{"status": "pass"\|"fail"\|"incomplete", "failed_lines": [...]}` |
| **10선** | `R1`~`R4` → `C1`~`C4` → `D1`·`D2` (검사 순서 고정) |

---

## AAA 절차

각 테스트는 **Arrange → Act → Assert** 순으로 작성한다.

1. **Arrange** — 4×4 격자를 만든다. `0`=빈칸, 채운 값 `1~16`. 시나리오 의도를 주석으로 남긴다.
2. **Act** — `result = validate_lines(grid)` 한 번만 호출한다.
3. **Assert** — `result["status"]`와 `result["failed_lines"]`를 **엄격히** 검증한다. 첫 위반 1개만 기대할 때는 길이·라벨을 모두 단언한다.

RED가 끝나면 `pytest`가 **실패**해야 한다. 통과하면 테스트가 약하거나 구현이 이미 들어간 것이다.

---

## RED 시나리오 우선순위

| ID | 시나리오 | 기대 |
|:---|:---|:---|
| **RED-1** | 완성 격자, **대각선만** 틀림 | `status=="fail"`, `failed_lines==["D1"]` 또는 `["D2"]` |
| **RED-2** | 행·열 합은 34, 대각선만 틀림 | 검사 순서상 **대각선**이 첫 위반 |
| **RED-3** | `incomplete` — 빈칸(`0`) 존재 | `status=="incomplete"`, `failed_lines==[]` |
| **RED-4** | 완성 격자, 행이 먼저 틀림 | `failed_lines==["R1"]` 등 **첫 행** 1개만 |
| **RED-5** | *(GREEN 이후)* 검사 순서 변경 시 회귀 | 순서 바꾸면 테스트 **실패** *(RED 단계에서는 주석·스켈레톤만)* |

한 번에 **하나의 행동**만 검증한다. 여러 축을 한 테스트에 섞지 않는다.

---

## pytest 예시

```python
from validate_lines import validate_lines

# RED-1: 완성 격자, D1(↘)만 합 ≠ 34
def test_fail_reports_first_diagonal_violation_d1():
    # Arrange — 행·열·D2는 34, D1만 깨짐
    grid = [
        [16,  2,  3, 13],
        [ 5, 11, 10,  8],
        [ 9,  7,  6, 12],
        [ 4, 14, 15,  1],
    ]
    grid[0][0] = 99  # D1 합만 틀리게

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert result["failed_lines"] == ["D1"]


def test_incomplete_when_blank_exists():
    # Arrange — 빈칸 1개
    grid = [
        [16,  2,  3, 13],
        [ 5, 11, 10,  8],
        [ 9,  7,  6, 12],
        [ 4, 14,  0,  1],
    ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []
```

실행:

```bash
pytest tests/test_validate_lines.py -v
```

기대 결과: **FAILED** (구현이 `...`이거나 없으므로).

---

## 금지

| 금지 | 이유 |
|:---|:---|
| `src/` 수정 (`validate_lines.py`, `commands.py` 등) | RED는 테스트만 |
| assert 완화 (`==` → `in`, `>=`, truthy만 검사) | 요구사항 흐림 |
| `@pytest.mark.skip`, `xfail` | RED 회피 |
| 실패 테스트 삭제·이름 변경으로 우회 | 회귀 보호 무력화 |
| `failed_lines`에 복수 라벨 기대 | R-06 위반 — 첫 위반 1개만 |
| Solver·UI·Command 구현을 RED에 끼워 넣기 | Entity 범위 밖 |

---

## 보고 형식

RED 작업 완료 후 아래 형식으로 보고한다.

```markdown
Phase: RED

## 요약
- 시나리오: RED-N — (한 줄 설명)
- 수정 파일: tests/test_validate_lines.py

## 추가한 테스트
| 테스트 함수 | Arrange 요지 | Assert 기대 |
|:---|:---|:---|
| test_... | ... | status=..., failed_lines=[...] |

## pytest 결과
- 명령: `pytest tests/test_validate_lines.py -v`
- 결과: N failed, M passed *(전부 failed여도 RED 성공)*

## 다음 단계
- GREEN: `src/validate_lines.py` 최소 구현
```

---

## 체크리스트

- [ ] 응답 첫 줄 `Phase: RED`
- [ ] `tests/`만 변경
- [ ] AAA 주석 또는 빈 줄로 구역 구분
- [ ] `pytest` 실행 결과 **실패** 확인
- [ ] assert 완화·skip·xfail 없음
