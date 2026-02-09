"""
Quick setup script to initialize the environment
"""
import sys
import os
from pathlib import Path

# UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

def setup_environment():
    """Initialize environment for AI webtoon service"""
    
    print("="*70)
    print("🚀 AI 웹툰 서비스 환경 설정")
    print("="*70)
    
    # Check .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("\n❌ .env 파일이 없습니다!")
        print("   .env.example을 복사하여 .env 파일을 생성하세요:")
        print("   cp .env.example .env")
        return False
    
    print("\n✅ .env 파일 확인 완료")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check required API keys
    required_keys = {
        "ANTHROPIC_API_KEY": "Claude API (필수)",
        "REPLICATE_API_TOKEN": "Replicate API (필수)"
    }
    
    optional_keys = {
        "FAL_KEY": "Fal.ai API (옵션)",
        "INSTAGRAM_ACCESS_TOKEN": "Instagram API (옵션)",
        "INSTAGRAM_USER_ID": "Instagram User ID (옵션)"
    }
    
    print("\n📋 API 키 확인:")
    all_set = True
    
    for key, desc in required_keys.items():
        value = os.getenv(key)
        if value and value != f"your_{key.lower()}_here":
            print(f"   ✅ {desc}: 설정됨")
        else:
            print(f"   ❌ {desc}: 미설정")
            all_set = False
    
    for key, desc in optional_keys.items():
        value = os.getenv(key)
        if value and value != f"your_{key.lower()}_here":
            print(f"   ✅ {desc}: 설정됨")
        else:
            print(f"   ⚠️ {desc}: 미설정 (옵션)")
    
    if not all_set:
        print("\n❌ 필수 API 키가 설정되지 않았습니다!")
        print("   .env 파일을 편집하여 API 키를 설정하세요.")
        return False
    
    # Initialize database
    print("\n💾 데이터베이스 초기화 중...")
    try:
        from src.core.database import Database
        from src.core.config import Config
        
        db = Database(Config.DATABASE_PATH)
        print(f"   ✅ 데이터베이스 생성 완료: {Config.DATABASE_PATH}")
    except Exception as e:
        print(f"   ❌ 데이터베이스 초기화 실패: {e}")
        return False
    
    # Create data directories
    print("\n📁 데이터 디렉토리 생성 중...")
    directories = [
        "data/stories",
        "data/images",
        "data/webtoons"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {dir_path}")
    
    print("\n" + "="*70)
    print("✅ 환경 설정 완료!")
    print("="*70)
    print("\n다음 단계:")
    print("  1. 테스트 실행: python scripts/test_pipeline.py")
    print("  2. 웹툰 생성: python -m src.main")
    print("  3. 대시보드 실행: python -m src.dashboard.app")
    print("="*70)
    
    return True


if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)
