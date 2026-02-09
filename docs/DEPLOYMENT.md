# GitHub 저장소 생성 및 배포 가이드

## 1. GitHub 저장소 생성

### 웹 인터페이스 사용
1. https://github.com/new 접속
2. Repository name: `ai-webtoon-service` (또는 원하는 이름)
3. Description: `AI-powered automated webtoon generation and Instagram posting service`
4. Public 또는 Private 선택
5. **Initialize this repository with a README 체크 해제** (이미 로컬에 있음)
6. **Create repository** 클릭

### 저장소 URL 복사
생성 후 나오는 URL을 복사하세요:
```
https://github.com/YOUR_USERNAME/ai-webtoon-service.git
```

## 2. 로컬 저장소와 연결

```bash
cd ai-webtoon-service

# GitHub 저장소 연결
git remote add origin https://github.com/YOUR_USERNAME/ai-webtoon-service.git

# 코드 푸시
git branch -M main
git push -u origin main
```

## 3. Repository Secrets 설정

### 3.1 Secrets 페이지 접속
1. GitHub 저장소 페이지로 이동
2. **Settings** 탭 클릭
3. 왼쪽 메뉴에서 **Secrets and variables** > **Actions** 클릭

### 3.2 필수 Secrets 추가

**New repository secret** 버튼을 클릭하여 다음 Secrets를 추가:

#### ANTHROPIC_API_KEY
- Name: `ANTHROPIC_API_KEY`
- Secret: `.env` 파일의 `ANTHROPIC_API_KEY` 값 복사

#### REPLICATE_API_TOKEN
- Name: `REPLICATE_API_TOKEN`
- Secret: `.env` 파일의 `REPLICATE_API_TOKEN` 값 복사

### 3.3 옵션 Secrets (Instagram 포스팅용)

#### INSTAGRAM_ACCESS_TOKEN
- Name: `INSTAGRAM_ACCESS_TOKEN`
- Secret: `.env` 파일의 `INSTAGRAM_ACCESS_TOKEN` 값 복사

#### INSTAGRAM_USER_ID
- Name: `INSTAGRAM_USER_ID`
- Secret: `.env` 파일의 `INSTAGRAM_USER_ID` 값 복사

#### FAL_KEY (Flux Pro 사용 시)
- Name: `FAL_KEY`
- Secret: `.env` 파일의 `FAL_KEY` 값 복사

## 4. GitHub Actions 권한 설정

### 4.1 Workflow 권한 설정
1. Settings > Actions > General
2. **Workflow permissions** 섹션에서:
   - ✅ **Read and write permissions** 선택
   - ✅ **Allow GitHub Actions to create and approve pull requests** 체크
3. **Save** 클릭

이 설정은 워크플로우가 데이터베이스를 커밋할 수 있도록 합니다.

## 5. GitHub Actions 워크플로우 테스트

### 5.1 수동 실행
1. 저장소의 **Actions** 탭으로 이동
2. 왼쪽에서 **Daily Webtoon Generator** 워크플로우 선택
3. **Run workflow** 버튼 클릭
4. 입력 필드:
   - **웹툰 주제**: `개발자 일상` (또는 원하는 주제)
   - **웹툰 스타일**: `유머` (또는 원하는 스타일)
5. **Run workflow** 클릭

### 5.2 실행 모니터링
- 워크플로우가 시작되면 실시간 로그를 볼 수 있습니다
- 각 단계별 진행 상황 확인:
  - ✅ Checkout code
  - ✅ Set up Python
  - ✅ Install dependencies
  - ✅ Run webtoon pipeline
  - ✅ Upload webtoon artifacts

### 5.3 결과 확인
1. 워크플로우 완료 후 **Summary** 페이지로 이동
2. **Artifacts** 섹션에서 생성된 웹툰 다운로드
3. `webtoons-{run_number}.zip` 파일 확인

## 6. 자동 스케줄링 확인

워크플로우는 매일 **UTC 00:00** (한국 시간 오전 9시)에 자동 실행됩니다.

### 스케줄 변경 (옵션)
`.github/workflows/daily-webtoon.yml` 파일 수정:

```yaml
on:
  schedule:
    # 원하는 시간으로 변경
    - cron: '0 12 * * *'  # UTC 12:00 (KST 21:00)
```

## 7. 문제 해결

### Q: "ANTHROPIC_API_KEY not found" 오류
**A**: Repository Secrets가 올바르게 설정되었는지 확인
- Secret 이름이 정확한지 확인 (대소문자 구분)
- Secret 값에 공백이 없는지 확인

### Q: 워크플로우가 실행되지 않음
**A**: 
1. `.github/workflows/daily-webtoon.yml` 파일이 main 브랜치에 있는지 확인
2. YAML 문법 오류가 없는지 확인
3. Actions 탭에서 워크플로우가 활성화되어 있는지 확인

### Q: "Permission denied" 오류
**A**: Workflow permissions 설정 확인
- Settings > Actions > General
- "Read and write permissions" 선택

### Q: 이미지 생성 실패
**A**: 
1. Replicate API 크레딧 확인
2. API 토큰이 유효한지 확인
3. 네트워크 연결 확인

## 8. 성공 확인 체크리스트

- [ ] GitHub 저장소 생성 완료
- [ ] 코드 푸시 완료
- [ ] Repository Secrets 설정 완료 (최소 2개)
- [ ] Workflow permissions 설정 완료
- [ ] 수동 워크플로우 실행 성공
- [ ] Artifacts 다운로드 및 확인
- [ ] 자동 스케줄링 설정 확인

## 9. 다음 단계

✅ 모든 설정이 완료되면:
1. 매일 자동으로 웹툰이 생성됩니다
2. Artifacts에서 다운로드 가능
3. 데이터베이스가 자동으로 업데이트됩니다
4. 실패 시 자동으로 Issue가 생성됩니다

🎯 **서비스 운영 시작!**
