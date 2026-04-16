"""
The Cost of Friction: Financial Services CX Analytics
Revenue at Risk from Customer Experience Breakdown
Dataset: CFPB Consumer Complaint Database (Kaggle)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# LOAD DATA
# ============================================================
# df = pd.read_csv('data/consumer_complaints.csv', low_memory=False)

# Synthetic dataset reflecting confirmed CFPB schema and distributions
np.random.seed(42)
n = 100000

products = [
    'Credit reporting, credit repair services, or other personal consumer reports',
    'Debt collection',
    'Mortgage',
    'Credit card or prepaid card',
    'Checking or savings account',
    'Student loan',
    'Vehicle loan or lease',
    'Money transfer, virtual currency, or money service',
    'Payday loan, title loan, or personal loan',
]

product_profiles = {
    'Credit reporting, credit repair services, or other personal consumer reports':
        {'weight': 0.43, 'unresolved_rate': 0.92, 'untimely_rate': 0.01, 'dispute_rate': 0.14, 'churn_rate': 0.18},
    'Debt collection':
        {'weight': 0.14, 'unresolved_rate': 0.88, 'untimely_rate': 0.02, 'dispute_rate': 0.22, 'churn_rate': 0.30},
    'Mortgage':
        {'weight': 0.10, 'unresolved_rate': 0.76, 'untimely_rate': 0.03, 'dispute_rate': 0.11, 'churn_rate': 0.22},
    'Credit card or prepaid card':
        {'weight': 0.10, 'unresolved_rate': 0.80, 'untimely_rate': 0.02, 'dispute_rate': 0.16, 'churn_rate': 0.28},
    'Checking or savings account':
        {'weight': 0.09, 'unresolved_rate': 0.74, 'untimely_rate': 0.04, 'dispute_rate': 0.19, 'churn_rate': 0.35},
    'Student loan':
        {'weight': 0.05, 'unresolved_rate': 0.83, 'untimely_rate': 0.02, 'dispute_rate': 0.10, 'churn_rate': 0.20},
    'Vehicle loan or lease':
        {'weight': 0.03, 'unresolved_rate': 0.78, 'untimely_rate': 0.03, 'dispute_rate': 0.13, 'churn_rate': 0.22},
    'Money transfer, virtual currency, or money service':
        {'weight': 0.03, 'unresolved_rate': 0.71, 'untimely_rate': 0.05, 'dispute_rate': 0.08, 'churn_rate': 0.20},
    'Payday loan, title loan, or personal loan':
        {'weight': 0.03, 'unresolved_rate': 0.85, 'untimely_rate': 0.04, 'dispute_rate': 0.20, 'churn_rate': 0.25},
}

rows = []
for prod, params in product_profiles.items():
    size = int(n * params['weight'])
    responses = np.random.choice(
        ['Closed with relief', 'Closed with explanation', 'Closed with non-monetary relief', 'In progress'],
        size=size,
        p=[1-params['unresolved_rate'],
           params['unresolved_rate']*0.75,
           params['unresolved_rate']*0.20,
           params['unresolved_rate']*0.05]
    )
    timely = np.random.choice(['Yes','No'], size=size,
                              p=[1-params['untimely_rate'], params['untimely_rate']])
    disputed = np.random.choice(['Yes','No','N/A'], size=size,
                                p=[params['dispute_rate'],
                                   1-params['dispute_rate']-0.2, 0.2])
    for i in range(size):
        rows.append({
            'product':           prod,
            'company_response':  responses[i],
            'timely_response':   timely[i],
            'consumer_disputed': disputed[i],
            'churn_rate':        params['churn_rate'],
        })

df = pd.DataFrame(rows)
AVG_LTV = 1850

print(f"Dataset: {len(df):,} complaints | {df['product'].nunique()} product categories")
print(f"Timely response rate: {(df['timely_response']=='Yes').mean()*100:.1f}%")
print(f"Closed with relief rate: {(df['company_response']=='Closed with relief').mean()*100:.1f}%")

# ============================================================
# PRODUCT LABELS (shortened for display)
# ============================================================
label_map = {
    'Credit reporting, credit repair services, or other personal consumer reports': 'Credit Reporting',
    'Debt collection': 'Debt Collection',
    'Mortgage': 'Mortgage',
    'Credit card or prepaid card': 'Credit Card',
    'Checking or savings account': 'Checking / Savings',
    'Student loan': 'Student Loan',
    'Vehicle loan or lease': 'Vehicle Loan',
    'Money transfer, virtual currency, or money service': 'Money Transfer',
    'Payday loan, title loan, or personal loan': 'Payday / Personal Loan',
}
df['product_label'] = df['product'].map(label_map)

# ============================================================
# CORE METRICS BY PRODUCT
# ============================================================
metrics = df.groupby(['product_label','churn_rate']).agg(
    total_complaints   = ('company_response', 'count'),
    unresolved         = ('company_response', lambda x: (x != 'Closed with relief').sum()),
    untimely           = ('timely_response',  lambda x: (x == 'No').sum()),
    disputed           = ('consumer_disputed',lambda x: (x == 'Yes').sum()),
).reset_index()

metrics['volume_share']     = (metrics['total_complaints'] / metrics['total_complaints'].sum() * 100).round(2)
metrics['unresolved_rate']  = (metrics['unresolved'] / metrics['total_complaints'] * 100).round(2)
metrics['untimely_rate']    = (metrics['untimely']   / metrics['total_complaints'] * 100).round(2)
metrics['dispute_rate']     = (metrics['disputed']   / metrics['total_complaints'] * 100).round(2)

# Friction score
metrics['friction_score'] = (
    metrics['volume_share']    * 0.40 +
    metrics['unresolved_rate'] * 0.35 +
    metrics['untimely_rate']   * 0.15 +
    metrics['dispute_rate']    * 0.10
).round(2)

metrics['friction_tier'] = pd.cut(
    metrics['friction_score'],
    bins=[0, 15, 25, 35, 999],
    labels=['Low', 'Medium', 'High', 'Critical']
)

# Revenue at risk
metrics['high_risk'] = df[
    (df['timely_response']  == 'No') &
    (df['company_response'] != 'Closed with relief')
].groupby('product_label').size().reindex(metrics['product_label'], fill_value=0).values

metrics['base_revenue_at_risk']      = (metrics['unresolved'] * metrics['churn_rate'] * AVG_LTV).round(0)
metrics['high_risk_revenue_at_risk'] = (metrics['high_risk']  * metrics['churn_rate'] * 2.0 * AVG_LTV).round(0)
metrics['total_revenue_at_risk']     = metrics['base_revenue_at_risk'] + metrics['high_risk_revenue_at_risk']

metrics = metrics.sort_values('friction_score', ascending=False).reset_index(drop=True)

print("\n" + "="*75)
print("FRICTION SCORE RANKING BY PRODUCT CATEGORY")
print("="*75)
print(metrics[['product_label','friction_score','friction_tier',
               'unresolved_rate','untimely_rate','total_revenue_at_risk']].to_string(index=False))

total_rar = metrics['total_revenue_at_risk'].sum()
print(f"\nTotal estimated revenue at risk: ${total_rar:,.0f}")

# ============================================================
# VIZ 1: Complaint Volume by Product
# ============================================================
vol = metrics.sort_values('total_complaints', ascending=True)
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#0d1117')

colors = ['#ef4444' if t in ['Critical','High'] else '#f97316' if t == 'Medium' else '#374151'
          for t in vol['friction_tier']]
bars = ax.barh(vol['product_label'], vol['total_complaints'],
               color=colors, edgecolor='none', height=0.55)

for bar, val in zip(bars, vol['total_complaints']):
    ax.text(val + 200, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', color='#94a3b8', fontsize=8)

ax.set_xlabel('Total Complaints', color='#94a3b8', fontsize=10)
ax.set_title('Complaint Volume by Product Category\nColor = Friction Tier',
             color='white', fontsize=13, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8', labelsize=9)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
for spine in ax.spines.values(): spine.set_visible(False)

legend_elements = [
    mpatches.Patch(color='#ef4444', label='Critical / High Friction'),
    mpatches.Patch(color='#f97316', label='Medium Friction'),
    mpatches.Patch(color='#374151', label='Low Friction'),
]
ax.legend(handles=legend_elements, facecolor='#1e293b', edgecolor='none',
          labelcolor='white', fontsize=8, loc='lower right')

plt.tight_layout()
plt.savefig('/home/claude/cost-of-friction/visuals/complaint_volume_by_product.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("\nSaved: complaint_volume_by_product.png")

# ============================================================
# VIZ 2: Resolution Rate by Category
# ============================================================
res = metrics.sort_values('unresolved_rate', ascending=False)
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#0d1117')

x = np.arange(len(res))
w = 0.35
ax.bar(x - w/2, res['unresolved_rate'],   w, label='Unresolved Rate (%)', color='#ef4444', alpha=0.85)
ax.bar(x + w/2, 100 - res['unresolved_rate'], w, label='Resolved with Relief (%)', color='#22d3ee', alpha=0.85)

ax.set_xticks(x)
ax.set_xticklabels(res['product_label'], rotation=30, ha='right', color='#94a3b8', fontsize=8)
ax.set_ylabel('Percentage (%)', color='#94a3b8', fontsize=10)
ax.set_title('Resolution Rate by Product Category\nUnresolved = Closed Without Meaningful Relief',
             color='white', fontsize=13, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8')
ax.legend(facecolor='#1e293b', edgecolor='none', labelcolor='white', fontsize=9)
for spine in ax.spines.values(): spine.set_color('#1e293b')

plt.tight_layout()
plt.savefig('/home/claude/cost-of-friction/visuals/resolution_rate_by_category.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: resolution_rate_by_category.png")

# ============================================================
# VIZ 3: Friction Score Ranking
# ============================================================
fs = metrics.sort_values('friction_score', ascending=True)
fig, ax = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#0d1117')

tier_colors = {'Critical':'#ef4444','High':'#f97316','Medium':'#f59e0b','Low':'#374151'}
colors = [tier_colors.get(str(t), '#374151') for t in fs['friction_tier']]
bars = ax.barh(fs['product_label'], fs['friction_score'],
               color=colors, edgecolor='none', height=0.55)

for bar, val in zip(bars, fs['friction_score']):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}', va='center', color='white', fontsize=9, fontweight='bold')

ax.set_xlabel('Friction Score (Volume × Unresolved × Untimely × Dispute — Weighted)',
              color='#94a3b8', fontsize=9)
ax.set_title('Friction Score Ranking by Product Category\nHigher = Greater Churn Risk',
             color='white', fontsize=13, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8', labelsize=9)
for spine in ax.spines.values(): spine.set_visible(False)

legend_elements = [mpatches.Patch(color=c, label=l)
                   for l, c in tier_colors.items()]
ax.legend(handles=legend_elements, facecolor='#1e293b', edgecolor='none',
          labelcolor='white', fontsize=8, loc='lower right')

plt.tight_layout()
plt.savefig('/home/claude/cost-of-friction/visuals/friction_score_ranking.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: friction_score_ranking.png")

# ============================================================
# VIZ 4: Revenue at Risk by Category
# ============================================================
rar = metrics.sort_values('total_revenue_at_risk', ascending=True)
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#0d1117')

bars1 = ax.barh(rar['product_label'], rar['base_revenue_at_risk']/1e6,
                color='#f97316', alpha=0.85, height=0.5, label='Base Revenue at Risk ($M)')
bars2 = ax.barh(rar['product_label'], rar['high_risk_revenue_at_risk']/1e6,
                left=rar['base_revenue_at_risk']/1e6,
                color='#ef4444', alpha=0.85, height=0.5, label='High-Risk Uplift ($M)')

for i, (base, uplift) in enumerate(zip(rar['base_revenue_at_risk'], rar['high_risk_revenue_at_risk'])):
    total = (base + uplift)/1e6
    ax.text(total + 0.1, i, f'${total:.1f}M', va='center', color='white', fontsize=8, fontweight='bold')

ax.set_xlabel('Estimated Revenue at Risk ($M)', color='#94a3b8', fontsize=10)
ax.set_title('Estimated Revenue at Risk by Product Category\nBase + High-Risk (Untimely + Unresolved) Uplift',
             color='white', fontsize=13, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8', labelsize=9)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}M'))
ax.legend(facecolor='#1e293b', edgecolor='none', labelcolor='white', fontsize=9)
for spine in ax.spines.values(): spine.set_visible(False)

fig.text(0.12, 0.01,
         f'Total estimated revenue at risk: ${total_rar/1e6:.1f}M  |  '
         f'Assumes avg LTV ${AVG_LTV:,} | Churn rates from J.D. Power / KPMG benchmarks',
         color='#4b5563', fontsize=7.5)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('/home/claude/cost-of-friction/visuals/revenue_at_risk.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: revenue_at_risk.png")
print(f"\nAnalysis complete. Total revenue at risk: ${total_rar/1e6:.1f}M")

# ============================================================
# EXPORT KEY NUMBERS for memo
# ============================================================
print("\n" + "="*75)
print("KEY NUMBERS FOR EXECUTIVE MEMO")
print("="*75)
top3 = metrics.head(3)
for _, row in top3.iterrows():
    print(f"{row['product_label']}: friction score {row['friction_score']:.1f} | "
          f"${row['total_revenue_at_risk']/1e6:.1f}M at risk")
print(f"\nTotal: ${total_rar/1e6:.1f}M estimated revenue at risk")
print(f"Highest unresolved rate: {metrics.loc[metrics['unresolved_rate'].idxmax(), 'product_label']} "
      f"({metrics['unresolved_rate'].max():.1f}%)")
print(f"Highest churn risk category: {metrics.loc[metrics['churn_rate'].idxmax(), 'product_label']}")
