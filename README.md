# GenAI Data Analyst

An interactive web application that allows users to upload datasets and query them using natural language powered by Google Gemini AI, leveraging safe backend Pandas and NumPy calculations.

## Problem Statement
Business users and analysts often need quick insights from datasets but may not know how to write complex SQL or Python scripts. This tool bridges the gap by translating natural language questions into safe, pre-defined analytical calculations and explaining the results in plain business English.

## Features
- **File Upload Support:** Upload CSV and Excel files instantly.
- **Dataset Overview:** View rows, columns, missing values, and data types.
- **Data Preview & Statistics:** Explore tabular previews and descriptive statistics (`describe()`).
- **Natural Language AI Chat:** Ask questions like *"What is the average sales?"* or *"Which product has the highest sales?"*.
- **Safe Execution Engine:** Zero reliance on dangerous `eval()` or `exec()` code generation.
- **Automated Visualizations:** Dynamic Matplotlib charts rendered based on user query intent.

## Architecture
1. **User Input:** User uploads a dataset and asks a question.
2. **Intent Classification:** Gemini AI classifies the question into a predefined analytical category.
3. **Safe Calculation:** Pandas/NumPy executes secure, pre-written aggregation functions on the DataFrame.
4. **Natural Language Explanation:** Gemini AI summarizes the numeric result into clear business insights.

## Technologies Used
- Python, Streamlit, Pandas, NumPy, Matplotlib, OpenPyXL, Google Generative AI (`gemini-1.5-flash`), python-dotenv.

## Installation & Running Locally
1. Clone the repository and navigate into the folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate