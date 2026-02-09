"""
Test pipeline script
"""
import sys
import os
from pathlib import Path

# UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_story_generation():
    """Test story generation service"""
    print("\n" + "="*70)
    print("📖 스토리 생성 테스트")
    print("="*70)
    
    try:
        from src.services.story_generator import StoryGenerator
        from src.core.config import Config
        
        generator = StoryGenerator(Config.ANTHROPIC_API_KEY)
        story = generator.generate(topic="개발자 일상", style="유머", num_panels=4)
        
        print(f"\n✅ 스토리 생성 성공!")
        print(f"   제목: {story['title']}")
        print(f"   패널 수: {len(story['panels'])}")
        
        return True
    except Exception as e:
        print(f"\n❌ 스토리 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_image_generation():
    """Test image generation service"""
    print("\n" + "="*70)
    print("🎨 이미지 생성 테스트")
    print("="*70)
    
    try:
        from src.services.image_generator import ImageGenerator
        from src.core.config import Config
        
        generator = ImageGenerator(
            provider=Config.IMAGE_GENERATOR,
            api_token=Config.REPLICATE_API_TOKEN
        )
        
        test_prompt = "A cute cartoon character, office worker, simple background, webtoon style"
        
        print(f"\n테스트 프롬프트: {test_prompt}")
        print("⚠️ 이미지 생성은 시간이 걸릴 수 있습니다 (30-60초)")
        
        image_url = generator.generate(test_prompt, width=512, height=512)
        
        print(f"\n✅ 이미지 생성 성공!")
        print(f"   URL: {image_url}")
        
        # Download test
        test_path = "data/images/test_image.png"
        Path(test_path).parent.mkdir(parents=True, exist_ok=True)
        generator.download_image(image_url, test_path)
        
        print(f"   저장: {test_path}")
        
        return True
    except Exception as e:
        print(f"\n❌ 이미지 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database():
    """Test database operations"""
    print("\n" + "="*70)
    print("💾 데이터베이스 테스트")
    print("="*70)
    
    try:
        from src.core.database import Database
        from src.core.config import Config
        import json
        
        db = Database(Config.DATABASE_PATH)
        
        # Insert test story
        test_story = {
            "title": "테스트 스토리",
            "panels": [
                {"panel_number": 1, "dialogue": "테스트"}
            ]
        }
        
        story_id = db.insert_story(
            title=test_story['title'],
            topic="테스트",
            style="테스트",
            panels_json=json.dumps(test_story['panels'])
        )
        
        print(f"\n✅ 데이터베이스 작동 확인!")
        print(f"   Story ID: {story_id}")
        
        return True
    except Exception as e:
        print(f"\n❌ 데이터베이스 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("="*70)
    print("🧪 AI 웹툰 서비스 테스트 시작")
    print("="*70)
    
    results = {
        "데이터베이스": test_database(),
        "스토리 생성": test_story_generation(),
        "이미지 생성": test_image_generation()
    }
    
    print("\n" + "="*70)
    print("📊 테스트 결과")
    print("="*70)
    
    for test_name, result in results.items():
        status = "✅ 성공" if result else "❌ 실패"
        print(f"   {test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ 모든 테스트 통과!")
        print("\n다음 단계:")
        print("  python -m src.main --topic '개발자 일상' --style '유머'")
    else:
        print("\n❌ 일부 테스트 실패")
        print("   .env 파일의 API 키를 확인하세요")
    
    print("="*70)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
