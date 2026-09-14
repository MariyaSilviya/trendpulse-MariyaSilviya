import pandas as pd
import numpy as np

# load the cleaned CSV from task 2
df=pd.read_csv("data/trends_clean.csv")
print("Loaded data:",df.shape)

print("\nFirst 5 rows of the cleaned data:")
print(df.head())

# calculate average score and average comments
average_score=np.mean(df["score"])
average_comments=np.mean(df["num_comments"])

print(f"\nAverage Score: {average_score}")
print(f"Average Comments: {average_comments}")

# calculate statistics using Numpy
mean_score=np.mean(df["score"])
median_score=np.median(df["score"])
std_score=np.std(df["score"])
max_score=np.max(df["score"])
min_score=np.min(df["score"])

print("\n -------------Numpy Stats-----------")
print(f"Mean Score: {mean_score}")
print(f"Median Score: {median_score}")
print(f"Standard Deviation of Score: {std_score}")
print(f"Maximum Score: {max_score}")
print(f"Minimum Score: {min_score}")

# count stories per category
category_counts=df["category"].value_counts()

most_common_category=category_counts.idxmax()
most_common_count=category_counts.max()

print(f"\nMost Common Category: {most_common_category} with {most_common_count} stories")

# find the story with the highest number of comments
most_commented_index=df["num_comments"].idxmax()
most_commented_title=df.loc[most_commented_index,"title"]
most_commented_count=df.loc[most_commented_index,"num_comments"]
print(f"\nMost Commented Story: {most_commented_title} with {most_commented_count} comments")

# Add engagement column using formula from the task
df["engagement"]=(df["num_comments"]/df["score"]+1)

# add is_popular column based on average score
df["is_popular"]=df["score"]>average_score

# save the analysed data for task 4
output_csv_file="data/trends_analysed.csv"
df.to_csv(output_csv_file,index=False)

print(f"\nAnalyzed data saved to {output_csv_file}")