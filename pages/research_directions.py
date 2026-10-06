import streamlit as st

from src.storage import (
    load_research_gaps,
    update_research_gap_status
)

st.title("Research Directions")

st.write(
    "Explore and track research gaps identified from your saved papers."
)

gaps = load_research_gaps()

if not gaps:

    st.info(
        "You haven't saved any research gaps yet."
    )

else:

    st.success(
        f"{len(gaps)} research gap(s) saved."
    )

    statuses = [
        "New",
        "Exploring",
        "Addressed"
    ]

    for i, item in enumerate(gaps):

        with st.expander(
            f"Research Gap {i + 1}"
        ):

            st.subheader("Research Gap")

            st.write(
                item["gap"]
            )

            st.subheader(
                "Potential Research Direction"
            )

            st.write(
                item["direction"]
            )

            st.subheader(
                "Related Papers"
            )

            for paper in item["papers"]:
                st.write(f"• {paper}")

            st.divider()

            current_status = item.get(
                "status",
                "New"
            )

            new_status = st.selectbox(
                "Status",
                statuses,
                index=statuses.index(current_status)
                if current_status in statuses
                else 0,
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

            st.caption(
                f"Created: {item['created_at']}"
            )