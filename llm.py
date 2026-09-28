import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

def get_gemini_model():
    """Initializes and returns the Gemini model securely."""
    if not api_key or api_key == "your_actual_api_key_here":
        return None
    # Using gemini-1.5-flash as a fast, reliable model for text analysis
    return genai.GenerativeModel('gemini-1.5-flash')

def classify_intent(question):
    """Uses Gemini to map user questions to predefined analysis intents."""
    model = get_gemini_model()
    if not model:
        return "dataset_summary" # Fallback if API key is missing
    
    prompt = f"""
    You are an AI data analyst assistant. Classify the user question into one of these exact categories:
    - average_sales (if asking for average sales, mean revenue, etc.)
    - highest_product_sales (if asking which product sold the most or has highest sales/revenue)
    - highest_category_revenue (if asking about categories or departments)
    - highest_month_sales (if asking about months or seasonal trends)
    - dataset_summary (if asking for a general summary, overview, or anything else)

    User Question: "{question}"

    Return ONLY the category name and nothing else.
    """
    
    try:
        response = model.generate_content(prompt)
        intent = response.text.strip().lower()
        valid_intents = ["average_sales", "highest_product_sales", "highest_category_revenue", "highest_month_sales", "dataset_summary"]
        
        for vi in valid_intents:
            if vi in intent:
                return vi
        return "dataset_summary"
    except Exception:
        return "dataset_summary"

def explain_result(question, analysis_result):
    """Uses Gemini to generate a natural, professional explanation of the calculated results."""
    model = get_gemini_model()
    if not model:
        return f"Calculated Result: {analysis_result}. (Note: Please configure a valid Gemini API key in the .env file for AI-powered explanations)."
    
    prompt = f"""
    You are a professional Data Analyst assistant.
    The user asked: "{question}"
    Here is the structured calculation result from the dataset: {analysis_result}

    Provide a clear, concise, professional business explanation of this result in 2-3 sentences. Do not mention technical implementation details.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Result calculated successfully, but AI explanation failed due to API error: {str(e)}"