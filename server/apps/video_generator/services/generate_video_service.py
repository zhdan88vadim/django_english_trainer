import os
import tempfile
import textwrap
import json
from typing import Callable, List, Optional, Tuple, Dict, Any
import numpy as np
from gtts import gTTS
from pydub import AudioSegment
from moviepy.editor import (
    AudioFileClip, 
    CompositeVideoClip, 
    ColorClip, 
    VideoClip
)
from PIL import Image, ImageDraw, ImageFont

# ---------- Settings ----------
VIDEO_SIZE = (1280, 720)
BG_COLOR = (0, 0, 0)
RU_TEXT_COLOR = (194, 194, 194)
EN_TEXT_COLOR = (255, 215, 0)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 64
FPS = 24

PAUSE_MS = 4000
SILENCE_AFTER_EN1_MS = 2000
SILENCE_AFTER_EN2_MS = 1000
# -----------------------------------------------------------------

# Text image cache
_text_image_cache: Dict[Tuple, np.ndarray] = {}

def change_speed(sound: AudioSegment, speed: float = 1.0) -> AudioSegment:
    if speed == 1.0:
        return sound
    new_frame_rate = int(sound.frame_rate * speed)
    return sound._spawn(sound.raw_data, overrides={"frame_rate": new_frame_rate}).set_frame_rate(sound.frame_rate)

def make_tts_segment(text: str, lang: str, tmpdir: str) -> AudioSegment:
    if not text:
        return AudioSegment.silent(duration=0)
    
    tmp_path = os.path.join(tmpdir, f"tts_{lang}_{abs(hash(text))}.mp3")
    tts = gTTS(text, lang=lang)
    tts.save(tmp_path)
    seg = AudioSegment.from_file(tmp_path, format="mp3")
    return seg

def _measure_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> Tuple[int, int]:
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        return w, h
    except Exception:
        pass
    try:
        w, h = draw.textsize(text, font=font)
        return w, h
    except Exception:
        pass
    try:
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        return w, h
    except Exception:
        pass
    try:
        w, h = font.getsize(text)
        return w, h
    except Exception:
        pass
    return max(10, len(text) * 8), FONT_SIZE

def render_text_image(
    text: str, 
    color: Tuple[int, int, int], 
    video_size: Tuple[int, int], 
    font_path: str, 
    fontsize: int, 
    margin: int = 200, 
    line_spacing_px: int = 10, 
    line_spacing_mul: float = 0.0
) -> np.ndarray:
    w, h = video_size
    # Use RGB canvas with background color
    canvas = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype(font_path, fontsize) if font_path else ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    sample_w, _ = _measure_text(draw, "x" * 10, font)
    avg_char_width = max(1, sample_w // 10)
    max_text_width = w - margin
    approx_chars_per_line = max(20, max_text_width // max(1, avg_char_width))
    wrapped = textwrap.fill(text, width=approx_chars_per_line)

    lines = wrapped.split("\n")
    line_sizes = [_measure_text(draw, line, font) for line in lines]

    line_heights = []
    for (lw, lh) in line_sizes:
        spacing = line_spacing_px + int(line_spacing_mul * lh)
        line_heights.append(lh + spacing)

    total_text_height = sum(line_heights) - (line_spacing_px + int(line_spacing_mul * line_sizes[-1][1]))
    y = (h - total_text_height) // 2

    for i, line in enumerate(lines):
        lw, lh = line_sizes[i]
        x = (w - lw) // 2
        draw.text((x, y), line, fill=color, font=font)
        spacing = line_spacing_px + int(line_spacing_mul * lh)
        y += lh + spacing

    return np.array(canvas)

def get_text_image_array(
    text: str, 
    color: Tuple[int, int, int], 
    video_size: Tuple[int, int] = VIDEO_SIZE, 
    font_path: str = FONT_PATH, 
    fontsize: int = FONT_SIZE, 
    margin: int = 200
) -> np.ndarray:
    key = (text, tuple(color) if isinstance(color, (list, tuple)) else color, fontsize)
    if key in _text_image_cache:
        return _text_image_cache[key]
    
    arr = render_text_image(
        text=text,
        color=color,
        video_size=video_size,
        font_path=font_path,
        fontsize=fontsize,
        margin=margin,
        line_spacing_px=20,
        line_spacing_mul=0.20
    )
    _text_image_cache[key] = arr
    return arr

def make_current_text_lookup_with_pause(events: List[Tuple[float, float, str, Tuple[int, int, int]]]):
    sorted_events = sorted(events, key=lambda e: e[0])
    timeline = []
    for start, dur, text, color in sorted_events:
        end = start + dur
        timeline.append((start, end, text, color))

    def current_at(t: float) -> Tuple[Optional[str], Optional[Tuple[int, int, int]]]:
        for start, end, text, color in timeline:
            if start <= t < end:
                return text, color
        
        # Find last displayed text
        prev = None
        for start, end, text, color in timeline:
            if start <= t:
                prev = (start, end, text, color)
            elif start > t:
                break
                
        if prev is not None:
            return prev[2], prev[3]
        return None, None

    return current_at

def generate_video_from_lines(
    lines: List[str],
    out_video_path: str,
    progress_cb: Optional[Callable[[int, str], None]] = None,
    video_size: Tuple[int, int] = VIDEO_SIZE,
    font_path: str = FONT_PATH,
    font_size: int = FONT_SIZE,
    fps: int = FPS
) -> str:
    """
    Generate video from lines of text
    
    Args:
        lines: List of strings in format "RU;EN"
        out_video_path: Full path to output mp4
        progress_cb: Callback function(percent:int, message:str)
        video_size: (width, height) tuple
        font_path: Path to TrueType font file
        font_size: Font size for text
        fps: Frames per second
    
    Returns:
        Path to generated video file
    """
    def _progress(p: int, msg: str):
        if progress_cb:
            try:
                progress_cb(int(max(0, min(100, p))), str(msg))
            except Exception:
                pass

    _progress(1, "Starting video generation")
    audio_tmp = None

    try:
        print(f"Checking font at: {font_path}")
        print(f"Font exists: {os.path.exists(font_path)}")

        # 1) Build audio and events
        _progress(3, "Building audio segments")
        final_audio = AudioSegment.silent(duration=0)
        text_events: List[Tuple[float, float, str, Tuple[int, int, int]]] = []
        current_ms = 0
        total_lines = max(1, len([ln for ln in lines if ln and ";" in ln]))

        temp_dir = "/tmp/video_generation"
        os.makedirs(temp_dir, exist_ok=True)
        
        with tempfile.TemporaryDirectory(dir=temp_dir) as tmpdir:
            processed = 0
            
            for idx, raw_line in enumerate(lines, start=1):
                line = raw_line.strip()
                if not line or ";" not in line:
                    continue
                    
                ru, en = line.split(";", 1)
                ru = ru.strip()
                en = en.strip()

                _progress(5 + int(40 * processed / total_lines), f"Generating TTS for line {idx}")
                
                audio_ru = make_tts_segment(ru, lang="ru", tmpdir=tmpdir)
                audio_ru = change_speed(audio_ru, speed=1.0)
                audio_en = make_tts_segment(en, lang="en", tmpdir=tmpdir)
                audio_en = change_speed(audio_en, speed=1.0)

                seg = AudioSegment.silent(duration=0)
                seg += audio_ru
                seg += AudioSegment.silent(duration=PAUSE_MS)
                seg += audio_en
                seg += AudioSegment.silent(duration=SILENCE_AFTER_EN1_MS)
                seg += audio_en
                seg += AudioSegment.silent(duration=SILENCE_AFTER_EN2_MS)

                final_audio += seg

                # Events in seconds
                ru_start = current_ms / 1000.0
                ru_dur = len(audio_ru) / 1000.0
                text_events.append((ru_start, ru_dur, ru, RU_TEXT_COLOR))

                en1_start = (current_ms + len(audio_ru) + PAUSE_MS) / 1000.0
                en1_dur = len(audio_en) / 1000.0
                text_events.append((en1_start, en1_dur, en, EN_TEXT_COLOR))

                en2_start = (current_ms + len(audio_ru) + PAUSE_MS + len(audio_en) + SILENCE_AFTER_EN1_MS) / 1000.0
                en2_dur = len(audio_en) / 1000.0
                text_events.append((en2_start, en2_dur, en, EN_TEXT_COLOR))

                current_ms += len(seg)
                processed += 1
                _progress(5 + int(40 * processed / total_lines), f"Processed line {idx}")
            
            _progress(46, "Exporting combined audio")
            audio_tmp = out_video_path + ".tmp_audio.mp3"
            final_audio.export(audio_tmp, format="mp3")

        # 2) Prepare video composition
        _progress(50, "Preparing video composition")
        total_duration = len(final_audio) / 1000.0
        
        bg_clip = ColorClip(
            size=video_size, 
            color=BG_COLOR, 
            duration=total_duration
        )

        current_at = make_current_text_lookup_with_pause(text_events)

        def make_frame(t: float) -> np.ndarray:
            """Generate frame at time t - returns RGB array"""
            text, color = current_at(t)
            if text is None:
                # Return black frame (RGB)
                return np.zeros((video_size[1], video_size[0], 3), dtype=np.uint8)
            
            # Get RGB array directly
            arr = get_text_image_array(
                text, color, video_size, font_path, font_size, margin=200
            )
            return arr

        # Create text video
        text_video = VideoClip(make_frame, duration=total_duration)
        
        # ✅ MoviePy 1.0.3: Use set_position() instead of with_position()
        video = CompositeVideoClip([bg_clip, text_video.set_position("center")])
        
        # ✅ MoviePy 1.0.3: Use set_audio() instead of with_audio()
        audio_clip = AudioFileClip(audio_tmp)
        video = video.set_audio(audio_clip)

        # 3) Render video
        _progress(60, "Rendering video (this may take a while)")
        
        # ✅ MoviePy 1.0.3: Use logger=None to suppress output
        video.write_videofile(
            out_video_path, 
            fps=fps, 
            codec="libx264", 
            audio_codec="aac",
            verbose=False,
            logger=None
        )
        
        _progress(95, "Finalizing")

    except Exception as e:
        _progress(0, f"Error: {str(e)}")
        raise

    finally:
        # Cleanup temporary audio file
        if audio_tmp and os.path.exists(audio_tmp):
            try:
                os.remove(audio_tmp)
            except Exception:
                pass

    _progress(100, "Video generation completed")
    return out_video_path


# --- Local test ---
if __name__ == "__main__":
    sample_input = "/media/vadim/1TB_SSD/my_github/django_english_trainer/phrases.txt"
    if os.path.exists(sample_input):
        with open(sample_input, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    else:
        lines = ["Привет;Hello", "Как дела;How are you"]

    def print_progress(p: int, m: str):
        print(f"[{p}%] {m}")

    out = "out_test_video.mp4"
    try:
        generate_video_from_lines(lines, out, progress_cb=print_progress)
        print("✓ Video saved:", out)
    except Exception as exc:
        print("✗ Generation failed:", exc)