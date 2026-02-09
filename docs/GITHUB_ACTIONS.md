# GitHub Actions 설정 가이드

## 1. Repository Secrets 설정

GitHub 저장소에 API 키를 안전하게 저장하세요.

### 1.1 Secrets 추가 방법
1. GitHub 저장소 페이지로 이동
2. **Settings** 탭 클릭
3. 왼쪽 메뉴에서 **Secrets and variables** > **Actions** 클릭
4. **New repository secret** 버튼 클릭

### 1.2 필수 Secrets

다음 Secrets를 추가하세요:

| Secret Name | 설명 | 예시 |
|-------------|------|------|
| `ANTHROPIC_API_KEY` | Claude API 키 | `sk-ant-xxxxx` |
| `REPLICATE_API_TOKEN` | Replicate API 토큰 | `r8_xxxxx` |

### 1.3 옵션 Secrets (Instagram 포스팅용)

| Secret Name | 설명 |
|-------------|------|
| `FAL_KEY` | Fal.ai API 키 (옵션) |
| `INSTAGRAM_ACCESS_TOKEN` | Instagram Access Token |
| `INSTAGRAM_USER_ID` | Instagram User ID |

## 2. 워크플로우 파일 확인

`.github/workflows/daily-webtoon.yml` 파일이 저장소에 있는지 확인하세요.

```bash
git add .github/workflows/daily-webtoon.yml
git commit -m "Add GitHub Actions workflow"
git push
```

## 3. 워크플로우 테스트

### 3.1 수동 실행
1. GitHub 저장소의 **Actions** 탭으로 이동
2. 왼쪽에서 **Daily Webtoon Generator** 워크플로우 선택
3. **Run workflow** 버튼 클릭
4. 주제와 스타일 입력 (옵션)
5. **Run workflow** 클릭

### 3.2 실행 확인
- 워크플로우가 실행되면 실시간으로 로그를 볼 수 있습니다
- 각 단계의 성공/실패 여부를 확인하세요
- 생성된 웹툰은 Artifacts에서 다운로드할 수 있습니다

## 4. 자동 스케줄링

워크플로우는 매일 **UTC 00:00** (한국 시간 오전 9시)에 자동 실행됩니다.

### 4.1 스케줄 변경
`.github/workflows/daily-webtoon.yml` 파일의 `cron` 값을 수정:

```yaml
on:
  schedule:
    # 매일 UTC 00:00 (KST 09:00)
    - cron: '0 0 * * *'
```

**Cron 표현식 예시:**
- `0 0 * * *` - 매일 UTC 00:00
- `0 12 * * *` - 매일 UTC 12:00 (KST 21:00)
- `0 0 * * 1` - 매주 월요일 UTC 00:00
- `0 0 1 * *` - 매월 1일 UTC 00:00

## 5. 문제 해결

### Q: "ANTHROPIC_API_KEY not found" 오류
A: Repository Secrets에 API 키가 올바르게 설정되었는지 확인하세요.

### Q: 워크플로우가 실행되지 않음
A: 
1. `.github/workflows/` 디렉토리가 저장소 루트에 있는지 확인
2. YAML 파일 문법 오류가 없는지 확인
3. Actions 탭에서 워크플로우가 활성화되어 있는지 확인

### Q: 이미지 생성 실패
A: Replicate API 크레딧이 충분한지 확인하세요.

### Q: 데이터베이스 커밋 실패
A: GitHub Actions에 write 권한이 있는지 확인:
   - Settings > Actions > General > Workflow permissions
   - "Read and write permissions" 선택

## 6. 고급 설정

### 6.1 알림 설정
워크플로우 실패 시 자동으로 Issue가 생성됩니다.

### 6.2 Artifacts 보관
생성된 웹툰은 30일간 보관됩니다. 기간 변경:

```yaml
- name: Upload webtoon artifacts
  uses: actions/upload-artifact@v3
  with:
    retention-days: 90  # 90일로 변경
```

### 6.3 병렬 실행
여러 주제를 동시에 생성하려면 matrix strategy 사용:

```yaml
strategy:
  matrix:
    topic: ["직장인 공감", "개발자 일상", "육아맘 일상"]
```

## 7. 비용 관리

### GitHub Actions 무료 한도
- Public 저장소: 무료 무제한
- Private 저장소: 월 2,000분 무료

### 예상 사용량
- 1회 실행: 약 5-10분
- 일일 1회: 월 150-300분
- **결론: 무료 한도 내에서 충분히 사용 가능**

## 8. 다음 단계

1. ✅ Secrets 설정 완료
2. ✅ 워크플로우 수동 실행 테스트
3. ✅ 자동 스케줄링 확인
4. 🎯 Instagram 연동 (옵션)
5. 🎯 분석 대시보드 구축
