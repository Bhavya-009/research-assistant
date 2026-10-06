import streamlit as st
from dotenv import load_dotenv

from src.paper_search import search_papers
from src.summarizer import summarize_paper
from src.storage import save_summary
from src.research_config import (
    load_research_interests,
    save_research_interest
)

load_dotenv()

st.title("Research Assistant Agent")
st.write("Your AI research assistant")


# Store papers between Streamlit reruns
if "papers" not in st.session_state:
    st.session_state.papers = []


# Load saved research interests
interests = load_research_interests()


# --------------------------------------------------
# RESEARCH INTERESTS
# --------------------------------------------------

st.subheader("Research Interests")


topic = st.text_input(
    "Enter a research interest",
    placeholder="e.g. AI agents, cloud computing, computer vision"
)


if st.button("Add Interest"):

    if not topic.strip():

        st.warning("Please enter a research interest.")

    else:

        save_research_interest(topic.strip())

        st.success(
            f"'{topic.strip()}' added to your research interests."
        )

        st.rerun()



if interests:

    selected_interest = st.selectbox(
        "Select an interest to find papers",
        interests
    )

else:

    selected_interest = None

    st.info(
        "Add a research interest before searching for papers."
    )



if st.button("Find Papers"):

    if not selected_interest:

        st.warning(
            "Please add and select a research interest first."
        )

    else:

        with st.spinner("Searching for papers..."):

            st.session_state.papers = search_papers(
                selected_interest,
                5
            )


if st.session_state.papers:

    st.success(
        f"Found {len(st.session_state.papers)} papers"
    )

    for i, paper in enumerate(
        st.session_state.papers,
        1
    ):

        st.subheader(
            f"{i}. {paper['title']}"
        )

        st.write(
            f"**Published:** {paper['published']}"
        )

        st.write(
            f"**Authors:** {', '.join(paper['authors'])}"
        )

        st.write(
            paper["summary"]
        )

        st.link_button(
            "View Paper",
            paper["url"]
        )


        # Generate summary
        if st.button(
            "Summarize",
            key=f"summary_{i}"
        ):

            with st.spinner(
                "Generating AI summary..."
            ):

                summary = summarize_paper(
                    paper["title"],
                    paper["summary"]
                )

            st.session_state[
                f"summary_{i}"
            ] = summary


        # Display summary
        if f"summary_{i}" in st.session_state:

            summary = st.session_state[
                f"summary_{i}"
            ]

            st.subheader("AI Summary")

            st.write(summary)


            # Save summary
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