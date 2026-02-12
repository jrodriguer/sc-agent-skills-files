import csv
from collections import defaultdict

# Read the CSV data
campaign_data = []
with open('/Users/juliorodriguez/Documents/sc-agent-skills-files/L1-partI/campaign_data_week1.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        campaign_data.append(row)

print("=== DATA QUALITY CHECK ===")
print(f"Total records: {len(campaign_data)}")

# Check for missing values
missing_report = {}
for field in ['impressions', 'clicks', 'conversions', 'spend', 'revenue', 'orders']:
    missing = sum(1 for row in campaign_data if not row[field] or row[field].strip() == '')
    if missing > 0:
        missing_report[field] = missing

if missing_report:
    print(f"Missing values: {missing_report}")
else:
    print("No missing values in numeric fields")

# Check for negative values
negative_report = {}
for field in ['impressions', 'clicks', 'conversions', 'spend', 'revenue', 'orders']:
    negative = sum(1 for row in campaign_data if row[field] and float(row[field]) < 0)
    if negative > 0:
        negative_report[field] = negative

if negative_report:
    print(f"Negative values: {negative_report}")
else:
    print("No negative values found")

# Check for conversions without clicks
conversions_no_clicks = sum(1 for row in campaign_data 
                          if row['conversions'] and float(row['conversions']) > 0 
                          and (not row['clicks'] or float(row['clicks']) == 0))
if conversions_no_clicks > 0:
    print(f"⚠️  Found {conversions_no_clicks} records with conversions but no clicks")
else:
    print("✓ No conversions without clicks found")

print("\n")

# Aggregate data by channel
channel_data = defaultdict(lambda: {
    'impressions': 0, 'clicks': 0, 'conversions': 0, 
    'spend': 0, 'revenue': 0, 'orders': 0, 'count': 0
})

for row in campaign_data:
    channel = row['channel']
    for field in ['impressions', 'clicks', 'conversions', 'spend', 'revenue', 'orders']:
        if row[field] and row[field].strip() != '':
            channel_data[channel][field] += float(row[field])
    channel_data[channel]['count'] += 1

print("=== AGGREGATED CHANNEL DATA ===")
print(f"{'Channel':<12} {'Impressions':<12} {'Clicks':<8} {'Conversions':<12} {'Spend':<10} {'Revenue':<10} {'Orders':<8}")
print("-" * 80)
for channel, data in sorted(channel_data.items()):
    print(f"{channel:<12} {data['impressions']:<12.0f} {data['clicks']:<8.0f} {data['conversions']:<12.0f} ${data['spend']:<9.2f} ${data['revenue']:<9.2f} {data['orders']:<8.0f}")

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

print("=== FUNNEL ANALYSIS ===")
print("| Channel | CTR Actual | CTR Benchmark | CTR Diff | CVR Actual | CVR Benchmark | CVR Diff |")
print("|---------|------------|---------------|----------|------------|---------------|----------|")

funnel_results = []
for channel, data in sorted(channel_data.items()):
    if channel == 'Email':
        ctr_actual = None
        ctr_diff = None
        ctr_bench = "N/A"
    else:
        ctr_actual = (data['clicks'] / data['impressions']) * 100 if data['impressions'] > 0 else 0
        ctr_bench_val = benchmarks.get(channel, {}).get('ctr', 0)
        ctr_bench = f"{ctr_bench_val:.1f}%"
        ctr_diff = ctr_actual - ctr_bench_val
        ctr_diff_str = f"{ctr_diff:+.2f}pp"
    
    cvr_actual = (data['conversions'] / data['clicks']) * 100 if data['clicks'] > 0 else 0
    cvr_bench_val = benchmarks.get(channel, {}).get('cvr', 0)
    cvr_bench = f"{cvr_bench_val:.1f}%"
    cvr_diff = cvr_actual - cvr_bench_val
    cvr_diff_str = f"{cvr_diff:+.2f}pp"
    
    funnel_results.append({
        'channel': channel,
        'ctr_actual': ctr_actual,
        'cvr_actual': cvr_actual,
        'ctr_diff': ctr_diff,
        'cvr_diff': cvr_diff
    })
    
    ctr_actual_str = f"{ctr_actual:.2f}%" if ctr_actual is not None else "N/A"
    if ctr_diff is not None:
        ctr_diff_display = f"{ctr_diff:+.2f}pp"
    else:
        ctr_diff_display = "N/A"
    print(f"| {channel:<9} | {ctr_actual_str:<10} | {ctr_bench:<13} | {ctr_diff_display:<8} | {cvr_actual:.2f}% | {cvr_bench:<13} | {cvr_diff_str:<8} |")

print("\n")

print("=== EFFICIENCY ANALYSIS ===")
print("| Channel | ROAS | Status | CPA | Status | Net Profit | Status |")
print("|---------|------|--------|-----|--------|------------|--------|")

efficiency_results = []
for channel, data in sorted(channel_data.items()):
    # ROAS
    roas = data['revenue'] / data['spend'] if data['spend'] > 0 else 0
    roas_status = "[OK] Above" if roas >= target_roas else "[X] Below"
    
    # CPA
    cpa = data['spend'] / data['conversions'] if data['conversions'] > 0 else float('inf')
    cpa_status = "[OK] Below" if cpa <= max_cpa else "[X] Above"
    
    # Net Profit
    total_costs = data['spend'] + (data['orders'] * shipping_cost) + (data['revenue'] * product_cost_pct)
    net_profit = data['revenue'] - total_costs
    profit_status = "[OK] Positive" if net_profit > 0 else "[X] Negative"
    
    efficiency_results.append({
        'channel': channel,
        'spend': data['spend'],
        'conversions': data['conversions'],
        'roas': roas,
        'roas_status': roas_status,
        'cpa': cpa,
        'cpa_status': cpa_status,
        'net_profit': net_profit,
        'profit_status': profit_status
    })
    
    print(f"| {channel:<9} | {roas:.2f}x | {roas_status:<6} | ${cpa:.2f} | {cpa_status:<6} | ${net_profit:.2f} | {profit_status:<6} |")

print("\n")

# Budget Reallocation Analysis
print("=== BUDGET REALLOCATION ANALYSIS ===")

# Rule 0: Check eligibility (>= 50 conversions)
print("Step 1: Eligibility Check (>= 50 conversions)")
for result in efficiency_results:
    status = "✓ Eligible" if result['conversions'] >= 50 else "✗ Ineligible"
    print(f"  {result['channel']}: {result['conversions']:.0f} conversions - {status}")

# Classify channels
print("\nStep 2: Channel Classification")
print("| Channel | ROAS | % of Target | CPA | % of Max | Net Profit | Classification |")
print("|---------|------|-------------|-----|----------|------------|----------------|")

for result in efficiency_results:
    if result['conversions'] < 50:
        classification = 'INSUFFICIENT_DATA -> MAINTAIN'
        roas_pct = 0
        cpa_pct = 0
    else:
        roas_pct_target = (result['roas'] / target_roas) * 100
        cpa_pct_max = (result['cpa'] / max_cpa) * 100
        net_profit = result['net_profit']
        
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
        
        roas_pct = roas_pct_target
        cpa_pct = cpa_pct_max
    
    result['classification'] = classification
    result['roas_pct'] = roas_pct
    result['cpa_pct'] = cpa_pct
    
    print(f"| {result['channel']:<9} | {result['roas']:.2f}x | {roas_pct:<11.0f}% | ${result['cpa']:.2f} | {cpa_pct:<8.0f}% | ${result['net_profit']:.2f} | {classification:<14} |")

# Calculate budget changes
decrease_heavy = [r for r in efficiency_results if r['classification'] == 'DECREASE_HEAVY']
decrease_light = [r for r in efficiency_results if r['classification'] == 'DECREASE_LIGHT']
increase = [r for r in efficiency_results if r['classification'] == 'INCREASE']

print(f"\nStep 3: Budget Change Calculations")
print(f"Channels to decrease heavy: {[r['channel'] for r in decrease_heavy]}")
print(f"Channels to decrease light: {[r['channel'] for r in decrease_light]}")
print(f"Channels to increase: {[r['channel'] for r in increase]}")

# Calculate decreases
total_freed_budget = 0
decrease_details = []

for result in decrease_heavy:
    decrease_amount = result['spend'] * 0.45
    total_freed_budget += decrease_amount
    decrease_details.append({'channel': result['channel'], 'amount': decrease_amount, 'type': 'DECREASE_HEAVY'})

for result in decrease_light:
    decrease_amount = result['spend'] * 0.25
    total_freed_budget += decrease_amount
    decrease_details.append({'channel': result['channel'], 'amount': decrease_amount, 'type': 'DECREASE_LIGHT'})

print(f"\nStep 4: Freed Budget from Decreases: ${total_freed_budget:.2f}")
for detail in decrease_details:
    print(f"  {detail['channel']}: -${detail['amount']:.2f} ({detail['type']})")

# Allocate to increase channels
increase_details = []
user_limit = 10000  # User can shift up to $10k
increase_cap = 0.15  # 15% per channel limit

if increase and total_freed_budget > 0:
    # Calculate weights based on Net Profit
    total_net_profit = sum(r['net_profit'] for r in increase)
    
    for result in increase:
        weight = result['net_profit'] / total_net_profit if total_net_profit > 0 else 0
        proposed_increase = total_freed_budget * weight
        max_increase = result['spend'] * increase_cap
        capped_increase = min(proposed_increase, max_increase)
        
        increase_details.append({
            'channel': result['channel'],
            'proposed': proposed_increase,
            'max_allowed': max_increase,
            'final': capped_increase,
            'weight': weight
        })
    
    # Check if total increases exceed user limit
    total_proposed = sum(d['final'] for d in increase_details)
    
    if total_proposed > user_limit:
        scale_factor = user_limit / total_proposed
        for detail in increase_details:
            detail['final'] = detail['final'] * scale_factor
        print(f"\n⚠️  Increases exceed $10k limit. Scaling down by factor: {scale_factor:.3f}")
    
    total_increases = sum(d['final'] for d in increase_details)
    unallocated = total_freed_budget - total_increases
    
    print(f"\nStep 5: Budget Allocation to Increase Channels")
    for detail in increase_details:
        print(f"  {detail['channel']}: Proposed ${detail['proposed']:.2f}, Max ${detail['max_allowed']:.2f}, Final ${detail['final']:.2f} (Weight: {detail['weight']:.1%})")
    
    print(f"\nTotal Increases: ${total_increases:.2f}")
    print(f"Unallocated (Reserve): ${unallocated:.2f}")

else:
    print(f"\nNo channels qualify for increases.")
    unallocated = total_freed_budget
    total_increases = 0

print("\n=== FINAL BUDGET REALLOCATION TABLE ===")
print("| Channel | Current | Change | New Budget | Classification |")
print("|---------|---------|--------|------------|----------------|")

for result in efficiency_results:
    current = result['spend']
    classification = result['classification']
    
    if classification == 'DECREASE_HEAVY':
        change = -current * 0.45
    elif classification == 'DECREASE_LIGHT':
        change = -current * 0.25
    elif classification == 'INCREASE':
        # Find the corresponding increase detail
        increase_detail = next((d for d in increase_details if d['channel'] == result['channel']), None)
        change = increase_detail['final'] if increase_detail else 0
    else:
        change = 0
    
    new_budget = current + change
    change_str = f"${change:+.2f}" if change != 0 else "$0.00"
    
    print(f"| {result['channel']:<9} | ${current:<7.2f} | {change_str:<8} | ${new_budget:<10.2f} | {classification:<14} |")

if unallocated > 0:
    print(f"| Reserve | - | ${unallocated:+.2f} | ${unallocated:<10.2f} | AVAILABLE |")

print("\n=== KEY INSIGHTS & RECOMMENDATIONS ===")

# Channel-by-channel analysis
for result in funnel_results:
    channel = result['channel']
    
    # Get corresponding efficiency data
    eff_data = next(e for e in efficiency_results if e['channel'] == channel)
    
    print(f"\n{channel}:")
    
    # Funnel insights
    if channel != 'Email':
        if result['ctr_diff'] > 0:
            print(f"  ✓ CTR exceeding benchmark by +{result['ctr_diff']:.2f}pp")
        else:
            print(f"  ⚠ CTR below benchmark by {result['ctr_diff']:.2f}pp")
    
    if result['cvr_diff'] > 0:
        print(f"  ✓ CVR exceeding benchmark by +{result['cvr_diff']:.2f}pp")
    else:
        print(f"  ⚠ CVR below benchmark by {result['cvr_diff']:.2f}pp")
    
    # Efficiency insights
    print(f"  • ROAS: {eff_data['roas']:.2f}x {eff_data['roas_status']}")
    print(f"  • CPA: ${eff_data['cpa']:.2f} {eff_data['cpa_status']}")
    print(f"  • Net Profit: ${eff_data['net_profit']:.2f} {eff_data['profit_status']}")
    
    # Classification insight
    print(f"  • Action: {eff_data['classification']}")

print(f"\n=== OVERALL PERFORMANCE SUMMARY ===")
total_spend = sum(r['spend'] for r in efficiency_results)
total_revenue = sum(r['spend'] * r['roas'] for r in efficiency_results)
total_conversions = sum(r['conversions'] for r in efficiency_results)
overall_roas = total_revenue / total_spend if total_spend > 0 else 0

print(f"Total Spend: ${total_spend:.2f}")
print(f"Total Revenue: ${total_revenue:.2f}")
print(f"Total Conversions: {total_conversions:.0f}")
print(f"Overall ROAS: {overall_roas:.2f}x")

# Additional insights
print(f"\n=== ADDITIONAL INSIGHTS ===")
best_roas = max(efficiency_results, key=lambda x: x['roas'])
worst_roas = min(efficiency_results, key=lambda x: x['roas'] if x['roas'] > 0 else float('inf'))
best_cpa = min(efficiency_results, key=lambda x: x['cpa'] if x['cpa'] > 0 else float('inf'))
worst_cpa = max(efficiency_results, key=lambda x: x['cpa'])

print(f"🏆 Best ROAS: {best_roas['channel']} ({best_roas['roas']:.2f}x)")
print(f"⚠️  Worst ROAS: {worst_roas['channel']} ({worst_roas['roas']:.2f}x)")
print(f"🎯 Best CPA: {best_cpa['channel']} (${best_cpa['cpa']:.2f})")
print(f"💸 Worst CPA: {worst_cpa['channel']} (${worst_cpa['cpa']:.2f})")

profitable_channels = [r for r in efficiency_results if r['net_profit'] > 0]
unprofitable_channels = [r for r in efficiency_results if r['net_profit'] <= 0]

print(f"\n💰 Profitable Channels: {len(profitable_channels)}/4 ({', '.join(r['channel'] for r in profitable_channels)})")
print(f"📉 Unprofitable Channels: {len(unprofitable_channels)}/4 ({', '.join(r['channel'] for r in unprofitable_channels)})")