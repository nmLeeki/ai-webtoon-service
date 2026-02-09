"""
Main pipeline - orchestrates the entire webtoon generation and posting process
"""
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# UTF-8 encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, TypeError):
    pass

from src.core.config import Config
from src.core.database import Database
from src.services.story_generator import StoryGenerator
from src.services.image_generator import ImageGenerator
from src.services.image_composer import ImageComposer
from src.services.instagram_poster import InstagramPoster


def run_pipeline(topic: str = "직장인 공감", style: str = "유머", 
                post_to_instagram: bool = False):
    """
    Run the complete webtoon generation pipeline
    
    Args:
        topic: Story topic
        style: Story style
        post_to_instagram: Whether to post to Instagram
    """
    print("="*70)
    print("🚀 AI 웹툰 자동 생성 파이프라인 시작")
    print("="*70)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Validate config
        Config.validate()
        
        # Initialize database
        db = Database(Config.DATABASE_PATH)
        
        # Step 1: Generate story
        print("\n[1/5] 스토리 생성 중...")
        story_gen = StoryGenerator(Config.ANTHROPIC_API_KEY)
        story = story_gen.generate(topic=topic, style=style)
        
        # Save story to database
        story_id = db.insert_story(
            title=story['title'],
            topic=topic,
            style=style,
            panels_json=json.dumps(story['panels'], ensure_ascii=False)
        )
        
        # Save story JSON
        story_path = Path(Config.STORIES_DIR) / f"story_{timestamp}.json"
        story_path.parent.mkdir(parents=True, exist_ok=True)
        with open(story_path, 'w', encoding='utf-8') as f:
            json.dump(story, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 스토리 저장 완료: {story_path}")
        
        # Step 2: Generate images for each panel
        print("\n[2/5] 이미지 생성 중...")
        image_gen = ImageGenerator(
            provider=Config.IMAGE_GENERATOR,
            api_token=Config.REPLICATE_API_TOKEN
        )
        
        panel_images = []
        for i, panel in enumerate(story['panels']):
            print(f"\n  [{i+1}/4] 패널 이미지 생성 중...")
            
            try:
                # Generate image
                image_url = image_gen.generate(
                    prompt=panel['visual_prompt'],
                    width=512,  # Smaller for faster generation
                    height=512
                )
                
                # Download image
                image_path = Path(Config.IMAGES_DIR) / f"panel_{timestamp}_{i+1}.png"
                image_path.parent.mkdir(parents=True, exist_ok=True)
                
                image_gen.download_image(image_url, str(image_path))
                panel_images.append(str(image_path))
                
            except Exception as e:
                print(f"  ❌ 패널 {i+1} 이미지 생성 실패: {str(e)}")
                import traceback
                traceback.print_exc()
                print(f"  ⚠️ Placeholder 사용")
                # Create placeholder
                from PIL import Image
                placeholder = Image.new('RGB', (512, 512), color=f'#{i*50:02x}{i*50:02x}{i*50:02x}')
                placeholder_path = Path(Config.IMAGES_DIR) / f"panel_{timestamp}_{i+1}_placeholder.png"
                placeholder_path.parent.mkdir(parents=True, exist_ok=True)
                placeholder.save(placeholder_path)
                panel_images.append(str(placeholder_path))
        
        # Step 3: Compose webtoon
        print("\n[3/5] 웹툰 레이아웃 합성 중...")
        composer = ImageComposer(
            width=Config.IMAGE_WIDTH,
            height=Config.IMAGE_HEIGHT
        )
        
        webtoon_path = Path(Config.WEBTOONS_DIR) / f"webtoon_{timestamp}.png"
        webtoon_path.parent.mkdir(parents=True, exist_ok=True)
        
        composer.create_layout(panel_images, story, str(webtoon_path))
        
        # Save to database
        webtoon_id = db.insert_webtoon(
            story_id=story_id,
            image_path=str(webtoon_path)
        )
        
        # Step 4: Post to Instagram (optional)
        if post_to_instagram and Config.INSTAGRAM_ACCESS_TOKEN:
            print("\n[4/5] Instagram 포스팅 중...")
            
            # Upload image to a public URL first (you'll need to implement this)
            # For now, we'll skip actual posting
            print("⚠️ Instagram 포스팅은 이미지 URL이 필요합니다")
            print("   이미지를 공개 URL에 업로드한 후 포스팅하세요")
            
            # poster = InstagramPoster(
            #     access_token=Config.INSTAGRAM_ACCESS_TOKEN,
            #     user_id=Config.INSTAGRAM_USER_ID
            # )
            # 
            # caption = f"{story['title']}\n\n#AI웹툰 #자동화"
            # result = poster.post_image(image_url, caption)
        else:
            print("\n[4/5] Instagram 포스팅 건너뛰기")
        
        # Step 5: Summary
        print("\n[5/5] 완료!")
        print("\n" + "="*70)
        print("✅ 웹툰 생성 완료!")
        print("="*70)
        print(f"📖 제목: {story['title']}")
        print(f"📁 스토리: {story_path}")
        print(f"🖼️ 웹툰: {webtoon_path}")
        print(f"💾 데이터베이스 ID: Story #{story_id}, Webtoon #{webtoon_id}")
        print("="*70)
        
        return {
            "success": True,
            "story_id": story_id,
            "webtoon_id": webtoon_id,
            "webtoon_path": str(webtoon_path)
        }
        
    except Exception as e:
        print(f"\n❌ 파이프라인 실패: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 웹툰 생성 파이프라인")
    parser.add_argument("--topic", default="직장인 공감", help="웹툰 주제")
    parser.add_argument("--style", default="유머", help="웹툰 스타일")
    parser.add_argument("--post", action="store_true", help="Instagram 포스팅")
    
    args = parser.parse_args()
    
    result = run_pipeline(
        topic=args.topic,
        style=args.style,
        post_to_instagram=args.post
    )
    
    # Exit with appropriate code for CI
    if not result.get("success", False):
        sys.exit(1)
    sys.exit(0)
