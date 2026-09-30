import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


# Initialize Gemini through LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)


def summarize_paper(title, abstract):

    prompt = ChatPromptTemplate.from_template(
        """
You are a research assistant.

Summarize the following research paper in simple language.

Title:
{title}

Abstract:
{abstract}

Give the answer in this format:

1. Problem
2. Solution
3. Key Findings
4. Research Gap

Keep the explanation concise and easy to understand.
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "title": title,
        "abstract": abstract
    })

    return response.content


def find_research_gaps(papers_text):

    prompt = ChatPromptTemplate.from_template(
        """
You are a research assistant analyzing multiple research papers.

Analyze the following papers:

{papers_text}

Identify:

1. Common Problems
2. Common Approaches
3. Limitations
4. Potential Research Gaps
5. Future Research Directions

Keep the analysis simple, concise, and suitable for a college research project.
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "papers_text": papers_text
    })

    return response.content