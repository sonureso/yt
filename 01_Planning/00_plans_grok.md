> # Phase 0: Local Setup (One-Time, Free)
- **Hardware**: Decent GPU (NVIDIA preferred for speed) helps with LLMs/image gen; CPU fallback works but slower.
- **Core Tools**:
  - **Ollama** (or LM Studio/OpenWebUI): Run local LLMs like Llama 3.1/3.2, Qwen2.5, or DeepSeek for topic/script generation. Free, easy.
  - **TTS**: Piper (fast, lightweight), Coqui TTS, or Kokoro/Fish Speech (higher quality, local). Alternatives: ChatTTS for expressive. Avoid paid like ElevenLabs.
  - **Image/Video Gen**: Stable Diffusion (via ComfyUI or Automatic1111) for custom visuals. Use Flux or SDXL variants.
  - **Stock Media**: Pexels + Pixabay APIs (free keys, royalty-free images/videos).
  - **Editing**: MoviePy (Python) + FFmpeg (powerful, scriptable). FFmpeg for speed/concat.
  - **Other**: yt-dlp (if repurposing), pydub (audio), requests (APIs), schedule/cron (automation).
- Install: `pip install moviepy ffmpeg-python requests pexels-api-py` (or similar), plus Ollama and Stable Diffusion tools.

> # Phase 1: Working end-to-end code for automation

### Step 1: Automatic Topic Selection
- **Sources for Ideas**:
  - Scrape Reddit (PRAW library, subreddits in your niche) or use RSS/news APIs.
  - YouTube Trends/Google Trends (free APIs or scraping).
  - Competitor analysis: Use YouTube Data API (free quota) to fetch top videos in niche.
  - LLM-generated: Prompt Ollama with "Generate 10 viral [niche] video topics for YouTube, trending angles, hooks."
- **Automation**:
  - Daily cron/job: Pull trends → LLM ranks by virality potential (search volume, engagement proxies).
  - Store in SQLite/Postgres queue with scores.
- **Output**: List of topics + keywords (e.g., "Top 10 AI Tools 2026").
- **Cost**: Free. Add simple deduplication.

### Step 2: Research & Script Generation
- Feed topic to Ollama (e.g., Llama 3.1 8B or larger if hardware allows).
- **Prompt Structure**:
  - Research key facts, structure (hook, points, CTA).
  - Format: Timed script with [visual cues], e.g., "00:00 Hook [show exciting image]".
  - Length: 150-300 words for Shorts; scale for longer.
- **Enhance**: Use local embeddings (if needed) for fact-checking against saved knowledge.
- **Output**: Markdown/JSON script with sections, timings, visual prompts.
- **Flask**: Button to regenerate script or edit.

### Step 3: Voiceover (TTS)
- Split script into sentences.
- Use local TTS (Piper/Kokoro):
  - Generate WAV/MP3 segments.
  - Add pauses, emphasis via SSML or tags if model supports.
  - Combine with pydub.
- **Quality Tips**: Fine-tune voice if possible; test multiple models. Background music later.
- **Output**: Single audio file synced to script timings.
- **Alternatives**: If quality insufficient, hybrid with free-tier paid (but prioritize local).

### Step 4: Visuals & Assets Generation
- **From Script**: Extract visual prompts (e.g., "futuristic AI robot").
- **Options** (mix for best results):
  - **Stock**: Query Pexels/Pixabay APIs for images/videos matching keywords. Download relevant clips (free, high-quality).
  - **Generated**: Stable Diffusion/ComfyUI for custom images/illustrations (batch generate). Use ControlNet for consistency.
  - **Video Clips**: Short generated clips if advanced (Stable Video Diffusion) or stock loops.
- **Automation**: Script loops through script sections → search/generate → resize/crop to target aspect (9:16 for Shorts, 16:9 otherwise).
- **B-roll**: Download 5-10s stock clips and loop/trim.
- **Output**: Folder of synced assets (images as ImageClips, videos as VideoClips).

### Step 5: Video Assembly & Editing
- **Use MoviePy + FFmpeg**:
  - Load audio as base timeline.
  - Composite visuals: ImageClip/VideoClip synced to timings (subclips, crossfades).
  - Add text overlays (captions, titles) with MoviePy's TextClip.
  - Background music (free library or generated), volume ducking.
  - Transitions, zooms (Ken Burns effect on images), speed adjustments.
  - Subtitles: Auto-generate with timestamps (or Whisper if transcribing).
- **Script Example Flow**:
  ```python
  from moviepy.editor import *
  audio = AudioFileClip("voice.mp3")
  clips = [ImageClip(img).set_duration(dur).crossfadein(0.5) for ...]
  video = concatenate_videoclips(clips, method="compose")
  final = video.set_audio(audio).resize((1080,1920))  # for Shorts
  final.write_videofile("output.mp4", fps=24, codec="libx264")
  ```
- **Speed**: Use FFmpeg directly via subprocess for heavy lifting (concat, filters).
- **Output**: Rendered MP4. Add thumbnail generation (Stable Diffusion).

### Step 6: Final Rendering, QA & Output
- **Post-Process**: FFmpeg for compression, metadata, watermark (optional).
- **QA Automation**: Basic checks (duration matches, no silent gaps via audio analysis). Manual review queue in Flask.
- **Storage**: Organized folders (topic/date/video.mp4, assets, script).
- **Rendering Time**: Optimize for batch (GPU accel where possible). Shorts render fast.

### Step 7: Flask Application Wrapper
- **Structure**:
  - Dashboard: Pending topics, generated scripts, videos ready.
  - Endpoints: `/generate?topic=xxx`, status polling, manual triggers per stage.
  - Use Celery/Threading for background jobs (long-running generation).
  - Database: Track pipeline state.
  - Controls: Approve script, regenerate section, preview renders.
- **Deployment**: Local server → later VPS (cheap) with cron for daily runs.
- **Safety**: Rate limits on APIs, error handling, logging.

### Overall Automation Flow (One Command/Script)
1. Topic selector runs → picks/queues.
2. `python pipeline.py --topic "xxx"` or Flask trigger.
3. Script → TTS → Visuals → Edit → Render.
- Scheduler: Daily/ hourly for batch.
- Monitoring: Email/Slack notifications on completion or errors.

### Cost & Scaling Tips (Minimal)
- **Almost Zero**: Local LLMs/TTS/SD + free stock APIs.
- **Potential Low Costs**: Electricity/GPU; optional cheap VPS. YouTube API for upload (free quota, Selenium fallback but brittle).
- **Optimization**: Quantized models (Ollama), smaller TTS, cache stock downloads.
- **Legal**: Use royalty-free only; disclose AI if needed. Comply with YouTube policies (no spam).

### Potential Enhancements
- Repurpose long videos into Shorts (Whisper transcription + LLM highlights).
- Auto-upload (YouTube API + OAuth).
- A/B testing thumbnails/titles via analytics feedback loop (advanced).
- Multi-niche support.

**Start Small**: Implement end-to-end for one Shorts video manually, then automate stages. Many open-source repos (e.g., similar to MoneyPrinter or ffmpeg-ai) provide starting code—adapt them.

This plan is modular, debuggable, and controllable via Flask. Iterate based on your niche/hardware. If you hit specifics (e.g., code for a stage), provide details!