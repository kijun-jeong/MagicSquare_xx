# TDD RED — validate_lines

`validate_lines` Entity의 **RED 단계 전용** 커맨드.  
`tests/`만 수정한다. `src/`는 건드리지 않는다.

---

## Phase 선언

```
Phase: RED
```

---

## RED 시나리오 우선순위

| ID | 시나리오 | 기대 |
|:---|:---|:---|
| **RED-1** | 완성 격자, **대각선만** 틀림 | `status=="fail"`, `failed_lines==["D1"]` 또는 `["D2"]` |
| **RED-2** | 행·열 합은 34, 대각선만 틀림 | 검사 순서상 **대각선**이 첫 위반 |
| **RED-3** | `incomplete` — 빈칸(`0`) 존재 | `status=="incomplete"`, `failed_lines==[]` |

---

## 금지

`src/` 수정 · assert 완화 · skip/xfail · Solver·UI·Command RED 끼워넣기
