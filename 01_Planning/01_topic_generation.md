> # Automatic Topic Generation
- STEP-1: Collect Sources for latest trends and new titles.
- STEP-2: Refine the titles with Ollama models to get video title and tags.
- STEP-3: Automate the whole process with one click or LangChain.

## STEP-1: Collect Sources
- gnews: https://pypi.org/project/gnews/
- others:

## STEP-2: Refine the titles with AI
- Ollama models is good option.










> # Temp Things
**Installation**
```bash
pip install pytrends pandas requests praw
# Optional: ollama (for local LLM refinement)
# Create virtual environment:
python -m venv yt_env
yt_env/Scripts/activate
# If getting error in VS Code, try running below command:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Code

```python
import random
import json
from datetime import datetime
from typing import List, Dict, Optional

import pandas as pd
from pytrends.request import TrendReq
import praw
import requests

# Optional: Local LLM via Ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False



def refine_with_llm(topics: List[str], hint: str, limit: int, lang: str) -> List[str]:
    """Use local Ollama to turn raw trends into catchy YouTube video titles"""
    if not OLLAMA_AVAILABLE or not topics:
        return topics[:limit]

    prompt = f"""
You are a YouTube content strategist. Generate {limit*2} engaging, clickable video title ideas in {lang}.
- Base them on these trending topics: {topics[:20]}
- Hint/niche: {hint or 'General trending content'}
- Make them SEO-friendly, curiosity-driven, and suitable for YouTube (use numbers, questions, power words where natural).
- Keep titles under 70 characters when possible.
- Return only a valid JSON array of strings.
"""

    try:
        response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
        content = response['message']['content']
        # Extract JSON
        start = content.find('[')
        end = content.rfind(']') + 1
        if start != -1 and end != -1:
            titles = json.loads(content[start:end])
            random.shuffle(titles)
            return titles[:limit]
    except Exception as e:
        print(f"LLM refinement error: {e}")

    return topics[:limit]

# Example Usage
if __name__ == "__main__":
    print("=== With Hint ===")
    results = get_video_titles(hint="Artificial Intelligence", region="Global", lang="English", limit=5)
    for r in results:
        print(f"{r['rank']}. {r['title']}")

    print("\n=== No Hint (General Trending) ===")
    results = get_video_titles(limit=5)
    for r in results:
        print(f"{r['rank']}. {r['title']}")
```


