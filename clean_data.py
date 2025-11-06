import pandas as pd

# Load data
df = pd.read_csv("imdb_top250.csv")

# --- Convert Year column to string first ---
df["Year"] = df["Year"].astype(str)

# Extract only the 4-digit year
df["Year"] = df["Year"].str.extract(r"(\d{4})")

# Convert Rating to numeric
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# Drop missing ratings
df = df.dropna(subset=["Rating"])

# Sort by Rating descending
df = df.sort_values(by="Rating", ascending=False)

# Save cleaned version
df.to_csv("imdb_top250_cleaned.csv", index=False, encoding="utf-8-sig")

print("✅ Data cleaned and saved to imdb_top250_cleaned.csv")
print(df.head(10))