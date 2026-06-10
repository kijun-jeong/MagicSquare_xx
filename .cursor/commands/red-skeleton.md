# RED Skeleton — ARRR A단계 (RED ④)

[`/red-test-plan`](red-test-plan.md) 설계표 기준 **`pytest.fail` 스켈레톤만** 작성하는 커맨드.  
`tests/`만 수정한다. `src/`는 **건드리지 않는다.**  
다음 단계: `/green-minimal` — `pytest.fail` 제거 후 최소 GREEN.

**Skill 참조:** **magic-square-tdd Skill이 있으면 자동 따른다**.

---

## Phase 선언

```
Phase: red | Layer: {entity|boundary} | Track: {Logic|UI}
```

---

## AAA 절차

- `# Given` / `# When` / `# Then` 주석 필수
- Then = `pytest.fail("RED: {Test ID} — …")` **한 줄만**
- assert 본문·skip·xfail·통과 더미 **금지**

---

## 상수·import

- `from constants import GRID_SIZE, MAGIC_SUM, VALUE_MAX`
- Domain Mock **금지**

---

## conftest

`tests/conftest.py` — `grid_g1` (0×2, row-major)

---

## 완료 보고

pytest **FAIL** 확인 · Test ID · 변경 파일(`tests/`만)

---

## 파이프라인

```
/red-test-plan  →  /red-skeleton  →  /green-minimal
                    RED ④
```
