import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

import analyzer
import llm

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GenAI Data Analyst",
    page_icon="📊",
    layout="wide"
)

# App Title & Description
st.title("📊 GenAI Data Analyst")
st.markdown("Upload your dataset and chat with your data using safe Pandas calculations and Google Gemini AI.")

# Sidebar - Dataset Upload & Configuration
st.sidebar.header("1. Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

# Use sample data option if no file uploaded
use_sample = st.sidebar.checkbox("Use Sample E-Commerce Dataset", value=False)

df = None
file_error = None

if uploaded_file is not None:
    df, file_error = analyzer.load_data(uploaded_file)
elif use_sample:
    if os.path.exists("sample_data.csv"):
        df, file_error = analyzer.load_data(open("sample_data.csv", "rb"))
    else:
        file_error = "Sample dataset not found. Please upload a file."

if file_error:
    st.error(file_error)

if df is not None:
    # Get dataset info
    info, info_error = analyzer.get_dataset_info(df)
    
    if info_error:
        st.error(info_error)
    else:
        # Section 2: Dataset Overview
        st.header("2. Dataset Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", info["rows"])
        with col2:
            st.metric("Total Columns", info["columns"])
        with col3:
            missing_total = sum(info["missing_values"].values())
            st.metric("Missing Values", missing_total)
        
        st.write("**Column Names:**", ", ".join(info["column_names"]))

        # Section 3: Data Preview
        st.header("3. Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

        # Section 4: Statistics
        st.header("4. Statistics")
        st.dataframe(df.describe(include='all'), use_container_width=True)

        # Section 5 & 6: Ask AI About Your Data & Results
        st.header("5. Ask AI About Your Data")
        
        # Check API key status warning in sidebar
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_actual_api_key_here":
            st.sidebar.warning("⚠️ Gemini API Key not detected or set to placeholder in `.env`. AI explanations will run in offline fallback mode.")

        user_question = st.text_input("Ask a question about your dataset (e.g., 'What is the average sales?', 'Which product has the highest sales?'):")

        if st.button("Analyze with AI"):
            if not user_question.strip():
                st.warning("Please enter a valid question.")
            else:
                with st.spinner("Analyzing data and generating AI explanation..."):
                    # Step 1: Classify intent using LLM
                    intent = llm.classify_intent(user_question)
                    
                    # Step 2: Run safe predefined pandas/numpy analysis
                    calc_result = analyzer.run_predefined_analysis(df, intent)
                    
                    # Step 3: Explain result using LLM
                    ai_explanation = llm.explain_result(user_question, calc_result)

                # Section 6: Result Display
                st.subheader("6. Result")
                st.success(ai_explanation)
                
                with st.expander("View Underlying Calculation Details"):
                    st.json(calc_result)

                # Section 7: Chart Generation (When applicable)
                st.subheader("7. Chart")
                try:
                    cols = {str(c).lower().strip(): c for c in df.columns}
                    rev_col = next((cols[c] for c in cols if 'revenue' in c or 'sales' in c or 'amount' in c), None)
                    prod_col = next((cols[c] for c in cols if 'product' in c or 'item' in c), None)
                    cat_col = next((cols[c] for c in cols if 'category' in c or 'department' in c), None)

                    fig, ax = plt.subplots(figsize=(8, 4))
                    
                    if intent == "highest_product_sales" and rev_col and prod_col:
                        top_data = df.groupby(prod_col)[rev_col].sum().nlargest(5)
                        top_data.plot(kind='bar', ax=ax, color='skyblue')
                        ax.set_title("Top 5 Products by Sales / Revenue")
                        ax.set_ylabel("Revenue")
                        plt.xticks(rotation=45, ha='right')
                        st.pyplot(fig)
                    elif intent == "highest_category_revenue" and rev_col and cat_col:
                        cat_data = df.groupby(cat_col)[rev_col].sum()
                        cat_data.plot(kind='bar', ax=ax, color='salmon')
                        ax.set_title("Revenue by Category")
                        ax.set_ylabel("Revenue")
                        plt.xticks(rotation=45, ha='right')
                        st.pyplot(fig)
                    else:
                        # Default distribution chart for numeric column
                        num_cols = df.select_dtypes(include=['number']).columns
                        if len(num_cols) > 0:
                            df[num_cols[0]].plot(kind='hist', ax=ax, bins=10, color='lightgreen', edgecolor='black')
                            ax.set_title(f"Distribution of {num_cols[0]}")
                            st.pyplot(fig)
                        else:
                            st.info("No suitable numeric column found for automatic charting.")
                except Exception as chart_err:
                    st.info(f"Chart could not be generated for this specific query: {chart_err}")
else:
    st.info("👈 Please upload a CSV/Excel file or check 'Use Sample E-Commerce Dataset' in the sidebar to get started.")