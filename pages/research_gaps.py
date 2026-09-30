import streamlit as st
from dotenv import load_dotenv

from src.research_library import load_saved_summaries
from src.summarizer import find_research_gaps


load_dotenv()


st.title("Research Gaps")

st.write(
    "Select research papers and use AI to identify potential research gaps."
)


# Load saved papers
saved_summaries = load_saved_summaries()


# Need at least 2 papers
if len(saved_summaries) < 2:

    st.info(
        "Save at least 2 research papers to identify research gaps."
    )

else:

    st.success(
        f"{len(saved_summaries)} saved papers available."
    )


    # Select papers
    paper_options = [
        paper["title"]
        for paper in saved_summaries
    ]


    selected_titles = st.multiselect(
        "Select papers to compare",
        paper_options,
        default=paper_options
    )


    # Get selected papers
    selected_papers = [
        paper
        for paper in saved_summaries
        if paper["title"] in selected_titles
    ]


    st.divider()


    # Check number of selected papers
    if len(selected_papers) < 2:

        st.warning(
            "Select at least 2 papers for comparison."
        )


    else:

        st.subheader("Selected Papers")


        # Display selected papers
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

                st.write(
                    paper["summary"]
                )

                st.link_button(
                    "View Paper",
                    paper["url"]
                )


        st.divider()


        # Test rate limit option
        simulate_rate_limit = st.checkbox(
            "Test rate limit error"
        )


        # Find Research Gaps button
        if st.button("Find Research Gaps"):

            # Manual rate-limit simulation
            if simulate_rate_limit:

                st.error(
                    "⚠️ Gemini API rate limit reached. "
                    "Please try again later."
                )


            else:

                # Prepare paper summaries
                papers_text = ""


                for i, paper in enumerate(selected_papers, 1):

                    papers_text += f"""
Paper {i}
Title: {paper["title"]}

Summary:
{paper["summary"]}

-------------------------
"""


                # Call AI
                with st.spinner(
                    "AI is analyzing the selected papers..."
                ):

                    try:

                        result = find_research_gaps(
                            papers_text
                        )


                        st.subheader(
                            "Research Gap Analysis"
                        )

                        st.write(
                            result
                        )


                    except Exception as e:

                        st.error(
                            "Unable to generate the research gap analysis."
                        )

                        st.warning(
                            f"API/Model error: {str(e)}"
                        )