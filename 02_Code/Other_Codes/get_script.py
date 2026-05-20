from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Dict
import json
from datetime import datetime


def generate_script(
    title: str,
    video_type: str = "short",
    lang: str = "English",
    model: str = "llama3.2:1b",
    temperature: float = 0.7
) -> Dict:
    """
    Generate YouTube script using LangChain + ChatOllama + JsonOutputParser
    """

    parser = JsonOutputParser()

    prompt_template = """
You are a professional YouTube scriptwriter for faceless channels.

**Title:** {title}

**Task:**
Write a high-quality, engaging script in {lang} for a {video_type} video.

**Length Guidelines:**
- If "short": 30-60 seconds (150-280 words)
- If "long": 5-8 minutes (650-1100 words)

**Requirements:**
- Conversational and addictive tone.
- Start with a strong hook.
- Include clear [visual cues] in square brackets.
- Add timing markers like (00:00), (00:15).
- End with a strong Call-to-Action.

{format_instructions}

Answer ONLY with valid JSON. Do not add any extra text, explanation, or markdown.
"""

    chat_template = ChatPromptTemplate.from_template(prompt_template)

    llm = ChatOllama(
        model=model,
        temperature=temperature,
        num_ctx=8192,
    )

    # Create the chain with JsonOutputParser
    chain = chat_template | llm | parser

    try:
        response = chain.invoke({
            "title": title,
            "video_type": video_type,
            "lang": lang,
            "format_instructions": parser.get_format_instructions()
        })

        return response

    except Exception as e:
        print(f"Error generating script: {e}")
        
        # Strong Fallback
        return {
            "title": title,
            "video_type": video_type,
            "duration_estimate": "45 seconds",
            "script": f"Script generation failed.\nTitle: {title}",
            "sections": [],
            "thumbnail_idea": "Bold text on eye-catching background",
            "keywords": ["ai", "technology", title.lower().split()[0]]
        }


# ========================
# Test / Example Usage
# ========================
if __name__ == "__main__":
    test_title = "10 AI Tools That Will Replace Developers in 2026"

    script = generate_script(
        title=test_title,
        video_type="short",
        lang="English",
        model="llama3.2:1b",
        temperature=0.75
    )

    print("=" * 80)
    print("✅ SCRIPT GENERATED SUCCESSFULLY")
    print("TITLE:", script.get("title"))
    print("DURATION:", script.get("duration_estimate"))
    print("THUMBNAIL:", script.get("thumbnail_idea"))
    print("=" * 80)
    print("\nFULL SCRIPT:\n")
    print(script)
    
    # Optional: Save to file
    # with open(f"scripts/{test_title[:40]}.json", "w", encoding="utf-8") as f:
    #     json.dump(script, f, indent=2, ensure_ascii=False)