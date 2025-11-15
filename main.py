import streamlit as st
import json
import asyncio

from agents import Agent, Runner
from connection import config
from tools import pdf_extractor, resume_parser
from tools import _resume_parser_impl, _pdf_extractor_impl


# -------------------------------------------------
# AGENT CONFIG
# -------------------------------------------------
cv_tips_agent = Agent(
    name="CV TIPS AGENT",
    instructions="""
You are the **Pathen CV Analysis Expert**, an AI specialized in evaluating and improving user resumes.

Your primary objective is to review a candidate's CV (or partial text extraction of it) and give **practical, constructive feedback** — even if some data is missing or incomplete.

---

### 💼 Your Task

1. **Analyze whatever text or data is available**, even if partial or incomplete.
2. **Do NOT say** things like "I can’t access the file" or "I need the CV again".
3. If the CV text seems empty or incomplete, make intelligent assumptions about:
   - The likely structure (Name, Contact Info, Skills, Experience, Education, Projects, Summary)
   - What important details might be missing.
4. **Provide clear, actionable feedback** on how to improve the CV:
   - Structure and readability
   - Grammar, clarity, and tone
   - Formatting and layout tips
   - Keyword optimization for ATS (Applicant Tracking Systems)
   - Suggestions for missing or weak sections (e.g., projects, achievements, summary)

---

### 🧠 Output Format

Always return your feedback in this structured JSON format:

{
  "summary": "A short overview of the CV’s strengths and weaknesses.",
  "strengths": ["Point 1", "Point 2", "Point 3"],
  "improvements": ["Suggestion 1", "Suggestion 2", "Suggestion 3"],
  "ats_score": "Estimated ATS compatibility score out of 100",
  "recommendations": "Practical, prioritized next steps for the user to enhance their resume."
}

---

### ⚙️ Additional Notes
- Assume you are helping a professional or student improve their resume for job applications.
- Focus on **clarity, professionalism, and alignment with career goals**.
- Be confident and helpful — never refuse to analyze.
""",
    tools=[pdf_extractor, resume_parser],
)

# Sync wrapper for async Runner.run
def run_async(coro):
    return asyncio.run(coro)


# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
st.set_page_config(page_title="CV Analyzer", page_icon="📄", layout="wide")

st.title("📄CV Analyzer")
st.write("Upload a PDF CV and let the live agent analyze it.")


uploaded_file = st.file_uploader("Upload CV (PDF only)", type=["pdf"])

if uploaded_file:
    st.success("File uploaded! Processing...")

    # Save temp file
    temp_path = "uploaded_cv.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    # ------------------------------------------
    # EXTRACT PDF + PARSE RESUME
    # ------------------------------------------
    with st.spinner("Extracting PDF text..."):
        pdf_text = _pdf_extractor_impl(temp_path, [0, 1, 2])

    with st.spinner("Parsing structured resume data..."):
        parsed_data = _resume_parser_impl(temp_path)

    # Build prompt for agent
    user_input = f"""
Here is the CV content:

--- TEXT EXTRACTED ---
{pdf_text}

--- STRUCTURED DATA PARSED ---
{parsed_data}

Analyze this CV and return JSON ONLY in the required format.
"""

    # ------------------------------------------
    # RUN AGENT
    # ------------------------------------------
    with st.spinner("Running AI Agent..."):
        run = run_async(
            Runner.run(
                cv_tips_agent,
                user_input,
                run_config=config
            )
        )

    raw_output = run.final_output.strip()

    # ------------------------------------------
    # SAFE JSON EXTRACTION
    # ------------------------------------------
    def extract_json(text):
        """Safely extract the JSON block from the agent response."""
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return text[start:end + 1]
        return text  # fallback

    cleaned_output = extract_json(raw_output)

    try:
        result = json.loads(cleaned_output)
    except Exception:
        st.error("❌ The agent returned invalid JSON. Showing raw output:")
        st.code(raw_output)
        st.stop()

    # -------------------------------------------------
    # VISUAL REPORT
    # -------------------------------------------------
    st.markdown("---")
    st.header("🎨 Visual CV Analysis Report")

    # SUMMARY
    st.markdown(
        f"""
        <div style="
            padding:20px;
            background:#1E3A8A;
            border-left:6px solid #6366f1;
            border-radius:10px;
            margin-bottom:20px;">
            <h3>📝 Summary</h3>
            <p>{result.get("summary", "No summary found")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # STRENGTHS + IMPROVEMENTS
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✔ Strengths")
        strengths = result.get("strengths", [])
        if isinstance(strengths, list):
            for s in strengths:
                st.markdown(f"- 🟢 {s}")
        else:
            st.write(strengths)

    with col2:
        st.markdown("### ⚠ Improvements")
        improvements = result.get("improvements", [])
        if isinstance(improvements, list):
            for i in improvements:
                st.markdown(f"- 🟠 {i}")
        else:
            st.write(improvements)

    st.markdown("---")

    # ATS SCORE
    ats_score = int(result.get("ats_score", 0))
    st.markdown("### 📊 ATS Score")
    st.progress(ats_score / 100)
    st.markdown(
        f"<h2 style='text-align:center;'>{ats_score}/100</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # RECOMMENDATIONS
    st.markdown(
        f"""
        <div style="
            padding:20px;
            background:#f0fdf4;
            border-left:6px solid #22c55e;
            border-radius:10px;">
            <h3>📌 Recommendations</h3>
            <p>{result.get("recommendations", "No recommendations provided")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("👆 Please upload a PDF to continue.")
