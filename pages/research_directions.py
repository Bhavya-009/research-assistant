import streamlit as st

from src.storage import (
    load_research_gaps,
    update_research_gap_status,
    save_research_proposal
)

from src.summarizer import generate_research_direction


st.title("Research Directions")

st.write(
    "Explore and track research gaps identified from your saved papers."
)


# ==================================================
# LOAD SAVED RESEARCH GAPS
# ==================================================

gaps = load_research_gaps()


if not gaps:

    st.info(
        "You haven't saved any research gaps yet."
    )

else:

    st.success(
        f"{len(gaps)} research gap(s) saved."
    )


    # ==================================================
    # STATUS OPTIONS
    # ==================================================

    statuses = [
        "New",
        "Exploring",
        "Addressed"
    ]


    # ==================================================
    # DISPLAY EACH RESEARCH GAP
    # ==================================================

    for i, item in enumerate(gaps):

        with st.expander(
            f"Research Gap {i + 1}"
        ):

            # ------------------------------------------
            # RESEARCH GAP
            # ------------------------------------------

            st.subheader("Research Gap")

            st.write(
                item["gap"]
            )


            # ------------------------------------------
            # POTENTIAL RESEARCH DIRECTION
            # ------------------------------------------

            st.subheader(
                "Potential Research Direction"
            )

            st.write(
                item["direction"]
            )


            # ------------------------------------------
            # RELATED PAPERS
            # ------------------------------------------

            st.subheader(
                "Related Papers"
            )

            for paper in item["papers"]:

                st.write(
                    f"• {paper}"
                )


            st.divider()


            # ==================================================
            # STATUS
            # ==================================================

            current_status = item.get(
                "status",
                "New"
            )

            new_status = st.selectbox(
                "Status",
                statuses,

                index=(
                    statuses.index(current_status)
                    if current_status in statuses
                    else 0
                ),

                key=f"status_{i}"
            )


            if new_status != current_status:

                update_research_gap_status(
                    i,
                    new_status
                )

                st.success(
                    f"Status updated to {new_status}."
                )

                st.rerun()


            # ==================================================
            # RESEARCH QUESTION + METHODOLOGY
            # ==================================================

            st.divider()

            st.subheader(
                "Research Question & Methodology"
            )


            # Generate button
            if st.button(
                "🤖 Generate Research Proposal",
                key=f"generate_proposal_{i}"
            ):

                # Prepare related papers
                papers_text = "\n".join(
                    f"- {paper}"
                    for paper in item["papers"]
                )


                with st.spinner(
                    "AI is generating the research question and methodology..."
                ):

                    try:

                        result = generate_research_direction(

                            gap=item["gap"],

                            direction=item["direction"],

                            papers_text=papers_text

                        )


                        # Store result temporarily
                        st.session_state[
                            f"proposal_{i}"
                        ] = result

                        save_research_proposal(
                            i,
                            result
                        )


                    except Exception as e:

                        st.error(
                            "Unable to generate the research proposal."
                        )

                        st.warning(
                            f"API/Model error: {str(e)}"
                        )


            # ------------------------------------------
            # DISPLAY GENERATED PROPOSAL
            # ------------------------------------------

            saved_proposal = item.get("research_proposal")

            if saved_proposal:
                st.write(saved_proposal)
            elif f"proposal_{i}" in st.session_state:
                st.write(st.session_state[f"proposal_{i}"])


            # ==================================================
            # CREATED DATE
            # ==================================================

            st.caption(
                f"Created: {item['created_at']}"
            )