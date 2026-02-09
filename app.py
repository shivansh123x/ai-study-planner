import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if api_key:
    genai.configure(api_key=api_key)

# Streamlit UI
st.set_page_config(page_title="AI Study Planner", page_icon="📚")
st.title("📚 AI-Powered Smart Study Planner")

st.write("Generate a personalized daily study timetable using AI.")

# User inputs
subjects = st.text_input("Enter subjects (comma separated)")
hours = st.number_input("Hours available per day", min_value=1, max_value=12, value=4)
exam_date = st.date_input("Exam date")

# Generate plan
if st.button("Generate Study Plan"):

    # Check API key
    if not api_key:
        st.error("❌ Gemini API key not found. Please check your .env file.")
        st.stop()

    # Check input
    if not subjects:
        st.warning("⚠️ Please enter at least one subject.")
        st.stop()

    # Create prompt
    prompt = f"""
    Create a simple, clear, and practical daily study timetable for a student.

    Subjects: {subjects}
    Study hours per day: {hours}
    Exam date: {exam_date}

    Requirements:
    - Provide a day-wise study schedule
    - Distribute time evenly across subjects
    - Keep the plan realistic and easy to follow
    - Add a short motivational tip at the end
    """

    try:
        # Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate response
        response = model.generate_content(prompt)
        plan = response.text

        # Show result
        st.subheader("📝 Your Personalized Study Plan")
        st.write(plan)

    except Exception as e:
        st.error("⚠️ Error generating study plan. Check your API key or internet.")
        st.exception(e)

