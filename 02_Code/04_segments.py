import json
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import sk_tools.yt_function as yt_func
# from pathlib import Path
# from langchain_core.messages.base import TextAccessor

LANG = "Hindi"
MODEL = "gemma4:31b-cloud" #"llama3.2:1b"
# Example usage
parser = StrOutputParser()
llm = ChatOllama(model=MODEL, temperature=0.1)
chat_template = ChatPromptTemplate([
    ('system', 'You are an expert in {lang} Scriptwriting for faceless YouTube channels videos.'),
    ('human', """Split this script into logical segments for image visuals.
    Output JSON list with list of dictionaries containing keys - 'text', 'visual_prompt' (detailed image prompt), 'approx_duration' (seconds).
    Total should match ~{audio_duration}s if provided.
    Script: {full_script}""")
])

# Function to segment script into logical segments for visuals:
def segment_script(full_script: str, audio_duration: float = None):
    chain = chat_template | llm | parser
    print("Invoking Chain for segmentation...")
    response = chain.invoke({'lang':LANG,'full_script':full_script,'audio_duration':audio_duration})
    return response

# Read Script:
with open('output/cleaned_script.txt', 'r', encoding='utf-8') as f:
    your_script_text = f.read()

chain = chat_template | llm | parser
segments = segment_script(your_script_text, audio_duration=63)  # Assuming 63 seconds of audio
segments = segments.replace("```json","").replace("```","").strip()  # Clean up any code block formatting
segments = json.loads(segments)  # Parse the JSON string into a Python object

print("Type: ",type(segments))
print("Segments:", segments)

# Save to json file:
yt_func.saveListToJson(segments, 'output/segments.json')

# # Read from json file:
# retrieved_data = yt_func.readListFromJson('output/segments.json')

print("File saved.")
# print("Retrieved Data:", retrieved_data)