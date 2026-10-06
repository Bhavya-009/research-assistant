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
You are a research assistant helping a college student identify
research opportunities from existing papers.

Analyze the following research papers:

{papers_text}

Provide the analysis using exactly these sections:

1. Common Problem
Explain the main problem addressed across the papers.

2. Existing Approaches
Describe the main technologies or approaches used.

3. Limitations
Identify important limitations or unresolved issues.

4. Research Gaps
Identify areas that are not adequately addressed by the existing papers.
Only mention gaps that can reasonably be inferred from the papers.

5. Potential Research Direction
Suggest a practical research direction based on the identified gaps.
Do not present it as a proven solution.

6. Paper Relationship
Explain briefly how the selected papers are related to each other.

Keep the language simple and suitable for a college research project.
Avoid making unsupported claims.
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "papers_text": papers_text
    })

    return response.content