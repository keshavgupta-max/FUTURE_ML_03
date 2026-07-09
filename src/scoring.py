import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ExplainableScorer:
    def __init__(self, dict_path="config/skills_dictionary.json"):
        # Block D: Dictionary Initialization
        try:
            with open(dict_path, 'r') as f:
                self.skills_map = json.load(f)
        except FileNotFoundError:
            self.skills_map = {}

    def _extract_mapped_skills(self, text: str) -> set:
        # Block E: Token Protection Matcher
        found_skills = set()
        text_lower = text.lower()
        
        for skill_key, synonyms in self.skills_map.items():
            for synonym in synonyms:
                pattern = r'\b' + re.escape(synonym) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.add(skill_key)
                    break
        return found_skills

    def evaluate_fit(self, structured_resume: dict, job_description: str) -> dict:
        # Block F: Twin Entity Difference Analysis
        jd_skills = self._extract_mapped_skills(job_description)
        resume_skills = self._extract_mapped_skills(structured_resume.get("raw_full_text", ""))
        
        matched = jd_skills.intersection(resume_skills)
        missing = jd_skills.difference(resume_skills)
        
        # Block G: Fragmented TF-IDF Context Matcher
        vectorizer = TfidfVectorizer(stop_words='english')
        exp_score = 0.0
        if structured_resume.get("experience") and job_description.strip():
            try:
                tfidf_matrix = vectorizer.fit_transform([job_description, structured_resume["experience"]])
                exp_score = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
            except ValueError:
                exp_score = 0.0

        # Block H: Layout and Structural Code Auditor
        suggestions = []
        layout_status = "Excellent"
        
        if not structured_resume.get("skills"):
            layout_status = "Needs Improvement"
            suggestions.append("CRITICAL LAYOUT CHANGE: We could not detect an isolated 'Skills' section. Ensure your resume contains a distinct header named 'Technical Skills'.")
            
        if not structured_resume.get("experience"):
            layout_status = "Needs Improvement"
            suggestions.append("CRITICAL LAYOUT CHANGE: No clear 'Experience' or 'Projects' section header was found. Use explicit titles like 'Professional Experience' or 'Projects'.")
            
        if len(structured_resume.get("experience", "")) < 150 and structured_resume.get("experience"):
            suggestions.append("CONTENT IMPROVEMENT: Your project/experience descriptions are exceptionally short. Expand them by explaining the core environment setup, execution steps, and quantifiable results.")

        # Block I: Mathematical Multi-Objective Scoring
        readable_missing = [skill.replace("SKILL_", "") for skill in missing]
        readable_matched = [skill.replace("SKILL_", "") for skill in matched]
        
        overall_score = (len(matched) / len(jd_skills) * 60) + (exp_score * 40) if jd_skills else exp_score * 100

        # Block J: Double-Sided Output Generation
        return {
            "overall_match_score": round(overall_score, 1),
            "layout_integrity": layout_status,
            "recruiter_brief": {
                "verified_skills_present": readable_matched,
                "missing_requirements": readable_missing,
                "experience_context_alignment": f"{round(exp_score * 100, 1)}%",
                "risk_factor": "High" if len(readable_missing) > 2 or layout_status == "Needs Improvement" else "Low"
            },
            "candidate_action_plan": {
                "skills_to_add": [f"Gain or list proficiency in {s}" for s in readable_missing],
                "formatting_and_layout_changes": suggestions if suggestions else ["Layout structure is clean and parsed perfectly by corporate ATS applications."]
            }
        }