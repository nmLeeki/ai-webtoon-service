# AI 웹툰 서비스 설치 가이드

## 1. 사전 요구사항

- Python 3.10 이상
- Git
- Instagram 비즈니스 계정 (포스팅용)

## 2. 설치 단계

### 2.1 저장소 클론
```bash
git clone <your-repo-url>
cd ai-webtoon-service
```

### 2.2 Python 패키지 설치
```bash
pip install -r requirements.txt
```

### 2.3 환경 변수 설정

`.env` 파일 생성:
```bash
cp .env.example .env
```

`.env` 파일 편집:
```env
# API Keys
ANTHROPIC_API_KEY=sk-ant-xxxxx
REPLICATE_API_TOKEN=r8_xxxxx
FAL_KEY=xxxxx  # 옵션

# Instagram (옵션)
INSTAGRAM_ACCESS_TOKEN=xxxxx
INSTAGRAM_USER_ID=xxxxx

# Database
DATABASE_PATH=data/database.db

# Image Generation
IMAGE_GENERATOR=replicate  # replicate or fal
```

### 2.4 API 키 발급

#### Claude API
1. https://console.anthropic.com/ 접속
2. API Keys 메뉴에서 새 키 생성
3. `.env`에 `ANTHROPIC_API_KEY` 설정

#### Replicate API
1. https://replicate.com/ 가입
2. Account Settings > API Tokens
3. `.env`에 `REPLICATE_API_TOKEN` 설정

#### Fal.ai (옵션)
1. https://fal.ai/ 가입
2. API 키 발급
3. `.env`에 `FAL_KEY` 설정

## 3. Instagram 설정 (옵션)

### 3.1 Instagram 비즈니스 계정 전환
1. Instagram 앱에서 설정 > 계정 > 프로페셔널 계정으로 전환
2. 비즈니스 또는 크리에이터 선택

### 3.2 Facebook 페이지 연결
1. Facebook에서 새 페이지 생성
2. Instagram 설정에서 Facebook 페이지 연결

### 3.3 Facebook 앱 생성
1. https://developers.facebook.com/ 접속
2. 내 앱 > 앱 만들기
3. 비즈니스 선택
4. 앱 이름 입력

### 3.4 Instagram Graph API 설정
1. 앱 대시보드 > 제품 추가 > Instagram
2. Instagram Basic Display 설정
3. 권한 요청: `instagram_business_basic`, `instagram_business_content_publish`

### 3.5 Access Token 발급
1. Graph API Explorer 사용
2. 권한 선택 후 토큰 생성
3. `.env`에 `INSTAGRAM_ACCESS_TOKEN` 설정

### 3.6 User ID 확인
```bash
curl "https://graph.facebook.com/v19.0/me/accounts?access_token=YOUR_TOKEN"
```

## 4. 테스트 실행

### 4.1 데이터베이스 초기화
```bash
python -c "from src.core.database import Database; Database('data/database.db')"
```

### 4.2 스토리 생성 테스트
```bash
python src/services/story_generator.py
```

### 4.3 전체 파이프라인 테스트
```bash
python -m src.main --topic "개발자 일상" --style "유머"
```

## 5. GitHub Actions 설정

### 5.1 저장소 Secrets 설정
1. GitHub 저장소 > Settings > Secrets and variables > Actions
2. New repository secret 클릭
3. 다음 Secrets 추가:
   - `ANTHROPIC_API_KEY`
   - `REPLICATE_API_TOKEN`
   - `INSTAGRAM_ACCESS_TOKEN` (옵션)
   - `INSTAGRAM_USER_ID` (옵션)

### 5.2 워크플로우 활성화
1. Actions 탭 확인
2. "Daily Webtoon Generator" 워크플로우 확인
3. "Run workflow" 버튼으로 수동 실행 테스트

## 6. 문제 해결

### Q: "ANTHROPIC_API_KEY not found" 오류
A: `.env` 파일이 올바른 위치에 있는지 확인하고, API 키가 정확한지 확인하세요.

### Q: Replicate 이미지 생성 실패
A: API 토큰이 유효한지 확인하고, 계정에 크레딧이 있는지 확인하세요.

### Q: Instagram 포스팅 실패
A: Access Token이 만료되지 않았는지, 권한이 올바른지 확인하세요.

## 7. 다음 단계

- [API 문서](API.md) 참조
- [배포 가이드](DEPLOYMENT.md) 참조
- 대시보드 실행: `python -m src.dashboard.app`
