from validate_lines import ValidateResult, validate_lines

# RED-1: 완성 격자, 대각선만 틀림 → 첫 위반 D1 또는 D2
# RED-2: 행·열만 맞고 대각선 틀림 → 검사 순서상 대각선이 첫 위반
# RED-3: 검사 순서 변경 시 회귀 실패
