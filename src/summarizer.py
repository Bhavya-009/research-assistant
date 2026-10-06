import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Initialize Gemini through LangChain
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
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

Identify the most important research gap and a practical potential
research direction.

Return EXACTLY in this format:

RESEARCH GAP:
<2-4 sentence explanation of the research gap>

POTENTIAL RESEARCH DIRECTION:
<2-4 sentence explanation of a possible research direction>

LIMITATIONS:
<2-4 sentence explanation of the limitations that lead to this gap>

Do not add any other sections.
Keep the language simple and suitable for a college research project.
Only mention gaps that can reasonably be inferred from the papers.
Do not present the potential direction as a proven solution.
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "papers_text": papers_text
    })

    return response.content

def analyze_paper_relationship(
    original_paper,
    related_paper
):
    prompt = ChatPromptTemplate.from_template(
        """
You are a research assistant.

Compare these two research papers and determine how they
are related.

ORIGINAL PAPER
Title:
{original_title}

Abstract:
{original_abstract}


RELATED PAPER
Title:
{related_title}

Abstract:
{related_abstract}


Choose the MOST appropriate relationship from:

1. Same Problem
2. Similar Methodology
3. Extension of Previous Work
4. Improvement over Previous Work
5. Different Approach to Same Problem
6. Weakly Related
7. Not Clearly Related

Then explain the relationship in 1-2 simple sentences.

Return exactly this format:

Relationship: <one category>

Explanation: <1-2 sentences>
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "original_title": original_paper["title"],
        "original_abstract": original_paper["summary"],
        "related_title": related_paper["title"],
        "related_abstract": related_paper["summary"]
    })

    return response.content

def generate_research_direction(gap, direction, papers_text):

    prompt = ChatPromptTemplate.from_template(
        """
You are a research assistant helping a college student
convert a research gap into a practical research proposal.

Research Gap:
{gap}

Potential Research Direction:
{direction}

Related Papers:
{papers_text}

Generate a focused research question and a practical methodology.

Return EXACTLY this format:

RESEARCH QUESTION:
<one clear and specific research question>

METHODOLOGY:
1. Dataset / Data Collection:
<what data is required and where it can be obtained>

2. Proposed Approach:
<models, algorithms, agents, or techniques that could be used>

3. Evaluation:
<metrics and experiments that can be used to evaluate the approach>

4. Baseline:
<what existing approach or method should be used for comparison>

5. Expected Outcome:
<what the research aims to demonstrate>

Keep the proposal realistic for a college research project.
Do not claim that the proposed approach will definitely work.
Do not invent experimental results.
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "gap": gap,
        "direction": direction,
        "papers_text": papers_text
    })

    return response.content