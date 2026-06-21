# Insurance-Data-Portfolio
Underwriting metrics with synthetic insurance dataset

Project Overview
Dataset is a synthetic P&C insurance dataset sourced from Kaggle, designed to reflect real-world loss distributions.  Dataset contains 15,000 rows for more than three years across four lines of business in five territories.  It can be found on Kaggle: Insurance Dataset for Data Engineering Practice. Data is prepared for underwriting and pricing personnel to make informed, strategic-level decisions.

Data Pipeline
*	Cleaned three separate data tables of contracts, vehicles, and claims using  BigQuery/SQL.  
*	Imported tables into Python to finalize data cleaning using NumPy and Pandas.  Merged the three tables into one table using common key of ‘contract_id’.
*	Created columns, functions, and objects to facilitate loss data visuals.  Including a simple pro rata calculator, Boolean masks, and exchange rate conversion (Euros to Dollars on 1/1/26).
*	Used Matplotlib/ Seaborn to create visuals including heatmap, scatter, box plot and bar graphs.
*	Transferred merged table into Tableau to render visualizations. Created calculations and parameters to transform data into meaningful tools for decision-making.
*	Created dashboards from worksheets in Tableau.  Created dynamic charts to toggle closed without payment claims for loss frequency.  Developed a dynamic loss distribution histogram with bin size selector.

Data decisions made and rationale:
-Included null values for gender as they represent over 20% of the dataset.  Management should be aware and adjust data input/ collection methods.
-Data for occurrence years 2025 and 2026 were omitted from the Python trend analysis as there were few data points.  Whether a product of a synthetic dataset, longer liability tails in France/ Europe, or a data collection issue, it skews the data unjustifiably.  Only two years for the trend analysis is not ideal, but it’s still a useful metric for management, actuaries/ pricing, and underwriting.
-Some values for engine power were not labeled.  As the integer values were in line with horsepower, assumed the values were for horsepower.   A user interface forcing a label will eliminate future confusion and ensure data is accurate.

Insurance conclusions based on the Data:
1.	Auto loss frequency^1 does not conform to expected age results. Ages 35-39 have a frequency three times higher (1.091%) than ages 18-23 (0.300%). Rates for 35-39 segment may be inadequate.
2.	Although 20.6% of gender records are null, the remaining 79.4% reflects a near-perfect 50/50 male/female split (50.3% male, 49.7% female)^2, consistent with global gender demographics. Null records were retained and flagged as Unknown rather than excluded as the unknown segment produced the highest loss ratio at 2.49% compared to 1.85% (female) and 1.13% (male).  This suggests potential adverse selection risk in records with missing demographic data.
3.	There are no losses for health or life lines of business. Although life policies typically have longer tails^3 than property & casualty lines, we’d expect to at least see some losses based on mortality rates (0.78%)^4.  Coupled with zero health claims, it is more likely we do not have data for claims in those lines of business.
4.	Loss frequency for low risk zone of 0.3932% is more than twice the high risk zone(0.1648%).  Although this may change with more years/ data points, management should consider the metrics of each risk zone.
5.	Auto is the worst performing product by loss frequency at 0.5358%.  Auto is likely still profitable, but the dataset lacks underwriting expense^5 data to properly determine combined ratio^6.

Methodology Notes:

*Python heatmap compares correlations across different metrics using the Pearson correlation coefficient.  Positive numbers indicate a directly proportional relationship with values closer to one indicating a stronger correlation.  Negative numbers show an inversely proportional relationship.  For more info, see: Pearson correlation coefficient - Wikipedia. 
*All currency amounts were converted from Euros to US Dollars at the 01/01/2026 exchange rate of 1 to $1.17.

Footnotes:
1.	Loss frequency: the number of times a specific loss or risk event occurs over a given period.
2.	2024, Human sex ratio - Wikipedia
3.	Tail: The period following policy cancellation/ expiration in which claims are made for occurrences during the policy period.
4.	2025, World Death Rate (1950-2026)
5.	Underwriting expense: the direct and indirect costs associated with underwriting.
6.	Combined ratio: a measure of underwriting profitability comparing underwriting expenses and losses to earned premium.
