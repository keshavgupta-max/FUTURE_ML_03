import fitz  # PyMuPDF
import re

class ResumeExtractor:
    def __init__(self):
        # Block A: Header Mapping Dictionary
        self.zone_keywords = {
            "skills": ["skills", "technical skills", "core competencies", "technologies", "expertise"],
            "experience": ["experience", "work experience", "professional experience", "employment history", "projects"],
            "education": ["education", "academic background", "qualifications"]
        }

    def extract_raw_text(self, pdf_path: str) -> str:
        # Block B: Spatial Coordinate Text Extraction
        doc = fitz.open(pdf_path)
        full_text = []
        
        for page in doc:
            blocks = page.get_text("blocks")
            blocks.sort(key=lambda b: (b[1], b[0]))
            
            for b in blocks:
                text_block = b[4].strip()
                if text_block:
                    full_text.append(text_block)
                    
        return "\n".join(full_text)

    def zone_resume(self, text: str) -> dict:
        # Block C: Structural Zoning Slicer
        lines = text.split("\n")
        zones = {
            "contact_and_about": [],
            "skills": [],
            "experience": [],
            "education": []
        }
        
        current_zone = "contact_and_about"
        
        for line in lines:
            clean_line = line.strip().lower()
            clean_line = re.sub(r'[^a-z\s]', '', clean_line).strip()
            
            header_found = False
            for zone_name, keywords in self.zone_keywords.items():
                if clean_line in keywords and len(clean_line) < 30:
                    current_zone = zone_name
                    header_found = True
                    break
            
            if header_found:
                continue
                
            zones[current_zone].append(line)
            
        return {k: "\n".join(v).strip() for k, v in zones.items()}