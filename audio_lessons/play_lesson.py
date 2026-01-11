"""
SQL Audio Lesson Player
Uses Google Text-to-Speech (gTTS) for high-quality online voice
"""

import os
from pathlib import Path
import sys
from gtts import gTTS
import time

# Available accents
ACCENTS = {
    'us': 'com',
    'uk': 'co.uk',
    'aus': 'com.au',
    'india': 'co.in',
    'ca': 'ca'
}

def read_lesson_script(lesson_file):
    """Read a lesson script from file"""
    with open(lesson_file, 'r', encoding='utf-8') as f:
        return f.read()

def text_to_speech(text, output_file, accent='us'):
    """Convert text to speech using Google TTS"""
    try:
        tld = ACCENTS.get(accent, 'com')
        print(f"\n🎵 Generating audio with Google Voice ({accent.upper()})...")
        
        tts = gTTS(text=text, lang='en', tld=tld, slow=False)
        tts.save(output_file)
        print(f"✅ Audio saved to {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error with Google TTS: {e}")
        return False

def play_audio_file(file_path):
    """Play the audio file using the default system player"""
    print(f"▶️  Playing audio...")
    if sys.platform == 'win32':
        os.startfile(file_path)
    elif sys.platform == 'darwin':
        os.system(f'open "{file_path}"')
    else:
        os.system(f'xdg-open "{file_path}"')

def play_lesson(lesson_name, accent='us'):
    """Play a specific lesson"""
    lessons_dir = Path(__file__).parent / 'lessons'
    lesson_file = lessons_dir / f'{lesson_name}.txt'
    
    if not lesson_file.exists():
        print(f"❌ Lesson '{lesson_name}' not found!")
        print(f"\nAvailable lessons:")
        list_lessons()
        return
    
    print(f"\n{'='*70}")
    print(f"📚 Lesson: {lesson_name.replace('_', ' ').title()}")
    print(f"{'='*70}\n")
    
    # Read lesson text
    lesson_text = read_lesson_script(lesson_file)
    
    # Display the text
    print("📖 Lesson Content:")
    print("-" * 70)
    paragraphs = lesson_text.split('\n\n')
    for para in paragraphs:
        if para.strip():
            print(para.strip())
            print()
    print("-" * 70)
    
    # Generate and play audio
    # Add accent to filename to avoid overwriting
    audio_file = lessons_dir / f'{lesson_name}_{accent}.mp3'
    
    if text_to_speech(lesson_text, str(audio_file), accent):
        play_audio_file(str(audio_file))
        print("\n(Audio should be playing in your default media player)")
    
    print(f"\n{'='*70}")
    print(f"✅ End of lesson: {lesson_name.replace('_', ' ').title()}")
    print(f"{'='*70}\n")

def list_lessons():
    """List all available lessons"""
    lessons_dir = Path(__file__).parent / 'lessons'
    
    if not lessons_dir.exists():
        print("📁 Creating lessons directory...")
        lessons_dir.mkdir(exist_ok=True)
        return
    
    lessons = sorted(lessons_dir.glob('*.txt'))
    
    if not lessons:
        print("📚 No lessons found yet!")
        return
    
    print("\n" + "="*70)
    print("📚 Available SQL Lessons")
    print("="*70)
    for i, lesson in enumerate(lessons, 1):
        lesson_name = lesson.stem.replace('_', ' ').title()
        print(f"  {i}. {lesson_name}")
    print("="*70)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n🎓 SQL Audio Lesson Player (Google Voice Edition)")
        print("="*70)
        print("Usage: python play_lesson.py <lesson_name> [accent]")
        print("\nAvailable accents:")
        for acc in ACCENTS:
            print(f"  - {acc}")
        print("\nExample: python play_lesson.py nike_query_breakdown uk")
        list_lessons()
    elif sys.argv[1] == 'list':
        list_lessons()
    else:
        lesson_name = sys.argv[1]
        accent = 'us'
        if len(sys.argv) > 2:
            accent = sys.argv[2]
            if accent not in ACCENTS:
                print(f"⚠️ Accent '{accent}' not found, defaulting to 'us'")
                accent = 'us'
        
        play_lesson(lesson_name, accent)
