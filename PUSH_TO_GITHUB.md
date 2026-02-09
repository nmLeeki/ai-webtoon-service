# GitHub 저장소 생성 및 푸시 명령어

## 1. GitHub에서 새 저장소 생성
1. https://github.com/new 접속
2. Repository name: `ai-webtoon-service`
3. **Public** 또는 **Private** 선택
4. **Initialize this repository with a README 체크 해제**
5. **Create repository** 클릭

## 2. 저장소 URL 복사
생성 후 표시되는 URL을 복사하세요 (예시):
```
https://github.com/YOUR_USERNAME/ai-webtoon-service.git
```

## 3. 로컬에서 실행할 명령어

아래 명령어를 PowerShell에서 실행하세요:

```powershell
cd "C:\Users\maee7\Desktop\workspace\연구자동화에이전트들\ai-webtoon-service"

# GitHub 저장소 연결 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
& "C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/YOUR_USERNAME/ai-webtoon-service.git

# 코드 푸시
& "C:\Program Files\Git\bin\git.exe" push -u origin main
```

## 4. 푸시 완료 후

GitHub 저장소 페이지를 새로고침하면 모든 코드가 업로드된 것을 확인할 수 있습니다!

다음 단계: Repository Secrets 설정
