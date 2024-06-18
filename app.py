import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# To load all the environment variables
load_dotenv() 

# Configure Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro') # Load the Gemini pro model
    response = model.generate_content(input) # Generate the response based on the input
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt_template = """
Act as a highly skilled and experienced ATS (Application Tracking System) with deep knowledge in tech fields, including software engineering, data science, data analysis, and big data engineering. 
Your task is to evaluate the resume considering the competitive job market. 
Provide detailed feedback on resume improvement, including missing keywords, JD match score, and suggest top 5 job matches with valid job application links. 
Ensure the links are for currently active job postings and relevant to the candidate's profile.
resume: {text}
"""

## Streamlit app
st.title("Smart Job Search Application")

uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt_template.format(text=text)
        response = get_gemini_response(input_prompt)
        st.markdown(response)
