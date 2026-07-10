import streamlit as st

st.set_page_config(page_title="Nexus AI - Talent Suite", page_icon="🎯", layout="wide")

st.title("Nexus AI")
st.caption("Enterprise Evaluation and Career Optimization Platform")
st.divider()

st.markdown("""
### Welcome to the Nexus AI Suite
Select the operational module below to initialize your workspace session. 
""")

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### Recruiter Assessment Suite")
        st.write(
            "Screen incoming applications against dynamic job metrics. "
            "Access text credibility statistics, domain risk factors, and semantic match alignment vectors."
        )
        st.markdown("---")
        if st.button("Initialize Recruiter Workspace", use_container_width=True, type="primary"):
            st.switch_page("pages/_Recruiter_portal.py")

with col2:
    with st.container(border=True):
        st.markdown("### Candidate Feedback Console")
        st.write(
            "Audit personal documents directly against automated system filters. "
            "Discover missing technical libraries, analyze layout parsing faults, and expand project descriptions."
        )
        st.markdown("---")
        if st.button("Initialize Candidate Workspace", use_container_width=True):
            st.switch_page("pages/_Candidate_coach.py")