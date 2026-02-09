# 빠른 GitHub 배포 가이드 (Git 없이)

Git이 설치되어 있지 않은 경우, 다음 두 가지 방법 중 하나를 선택하세요:

## 방법 1: GitHub Desktop 사용 (추천) ⭐

### 1.1 GitHub Desktop 설치
1. https://desktop.github.com/ 접속
2. **Download for Windows** 클릭
3. 다운로드 후 설치

### 1.2 저장소 생성 및 푸시
1. GitHub Desktop 실행
2. **File** > **Add local repository**
3. 경로 선택: `C:\Users\maee7\Desktop\workspace\연구자동화에이전트들\ai-webtoon-service`
4. **Create a repository** 클릭 (저장소가 없다고 나오면)
5. 왼쪽 하단에서 변경사항 확인
6. Summary 입력: `Initial commit: AI webtoon service`
7. **Commit to main** 클릭
8. 상단 **Publish repository** 클릭
9. Repository name: `ai-webtoon-service`
10. **Publish repository** 클릭

✅ 완료! 이제 GitHub에 코드가 업로드되었습니다.

---

## 방법 2: GitHub 웹 인터페이스 사용

### 2.1 저장소 생성
1. https://github.com/new 접속
2. Repository name: `ai-webtoon-service`
3. **Create repository** 클릭

### 2.2 파일 업로드
1. 생성된 저장소 페이지에서 **uploading an existing file** 클릭
2. 탐색기에서 `ai-webtoon-service` 폴더의 모든 파일 선택
3. 드래그 앤 드롭으로 업로드
4. Commit message: `Initial commit`
5. **Commit changes** 클릭

⚠️ **주의**: `.env` 파일은 업로드하지 마세요! (API 키 포함)

---

## 다음 단계: Repository Secrets 설정

### 3.1 Secrets 페이지 접속
1. GitHub 저장소 페이지로 이동
2. **Settings** 탭 클릭
3. 왼쪽 메뉴: **Secrets and variables** > **Actions**
4. **New repository secret** 클릭

### 3.2 필수 Secrets 추가

로컬 `.env` 파일을 열어서 값을 복사하세요:

#### Secret 1: ANTHROPIC_API_KEY
- Name: `ANTHROPIC_API_KEY`
- Secret: `.env` 파일의 `ANTHROPIC_API_KEY` 값
- **Add secret** 클릭

#### Secret 2: REPLICATE_API_TOKEN
- Name: `REPLICATE_API_TOKEN`
- Secret: `.env` 파일의 `REPLICATE_API_TOKEN` 값
- **Add secret** 클릭

#### Secret 3: INSTAGRAM_ACCESS_TOKEN (옵션)
- Name: `INSTAGRAM_ACCESS_TOKEN`
- Secret: `.env` 파일의 `INSTAGRAM_ACCESS_TOKEN` 값
- **Add secret** 클릭

#### Secret 4: INSTAGRAM_USER_ID (옵션)
- Name: `INSTAGRAM_USER_ID`
- Secret: `.env` 파일의 `INSTAGRAM_USER_ID` 값
- **Add secret** 클릭

---

## GitHub Actions 권한 설정

### 4.1 Workflow 권한
1. Settings > Actions > General
2. **Workflow permissions** 섹션:
   - ✅ **Read and write permissions** 선택
3. **Save** 클릭

---

## GitHub Actions 워크플로우 테스트

### 5.1 수동 실행
1. 저장소의 **Actions** 탭으로 이동
2. 왼쪽: **Daily Webtoon Generator** 선택
3. **Run workflow** 버튼 클릭
4. 입력:
   - 웹툰 주제: `개발자 일상`
   - 웹툰 스타일: `유머`
5. **Run workflow** 클릭

### 5.2 실행 확인
- 실시간 로그 확인
- 각 단계 성공 여부 확인
- 완료 후 **Artifacts**에서 웹툰 다운로드

---

## 체크리스트

- [ ] GitHub Desktop 설치 또는 웹 업로드 완료
- [ ] 코드가 GitHub에 업로드됨
- [ ] Repository Secrets 설정 (최소 2개)
- [ ] Workflow permissions 설정
- [ ] 수동 워크플로우 실행 성공
- [ ] 생성된 웹툰 확인

---

## 문제 해결

### Q: GitHub Desktop에서 "repository not found" 오류
**A**: 폴더를 직접 선택하지 말고, GitHub Desktop에서 "Create a repository" 선택

### Q: 웹 업로드 시 파일이 너무 많음
**A**: 
1. 필수 파일만 업로드:
   - `src/` 폴더
   - `.github/` 폴더
   - `docs/` 폴더
   - `scripts/` 폴더
   - `requirements.txt`
   - `README.md`
   - `.env.example`
   - `.gitignore`

### Q: Actions 탭에 워크플로우가 없음
**A**: `.github/workflows/daily-webtoon.yml` 파일이 업로드되었는지 확인

---

## 완료 후

✅ 설정이 완료되면:
- 매일 오전 9시 자동으로 웹툰 생성
- Actions 탭에서 실행 기록 확인
- Artifacts에서 웹툰 다운로드

🎉 **서비스 운영 시작!**
