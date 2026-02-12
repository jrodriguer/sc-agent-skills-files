import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

# Load and analyze the campaign data
df = pd.read_csv('/Users/juliorodriguez/Documents/sc-agent-skills-files/L1-partI/campaign_data_week1.csv')

# Data Quality Check
print("=== DATA QUALITY CHECK ===")
print(f"Total records: {len(df)}")
print(f"Missing values per column:")
print(df.isnull().sum())
print(f"Negative values check:")
numeric_cols = ['impressions', 'clicks', 'conversions', 'spend', 'revenue', 'orders']
for col in numeric_cols:
    if col in df.columns:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            print(f"  {col}: {neg_count} negative values")
        else:
            print(f"  {col}: No negative values")

# Check for conversions without clicks
anomaly_check = df[(df['conversions'] > 0) & (df['clicks'] == 0)]
if len(anomaly_check) > 0:
    print(f"⚠️  Found {len(anomaly_check)} records with conversions but no clicks")
else:
    print("✓ No conversions without clicks found")

print("\n")

# Aggregate data by channel
channel_data = df.groupby('channel').agg({
    'impressions': 'sum',
    'clicks': 'sum', 
    'conversions': 'sum',
    'spend': 'sum',
    'revenue': 'sum',
    'orders': 'sum'
}).reset_index()

print("=== AGGREGATED CHANNEL DATA ===")
print(channel_data.to_string(index=False))
print("\n")

# Benchmark values
benchmarks = {
    'Facebook_Ads': {'ctr': 2.5, 'cvr': 3.8},
    'Google_Ads': {'ctr': 5.0, 'cvr': 4.5}, 
    'TikTok_Ads': {'ctr': 2.0, 'cvr': 0.9},
    'Email': {'ctr': 15.0, 'cvr': 2.1}
}

# Target values
target_roas = 4.0
max_cpa = 50.0
shipping_cost = 8.0
product_cost_pct = 0.35

# Calculate funnel metrics
funnel_results = []
for _, row in channel_data.iterrows():
    channel = row['channel']
    
    if channel == 'Email':
        # Email doesn't have impressions, so CTR is not applicable
        ctr_actual = None
        ctr_diff = None
    else:
        ctr_actual = (row['clicks'] / row['impressions']) * 100 if row['impressions'] > 0 else 0
        ctr_bench = benchmarks.get(channel, {}).get('ctr', 0)
        ctr_diff = ctr_actual - ctr_bench
    
    cvr_actual = (row['conversions'] / row['clicks']) * 100 if row['clicks'] > 0 else 0
    cvr_bench = benchmarks.get(channel, {}).get('cvr', 0)
    cvr_diff = cvr_actual - cvr_bench
    
    funnel_results.append({
        'Channel': channel,
        'CTR Actual': f"{ctr_actual:.2f}%" if ctr_actual is not None else "N/A",
        'CTR Benchmark': f"{benchmarks.get(channel, {}).get('ctr', 0):.1f}%" if channel != 'Email' else "N/A",
        'CTR Diff': f"{ctr_diff:+.2f}pp" if ctr_diff is not None else "N/A",
        'CVR Actual': f"{cvr_actual:.2f}%",
        'CVR Benchmark': f"{cvr_bench:.1f}%",
        'CVR Diff': f"{cvr_diff:+.2f}pp"
    })

print("=== FUNNEL ANALYSIS ===")
print("| Channel | CTR Actual | CTR Benchmark | CTR Diff | CVR Actual | CVR Benchmark | CVR Diff |")
print("|---------|------------|---------------|----------|------------|---------------|----------|")
for result in funnel_results:
    print(f"| {result['Channel']:<9} | {result['CTR Actual']:<10} | {result['CTR Benchmark']:<13} | {result['CTR Diff']:<8} | {result['CVR Actual']:<10} | {result['CVR Benchmark']:<13} | {result['CVR Diff']:<8} |")

print("\n")

# Calculate efficiency metrics
efficiency_results = []
for _, row in channel_data.iterrows():
    channel = row['channel']
    
    # ROAS
    roas = row['revenue'] / row['spend'] if row['spend'] > 0 else 0
    roas_status = "[OK] Above" if roas >= target_roas else "[X] Below"
    
    # CPA
    cpa = row['spend'] / row['conversions'] if row['conversions'] > 0 else float('inf')
    cpa_status = "[OK] Below" if cpa <= max_cpa else "[X] Above"
    
    # Net Profit
    total_costs = row['spend'] + (row['orders'] * shipping_cost) + (row['revenue'] * product_cost_pct)
    net_profit = row['revenue'] - total_costs
    profit_status = "[OK] Positive" if net_profit > 0 else "[X] Negative"
    
    efficiency_results.append({
        'Channel': channel,
        'ROAS': f"{roas:.2f}x",
        'ROAS Status': roas_status,
        'CPA': f"${cpa:.2f}",
        'CPA Status': cpa_status, 
        'Net Profit': f"${net_profit:.2f}",
        'Profit Status': profit_status,
        'Spend': row['spend'],
        'Conversions': row['conversions'],
        'ROAS_Value': roas,
        'CPA_Value': cpa,
        'Net_Profit_Value': net_profit
    })

print("=== EFFICIENCY ANALYSIS ===")
print("| Channel | ROAS | Status | CPA | Status | Net Profit | Status |")
print("|---------|------|--------|-----|--------|------------|--------|")
for result in efficiency_results:
    print(f"| {result['Channel']:<9} | {result['ROAS']:<4} | {result['ROAS Status']:<6} | {result['CPA']:<7} | {result['CPA Status']:<6} | {result['Net Profit']:<10} | {result['Profit Status']:<6} |")

print("\n")

# Budget Reallocation Analysis
print("=== BUDGET REALLOCATION ANALYSIS ===")

# Rule 0: Check eligibility (>= 50 conversions)
eligible_channels = []
for result in efficiency_results:
    if result['Conversions'] >= 50:
        eligible_channels.append(result)
    else:
        result['Classification'] = 'INSUFFICIENT_DATA -> MAINTAIN'

print("Step 1: Eligibility Check (>= 50 conversions)")
for result in efficiency_results:
    status = "✓ Eligible" if result['Conversions'] >= 50 else "✗ Ineligible"
    print(f"  {result['Channel']}: {result['Conversions']} conversions - {status}")

# Classify eligible channels
for result in eligible_channels:
    roas_pct_target = (result['ROAS_Value'] / target_roas) * 100
    cpa_pct_max = (result['CPA_Value'] / max_cpa) * 100
    net_profit = result['Net_Profit_Value']
    
    # Apply classification rules in order
    if roas_pct_target < 50 and net_profit <= 0:
        classification = 'DECREASE_HEAVY'
    elif cpa_pct_max > 150 and net_profit <= 0:
        classification = 'DECREASE_HEAVY'
    elif roas_pct_target < 100 and cpa_pct_max > 100 and net_profit <= 0:
        classification = 'DECREASE_HEAVY'
    elif roas_pct_target >= 115 and cpa_pct_max <= 80 and net_profit > 0:
        classification = 'INCREASE'
    elif roas_pct_target < 80:
        classification = 'DECREASE_LIGHT'
    elif cpa_pct_max > 120:
        classification = 'DECREASE_LIGHT'
    else:
        classification = 'MAINTAIN'
    
    result['Classification'] = classification
    result['ROAS_Pct_Target'] = roas_pct_target
    result['CPA_Pct_Max'] = cpa_pct_max

print("\nStep 2: Channel Classification")
print("| Channel | ROAS | % of Target | CPA | % of Max | Net Profit | Classification |")
print("|---------|------|-------------|-----|----------|------------|----------------|")
for result in efficiency_results:
    if 'Classification' in result:
        roas_pct = result.get('ROAS_Pct_Target', 0)
        cpa_pct = result.get('CPA_Pct_Max', 0)
        print(f"| {result['Channel']:<9} | {result['ROAS']:<4} | {roas_pct:<11.0f}% | {result['CPA']:<7} | {cpa_pct:<8.0f}% | {result['Net Profit']:<10} | {result['Classification']:<14} |")

# Calculate budget changes
decrease_heavy_channels = [r for r in efficiency_results if r.get('Classification') == 'DECREASE_HEAVY']
decrease_light_channels = [r for r in efficiency_results if r.get('Classification') == 'DECREASE_LIGHT']
increase_channels = [r for r in efficiency_results if r.get('Classification') == 'INCREASE']

print(f"\nStep 3: Budget Change Calculations")
print(f"Channels to decrease heavy: {[c['Channel'] for c in decrease_heavy_channels]}")
print(f"Channels to decrease light: {[c['Channel'] for c in decrease_light_channels]}")
print(f"Channels to increase: {[c['Channel'] for c in increase_channels]}")

# Calculate decreases
total_freed_budget = 0
decrease_details = []

for channel in decrease_heavy_channels:
    decrease_amount = channel['Spend'] * 0.45
    total_freed_budget += decrease_amount
    decrease_details.append({'Channel': channel['Channel'], 'Amount': decrease_amount, 'Type': 'DECREASE_HEAVY'})

for channel in decrease_light_channels:
    decrease_amount = channel['Spend'] * 0.25
    total_freed_budget += decrease_amount
    decrease_details.append({'Channel': channel['Channel'], 'Amount': decrease_amount, 'Type': 'DECREASE_LIGHT'})

print(f"\nStep 4: Freed Budget from Decreases: ${total_freed_budget:.2f}")
for detail in decrease_details:
    print(f"  {detail['Channel']}: -${detail['Amount']:.2f} ({detail['Type']})")

# Allocate to increase channels
increase_details = []
user_limit = 10000  # User can shift up to $10k
increase_cap = 0.15  # 15% per channel limit

if increase_channels and total_freed_budget > 0:
    # Calculate weights based on Net Profit
    total_net_profit = sum(c['Net_Profit_Value'] for c in increase_channels)
    
    for channel in increase_channels:
        weight = channel['Net_Profit_Value'] / total_net_profit if total_net_profit > 0 else 0
        proposed_increase = total_freed_budget * weight
        max_increase = channel['Spend'] * increase_cap
        capped_increase = min(proposed_increase, max_increase)
        
        increase_details.append({
            'Channel': channel['Channel'],
            'Proposed': proposed_increase,
            'Max Allowed': max_increase,
            'Final': capped_increase,
            'Weight': weight
        })
    
    # Check if total increases exceed user limit
    total_proposed = sum(d['Final'] for d in increase_details)
    
    if total_proposed > user_limit:
        scale_factor = user_limit / total_proposed
        for detail in increase_details:
            detail['Final'] = detail['Final'] * scale_factor
        print(f"\n⚠️  Increases exceed $10k limit. Scaling down by factor: {scale_factor:.3f}")
    
    total_increases = sum(d['Final'] for d in increase_details)
    unallocated = total_freed_budget - total_increases
    
    print(f"\nStep 5: Budget Allocation to Increase Channels")
    for detail in increase_details:
        print(f"  {detail['Channel']}: Proposed ${detail['Proposed']:.2f}, Max ${detail['Max Allowed']:.2f}, Final ${detail['Final']:.2f} (Weight: {detail['Weight']:.1%})")
    
    print(f"\nTotal Increases: ${total_increases:.2f}")
    print(f"Unallocated (Reserve): ${unallocated:.2f}")

else:
    print(f"\nNo channels qualify for increases.")
    unallocated = total_freed_budget

print("\n=== FINAL BUDGET REALLOCATION TABLE ===")
print("| Channel | Current | Change | New Budget | Classification |")
print("|---------|---------|--------|------------|----------------|")

for result in efficiency_results:
    current = result['Spend']
    classification = result.get('Classification', 'MAINTAIN')
    
    if classification == 'DECREASE_HEAVY':
        change = -current * 0.45
    elif classification == 'DECREASE_LIGHT':
        change = -current * 0.25
    elif classification == 'INCREASE':
        # Find the corresponding increase detail
        increase_detail = next((d for d in increase_details if d['Channel'] == result['Channel']), None)
        change = increase_detail['Final'] if increase_detail else 0
    else:
        change = 0
    
    new_budget = current + change
    change_str = f"${change:+.2f}" if change != 0 else "$0.00"
    
    print(f"| {result['Channel']:<9} | ${current:<7.2f} | {change_str:<8} | ${new_budget:<10.2f} | {classification:<14} |")

if unallocated > 0:
    print(f"| Reserve | - | ${unallocated:+.2f} | ${unallocated:<10.2f} | AVAILABLE |")

print("\n=== KEY INSIGHTS & RECOMMENDATIONS ===")

# Channel-by-channel analysis
for result in funnel_results:
    channel = result['Channel']
    
    # Get corresponding efficiency data
    eff_data = next(e for e in efficiency_results if e['Channel'] == channel)
    
    print(f"\n{channel}:")
    
    # Funnel insights
    if channel != 'Email':
        ctr_diff_str = result['CTR Diff']
        if float(ctr_diff_str.replace('pp', '').replace('+', '')) > 0:
            print(f"  ✓ CTR exceeding benchmark by {ctr_diff_str}")
        else:
            print(f"  ⚠ CTR below benchmark by {ctr_diff_str}")
    
    cvr_diff_str = result['CVR Diff']
    if float(cvr_diff_str.replace('pp', '').replace('+', '')) > 0:
        print(f"  ✓ CVR exceeding benchmark by {cvr_diff_str}")
    else:
        print(f"  ⚠ CVR below benchmark by {cvr_diff_str}")
    
    # Efficiency insights
    print(f"  • ROAS: {eff_data['ROAS']} {eff_data['ROAS Status']}")
    print(f"  • CPA: {eff_data['CPA']} {eff_data['CPA Status']}")
    print(f"  • Net Profit: {eff_data['Net Profit']} {eff_data['Profit Status']}")
    
    # Classification insight
    if 'Classification' in eff_data:
        print(f"  • Action: {eff_data['Classification']}")

print(f"\n=== OVERALL PERFORMANCE SUMMARY ===")
total_spend = sum(r['Spend'] for r in efficiency_results)
total_revenue = sum(r['Spend'] * float(r['ROAS'].replace('x', '')) for r in efficiency_results)
total_conversions = sum(r['Conversions'] for r in efficiency_results)
overall_roas = total_revenue / total_spend if total_spend > 0 else 0

print(f"Total Spend: ${total_spend:.2f}")
print(f"Total Revenue: ${total_revenue:.2f}")
print(f"Total Conversions: {total_conversions}")
print(f"Overall ROAS: {overall_roas:.2f}x")