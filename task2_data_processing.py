# Import required libraries
import pandas as pd
import os

# Step 1: Load JSON file
folder_path = "data"

# Find JSON file automatically
json_file = ""
for file in os.listdir(folder_path):
    if file.endswith(".json"):
        json_file = os.path.join(folder_path, file)

# Load into DataFrame
df = pd.read_json(json_file)

print(f"Loaded {len(df)} stories from {json_file}")

# Step 2: Clean the Data

# Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print("After removing duplicates:", len(df))

# Remove missing values
df = df.dropna(subset=["post_id", "title", "score"])
print("After removing nulls:", len(df))

# Convert data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low quality stories (score < 5)
df = df[df["score"] >= 5]
print("After removing low scores:", len(df))

# Remove extra spaces in title
df["title"] = df["title"].str.strip()

# Step 3: Save cleaned data as CSV
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"Saved {len(df)} rows to {output_file}")

# Print summary of stories per category
print("\nStories per category:")
print(df["category"].value_counts())
