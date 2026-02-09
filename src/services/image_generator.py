"""
Image generation service using Replicate and Fal.ai APIs
"""
import sys
import requests
from typing import Optional
import time

# UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

class ImageGenerator:
    """Generate images using AI APIs"""
    
    def __init__(self, provider: str = "replicate", api_token: str = None):
        """
        Initialize image generator
        
        Args:
            provider: "replicate" or "fal"
            api_token: API token for the provider
        """
        self.provider = provider
        self.api_token = api_token
    
    def generate(self, prompt: str, width: int = 1024, height: int = 1024) -> str:
        """
        Generate an image from a prompt
        
        Args:
            prompt: Text prompt for image generation
            width: Image width
            height: Image height
        
        Returns:
            URL of the generated image
        """
        if self.provider == "replicate":
            return self._generate_replicate(prompt, width, height)
        elif self.provider == "fal":
            return self._generate_fal(prompt, width, height)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _generate_replicate(self, prompt: str, width: int, height: int) -> str:
        """Generate image using Replicate API"""
        try:
            import replicate
            
            print(f"🎨 Replicate API로 이미지 생성 중...")
            print(f"   프롬프트: {prompt[:100]}...")
            
            client = replicate.Client(api_token=self.api_token)
            
            # Stable Diffusion 3.5
            output = client.run(
                "stability-ai/stable-diffusion-3.5-large",
                input={
                    "prompt": prompt,
                    "width": width,
                    "height": height,
                    "num_outputs": 1,
                    "output_format": "png",
                    "output_quality": 90
                }
            )
            
            # Output is a list of URLs
            image_url = output[0] if isinstance(output, list) else output
            
            print(f"✅ 이미지 생성 완료: {image_url}")
            return image_url
            
        except Exception as e:
            print(f"❌ Replicate 이미지 생성 실패: {e}")
            raise
    
    def _generate_fal(self, prompt: str, width: int, height: int) -> str:
        """Generate image using Fal.ai API"""
        try:
            import fal_client
            
            print(f"🎨 Fal.ai API로 이미지 생성 중...")
            print(f"   프롬프트: {prompt[:100]}...")
            
            # Flux Pro
            result = fal_client.subscribe(
                "fal-ai/flux-pro",
                arguments={
                    "prompt": prompt,
                    "image_size": {
                        "width": width,
                        "height": height
                    },
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                    "num_images": 1
                },
                with_logs=False
            )
            
            image_url = result["images"][0]["url"]
            
            print(f"✅ 이미지 생성 완료: {image_url}")
            return image_url
            
        except Exception as e:
            print(f"❌ Fal.ai 이미지 생성 실패: {e}")
            raise
    
    def download_image(self, url: str, save_path: str) -> str:
        """
        Download image from URL
        
        Args:
            url: Image URL
            save_path: Path to save the image
        
        Returns:
            Path to the saved image
        """
        try:
            print(f"📥 이미지 다운로드 중: {url}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 이미지 저장 완료: {save_path}")
            return save_path
            
        except Exception as e:
            print(f"❌ 이미지 다운로드 실패: {e}")
            raise


if __name__ == "__main__":
    # Test
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Test Replicate
    replicate_token = os.getenv("REPLICATE_API_TOKEN")
    if replicate_token:
        generator = ImageGenerator(provider="replicate", api_token=replicate_token)
        
        test_prompt = "A tired office worker with messy hair, surprised expression, sitting at desk with laptop, fluorescent office lighting, cartoon style, webtoon art"
        
        try:
            image_url = generator.generate(test_prompt, width=512, height=512)
            print(f"\n생성된 이미지 URL: {image_url}")
            
            # Download test
            generator.download_image(image_url, "test_image.png")
            
        except Exception as e:
            print(f"테스트 실패: {e}")
    else:
        print("REPLICATE_API_TOKEN not found in environment")
