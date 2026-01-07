import pandas as pd
import matplotlib.pyplot as plt

# Data from search results
data = {
    'Ticker': ['CHTR', 'EQT', 'APA', 'CMA', 'PSX', 'PFG', 'AIG', 'MOS', 'GM', 'VZ'],
    'Price': [210.00, 53.46, 25.43, 88.65, 136.65, 90.51, 78.07, 24.26, 81.00, 40.52],
    'High': [437.06, 62.23, 27.72, 91.26, 144.96, 92.10, 88.07, 38.23, 83.68, 47.36],
    'PE': [5.79, 18.24, 5.89, 16.96, 38.25, 13.02, 14.03, 6.30, 16.71, 8.58]
}

df = pd.DataFrame(data)

# Calculate Metric Y: 1 - (Price / 52W High)
# This represents the % drawdown from the high.
df['Drawdown'] = 1 - (df['Price'] / df['High'])

# Identify Pareto Front for (Min PE, Min Drawdown)
# "Best Price for Best Stability"
# Sort by PE (Primary Objective: Minimize)
df_sorted = df.sort_values(by='PE').reset_index(drop=True)

pareto_points = []
min_drawdown_so_far = float('inf')

for index, row in df_sorted.iterrows():
    # If this stock has a lower drawdown than any stock with a lower P/E, it's on the front.
    if row['Drawdown'] < min_drawdown_so_far:
        pareto_points.append(row)
        min_drawdown_so_far = row['Drawdown']

df_pareto = pd.DataFrame(pareto_points)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(df['PE'], df['Drawdown'], color='blue', label='S&P 500 Value Stocks')

# Highlight Pareto Front
plt.plot(df_pareto['PE'], df_pareto['Drawdown'], color='red', linestyle='--', marker='o', label='Pareto Front (Min P/E, Min Drawdown)')

# Annotate points
for i, txt in enumerate(df['Ticker']):
    plt.annotate(txt, (df['PE'][i], df['Drawdown'][i]), xytext=(5, 5), textcoords='offset points')

plt.xlabel('P/E Ratio (Lower is Better)')
plt.ylabel('Drawdown from 52-Week High (Lower is Better)')
plt.title('Pareto Front: P/E vs. Price Stability')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('pareto_front_plot.png')

print(df_pareto[['Ticker', 'PE', 'Drawdown']])
