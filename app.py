import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# Initialize Gemini with API key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash-lite') #Or 'gemini-pro'

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return ""

def generate_summary(text):
    try:
        prompt = f"Summarize the following literature in a concise manner:\n\n{text}"
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return summary
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return ""

def main():
    st.title("Literature Review Summarizer")
    st.write("Upload a PDF file containing literature to get a summary.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            text = extract_text_from_pdf(uploaded_file)
        if not text.strip():
            st.error("No text could be extracted from the PDF.")
            return
        with st.spinner("Generating summary..."):
            summary = generate_summary(text)
        if summary:
            st.subheader("Summary")
            st.write(summary)

if __name__ == "__main__":
    main()