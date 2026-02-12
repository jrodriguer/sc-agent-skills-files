#!/usr/bin/env python3
"""
Complete Marketing Campaign Excel Report Generator
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_and_analyze_data():
    """Load and analyze campaign data"""
    # Load raw data
    df = pd.read_csv('L1-partI/campaign_data_week1.csv')
    
    # Aggregate by channel
    channel_data = df.groupby('channel').agg({
        'impressions': 'sum',
        'clicks': 'sum', 
        'conversions': 'sum',
        'spend': 'sum',
        'revenue': 'sum',
        'orders': 'sum'
    }).reset_index()
    
    # Calculate metrics
    benchmarks = {
        'Facebook_Ads': {'CTR': 2.5, 'CVR': 3.8},
        'Google_Ads': {'CTR': 5.0, 'CVR': 4.5}, 
        'TikTok_Ads': {'CTR': 2.0, 'CVR': 0.9},
        'Email': {'CTR': 15.0, 'CVR': 2.1}
    }
    
    target_roas = 4.0
    max_cpa = 50.0
    shipping_cost = 8.0
    product_cost_pct = 0.35
    
    # Calculate funnel metrics
    channel_data['CTR_Actual'] = channel_data.apply(
        lambda row: (row['clicks'] / row['impressions'] * 100) if row['impressions'] > 0 and row['channel'] != 'Email' else np.nan, axis=1
    )
    channel_data['CTR_Benchmark'] = channel_data['channel'].map(lambda x: benchmarks[x]['CTR'])
    channel_data['CTR_Diff'] = channel_data.apply(
        lambda row: row['CTR_Actual'] - row['CTR_Benchmark'] if not pd.isna(row['CTR_Actual']) else np.nan, axis=1
    )
    
    channel_data['CVR_Actual'] = channel_data['conversions'] / channel_data['clicks'] * 100
    channel_data['CVR_Benchmark'] = channel_data['channel'].map(lambda x: benchmarks[x]['CVR'])
    channel_data['CVR_Diff'] = channel_data['CVR_Actual'] - channel_data['CVR_Benchmark']
    
    # Calculate efficiency metrics
    channel_data['ROAS'] = channel_data['revenue'] / channel_data['spend']
    channel_data['CPA'] = channel_data['spend'] / channel_data['conversions']
    channel_data['Total_Costs'] = (channel_data['spend'] + 
                                   (channel_data['orders'] * shipping_cost) + 
                                   (channel_data['revenue'] * product_cost_pct))
    channel_data['Net_Profit'] = channel_data['revenue'] - channel_data['Total_Costs']
    
    # Classification for budget reallocation
    def classify_channel(row):
        if row['Net_Profit'] <= 0 and row['ROAS'] < 2.0:  # 50% of target
            return 'DECREASE_HEAVY'
        elif row['Net_Profit'] > 0 and row['ROAS'] >= 4.6 and row['CPA'] <= 40:  # 115% ROAS, 80% CPA
            return 'INCREASE'
        elif row['ROAS'] < 3.2 or row['CPA'] > 60:  # 80% ROAS, 120% CPA
            return 'DECREASE_LIGHT'
        else:
            return 'MAINTAIN'
    
    channel_data['Classification'] = channel_data.apply(classify_channel, axis=1)
    
    return df, channel_data

def calculate_budget_reallocation(channel_data):
    """Calculate budget reallocation recommendations"""
    
    # Calculate budget changes
    freed_budget = 0
    budget_changes = []
    
    # Calculate decreases
    for _, row in channel_data.iterrows():
        current_spend = row['spend']
        if row['Classification'] == 'DECREASE_HEAVY':
            change = -current_spend * 0.45
            new_budget = current_spend + change
            freed_budget += abs(change)
            budget_changes.append({
                'Channel': row['channel'],
                'Current Budget': current_spend,
                'Change': change,
                'New Budget': new_budget,
                'Classification': row['Classification']
            })
    
    # Calculate increases
    increase_channels = channel_data[channel_data['Classification'] == 'INCREASE']
    total_increase_net_profit = increase_channels['Net_Profit'].sum()
    user_increase_cap = 0.15
    user_limit = 10000
    
    for _, row in increase_channels.iterrows():
        current_spend = row['spend']
        weight = row['Net_Profit'] / total_increase_net_profit
        proposed_increase = freed_budget * weight
        max_increase = current_spend * user_increase_cap
        final_increase = min(proposed_increase, max_increase)
        new_budget = current_spend + final_increase
        
        budget_changes.append({
            'Channel': row['channel'],
            'Current Budget': current_spend,
            'Change': final_increase,
            'New Budget': new_budget,
            'Classification': row['Classification']
        })
    
    # Calculate maintains
    for _, row in channel_data.iterrows():
        if row['Classification'] == 'MAINTAIN':
            budget_changes.append({
                'Channel': row['channel'],
                'Current Budget': row['spend'],
                'Change': 0,
                'New Budget': row['spend'],
                'Classification': row['Classification']
            })
    
    # Add reserve
    total_increases = sum([item['Change'] for item in budget_changes if item['Change'] > 0])
    unallocated = freed_budget - total_increases
    budget_changes.append({
        'Channel': 'Reserve',
        'Current Budget': 0,
        'Change': unallocated,
        'New Budget': unallocated,
        'Classification': 'AVAILABLE'
    })
    
    return budget_changes

def create_excel_report(raw_df, channel_df, budget_data):
    """Create comprehensive Excel report"""
    with pd.ExcelWriter('Marketing_Campaign_Report.xlsx', engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats
        formats = {
            'header': workbook.add_format({
                'bold': True, 'bg_color': '#2E75B6', 'font_color': 'white', 'border': 1
            }),
            'good': workbook.add_format({
                'bg_color': '#C6E0B4', 'border': 1, 'num_format': '$#,##0.00'
            }),
            'bad': workbook.add_format({
                'bg_color': '#F8B2B0', 'border': 1, 'num_format': '$#,##0.00'
            }),
            'neutral': workbook.add_format({
                'bg_color': '#FFFFFF', 'border': 1, 'num_format': '$#,##0.00'
            }),
            'percent_good': workbook.add_format({
                'bg_color': '#C6E0B4', 'border': 1, 'num_format': '0.00%'
            }),
            'percent_bad': workbook.add_format({
                'bg_color': '#F8B2B0', 'border': 1, 'num_format': '0.00%'
            }),
            'percent_neutral': workbook.add_format({
                'bg_color': '#FFFFFF', 'border': 1, 'num_format': '0.00%'
            }),
            'title': workbook.add_format({
                'bold': True, 'font_size': 16, 'bg_color': '#2E75B6', 'font_color': 'white', 'align': 'center'
            }),
            'subtitle': workbook.add_format({
                'bold': True, 'font_size': 12, 'bg_color': '#5B9BD5', 'font_color': 'white'
            })
        }
        
        # 1. Executive Summary Sheet
        exec_summary_data = []
        for _, row in channel_df.iterrows():
            exec_summary_data.append({
                'Channel': row['channel'],
                'Current Spend': row['spend'],
                'ROAS': row['ROAS'],
                'Net Profit': row['Net_Profit'],
                'Classification': row['Classification']
            })
        
        exec_df = pd.DataFrame(exec_summary_data)
        exec_df.to_excel(writer, sheet_name='Executive Summary', index=False, startrow=4)
        
        worksheet = writer.sheets['Executive Summary']
        worksheet.write(0, 0, 'Marketing Campaign Analysis - Executive Summary', formats['title'])
        worksheet.write(2, 0, 'Key Performance Indicators & Budget Recommendations', formats['subtitle'])
        
        # Format executive summary
        for col_num, value in enumerate(exec_df.columns):
            worksheet.write(4, col_num, value, formats['header'])
        
        # Apply color coding
        for row_num, (_, row) in enumerate(exec_df.iterrows(), 5):
            # ROAS formatting
            worksheet.write(row_num, 2, row['ROAS'], 
                           formats['good'] if row['ROAS'] >= 4.0 else formats['bad'])
            # Net Profit formatting  
            worksheet.write(row_num, 3, row['Net Profit'],
                           formats['good'] if row['Net Profit'] > 0 else formats['bad'])
        
        # 2. Funnel Analysis Sheet
        funnel_df = channel_df[['channel', 'CTR_Actual', 'CTR_Benchmark', 'CTR_Diff', 
                               'CVR_Actual', 'CVR_Benchmark', 'CVR_Diff']].copy()
        funnel_df.to_excel(writer, sheet_name='Funnel Analysis', index=False, startrow=4)
        
        worksheet = writer.sheets['Funnel Analysis']
        worksheet.write(0, 0, 'Funnel Performance Analysis', formats['title'])
        worksheet.write(2, 0, 'Click-Through Rate (CTR) & Conversion Rate (CVR) vs Benchmarks', formats['subtitle'])
        
        for col_num, value in enumerate(funnel_df.columns):
            worksheet.write(4, col_num, value, formats['header'])
        
        # Apply color coding for funnel metrics
        for row_num, (_, row) in enumerate(funnel_df.iterrows(), 5):
            # CTR difference
            if not pd.isna(row['CTR_Diff']):
                worksheet.write(row_num, 3, row['CTR_Diff'],
                               formats['percent_good'] if row['CTR_Diff'] >= 0 else formats['percent_bad'])
            # CVR difference
            worksheet.write(row_num, 6, row['CVR_Diff'],
                           formats['percent_good'] if row['CVR_Diff'] >= 0 else formats['percent_bad'])
        
        # 3. Efficiency Analysis Sheet
        efficiency_df = channel_df[['channel', 'spend', 'revenue', 'ROAS', 'CPA', 'Net_Profit']].copy()
        efficiency_df.columns = ['Channel', 'Spend', 'Revenue', 'ROAS', 'CPA', 'Net Profit']
        efficiency_df.to_excel(writer, sheet_name='Efficiency Analysis', index=False, startrow=4)
        
        worksheet = writer.sheets['Efficiency Analysis']
        worksheet.write(0, 0, 'Efficiency Analysis', formats['title'])
        worksheet.write(2, 0, 'ROAS, CPA & Net Profit Performance', formats['subtitle'])
        
        for col_num, value in enumerate(efficiency_df.columns):
            worksheet.write(4, col_num, value, formats['header'])
        
        # Apply color coding for efficiency metrics
        for row_num, (_, row) in enumerate(efficiency_df.iterrows(), 5):
            # ROAS
            worksheet.write(row_num, 3, row['ROAS'],
                           formats['good'] if row['ROAS'] >= 4.0 else formats['bad'])
            # CPA
            worksheet.write(row_num, 4, row['CPA'],
                           formats['good'] if row['CPA'] <= 50.0 else formats['bad'])
            # Net Profit
            worksheet.write(row_num, 5, row['Net Profit'],
                           formats['good'] if row['Net Profit'] > 0 else formats['bad'])
        
        # 4. Budget Reallocation Sheet
        budget_df = pd.DataFrame(budget_data)
        budget_df.to_excel(writer, sheet_name='Budget Reallocation', index=False, startrow=4)
        
        worksheet = writer.sheets['Budget Reallocation']
        worksheet.write(0, 0, 'Budget Reallocation Recommendations', formats['title'])
        worksheet.write(2, 0, 'Proposed Budget Changes Based on Performance Analysis', formats['subtitle'])
        
        # Format headers
        for col_num, value in enumerate(budget_df.columns):
            worksheet.write(4, col_num, value, formats['header'])
        
        # Apply color coding
        for row_num, (_, row) in enumerate(budget_df.iterrows(), 5):
            if row['Change'] > 0:
                cell_format = formats['good']
            elif row['Change'] < 0:
                cell_format = formats['bad']
            else:
                cell_format = formats['neutral']
            
            worksheet.write(row_num, 1, row['Current Budget'], cell_format)
            worksheet.write(row_num, 2, row['Change'], cell_format)
            worksheet.write(row_num, 3, row['New Budget'], cell_format)
        
        # 5. Raw Data Sheet
        raw_df.to_excel(writer, sheet_name='Raw Data', index=False)
        
        worksheet = writer.sheets['Raw Data']
        worksheet.write(0, 0, 'Raw Campaign Data', formats['title'])
        
        # Adjust column widths
        for worksheet_name in writer.sheets:
            worksheet = writer.sheets[worksheet_name]
            worksheet.set_column(0, 0, 20)  # Channel name column
            worksheet.set_column(1, 5, 15)  # Metric columns
            if worksheet_name == 'Raw Data':
                worksheet.set_column('A:J', 15)

if __name__ == "__main__":
    # Load and analyze data
    print("Analyzing campaign data...")
    raw_data, channel_data = load_and_analyze_data()
    
    # Calculate budget reallocation
    print("Calculating budget reallocation...")
    budget_data = calculate_budget_reallocation(channel_data)
    
    # Create Excel report
    print("Creating comprehensive Excel report...")
    create_excel_report(raw_data, channel_data, budget_data)
    
    print("✅ Marketing_Campaign_Report.xlsx created successfully!")
    print("📊 Report includes:")
    print("   • Executive Summary with key findings")
    print("   • Funnel Analysis (CTR/CVR vs benchmarks)")
    print("   • Efficiency Analysis (ROAS/CPA/Profit)")
    print("   • Budget Reallocation Recommendations")
    print("   • Raw Data for reference")
    print("   • Color coding: Green = Good, Red = Bad")