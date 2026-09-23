import pandas as pd
import numpy as np
from .cleaning import prepare_mapped_data

def run_analysis(file_path, mapping):
    df = prepare_mapped_data(file_path, mapping)
    
    if isinstance(df, dict):
        return df
    
    if df.empty:
        return {"error": "No valid data to analyze."}

    df = df.sort_values('sys_date')
    
    report = {
        'summary': {},
        'recommendation': []
    }

    # Time Series Analysys
    # Grouping by month
    df_monthly = df.set_index('sys_date').resample('ME')['sys_value'].sum().reset_index()
    
    # Dynamic (m/m)
    if len(df_monthly) >= 2:
        df_monthly['mom_growth'] = df_monthly['sys_value'].pct_change() * 100

        avg_growth = df_monthly['mom_growth'].mean()
        # POPRAWKA 1: Dodano float()
        report['summary']['avg_monthly_growth'] = float(round(avg_growth, 2))

        if avg_growth > 5:
            report['recommendation'].append(
                """Your business is experiencing steady, positive growth. It’s the ideal time to reinvest capital surplus into scaling processes or more aggressive marketing."""
            )
        elif avg_growth < -2:
            report['recommendation'].append(
                """Negative revenue growth has been observed. Conduct a review of fixed costs and determine if the decline stems from a structural issue or natural seasonality."""
            )

        cv = df_monthly['sys_value'].std() / df_monthly['sys_value'].mean()
        if cv > 0.4:
            report['recommendation'].append(
                """Your revenue shows high month-over-month volatility. It is recommended to build a liquidity buffer to cover operating expenses during slower periods."""
            )

    if 'sys_category' in df.columns:
        cat_grouped = df.groupby('sys_category')['sys_value'].agg(['sum', 'count']).reset_index()
        cat_grouped = cat_grouped.sort_values(by='sum', ascending=False)
        
        top_category = cat_grouped.iloc[0]
        total_value = df['sys_value'].sum()
        top_share = (top_category['sum'] / total_value) * 100
        
        # POPRAWKA 2: Dodano str() i float()
        report['summary']['top_category'] = str(top_category['sys_category'])
        report['summary']['top_category_proportion'] = float(round(top_share, 2))
        
        if top_share > 70:
            report['recommendation'].append(
                f"""Category '{top_category['sys_category']}' generates over 70% of total revenue. Such high concentration creates significant risk. Consider diversifying your product range or services"""
            )
        else:
            report['recommendation'].append(
                f"""Category '{top_category['sys_category']}' is your primary growth driver. Explore opportunities to increase margins on these operations."""
            )

    # POPRAWKA 3: Dodano float() i int()
    report['summary']['total_value'] = float(round(df['sys_value'].sum(), 2))
    report['summary']['records_number'] = int(len(df))
    
    return report