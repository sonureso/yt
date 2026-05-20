"""
STEP-1: Get news titles from various sources.
STEP-2: Prompt LLM to generate best YT Title for a video on topic.
"""

from gnews import GNews
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

# Set the logging level for httpx to WARNING or higher to hide INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)

## ********************************************************* ##
## Useful Functions
## ********************************************************* ##
def get_gnews_trends(hint='',region='US',lang='en',limit=3):
    # https://pypi.org/project/gnews/
    news = []
    limit = limit if limit>=3 else 3
    google_news = GNews(language=lang, country=region,period='7d',
                         max_results=10,exclude_websites=['yahoo.com', 'cnn.com'])
    trending_news = google_news.get_news(hint) if len(hint) > 3 else google_news.get_top_news()
    for article in trending_news[:limit]:
        news.append(article)
    return news


## ********************************************************* ##
## AI Related Things:
## ********************************************************* ##
chat_template = ChatPromptTemplate([
    ('system', 'You are an expert in Content Writing, YouTube Title, Description and SEO Management.'),
    ('human', "For a video around the new things in topic: '{topic}'. I want a short and eye catchy title for my YouTube Video."
    "- I want clear words to form the title. Respond with only Video title, nothing else. Use maximum of 15 words and minimum of 9 words.")
])

def refine_with_ollama(titles):
    refined_titles = []
    llm = ChatOllama(model="llama3.2:1b", temperature=0.2)
    parser = StrOutputParser()
    chain = chat_template | llm | parser
    for topic in titles:
        response = chain.invoke({'topic':topic})
        refined_titles.append(response)
    return refined_titles

## ********************************************************* ##
## general functions
## ********************************************************* ##
def print_list(str_list):
    print("==="*21)
    for i,s in enumerate(str_list):
        s = s.replace("\"","").replace("'","")
        print(f"{i}: {s}")
    print("==="*21)



## ********************************************************* ##
## main
## ********************************************************* ##
if __name__ == "__main__":
    print("01. Fetching News from gnews.")
    news = get_gnews_trends(hint='Top 3',region='IN',lang='en',limit=2)
    news_titles = ["-".join(n['title'].split("-")[:-1]) for n in news]
    print(f"02. Got {len(news_titles)} news titles:")
    print_list(news_titles)
    print(f"03. Refining with LLMs.")
    refined_titles = refine_with_ollama(news_titles)
    print_list(refined_titles)
    

