import pandas as pd

# Load survey data
df = pd.read_csv('survey_results_public.csv', low_memory=False)
sch_df = pd.read_csv('survey_results_schema.csv', low_memory=False)

# Configure display settings for better readability in output
pd.set_option('display.max_columns', 85)
pd.set_option('display.max_rows', None)


# Clean up 'DevType' by replacing specific entries with None and dropping missing values
df['DevType'] = df['DevType'].replace('Other (please specify):', None)
df.dropna(subset=['DevType'], inplace=True)

# Analyze salary data by development type
groups = df.groupby('DevType')
professions = df['DevType'].unique()

# Iterate through each profession and compute salary statistics
for profession in professions:
    salary = groups.get_group(profession)['ConvertedCompYearly'].agg(['mean', 'median'])
    mean = salary.mean()
    median = salary.median()
    print(f"{profession}: the mean salary is ${mean}, and the median salary is ${median}", end="\n")

# Analyze people's stances on AI benefits
grouped_counts = df.groupby('AIBen')['ResponseId'].count()
total_responses = grouped_counts.sum()
normalized_counts = grouped_counts / total_responses
print("Normalized counts of people's stances on AI benefits:")
print(normalized_counts, end = '\n\n')

# Analyze the most popular methods to learn coding
expansion = df['LanguageHaveWorkedWith'].str.split(';').explode()
print("Most popular languages worked with:")
print(expansion.value_counts(), end ='\n\n')

# Analyze education levels of high earners in the US
filt = (df['ConvertedCompYearly'] > 70000) & (df['Country'] == 'United States of America')
education = df[filt]['EdLevel']
print("Education levels of US respondents earning more than $70,000:")
print(education.value_counts())


