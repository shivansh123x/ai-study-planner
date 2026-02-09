import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

st.title("📚 AI-Powered Smart Study Planner")

subjects = st.text_input("Enter subjects (comma separated)")
hours = st.number_input("Hours available per day", 1, 12, 4)
exam_date = st.date_input("Exam date")

if st.button("Generate Study Plan"):
    if not os.getenv("GEMINI_API_KEY"):
        st.error("Gemini API key not found. Please check your .env file.")
    else:
        prompt = f"""
        Create a simple daily study timetable for a student.

        Subjects: {subjects}
        Study hours per day: {hours}
        Exam date: {exam_date}

        Provide:
        - Day-wise schedule
        - Balanced subject distribution
        - Short motivational tip at the end
        """

        response = model.generate_content(prompt)
        plan = response.text

        st.subheader("📝 Your Personalized Study Plan")
        st.write(plan)
