import streamlit as st
from dotenv import load_dotenv

from paper_search import search_papers
from summarizer import summarize_paper
from storage import save_summary
from research_library import load_saved_summaries

load_dotenv()

st.title("Research Assistant Agent")
st.write("Your AI research assistant")

# Store papers between Streamlit reruns
if "papers" not in st.session_state:
    st.session_state.papers = []

# Research interest input
topic = st.text_input(
    "Enter your research interest",
    placeholder="e.g. AI agents, cloud computing, computer vision"
)

# Search papers
if st.button("Find Papers"):

    if not topic:
        st.warning("Please enter a research interest.")

    else:
        with st.spinner("Searching for papers..."):
            st.session_state.papers = search_papers(topic, 5)

# Display papers
if st.session_state.papers:

    st.success(f"Found {len(st.session_state.papers)} papers")

    for i, paper in enumerate(st.session_state.papers, 1):

        st.subheader(f"{i}. {paper['title']}")

        st.write(f"**Published:** {paper['published']}")

        st.write(
            f"**Authors:** {', '.join(paper['authors'])}"
        )

        st.write(paper["summary"])

        st.link_button(
            "View Paper",
            paper["url"]
        )

        # Generate summary
        if st.button("Summarize", key=f"summary_{i}"):

            with st.spinner("Generating AI summary..."):

                summary = summarize_paper(
                    paper["title"],
                    paper["summary"]
                )

            # Store generated summary
            st.session_state[f"summary_{i}"] = summary

        # Display generated summary
        if f"summary_{i}" in st.session_state:

            summary = st.session_state[f"summary_{i}"]

            st.subheader("AI Summary")
            st.write(summary)

            # User decides whether to save
            if st.button(
                "Save to My Research",
                key=f"save_{i}"
            ):

                save_summary(
                    paper,
                    summary
                )

                st.success(
                    "Summary saved to your research collection."
                )

        st.divider()