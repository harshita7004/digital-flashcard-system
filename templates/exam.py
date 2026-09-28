# import numpy as np  # Commented out as requested
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# CSV Creation Part
num_countries = 10
num_days = 200
countries = [f'Country_{i+1}' for i in range(num_countries)]
data = {'Date': [], 'Country': [], 'Cases': [], 'Deaths': [], 'Recoveries': []}
start_date = datetime(2020, 1, 1)
for country in countries:
    total_cases, total_deaths, total_recoveries = 0, 0, 0
    for day in range(num_days):
        date = start_date + timedelta(days=day)
        daily_cases = max(0, int(np.random.normal(500, 100)))
        daily_deaths = max(0, int(daily_cases * np.random.uniform(0.01, 0.03)))
        daily_recoveries = max(0, int(daily_cases * np.random.uniform(0.8, 0.9)))
        total_cases += daily_cases
        total_deaths += daily_deaths
        total_recoveries += daily_recoveries
        data['Date'].append(date.strftime('%Y-%m-%d'))
        data['Country'].append(country)
        data['Cases'].append(total_cases)
        data['Deaths'].append(total_deaths)
        data['Recoveries'].append(total_recoveries)
df = pd.DataFrame(data)
df.to_csv('covid_data.csv', index=False)

# Analysis and Visualization
import numpy as np  # Re-importing numpy for analysis and visualization
covid_data = pd.read_csv('covid_data.csv')
data = covid_data.pivot(index='Date', columns='Country', values=['Cases', 'Deaths', 'Recoveries'])
data = data.fillna(0)
cases = data['Cases'].to_numpy()
deaths = data['Deaths'].to_numpy()
recoveries = data['Recoveries'].to_numpy()
countries = data['Cases'].columns

daily_new_cases = np.diff(cases, axis=0, prepend=0)
recovery_rates = np.divide(recoveries, cases, out=np.zeros_like(recoveries), where=cases != 0)
death_rates = np.divide(deaths, cases, out=np.zeros_like(deaths), where=cases != 0)

plt.figure(figsize=(12, 6))
for i, country in enumerate(countries[:5]):
    plt.plot(cases[:, i], label=country)
plt.xlabel('Days')
plt.ylabel('Cumulative Cases')
plt.title('Cumulative COVID-19 Cases Over Time')
plt.legend()
plt.show()

average_death_rates = death_rates.mean(axis=0)
top_10_countries = np.argsort(average_death_rates)[-10:]
top_10_death_rates = average_death_rates[top_10_countries]

plt.figure(figsize=(12, 6))
plt.bar(countries[top_10_countries], top_10_death_rates, color='red')
plt.xlabel('Country')
plt.ylabel('Average Death Rate')
plt.title('Top 10 Countries by COVID-19 Death Rate')
plt.show()

plt.figure(figsize=(12, 6))
plt.stackplot(range(daily_new_cases.shape[0]), daily_new_cases[:, :5].T, labels=countries[:5])
plt.xlabel('Days')
plt.ylabel('Daily New Cases')
plt.title('Daily COVID-19 Cases for Selected Countries')
plt.legend(loc='upper left')
plt.show()

metrics = np.array([cases.mean(axis=0), deaths.mean(axis=0), recoveries.mean(axis=0)])
correlation_matrix = np.corrcoef(metrics)

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', xticklabels=['Cases', 'Deaths', 'Recoveries'], yticklabels=['Cases', 'Deaths', 'Recoveries'])
plt.title('Correlation Between COVID-19 Metrics')
plt.show()
