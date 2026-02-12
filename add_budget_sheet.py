#!/usr/bin/env python3
"""
Add budget reallocation data to Excel report
"""

import pandas as pd
import numpy as np

def create_budget_reallocation_sheet():
    """Create budget reallocation data for Excel"""
    
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
    
    # Calculate metrics for budget reallocation
    shipping_cost = 8.0
    product_cost_pct = 0.35
    target_roas = 4.0
    max_cpa = 50.0
    
    # Calculate efficiency metrics
    channel_data['ROAS'] = channel_data['revenue'] / channel_data['spend']
    channel_data['CPA'] = channel_data['spend'] / channel_data['conversions']
    channel_data['Total_Costs'] = (channel_data['spend'] + 
                                   (channel_data['orders'] * shipping_cost) + 
                                   (channel_data['revenue'] * product_cost_pct))
    channel_data['Net_Profit'] = channel_data['revenue'] - channel_data['Total_Costs']
    
    # Classify channels based on rules
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
    
    # Add budget reallocation to existing Excel file
    with pd.ExcelWriter('Marketing_Campaign_Report.xlsx', engine='xlsxwriter', mode='a', if_sheet_exists='replace') as writer:
        workbook = writer.book
        
        # Define formats
        formats = {
            'header': workbook.add_format({
                'bold': True, 'bg_color': '#2E75B6', 'font_color': 'white', 'border': 1
            }),
            'increase': workbook.add_format({
                'bg_color': '#C6E0B4', 'border': 1, 'num_format': '$#,##0.00'
            }),
            'decrease': workbook.add_format({
                'bg_color': '#F8B2B0', 'border': 1, 'num_format': '$#,##0.00'
            }),
            'neutral': workbook.add_format({
                'bg_color': '#FFFFFF', 'border': 1, 'num_format': '$#,##0.00'
            }),
            'title': workbook.add_format({
                'bold': True, 'font_size': 16, 'bg_color': '#2E75B6', 'font_color': 'white', 'align': 'center'
            })
        }
        
        # Create budget reallocation dataframe
        budget_df = pd.DataFrame(budget_changes)
        budget_df.to_excel(writer, sheet_name='Budget Reallocation', index=False, startrow=4)
        
        worksheet = writer.sheets['Budget Reallocation']
        worksheet.write(0, 0, 'Budget Reallocation Recommendations', formats['title'])
        worksheet.write(2, 0, 'Proposed Budget Changes Based on Performance Analysis', formats['header'])
        
        # Format headers
        for col_num, value in enumerate(budget_df.columns):
            worksheet.write(4, col_num, value, formats['header'])
        
        # Apply color coding
        for row_num, (_, row) in enumerate(budget_df.iterrows(), 5):
            if row['Change'] > 0:
                cell_format = formats['increase']
            elif row['Change'] < 0:
                cell_format = formats['decrease']
            else:
                cell_format = formats['neutral']
            
            worksheet.write(row_num, 1, row['Current Budget'], cell_format)
            worksheet.write(row_num, 2, row['Change'], cell_format)
            worksheet.write(row_num, 3, row['New Budget'], cell_format)

if __name__ == "__main__":
    create_budget_reallocation_sheet()
    print("✅ Budget reallocation sheet added to Excel report!")