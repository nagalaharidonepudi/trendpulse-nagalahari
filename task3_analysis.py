# Import libraries
import pandas as pd
import numpy as np

# Step 1: Load data
file_path = "data/trends_clean.csv"
df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}")

# Show first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average values
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("\nAverage score:", avg_score)
print("Average comments:", avg_comments)

# Step 2: NumPy analysis

scores = df["score"].values

print("\n--- NumPy Stats ---")
print("Mean score   :", np.mean(scores))
print("Median score :", np.median(scores))
print("Std deviation:", np.std(scores))
print("Max score    :", np.max(scores))
print("Min score    :", np.min(scores))

# Category with most stories
top_category = df["category"].value_counts().idxmax()
top_count = df["category"].value_counts().max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Most commented story
max_comments = df["num_comments"].max()
top_story = df[df["num_comments"] == max_comments].iloc[0]

print(f"\nMost commented story: \"{top_story['title']}\" — {max_comments} comments")

# Step 3: Add new columns

# Engagement = comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular if score > average
df["is_popular"] = df["score"] > avg_score

# Step 4: Save new file
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")