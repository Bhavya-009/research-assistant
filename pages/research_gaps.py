import streamlit as st
from dotenv import load_dotenv

from src.research_library import load_saved_summaries
from src.summarizer import find_research_gaps
from src.storage import save_research_gap

load_dotenv()

st.title("Research Gaps")

st.write(
    "Select research papers and use AI to identify potential research gaps."
)

# Load saved papers
saved_summaries = load_saved_summaries()

# Initialize session state
if "research_gap_result" not in st.session_state:
    st.session_state.research_gap_result = None

if "research_gap_papers" not in st.session_state:
    st.session_state.research_gap_papers = []


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

        # Find Research Gaps
        if st.button("Find Research Gaps"):

            if simulate_rate_limit:

                st.error(
                    "⚠️ API rate limit reached. "
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

                        # Store result in session state
                        st.session_state.research_gap_result = result

                        # Store selected papers
                        st.session_state.research_gap_papers = [
                            paper["title"]
                            for paper in selected_papers
                        ]

                    except Exception as e:

                        st.error(
                            "Unable to generate the research gap analysis."
                        )

                        st.warning(
                            f"API/Model error: {str(e)}"
                        )


        # Display saved AI result
        if st.session_state.research_gap_result:

            st.subheader("Research Gap Analysis")

            st.write(
                st.session_state.research_gap_result
            )

            st.divider()

            # Save button is now OUTSIDE the Find Research Gaps button
            if st.button("💾 Save This Research Gap"):

                result = st.session_state.research_gap_result

                # Extract sections from AI response
                gap = result.split("POTENTIAL RESEARCH DIRECTION:")[0]
                gap = gap.replace("RESEARCH GAP:", "").strip()

                direction = result.split("POTENTIAL RESEARCH DIRECTION:")[1]

                if "LIMITATIONS:" in direction:
                    direction = direction.split("LIMITATIONS:")[0]

                direction = direction.strip()

                save_research_gap(
                    gap=gap,
                    direction=direction,
                    papers=st.session_state.research_gap_papers
                )

                st.success(
                    "Research gap saved successfully."
                )