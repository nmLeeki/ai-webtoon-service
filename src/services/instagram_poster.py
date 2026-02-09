"""
Instagram posting service using Graph API
"""
import sys
import requests
from typing import Dict, Optional
from datetime import datetime

# UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

class InstagramPoster:
    """Post webtoons to Instagram using Graph API"""
    
    def __init__(self, access_token: str, user_id: str):
        """
        Initialize Instagram poster
        
        Args:
            access_token: Instagram access token
            user_id: Instagram user ID
        """
        self.access_token = access_token
        self.user_id = user_id
        self.base_url = "https://graph.facebook.com/v19.0"
    
    def post_image(self, image_url: str, caption: str, hashtags: str = "") -> Dict:
        """
        Post an image to Instagram
        
        Args:
            image_url: Publicly accessible image URL
            caption: Post caption
            hashtags: Hashtags (space or newline separated)
        
        Returns:
            Dict with post ID and status
        """
        try:
            # Combine caption and hashtags
            full_caption = f"{caption}\n\n{hashtags}" if hashtags else caption
            
            print(f"📸 Instagram 포스팅 준비 중...")
            print(f"   캡션: {caption[:50]}...")
            
            # Step 1: Create media container
            create_url = f"{self.base_url}/{self.user_id}/media"
            create_data = {
                "image_url": image_url,
                "caption": full_caption,
                "access_token": self.access_token
            }
            
            print(f"   미디어 컨테이너 생성 중...")
            response = requests.post(create_url, data=create_data, timeout=30)
            response.raise_for_status()
            
            container_id = response.json().get("id")
            if not container_id:
                raise ValueError("Failed to create media container")
            
            print(f"   ✅ 컨테이너 생성 완료: {container_id}")
            
            # Step 2: Publish media
            publish_url = f"{self.base_url}/{self.user_id}/media_publish"
            publish_data = {
                "creation_id": container_id,
                "access_token": self.access_token
            }
            
            print(f"   미디어 게시 중...")
            response = requests.post(publish_url, data=publish_data, timeout=30)
            response.raise_for_status()
            
            post_id = response.json().get("id")
            
            print(f"✅ Instagram 포스팅 완료!")
            print(f"   Post ID: {post_id}")
            
            return {
                "success": True,
                "post_id": post_id,
                "posted_at": datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Instagram 포스팅 실패: {e}")
            if hasattr(e.response, 'text'):
                print(f"   응답: {e.response.text}")
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_insights(self, media_id: str) -> Optional[Dict]:
        """
        Get engagement metrics for a post
        
        Args:
            media_id: Instagram media ID
        
        Returns:
            Dict with engagement metrics
        """
        try:
            url = f"{self.base_url}/{media_id}/insights"
            params = {
                "metric": "engagement,impressions,reach,saved",
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json().get("data", [])
            
            # Parse metrics
            metrics = {}
            for item in data:
                metrics[item["name"]] = item["values"][0]["value"]
            
            return metrics
            
        except Exception as e:
            print(f"❌ 인사이트 조회 실패: {e}")
            return None
    
    def get_post_details(self, media_id: str) -> Optional[Dict]:
        """
        Get post details (likes, comments, etc.)
        
        Args:
            media_id: Instagram media ID
        
        Returns:
            Dict with post details
        """
        try:
            url = f"{self.base_url}/{media_id}"
            params = {
                "fields": "like_count,comments_count,timestamp,caption",
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"❌ 포스트 상세 조회 실패: {e}")
            return None


if __name__ == "__main__":
    # Test
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    user_id = os.getenv("INSTAGRAM_USER_ID")
    
    if access_token and user_id:
        poster = InstagramPoster(access_token, user_id)
        
        # Test with a sample image URL (replace with actual URL)
        test_image_url = "https://example.com/test.png"
        test_caption = "테스트 포스팅"
        test_hashtags = "#AI웹툰 #자동화 #테스트"
        
        print("Instagram API 테스트 (실제 포스팅하지 않음)")
        print(f"Access Token: {access_token[:20]}...")
        print(f"User ID: {user_id}")
    else:
        print("Instagram credentials not found in environment")
        print("INSTAGRAM_ACCESS_TOKEN 및 INSTAGRAM_USER_ID를 .env 파일에 설정하세요")
