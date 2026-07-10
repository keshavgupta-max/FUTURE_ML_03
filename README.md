
# Nexus AI: Dual-Perspective Explainable Resume Screener & Career Advisor

Nexus AI is an enterprise-grade Talent Suite designed to break the black box of traditional Applicant Tracking Systems (ATS). Instead of simple, unexplainable keyword matching, this platform zones document layout elements using raw coordinate parsing and evaluates profile matching via multi-objective mathematical weights. 

Crucially, the architecture enforces complete structural isolation between the employer's internal risk assessment and the candidate's developmental optimization roadmap.

---

## System Architecture & Data Flow

The platform is designed around a clean, modular Python architecture split into a core processing engine and an interactive user presentation layer:

```text
nexus-ai-talent-suite/
│
├── app.py                     # Main Gateway (Role Selection Landing UI)
├── pages/
│   ├── _Recruiter_portal.py   # Secure Internal Employer Metrics Console
│   └── _Candidate_coach.py    # Isolated Applicant Career Optimization Panel
│
├── config/
│   └── skills_dictionary.json # Token Map Vocabulary Dictionary
│
└── src/
    ├── __init__.py            # Python Package Initialization Trigger
    ├── extractor.py           # Document Ingestion & Structural Zoner Engine
    └── scoring.py             # Multi-Objective Analytics & Context Matcher