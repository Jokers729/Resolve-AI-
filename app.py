import streamlit as st
from db import create_table, add_complaint, get_complaints
from clustering import cluster_complaints

st.set_page_config(
    page_title="ResolveAI",
    page_icon="🧩",
    layout="wide"
)

create_table()

st.title("🧩 ResolveAI")
st.subheader("Smart Complaint Clustering System")
st.write("Submit and track individual complaints.")

st.divider()

st.header("📊 Complaint Dashboard")

complaints = get_complaints()

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Complaints", len(complaints))

with col2:
    pending = sum(1 for c in complaints if c[4] == "Pending")
    st.metric("Pending Complaints", pending)

st.divider()

st.header("📝 Submit a Complaint")

with st.form("complaint_form"):
    description = st.text_area("Describe your complaint")
    location = st.text_input("Location or Ward")

    category = st.selectbox(
        "Complaint Category",
        [
            "Road Damage",
            "Street Light",
            "Water Supply",
            "Garbage",
            "Drainage",
            "Electricity",
            "Other"
        ]
    )

    submitted = st.form_submit_button("Submit Complaint")

    if submitted:
        if description.strip() and location.strip():
            add_complaint(
                description.strip(),
                location.strip(),
                category
            )
            st.success("Complaint saved successfully!")
            st.rerun()
        else:
            st.error("Please fill in both fields.")

st.divider()
st.divider()

st.header("🧩 Smart Complaint Clustering")

if st.button("Find Similar Complaints"):
    complaints = get_complaints()

    if not complaints:
        st.info("First submit some complaints.")
    else:
        groups = cluster_complaints(complaints)

        st.success(
            f"Found {len(groups)} complaint groups."
        )

        for group_name, reports in groups.items():
            with st.expander(
                f"{group_name} ({len(reports)} reports)"
            ):
                for report in reports:
                    st.write(
                        f"Report #{report[0]} — {report[3]}"
                    )
                    st.write(
                        "Description:", report[1]
                    )
                    st.write(
                        "Location:", report[2]
                    )
                    st.write(
                        "Status:", report[4]
                    )
                    st.divider()
st.header("📋 Individual Reports")

if complaints:
    for complaint in get_complaints():
        with st.expander(
            f"Complaint #{complaint[0]} — {complaint[3]}"
        ):
            st.write("Description:", complaint[1])
            st.write("Location:", complaint[2])
            st.write("Category:", complaint[3])
            st.write("Status:", complaint[4])
else:
    st.info("No complaints yet. Submit your first complaint.")