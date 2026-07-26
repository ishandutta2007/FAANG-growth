import matplotlib.pyplot as plt
import pandas as pd

# 1. Establish the historical headcount dataset
data = {
    "Company": ["Meta", "Amazon", "Apple", "Netflix", "Alphabet"],
    "2019": [44942, 798000, 137000, 8600, 118899],
    "2020": [58604, 1298000, 147000, 9400, 135301],
    "2021": [71970, 1608000, 154000, 11300, 156500],
    "2022": [86482, 1541000, 164000, 12800, 190234],
    "2023": [67317, 1525000, 161000, 13000, 182502],
    "2024": [74067, 1556000, 164000, 14000, 183323],
    "2025": [78865, 1576000, 166000, 16000, 190820],
}
engineer_pct = {
    "Meta": 45,
    "Amazon": 3,
    "Apple": 41,
    "Netflix": 39,
    "Alphabet": 44,
    "Microsoft": 44,
}

df = pd.DataFrame(data)
years = ["2019", "2020", "2021", "2022", "2023", "2024", "2025"]

# Apply engineer percentage to the data
for company in df["Company"]:
    if company in engineer_pct:
        df.loc[df["Company"] == company, years] = df.loc[df["Company"] == company, years] * (engineer_pct[company] / 100.0)

# Convert back to integers
df[years] = df[years].astype(int)

# 2. Configure the plot canvas
plt.figure(figsize=(11, 6))
colors = {
    "Meta": "#1877F2",
    "Amazon": "#FF9900",
    "Apple": "#555555",
    "Netflix": "#E50914",
    "Alphabet": "#34A853",
}

# 3. Plot a trendline for each company
n_years = len(years) - 1
for idx, row in df.iterrows():
    company = row["Company"]
    counts = [row[y] for y in years]
    
    # Calculate CAGR
    start_value = counts[0]
    end_value = counts[-1]
    cagr = ((end_value / start_value) ** (1 / n_years)) - 1
    label_with_cagr = f"{company} (CAGR: {cagr*100:.1f}%)"
    
    plt.plot(
        years,
        counts,
        marker="o",
        linewidth=2.5,
        color=colors[company],
        label=label_with_cagr,
    )

# 4. Formatter enhancements for readability
plt.title("FAANG Historical Engineer Headcount Trends (2019 - 2025)", fontsize=14, pad=15)
plt.xlabel("Fiscal Year", fontsize=11, labelpad=10)
plt.ylabel("Total Global Engineers", fontsize=11, labelpad=10)

# Formats large numbers on the Y-axis with commas (e.g., 1,500,000)
plt.gca().get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, p: format(int(x), ","))
)

# Optional: Uncomment the next line if you want to inspect growth curves clearly without Amazon skewing the axis
# plt.yscale('log')

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title="Companies", frameon=True, facecolor="white")
plt.tight_layout()

# 5. Display the graph
plt.savefig("assets/FAANG_growth.png")

# 6. Calculate and plot year-over-year growth
plt.figure(figsize=(11, 6))
df_growth = df.set_index('Company')[years].diff(axis=1).dropna(axis=1)

# Plotting using pandas wrapper around matplotlib
df_growth.T.plot(kind='bar', figsize=(11, 6), color=[colors[c] for c in df_growth.index], width=0.7, ax=plt.gca())

plt.title("FAANG Year-over-Year Engineer Growth (2020 - 2025)", fontsize=14, pad=15)
plt.xlabel("Fiscal Year", fontsize=11, labelpad=10)
plt.ylabel("Net Engineer Change", fontsize=11, labelpad=10)
plt.xticks(rotation=0)

# Formats numbers with commas
plt.gca().get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, p: format(int(x), ","))
)

plt.grid(True, linestyle="--", alpha=0.5, axis='y')
plt.legend(title="Companies", frameon=True, facecolor="white")
plt.tight_layout()
plt.savefig("assets/FAANG_yoy_growth.png")

plt.show()
