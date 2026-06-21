import numpy as np
import pandas as pd
'''TO DO:
    refactor into functions
    matplotlib
'''
#import tables from local source
contracts = pd.read_csv(r"C:\Users\kalen\OneDrive\Desktop\portfolio\synth_ins data\contracts_clean.csv")
vehicles = pd.read_csv(r"C:\Users\kalen\OneDrive\Desktop\portfolio\synth_ins data\vehicles_clean.csv")
claims = pd.read_csv(r"C:\Users\kalen\OneDrive\Desktop\portfolio\synth_ins data\claims_clean.csv")

# fix data types BEFORE merging
contracts['zip_code'] = pd.to_numeric(contracts['zip_code'], errors='coerce')
contracts['inception_date_clean'] = pd.to_datetime(contracts['inception_date_clean'])
contracts['end_date_clean'] = pd.to_datetime(contracts['end_date_clean'])
contracts['annual_premium_clean'] = pd.to_numeric(contracts['annual_premium_clean'], errors='coerce')

# rename claims headers
claims.rename(columns={
    'string_field_0': 'claim_id',
    'string_field_1': 'contract_id',
    'string_field_4': 'claim_type',
    'string_field_7': 'claim_status',
    'string_field_8': 'expert_id',
    'string_field_9': 'liability'
}, inplace=True)

#change data type
claims['indemnified_amount_clean'] = pd.to_numeric(claims['indemnified_amount_clean'], errors='coerce')

#merge tables
pre_merged = contracts.merge(claims, on='contract_id', how='left')
merged = pre_merged.merge(vehicles, on='contract_id', how='left')

#Define euros to dollars exchange rate (using 1/1/26)
exchange_rate = 1.17
#add columns with USD conversions
merged['ann_prem_usd'] = merged['annual_premium_clean'] * exchange_rate
merged['dam_amt_usd'] = merged['damage_amount_clean'] * exchange_rate
merged['indem_amt_usd'] = merged['indemnified_amount_clean'] * exchange_rate

#set up variables and calculations useful for insurance purposes
merged['policy_period'] = (merged['end_date_clean'] - merged['inception_date_clean']).dt.days
merged['pro_rata'] = merged['policy_period'] / 365
merged['earned_premium'] = merged['ann_prem_usd'] * merged['pro_rata']
merged['loss_ratio'] = (merged['indem_amt_usd'] / merged['earned_premium']) * 100
merged['occurrence_date_clean'] = pd.to_datetime(merged['occurrence_date_clean'])
merged['occurrence_year'] = merged['occurrence_date_clean'].dt.year
merged['inception_year'] = merged['inception_date_clean'].dt.year

# Booleans for severity calculations
merged['freq_with_cwp'] = merged['indem_amt_usd'].notna()
merged['paid_only'] = merged['indem_amt_usd'] > 0

#create columns/ formulas for vizzes
freq_no_cwp_rate = merged['paid_only'].sum() / len(merged)
freq_with_cwp_rate = merged['freq_with_cwp'].sum() / len(merged)
severity = merged['indem_amt_usd'].sum() / merged['paid_only'].sum()
pure_premium = severity * freq_no_cwp_rate
paid = merged[merged['paid_only'] == True]['indem_amt_usd']

#create fields for sales data
expired = merged[merged['status'] == 'Expired']
cancelled = merged[merged['status'] == 'Cancelled']
renewed = merged[merged['status'] == 'Renewed']
active = merged[merged['status'] == 'Active']
suspended = merged[merged['status'] == 'Suspended']

'''sanity checks-----
check % of age column that is null
age_check = merged['client_age'].count()
age_null = (15000 - age_check) / 15000
percent_null = 100 * age_null
tot_ep = merged['earned_premium'].sum()
min_loss = merged[merged['indemnified_amount_clean'] <= 500]
age = merged[(merged['client_age'] >= 35) & (merged['client_age'] < 40)]'''

#Future expansion ideas
#expense_ratio = ()
#combined_ratio = expense_ratio + merged['loss_ratio']


#Save .csv file:
#merged.to_csv(r"C:\Users\kalen\OneDrive\Desktop\portfolio\synth_ins data\merged2.csv", index=False)



