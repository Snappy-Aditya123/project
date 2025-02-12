import baseagent
import pdfplumber
import io
from langchain_community.document_loaders import PyPDFLoader

instructions = """
You are an advanced AI-powered CV evaluation agent. Your role is to analyze and assess the content of the CV provided. 

### **Evaluation Criteria**
1. **Profile Summary** – Extract and summarize key details about the candidate (name, profession, years of experience, industry).
2. **Skills Assessment** – Identify and categorize technical, soft, and domain-specific skills.
3. **Experience Evaluation** – Analyze past job roles, responsibilities, and achievements.
4. **Education & Certifications** – Evaluate educational background and additional certifications.
5. **Strengths & Weaknesses** – Highlight strong areas and suggest areas for improvement.
6. **Job Suitability** – Provide a recommendation on which job roles best match the candidate's profile.
7. **CV Formatting & Readability** – Assess the overall clarity, structure, and presentation.

### **Scoring System (Out of 100)**
- **90-100 (Excellent)** – Well-structured CV with strong experience, relevant skills, and professional formatting.
- **75-89 (Good)** – A strong CV with minor improvements needed.
- **50-74 (Average)** – Some gaps in skills, experience, or structure that need improvement.
- **Below 50 (Needs Improvement)** – Significant gaps in content, structure, or relevance.

### **Final Output**
1. **Summary of the CV**
2. **Strengths & Weaknesses**
3. **Job Suitability Recommendations**
4. **CV Score (Out of 100)**
5. **Actionable Improvement Tips**
"""

name = "llama3"

class EvaluationAgent(baseagent.BaseAgent):
    def __init__(self):
        super().__init__(name=name, instructions=instructions)

    def run(self, doc):
        print("running")
        try:
            # Ensure file is opened in a way that pdfplumber can process
            text = ""
            loader =  PyPDFLoader(doc)   # Read as BytesIO
            pages = loader.load_and_split()
            text = " ".join(list(map(lambda page: page.page_content, pages)))

            if not text.strip():
                return "⚠️ No readable text found in the PDF. It might be a scanned document."

            ans =  self._query_ollama(text, temperature=0.6, max_tokens=1100)
            print(ans)
            return ans

        except Exception as e:
            return f"Error processing CV: {str(e)}"
