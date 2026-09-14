import glob
import pandas as pd

# find the json file 
json_files=glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON files found in the data folder.")
    exit()

# use the latest json file

json_file=json_files[0]

# load json data into pandas DataFrame
df=pd.read_json(json_file)
print(f"Loaded {len(df)} stories from {json_file}")

# remove duplicates based on post_id
df=df.drop_duplicates(subset="post_id")
print(f"Removed duplicates, {len(df)} stories remaining.")

# remove rows where title,post_id,score is missing
df=df.dropna(subset=["title","post_id","score"])
print(f"Removed rows with missing title, post_id, or score, {len(df)} stories remaining.")

# convert score and num_comments to integer
df["score"]=df["score"].astype(int)
df["num_comments"]=df["num_comments"].astype(int)

# remove stories with score less than 5
df=df[df["score"]>=5]
print(f"Removed stories with score less than 5, {len(df)} stories remaining.")

# remove extra whitespace from title
df["title"]=df["title"].str.strip()

# save the cleaned DataFrame to a new CSV file
output_csv_file="data/trends_clean.csv"
df.to_csv(output_csv_file,index=False)

print(f"Cleaned data saved to {output_csv_file}")

print("\nStories per category:")
print(df["category"].value_counts())