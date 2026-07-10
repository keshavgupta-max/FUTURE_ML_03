import streamlit as st
import os
from src.extractor import ResumeExtractor
from src.scoring import ExplainableScorer

st.set_page_config(page_title="AI Profiler Coach", layout="wide")

if st.button("Return to Main Gateway"):
    st.switch_page("app.py")

st.title("Technical Profile Coach")
st.caption("Review document architectures against baseline industry tracking parameters.")
st.divider()

extractor = ResumeExtractor()
scorer = ExplainableScorer()

col1, col2 = st.columns([2, 3], gap="large")

with col1:
    st.subheader("Profile Submissions")
    with st.container(border=True):
        uploaded_file = st.file_uploader("Upload Active Evaluation Document (PDF)", type=["pdf"])
        job_description = st.text_area("Target Job Attributes", placeholder="Paste required position criteria here...", height=250)
        st.markdown("---")
        submit = st.button("Analyze Optimization Roadmap", use_container_width=True, type="primary")

with col2:
    st.subheader("Structural Optimization Strategy")
    if submit and uploaded_file and job_description.strip():
        with st.spinner("Analyzing document vocabulary..."):
            temp_path = f"temp_cand_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            raw_text = extractor.extract_raw_text(temp_path)
            structured = extractor.zone_resume(raw_text)
            structured["raw_full_text"] = raw_text
            os.remove(temp_path)
            
            report = scorer.evaluate_fit(structured, job_description)
            plan = report["candidate_action_plan"]
            
            st.markdown("#### Layout Integrity Remediations")
            for change in plan['formatting_and_layout_changes']:
                if "CRITICAL" in change:
                    st.error(change)
                else:
                    st.warning(change)
            
            st.divider()
            
            st.markdown("#### Target Vocabulary Modifications")
            if plan['skills_to_add']:
                st.write("Incorporate these precise technical keywords into your experience/project bullet points:")
                for tip in plan['skills_to_add']:
                    st.info(tip)
            else:
                st.success("Excellent! Your vocabulary covers all baseline skills required for this position.")
    else:
        st.info("Input tracking profiles to generate customized optimization roadmaps.")

