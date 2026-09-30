import streamlit as st
from dotenv import load_dotenv
from google import genai
from paper_search import search_papers
import os

load_dotenv()

st.title("Research Assistant Agent")
st.write("Your AI research assistant")

# Research interest
topic = st.text_input(
    "Enter your research interest",
    placeholder="e.g. AI agents, cloud computing, computer vision"
)

if st.button("Find Papers"):

    if not topic:
        st.warning("Please enter a research interest.")

    else:
        st.write("Searching for papers...")

        papers = search_papers(topic, 5)

        if not papers:
            st.warning("No papers found.")

        else:
            st.success(f"Found {len(papers)} papers")

            for i, paper in enumerate(papers, 1):

                st.subheader(f"{i}. {paper['title']}")

                st.write(
                    f"**Published:** {paper['published']}"
                )

                st.write(
                    f"**Authors:** {', '.join(paper['authors'])}"
                )

                st.write(paper["summary"])

                st.link_button(
                    "View Paper",
                    paper["url"]
                )

                st.divider()