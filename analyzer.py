import pandas as pd
import numpy as np

def load_data(uploaded_file):
    """Loads CSV or Excel file into a Pandas DataFrame with error handling."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported file format. Please upload a CSV or Excel file."
        
        if df.empty:
            return None, "The uploaded dataset is empty."
        
        return df, None
    except Exception as e:
        return None, f"Error reading file: {str(e)}"

def get_dataset_info(df):
    """Extracts basic metadata, missing values, and summary statistics."""
    try:
        info = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "summary_stats": df.describe(include='all').to_dict()
        }
        return info, None
    except Exception as e:
        return None, f"Error processing dataset statistics: {str(e)}"

def run_predefined_analysis(df, query_type):
    """Executes safe, predefined Pandas/NumPy calculations based on intent."""
    try:
        # Normalize column names for flexible matching
        cols = {str(c).lower().strip(): c for c in df.columns}
        
        rev_col = next((cols[c] for c in cols if 'revenue' in c or 'sales' in c or 'amount' in c), None)
        prod_col = next((cols[c] for c in cols if 'product' in c or 'item' in c), None)
        cat_col = next((cols[c] for c in cols if 'category' in c or 'department' in c), None)
        date_col = next((cols[c] for c in cols if 'date' in c or 'time' in c), None)

        if query_type == "average_sales" and rev_col:
            val = df[rev_col].mean()
            return {"metric": "Average Sales / Revenue", "result": round(float(val), 2)}
        
        elif query_type == "highest_product_sales" and rev_col and prod_col:
            grouped = df.groupby(prod_col)[rev_col].sum()
            top_prod = str(grouped.idxmax())
            top_val = float(grouped.max())
            return {"metric": "Top Product by Sales", "result": top_prod, "value": round(top_val, 2)}

        elif query_type == "highest_category_revenue" and rev_col and cat_col:
            grouped = df.groupby(cat_col)[rev_col].sum()
            top_cat = str(grouped.idxmax())
            top_val = float(grouped.max())
            return {"metric": "Top Category by Revenue", "result": top_cat, "value": round(top_val, 2)}

        elif query_type == "highest_month_sales" and rev_col and date_col:
            df_temp = df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
            df_temp['Month_Year'] = df_temp[date_col].dt.strftime('%B %Y')
            grouped = df_temp.groupby('Month_Year')[rev_col].sum()
            if not grouped.empty:
                top_month = str(grouped.idxmax())
                top_val = float(grouped.max())
                return {"metric": "Month with Highest Sales", "result": top_month, "value": round(top_val, 2)}

        elif query_type == "dataset_summary":
            return {
                "metric": "Dataset Summary",
                "total_rows": int(df.shape[0]),
                "total_columns": int(df.shape[1]),
                "columns": list(df.columns),
                "missing_count": int(df.isnull().sum().sum())
            }

        return {"result": "Unable to calculate metric. Please verify your dataset columns contain relevant sales/revenue/product fields."}
    
    except Exception as e:
        return {"error": str(e)}