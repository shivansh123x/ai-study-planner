import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ------------------ LOAD ENV ------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI-Powered Smart Study Planner")
st.write("Generate a personalized daily study timetable using AI.")

# ------------------ DEBUG (remove later if needed) ------------------
# Shows whether key is detected
# st.write("DEBUG: API Key Loaded →", bool(api_key))

# ------------------ CHECK API KEY ------------------
if not api_key:
    st.error("❌ Gemini API key not found.\n\n"
             "Create a `.env` file in the same folder as `app.py` and add:\n\n"
             "`GEMINI_API_KEY=your_real_key_here`")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# ------------------ USER INPUTS ------------------
subjects = st.text_input("Enter subjects (comma separated)")
hours = st.number_input("Hours available per day", min_value=1, max_value=12, value=4)
exam_date = st.date_input("Exam date")

# ------------------ GENERATE PLAN ------------------
if st.button("Generate Study Plan"):

    if not subjects.strip():
        st.warning("⚠️ Please enter at least one subject.")
        st.stop()

    prompt = f"""
You are an academic planning assistant.

Create a **clear, realistic, and practical daily study timetable**.

Details:
- Subjects: {subjects}
- Study hours per day: {hours}
- Exam date: {exam_date}

Requirements:
- Provide a **day-wise schedule**
- Distribute time **evenly and logically**
- Keep plan **simple and achievable**
- Add a short **motivational tip** at the end
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        plan = response.text

        st.subheader("📝 Your Personalized Study Plan")
        st.write(plan)

    except Exception as e:
        st.error("⚠️ Failed to generate study plan.")
        st.error("Check your internet connection or Gemini API key.")
        st.exception(e)

