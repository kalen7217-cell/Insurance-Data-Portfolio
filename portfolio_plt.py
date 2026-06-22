import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


#Import .csv file
merged = pd.read_csv(r"C:\Users\kalen\OneDrive\Desktop\portfolio\synth_ins data\merged2.csv")

#clean 'power column'
def convert_power(val):
    if pd.isna(val):
        return np.nan
    val = str(val).strip()
    if 'kW' in val:
        return float(val.replace('kW', '').strip()) * 1.341
    elif 'HP' in val or 'hp' in val:
        return float(val.replace('HP', '').replace('hp', '').strip())
    elif 'CV' in val:
        return float(val.replace('CV', '').strip()) * 0.986
    else:
        return float(val)

#apply changes of convert_power to pwer column
merged['power_clean'] = merged['power'].apply(convert_power)

#create aliases for heatmap labels
labels = {
    'loss_ratio': 'Loss Ratio',
    'earned_premium': 'Earned Premium',
    'client_age': 'Client Age',
    'previous_claims': 'Previous Claims',
    'current_value_clean': 'Vehicle Current Value',
    'power_clean': 'Engine Power (HP)',
    'indem_amt_usd': 'Losses Paid'
}

#set up columns/ displays for heatmap
corr_cols = ['loss_ratio', 'earned_premium', 'client_age', 'previous_claims', 'current_value_clean', 'power_clean', 'indem_amt_usd']
corr_matrix = merged[corr_cols].corr()
corr_matrix_labeled = corr_matrix.rename(index=labels, columns=labels)

#create heat map
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix_labeled,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            vmin=-1,
            vmax=1)
plt.title('Heatmap Correlation of Risk Factors vs. Loss Ratio')
plt.tight_layout()

#assign colors for scatter plot
colors = {
    'Home': '#1F3A5F',
    'Health': '#2E86AB',
    'Auto': '#E84855',
    'Life': '#6B4C9A'
}

#create scatter plot
fig, ax = plt.subplots(figsize=(10, 7))
for product, group in merged.groupby('product'):
    ax.scatter(group['earned_premium'],
    group['indem_amt_usd'],
    c=colors[product],
    label=product,
    alpha=0.5,
    s=30)

#set labels/ display for scatter plot 
ax.set_xlabel('Earned Premium')
ax.set_ylabel('Losses Paid')
ax.set_title('Earned Premium vs Losses Paid by Product Line')
ax.legend(title='Product Line')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.set_ylim(bottom=-500)
plt.tight_layout()

#create box plot for severity by line of coverage
paid_claims = merged[merged['paid_only'] == True]
fig, ax = plt.subplots(figsize=(10, 7))
bp = paid_claims.boxplot(column='indem_amt_usd',
                    by='product',
                    ax=ax,
                    patch_artist=True)
#change boxplot colors (red=auto)
colors_box = ['#E84855', '#1F3A5F']
for patch, color in zip(bp.patches, colors_box):
    patch.set_facecolor(color)

#set labels/ display for box plot
ax.set_xlabel('Policy Line')
ax.set_ylabel('Losses Paid') 
ax.set_title('Loss Severity Distribution by Policy Line')
#add text annotation to describe what's happening
ax.text(0.5, -0.12, 'Horizontal lines above and below bars shows 25th-75th percentile range. Line within bar = median. Points = outliers.',
        transform=ax.transAxes, ha='center', fontsize=9, color='#333333')
plt.suptitle('') #remove default boxplot title
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _:f'${x:,.0f}'))
plt.tight_layout()

#build data for trend analysis
trend = merged[(merged['occurrence_year'] >= 2023) & (merged['occurrence_year'] <= 2024)].groupby('occurrence_year').agg(
    frequency=('paid_only', 'mean'),
    severity=('indem_amt_usd', lambda x: x[x > 0].mean())
).reset_index()

#set labels/ display for trend analysis
fig, ax1 = plt.subplots(figsize=(10, 7))
ax2 = ax1.twinx()
ax1.plot(trend['occurrence_year'], trend['frequency'], 
         color='#1F3A5F', marker='o', linewidth=2, label='Frequency')
ax2.plot(trend['occurrence_year'], trend['severity'], 
         color='#E84855', marker='o', linewidth=2, label='Severity')
ax1.set_xlabel('Occurrence Year')
ax1.set_ylabel('Loss Frequency (%)', color='#1F3A5F')
ax2.set_ylabel('Loss Severity', color='#E84855')
ax1.set_title('Loss Frequency & Severity Trends by Occurrence Year')
ax1.text(0.5, -0.12, 'CWP Claims Not Included', 
         transform=ax1.transAxes, ha='center', fontsize=9, color='#333333')
ax1.tick_params(axis='y', labelcolor='#1F3A5F')
ax1.set_xticks([2023, 2024])
ax2.tick_params(axis='y', labelcolor='#E84855')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='right')
plt.tight_layout()

#bar chart calc
liability_severity = merged.groupby('liability')['indem_amt_usd'].mean().reset_index()

#clean x axis labels for bar
liability_severity['liability'] = liability_severity['liability'].str.replace('_', ' ').str.title()
liability_severity['liability'] = liability_severity['liability'].replace('Force Majeure', 'Act of God')

#create bar chart bar display settings
fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(data=liability_severity,
            x='liability',
            y='indem_amt_usd',
            palette=['#1F3A5F'],
            ax=ax)
ax.set_xlabel('Liability Type')
ax.set_ylabel('Average Loss Severity')
ax.set_title('Average Loss Severity by Loss Type')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()

#create fields for bar2 graph
policy_status = merged['status'].value_counts(normalize=True).reset_index()
policy_status.columns = ['status', 'percentage']
policy_status['percentage'] = policy_status['percentage'] * 100

#write/label bar2
fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(data=policy_status,
            x='status',
            y='percentage',
            palette=['#1F3A5F'],
            ax=ax)
ax.set_xlabel('Policy Status')
ax.set_ylabel('Percentage of Policies')
ax.set_title('Policy Lifecycle Distribution') 
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.1f}%'))
ax.text(0.5, -0.08, '*Active and Suspended policies have not yet reached term', 
        transform=ax.transAxes, ha='center', fontsize=9, color='#333333')
plt.tight_layout()

#start the show
plt.show()

