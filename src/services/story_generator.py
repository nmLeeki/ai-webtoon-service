"""
Story generation service using Claude API
"""
import sys
import json
import anthropic
from typing import Dict, List

# UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

class StoryGenerator:
    """Generate 4-panel webtoon stories using Claude API"""
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate(self, topic: str = "직장인 공감", style: str = "유머", 
                 num_panels: int = 4) -> Dict:
        """
        Generate a webtoon story
        
        Args:
            topic: Story topic (e.g., "직장인 공감", "개발자 일상")
            style: Story style (e.g., "유머", "감동", "공포")
            num_panels: Number of panels (default: 4)
        
        Returns:
            Dict with title and panels
        """
        prompt = f"""
당신은 창의적인 웹툰 작가입니다. 다음 조건에 맞는 {num_panels}컷 만화 스토리를 생성해주세요.

**주제**: {topic}
**스타일**: {style}

**요구사항**:
1. {num_panels}컷 만화 형식 (기승전결)
2. 각 컷마다 명확한 장면 설명
3. 캐릭터 대사 포함
4. 마지막 컷에 반전이나 웃음 포인트
5. 각 컷마다 AI 이미지 생성을 위한 상세한 visual_prompt 포함

**출력 형식** (JSON):
{{
    "title": "웹툰 제목",
    "panels": [
        {{
            "panel_number": 1,
            "scene_description": "장면 상세 설명 (배경, 캐릭터 포즈, 표정 등)",
            "dialogue": "캐릭터 대사",
            "emotion": "감정 (예: 행복, 놀람, 화남)",
            "visual_prompt": "AI 이미지 생성용 영문 프롬프트 (detailed, specific, for Stable Diffusion)"
        }},
        ... (총 {num_panels}개)
    ]
}}

**visual_prompt 작성 가이드**:
- 영어로 작성
- 구체적인 장면, 캐릭터 외모, 배경, 조명 포함
- 예: "A tired office worker with messy hair, surprised expression, sitting at desk with laptop, fluorescent office lighting, cartoon style"

반드시 JSON 형식으로만 답변해주세요.
"""
        
        try:
            print(f"🎨 Claude API로 스토리 생성 중... (주제: {topic}, 스타일: {style})")
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text
            
            # JSON 추출
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            story = json.loads(response_text)
            
            # Validation
            if "title" not in story or "panels" not in story:
                raise ValueError("Invalid story format")
            
            if len(story["panels"]) != num_panels:
                raise ValueError(f"Expected {num_panels} panels, got {len(story['panels'])}")
            
            print(f"✅ 스토리 생성 완료: {story['title']}")
            return story
            
        except Exception as e:
            print(f"❌ 스토리 생성 실패: {e}")
            print("데모용 샘플 스토리를 사용합니다.")
            return self._get_sample_story(topic, style, num_panels)
    
    def _get_sample_story(self, topic: str, style: str, num_panels: int) -> Dict:
        """Fallback sample story"""
        return {
            "title": "월요일 아침의 기적",
            "panels": [
                {
                    "panel_number": 1,
                    "scene_description": "침대에서 알람 소리에 놀라 일어나는 직장인. 머리가 산발이고 눈이 반쯤 감긴 상태. 배경은 어두운 방.",
                    "dialogue": "으악! 벌써 7시?!",
                    "emotion": "놀람",
                    "visual_prompt": "A tired office worker with messy hair, half-closed eyes, shocked expression, waking up in dark bedroom, alarm clock ringing, cartoon style, webtoon art"
                },
                {
                    "panel_number": 2,
                    "scene_description": "황급히 옷을 입으며 거울을 보는 직장인. 넥타이가 삐뚤어져 있고 셔츠 단추를 잘못 끼웠다. 배경은 밝아진 방.",
                    "dialogue": "5분 안에 준비 완료!",
                    "emotion": "당황",
                    "visual_prompt": "Office worker rushing to get dressed, crooked tie, misaligned shirt buttons, looking at mirror, bright room, panicked expression, cartoon style, webtoon art"
                },
                {
                    "panel_number": 3,
                    "scene_description": "현관문을 열고 나가려는 순간, 스마트폰을 보며 멈춰선 직장인. 표정이 점점 밝아진다. 배경은 현관.",
                    "dialogue": "어? 잠깐... 오늘이...",
                    "emotion": "의아함",
                    "visual_prompt": "Office worker at front door, looking at smartphone, confused then brightening expression, hallway background, cartoon style, webtoon art"
                },
                {
                    "panel_number": 4,
                    "scene_description": "침대로 다시 돌아가 이불을 덮고 행복하게 웃는 직장인. 스마트폰 화면에 '토요일'이라고 표시되어 있다. 배경은 다시 어두운 방.",
                    "dialogue": "토요일이었어! 굿나잇~",
                    "emotion": "행복",
                    "visual_prompt": "Happy office worker back in bed, smiling under blanket, smartphone showing 'Saturday', dark cozy bedroom, relaxed expression, cartoon style, webtoon art"
                }
            ][:num_panels]
        }


if __name__ == "__main__":
    # Test
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if api_key:
        generator = StoryGenerator(api_key)
        story = generator.generate(topic="개발자 일상", style="유머")
        
        print("\n" + "="*60)
        print(f"제목: {story['title']}")
        print("="*60)
        
        for panel in story['panels']:
            print(f"\n[{panel['panel_number']}컷]")
            print(f"장면: {panel['scene_description']}")
            print(f"대사: {panel['dialogue']}")
            print(f"감정: {panel['emotion']}")
            print(f"프롬프트: {panel['visual_prompt']}")
    else:
        print("ANTHROPIC_API_KEY not found in environment")
