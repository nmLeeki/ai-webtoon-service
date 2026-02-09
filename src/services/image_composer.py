"""
Image composition service - combines panels into webtoon layout
"""
import sys
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple
import os

# UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

class ImageComposer:
    """Compose 4-panel webtoon layout"""
    
    def __init__(self, width: int = 1080, height: int = 1920):
        """
        Initialize composer
        
        Args:
            width: Total width (Instagram optimized: 1080)
            height: Total height (Instagram optimized: 1920)
        """
        self.width = width
        self.height = height
        self.panel_width = width // 2
        self.panel_height = height // 2
    
    def create_layout(self, panel_images: List[str], story: Dict, 
                     output_path: str) -> str:
        """
        Create 4-panel webtoon layout
        
        Args:
            panel_images: List of 4 image file paths
            story: Story dict with title and panels
            output_path: Path to save the final webtoon
        
        Returns:
            Path to the saved webtoon
        """
        print(f"🎨 4컷 레이아웃 생성 중: {story['title']}")
        
        # Create base image
        webtoon = Image.new('RGB', (self.width, self.height), color='white')
        draw = ImageDraw.Draw(webtoon)
        
        # Panel positions (2x2 grid)
        positions = [
            (0, 0),                                    # Top-left
            (self.panel_width, 0),                     # Top-right
            (0, self.panel_height),                    # Bottom-left
            (self.panel_width, self.panel_height)      # Bottom-right
        ]
        
        # Place panels
        for i, (img_path, pos) in enumerate(zip(panel_images, positions)):
            try:
                panel = Image.open(img_path)
                panel = panel.resize((self.panel_width - 10, self.panel_height - 10))
                webtoon.paste(panel, (pos[0] + 5, pos[1] + 5))
                
                print(f"  [{i+1}컷] 배치 완료")
                
            except Exception as e:
                print(f"  ❌ [{i+1}컷] 배치 실패: {e}")
                # Use placeholder
                self._draw_placeholder(draw, pos, i+1)
        
        # Draw grid lines
        line_width = 5
        draw.line([(self.width//2, 0), (self.width//2, self.height)], 
                 fill='black', width=line_width)
        draw.line([(0, self.height//2), (self.width, self.height//2)], 
                 fill='black', width=line_width)
        
        # Add title
        self._add_title(draw, story['title'])
        
        # Add speech bubbles
        for i, panel in enumerate(story['panels']):
            self._add_speech_bubble(draw, panel['dialogue'], positions[i], 
                                   panel.get('emotion', '중립'))
        
        # Save
        webtoon.save(output_path, quality=95)
        print(f"✅ 웹툰 저장 완료: {output_path}")
        
        return output_path
    
    def _draw_placeholder(self, draw: ImageDraw, pos: Tuple[int, int], 
                         panel_num: int):
        """Draw placeholder for missing panel"""
        x, y = pos
        colors = ['#FFE5E5', '#E5F0FF', '#E5FFE5', '#FFF4E5']
        bg_color = colors[(panel_num - 1) % 4]
        
        draw.rectangle([x+10, y+10, x+self.panel_width-10, y+self.panel_height-10], 
                      fill=bg_color)
        
        try:
            # Try multiple fonts for cross-platform compatibility
            fonts_to_try = ["malgun.ttf", "arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf"]
            font = None
            for font_name in fonts_to_try:
                try:
                    font = ImageFont.truetype(font_name, 80)
                    break
                except:
                    continue
            if not font:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        draw.text((x + 30, y + 30), f"{panel_num}", fill='#666666', font=font)
    
    def _add_title(self, draw: ImageDraw, title: str):
        """Add title at the top"""
        try:
            fonts_to_try = ["malgun.ttf", "arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf"]
            font = None
            for font_name in fonts_to_try:
                try:
                    font = ImageFont.truetype(font_name, 50)
                    break
                except:
                    continue
            if not font:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Title background
        draw.rectangle([0, 0, self.width, 80], fill='#333333')
        
        # Center title
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        title_x = (self.width - text_width) // 2
        
        draw.text((title_x, 15), title, fill='white', font=font)
    
    def _add_speech_bubble(self, draw: ImageDraw, dialogue: str, 
                          pos: Tuple[int, int], emotion: str):
        """Add speech bubble to panel"""
        try:
            fonts_to_try = ["malgun.ttf", "arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf"]
            font = None
            for font_name in fonts_to_try:
                try:
                    font = ImageFont.truetype(font_name, 35)
                    break
                except:
                    continue
            if not font:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Bubble position (bottom of panel)
        x, y = pos
        bubble_x = x + 50
        bubble_y = y + self.panel_height - 150
        
        # Text size
        bbox = draw.textbbox((0, 0), dialogue, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Bubble size
        padding = 20
        bubble_width = min(text_width + padding * 2, self.panel_width - 100)
        bubble_height = text_height + padding * 2
        
        # Emotion colors
        emotion_colors = {
            "행복": "#FFE5E5",
            "놀람": "#FFF4E5",
            "화남": "#FFE5E5",
            "슬픔": "#E5F0FF",
            "당황": "#FFF4E5",
            "의아함": "#F0F0F0",
            "중립": "#FFFFFF"
        }
        
        bubble_color = emotion_colors.get(emotion, "#FFFFFF")
        
        # Draw bubble
        bubble_coords = [bubble_x, bubble_y, 
                        bubble_x + bubble_width, bubble_y + bubble_height]
        draw.rounded_rectangle(bubble_coords, radius=15, 
                             fill=bubble_color, outline='black', width=3)
        
        # Draw text
        draw.text((bubble_x + padding, bubble_y + padding), 
                 dialogue, fill='black', font=font)


if __name__ == "__main__":
    # Test
    composer = ImageComposer()
    
    # Sample story
    story = {
        "title": "테스트 웹툰",
        "panels": [
            {"dialogue": "안녕하세요!", "emotion": "행복"},
            {"dialogue": "어? 뭐지?", "emotion": "놀람"},
            {"dialogue": "아하!", "emotion": "의아함"},
            {"dialogue": "좋아요!", "emotion": "행복"}
        ]
    }
    
    # Create placeholder images
    test_images = []
    for i in range(4):
        img = Image.new('RGB', (500, 500), color=f'#{i*50:02x}{i*50:02x}{i*50:02x}')
        path = f"test_panel_{i}.png"
        img.save(path)
        test_images.append(path)
    
    # Compose
    composer.create_layout(test_images, story, "test_webtoon.png")
    
    # Cleanup
    for path in test_images:
        os.remove(path)
