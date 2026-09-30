import streamlit as st
from src.research_library import load_saved_summaries

st.title("My Research")

st.write("Your saved research papers and AI summaries.")

saved_summaries = load_saved_summaries()

if not saved_summaries:

    st.info("You haven't saved any research papers yet.")

else:

    st.success(f"{len(saved_summaries)} saved paper(s)")

    for i, paper in enumerate(saved_summaries, 1):

        with st.expander(paper["title"]):

            st.write(
                f"**Authors:** {', '.join(paper['authors'])}"
            )

            st.write(
                f"**Published:** {paper['published']}"
            )

            st.write(
                f"**Saved:** {paper['saved_at']}"
            )

            st.divider()

            st.subheader("AI Summary")

            st.write(paper["summary"])

            st.link_button(
                "View Paper",
                paper["url"]
            )