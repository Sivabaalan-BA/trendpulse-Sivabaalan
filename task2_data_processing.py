import pandas as pd
import glob
import os


# Step 1: Load latest JSON file
# -------------------------------
files = glob.glob("data/trends_*.json")

if not files:
    print("No JSON file found in data/ folder")
    exit()

latest_file = max(files, key=os.path.getctime)

df = pd.read_json(latest_file)

print(f"Loaded {len(df)} stories from {latest_file}")


# Step 2: Clean the Data
# -------------------------------

# 1. Remove duplicates (based on post_id)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2. Remove rows with missing important values
df = df.dropna(subset=["title", "author", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# 4. Remove low-quality data (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Strip whitespace from title
df["title"] = df["title"].str.strip()


# Step 3: Save as CSV
# -------------------------------
output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")


# Step 4: Summary (stories per category)
# -------------------------------
print("\nStories per category:")
print(df["category"].value_counts())