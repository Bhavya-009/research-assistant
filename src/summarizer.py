from google import genai
import os


def summarize_paper(title, abstract):

    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = f"""
Summarize this research paper in simple language.

Title:
{title}

Abstract:
{abstract}

Give:

1. Problem
2. Solution
3. Key Findings
4. Research Gap
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text


def find_research_gaps(papers_text):

    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = f"""
You are a research assistant.

Analyze the following research papers:

{papers_text}

Identify:

1. Common Problems
2. Common Approaches
3. Limitations
4. Potential Research Gaps
5. Future Research Direction

Keep the answer simple and concise.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text