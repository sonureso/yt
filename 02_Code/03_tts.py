import re
import asyncio
from pathlib import Path
import edge_tts

INPUT_FILE = Path("video_script.txt")      # your script file
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

CLEAN_SCRIPT_FILE = OUTPUT_DIR / "cleaned_script.txt"
AUDIO_FILE = OUTPUT_DIR / "voiceover.mp3"
SUBTITLE_FILE = OUTPUT_DIR / "voiceover.srt"

# VOICE = "en-US-JennyNeural"
VOICE = "hi-IN-SwaraNeural"
# VOICE = "hi-IN-MadhurNeural"  
RATE = "+20%"
WPS = 2.08 * 1.2
VOLUME = "+0%"
PITCH = "+3Hz"


def parse_script_file(file_path: Path):
    raw = file_path.read_text(encoding="utf-8")

    lines = raw.splitlines()
    narration_blocks = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("==="):
            continue

        line = re.sub(r"^\(\d{2}:\d{2}\)\s*", "", line)
        line = re.sub(r"^\[Visual:.*?\]\s*", "", line)
        line = re.sub(r"^\*\*Audio:\*\*\s*", "", line)

        if line:
            narration_blocks.append(line)
    # print("Narration Blocks:\n",narration_blocks)
    return narration_blocks

def build_tts_text(blocks):
    cleaned = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        if not block.endswith((".", "!", "?")):
            block += "."

        cleaned.append(block)

    return "\n".join(cleaned)

def srt_timestamp(seconds: float):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

def estimate_srt_blocks(blocks, wps=WPS):
    entries = []
    current_time = 0.0

    for idx, block in enumerate(blocks, start=1):
        word_count = len(block.split())
        duration = max(2.0, word_count / wps)

        start = current_time
        end = start + duration

        entries.append(
            f"{idx}\n{srt_timestamp(start)} --> {srt_timestamp(end)}\n{block}\n"
        )

        current_time = end + 0.4

    return "\n".join(entries)

async def generate_audio(ssml_text):
    communicate = edge_tts.Communicate(
        text=ssml_text,
        voice=VOICE,
        rate=RATE,
        volume=VOLUME,
        pitch=PITCH,
    )
    await communicate.save(str(AUDIO_FILE))

async def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    blocks = parse_script_file(INPUT_FILE)
    if not blocks:
        raise ValueError("No narration text found in script file.")

    clean_text = "\n".join(blocks)
    CLEAN_SCRIPT_FILE.write_text(clean_text, encoding="utf-8")

    tts_text = build_tts_text(blocks)
    print(tts_text)
    await generate_audio(tts_text)

    srt_content = estimate_srt_blocks(blocks)
    SUBTITLE_FILE.write_text(srt_content, encoding="utf-8")

    print(f"Clean script saved to: {CLEAN_SCRIPT_FILE}")
    print(f"Audio saved to: {AUDIO_FILE}")
    print(f"SRT saved to: {SUBTITLE_FILE}")


if __name__ == "__main__":
    asyncio.run(main())