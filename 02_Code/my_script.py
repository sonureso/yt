from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import Dict
import json
from datetime import datetime



chat_template = ChatPromptTemplate([
    ('system', 'You are an expert Video {lang} Scriptwriter for faceless YouTube channels'),
    ('human', """**Title:** {topic}

**Type:** {length} video in {lang} Language

Write the script in the following clear format:

=== SCRIPT START ===
(00:00) [Visual: description] Hook text here...
(00:08) [Visual: description] Main content...
=== SCRIPT END ===

**Rules:**
- Make it engaging and conversational.
- Add clear [Visual cues] in every section.
- Use timing like (00:00), (00:15).
- End with a strong CTA (like, subscribe, comment).

Here are two good examples:

Example 1:
=== SCRIPT START ===
(00:00) [Visual: Shocking graph] Did you know 90% of people fail at this?
(00:10) [Visual: Fast clips] Here's why...
=== SCRIPT END ===

Now write the script for the given title but in {lang} Language.
""")
])


chat_template2 = ChatPromptTemplate([
    ('system', 'You are an expert Video {lang} Scriptwriter for faceless YouTube channels'),
    ('human', """**Title:** {topic}

**Type:** {length} video in {lang} Language

Write the script in the following clear format: (only audio transcript with no instructions/message)

=== SCRIPT START ===
audio_transcript_line_1....
audio_transcript_line_2....
=== SCRIPT END ===

**Rules:**
- Make it engaging and conversational.
- End with a strong CTA (like, subscribe, comment).

Here are two good examples:

Example 1:
=== SCRIPT START ===
Welcome! Do you know what foods are healthy and ...
Number-1: Eggs
Eggs are the best source of...
=== SCRIPT END ===

Example 2:
=== SCRIPT START ===
Hello Guy! Welcome to this video on ...
In this video we will ...
=== SCRIPT END ===""")
])

def save_text_file(text, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Text successfully saved to '{filename}'")
    except IOError as e:
        print(f"Error saving text to '{filename}': {e}")
        raise

def generate_script(title,lang,length):
    parser = StrOutputParser()
    llm = ChatOllama(model="gemma4:31b-cloud", temperature=0.1)
    # qwen3-coder:480b-cloud | gemma4:31b-cloud | llama3.2:1b
    chain = chat_template2 | llm | parser
    print("Invoking Chain with title:",title)
    response = chain.invoke({'topic':title,'lang':lang,'length':length})
    return response

if __name__ == "__main__":
    test_title = "सेल्फ़ एन्यूमरेशन 2027 क्या है?"
    lang = "Hindi"
    script = generate_script(test_title,lang=lang,length='Short') # Long (600-1000 words)
    save_text_file(script, 'video_script.txt')
    print("==="*21)
    print(script)





