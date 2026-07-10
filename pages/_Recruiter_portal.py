import streamlit as st
import os
from src.extractor import ResumeExtractor
from src.scoring import ExplainableScorer

st.set_page_config(page_title="Recruiter Core Dashboard", layout="wide")

if st.button("Return to Main Gateway"):
    st.switch_page("app.py")

st.title("Recruiter Verification Dashboard")
st.caption("Algorithmic screening matrix analyzing candidate attributes and semantic relevance.")
st.divider()

extractor = ResumeExtractor()
scorer = ExplainableScorer()

col1, col2 = st.columns([2, 3], gap="large")

with col1:
    st.subheader("Data Configuration")
    with st.container(border=True):
        uploaded_file = st.file_uploader("Upload Evaluation Resume (PDF format)", type=["pdf"])
        job_description = st.text_area("Hiring Parameters / Requirements", placeholder="Paste destination job description here...", height=250)
        st.markdown("---")
        submit = st.button("Execute Profile Assessment", use_container_width=True, type="primary")

with col2:
    st.subheader("System Alignment Profile")
    if submit and uploaded_file and job_description.strip():
        with st.spinner("Processing architectural metrics..."):
            temp_path = f"temp_rec_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            raw_text = extractor.extract_raw_text(temp_path)
            structured = extractor.zone_resume(raw_text)
            structured["raw_full_text"] = raw_text
            os.remove(temp_path)
            
            report = scorer.evaluate_fit(structured, job_description)
            brief = report["recruiter_brief"]
            
            # KPI Metrics Display Grid
            m1, m2, m3 = st.columns(3)
            m1.metric("Overall Fit Score", f"{report['overall_match_score']}%")
            m2.metric("Context Alignment", brief['experience_context_alignment'])
            m3.metric("Recruiting Risk Profile", brief['risk_factor'])
            
            st.divider()
            
            # Matrix Analysis Fields
            st.markdown("#### Competency Map Verification")
            
            with st.expander("Verified Candidate Capabilities", expanded=True):
                if brief['verified_skills_present']:
                    st.write(", ".join(brief['verified_skills_present']))
                else:
                    st.caption("No matching core capability tags detected.")
                    
            with st.expander("Flagged Domain Gaps / Deficiencies", expanded=True):
                if brief['missing_requirements']:
                    st.write(", ".join(brief['missing_requirements']))
                else:
                    st.caption("Zero gaps flagged against target criteria.")
    else:
        st.info("Awaiting input arrays. Populate the configuration parameters to initialize metrics.")