import streamlit as st
from dotenv import load_dotenv

from src.paper_search import search_papers
from src.related_papers import find_related_papers
from src.summarizer import (
    summarize_paper,
    analyze_paper_relationship
)
from src.storage import save_summary
from src.research_config import (
    load_research_interests,
    save_research_interest
)

load_dotenv()


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Research Assistant Agent",
    page_icon="🔬",
    layout="wide"
)

st.title("Research Assistant Agent")
st.write("Your AI research assistant")


# ==================================================
# SESSION STATE
# ==================================================

if "papers" not in st.session_state:
    st.session_state.papers = []


# ==================================================
# RESEARCH INTERESTS
# ==================================================

st.subheader("Research Interests")

topic = st.text_input(
    "Enter a research interest",
    placeholder="e.g. AI agents, cloud computing, computer vision"
)

if st.button("Add Interest"):

    if not topic.strip():

        st.warning(
            "Please enter a research interest."
        )

    else:

        save_research_interest(
            topic.strip()
        )

        st.success(
            f"'{topic.strip()}' added to your research interests."
        )

        st.rerun()


interests = load_research_interests()


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


# ==================================================
# FIND PAPERS
# ==================================================

st.subheader("Find Papers")

if st.button("Find Papers"):

    if not selected_interest:

        st.warning(
            "Please add and select a research interest first."
        )

    else:

        with st.spinner("Searching for papers..."):

            try:

                st.session_state.papers = search_papers(
                    selected_interest,
                    5
                )

                # Clear previous related-paper results
                keys_to_delete = [
                    key
                    for key in st.session_state.keys()
                    if key.startswith("related_")
                    or key.startswith("relationship_")
                ]

                for key in keys_to_delete:
                    del st.session_state[key]

            except Exception as e:

                st.error(
                    "Unable to search for papers."
                )

                st.warning(
                    f"Search error: {str(e)}"
                )


# ==================================================
# DISPLAY PAPERS
# ==================================================

if st.session_state.papers:

    st.markdown("### Filter Papers")

    access_filter = st.radio(
        "Paper Access",
        [
            "All",
            "Free",
            "Paid",
            "Unknown"
        ],
        horizontal=True
    )

    filtered_papers = []

    for paper in st.session_state.papers:

        access_status = paper.get(
            "access_status",
            "Unknown"
        )

        if (
            access_filter == "All"
            or access_status == access_filter
        ):

            filtered_papers.append(paper)

    st.write(
        f"Showing {len(filtered_papers)} "
        f"of {len(st.session_state.papers)} papers"
    )


    if not filtered_papers:

        st.warning(
            f"No {access_filter.lower()} papers found."
        )


    else:

        for i, paper in enumerate(
            filtered_papers,
            1
        ):

            # ==================================================
            # PAPER TITLE
            # ==================================================

            st.subheader(
                f"{i}. {paper['title']}"
            )


            # ==================================================
            # ACCESS STATUS
            # ==================================================

            access_status = paper.get(
                "access_status",
                "Unknown"
            )

            if access_status == "Free":

                st.success(
                    "🟢 FREE ACCESS"
                )

            elif access_status == "Paid":

                st.error(
                    "🔴 PAID ACCESS"
                )

            else:

                st.warning(
                    "⚪ ACCESS UNKNOWN"
                )


            # ==================================================
            # PAPER INFORMATION
            # ==================================================

            st.write(
                f"**Published:** "
                f"{paper['published']}"
            )

            st.write(
                f"**Authors:** "
                f"{', '.join(paper['authors'])}"
            )


            if paper.get("venue"):

                st.write(
                    f"**Venue:** "
                    f"{paper['venue']}"
                )


            if paper.get("venue_type"):

                st.write(
                    f"**Type:** "
                    f"{paper['venue_type']}"
                )


            # ==================================================
            # ABSTRACT
            # ==================================================

            st.write("### Abstract")

            st.write(
                paper["summary"]
            )


            # ==================================================
            # PAPER LINKS
            # ==================================================

            st.link_button(
                "View Paper",
                paper["url"]
            )


            if paper.get("pdf_url"):

                st.link_button(
                    "Open Free PDF",
                    paper["pdf_url"]
                )


            # ==================================================
            # RELATED PAPERS
            # ==================================================

            if st.button(
                "🔗 Find Related Papers",
                key=f"related_button_{i}"
            ):

                with st.spinner(
                    "Finding related papers..."
                ):

                    try:

                        related = find_related_papers(
                            paper
                        )

                        st.session_state[
                            f"related_{i}"
                        ] = related

                    except Exception as e:

                        st.error(
                            "Unable to find related papers."
                        )

                        st.warning(
                            f"Error: {str(e)}"
                        )


            # ==================================================
            # DISPLAY RELATED PAPERS
            # ==================================================

            if f"related_{i}" in st.session_state:

                related = st.session_state[
                    f"related_{i}"
                ]

                st.subheader(
                    "🔗 Related Papers"
                )


                if not related:

                    st.info(
                        "No related papers found."
                    )


                else:

                    for j, related_paper in enumerate(
                        related,
                        1
                    ):

                        with st.expander(
                            f"{j}. {related_paper['title']}"
                        ):

                            st.write(
                                f"**Authors:** "
                                f"{', '.join(related_paper['authors'])}"
                            )

                            st.write(
                                f"**Published:** "
                                f"{related_paper['published']}"
                            )

                            st.write(
                                "### Abstract"
                            )

                            st.write(
                                related_paper["summary"]
                            )

                            st.link_button(
                                "View Paper",
                                related_paper["url"]
                            )


                            if related_paper.get(
                                "pdf_url"
                            ):

                                st.link_button(
                                    "Open PDF",
                                    related_paper["pdf_url"]
                                )


                            # ==================================================
                            # AI RELATIONSHIP ANALYSIS
                            # ==================================================

                            if st.button(
                                "🤖 Analyze Relationship",
                                key=f"relationship_button_{i}_{j}"
                            ):

                                with st.spinner(
                                    "AI is analyzing the relationship..."
                                ):

                                    try:

                                        relationship = (
                                            analyze_paper_relationship(
                                                paper,
                                                related_paper
                                            )
                                        )

                                        st.session_state[
                                            f"relationship_{i}_{j}"
                                        ] = relationship

                                    except Exception as e:

                                        st.error(
                                            "Unable to analyze the relationship."
                                        )

                                        st.warning(
                                            f"API/Model error: {str(e)}"
                                        )


                            if (
                                f"relationship_{i}_{j}"
                                in st.session_state
                            ):

                                st.subheader(
                                    "🔎 Relationship Analysis"
                                )

                                st.write(
                                    st.session_state[
                                        f"relationship_{i}_{j}"
                                    ]
                                )


            # ==================================================
            # AI SUMMARY
            # ==================================================

            if st.button(
                "Summarize",
                key=f"summary_button_{i}"
            ):

                with st.spinner(
                    "Generating AI summary..."
                ):

                    try:

                        summary = summarize_paper(
                            paper["title"],
                            paper["summary"]
                        )

                        st.session_state[
                            f"summary_{i}"
                        ] = summary

                    except Exception as e:

                        st.error(
                            "Unable to generate the AI summary."
                        )

                        st.warning(
                            f"API/Model error: {str(e)}"
                        )


            # ==================================================
            # DISPLAY AI SUMMARY
            # ==================================================

            if f"summary_{i}" in st.session_state:

                st.subheader(
                    "AI Summary"
                )

                st.write(
                    st.session_state[
                        f"summary_{i}"
                    ]
                )


                # ==================================================
                # SAVE TO MY RESEARCH
                # ==================================================

                if st.button(
                    "Save to My Research",
                    key=f"save_{i}"
                ):

                    save_summary(
                        paper,
                        st.session_state[
                            f"summary_{i}"
                        ]
                    )

                    st.success(
                        "Summary saved to your research collection."
                    )


            st.divider()