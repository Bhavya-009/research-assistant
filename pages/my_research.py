import streamlit as st

from src.research_library import load_saved_summaries


st.title("Research Gaps")

st.write(
    "Select research papers to compare and identify potential research gaps."
)


# Load saved papers
saved_summaries = load_saved_summaries()


if len(saved_summaries) < 2:

    st.info(
        "Save at least 2 research papers to compare them."
    )

else:

    st.success(
        f"{len(saved_summaries)} saved papers available."
    )

    # Paper selection
    paper_options = [
        paper["title"]
        for paper in saved_summaries
    ]

    selected_titles = st.multiselect(
        "Select papers to compare",
        paper_options,
        default=paper_options
    )

    selected_papers = [
        paper
        for paper in saved_summaries
        if paper["title"] in selected_titles
    ]

    st.divider()

    # Display selected papers
    st.subheader("Selected Papers")

    if not selected_papers:

        st.info("Select at least 2 papers.")

    elif len(selected_papers) < 2:

        st.warning(
            "Select at least 2 papers for comparison."
        )

    else:

        for i, paper in enumerate(selected_papers, 1):

            with st.expander(
                f"{i}. {paper['title']}"
            ):

                st.write(
                    f"**Authors:** {', '.join(paper['authors'])}"
                )

                st.write(
                    f"**Published:** {paper['published']}"
                )

                st.write("### Summary")

                st.write(paper["summary"])

                st.link_button(
                    "View Paper",
                    paper["url"]
                )

        st.divider()

        st.subheader("Research Gap Analysis")

        st.info(
            "AI-based comparison will be added here once the Gemini API is available."
        )