# AI 웹툰 자동화 서비스

완전 자동화된 AI 웹툰 생성 및 Instagram 포스팅 서비스

## 🎯 주요 기능

- ✅ Claude API로 4컷 만화 스토리 자동 생성
- ✅ Stable Diffusion/Flux로 고품질 이미지 생성
- ✅ Instagram 자동 포스팅 (Graph API)
- ✅ GitHub Actions 스케줄링 (매일 자동 실행)
- ✅ 인게이지먼트 분석 대시보드
- ✅ A/B 테스팅 시스템

## 📁 프로젝트 구조

```
ai-webtoon-service/
├── src/                    # 소스 코드
│   ├── core/              # 핵심 설정
│   ├── services/          # AI 서비스
│   ├── models/            # 데이터 모델
│   ├── utils/             # 유틸리티
│   └── dashboard/         # 웹 대시보드
├── scripts/               # 설정 스크립트
├── data/                  # 데이터 저장소
├── tests/                 # 테스트
└── docs/                  # 문서
```

## 🚀 빠른 시작

### 1. 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일 생성:
```env
ANTHROPIC_API_KEY=your_key_here
REPLICATE_API_TOKEN=your_token_here
INSTAGRAM_ACCESS_TOKEN=your_token_here
INSTAGRAM_USER_ID=your_id_here
```

### 3. 데이터베이스 초기화
```bash
python scripts/setup_database.py
```

### 4. 테스트 실행
```bash
python scripts/test_pipeline.py
```

### 5. 대시보드 실행
```bash
python -m src.dashboard.app
```

## 📊 기술 스택

- **AI**: Claude 3.5 Sonnet, Stable Diffusion, Flux Pro
- **소셜 미디어**: Instagram Graph API
- **데이터베이스**: SQLite
- **웹 프레임워크**: Flask
- **스케줄링**: GitHub Actions
- **이미지 처리**: Pillow

## 💰 예상 비용

- **초기 (1-2개월)**: $20-60/월
- **성장기 (3-6개월)**: $90-150/월
- **확장기 (6개월+)**: $250-500/월

## 📖 문서

- [설치 가이드](docs/SETUP.md)
- [API 문서](docs/API.md)
- [배포 가이드](docs/DEPLOYMENT.md)

## 🎯 로드맵

- [x] Phase 1: MVP 프로토타입
- [ ] Phase 2: 프로덕션 구현
- [ ] Phase 3: Instagram 연동
- [ ] Phase 4: 자동화 및 스케줄링
- [ ] Phase 5: 분석 대시보드

## 📝 라이선스

MIT License
