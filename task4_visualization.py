import pandas as pd
import matplotlib.pyplot as plt
import os

# load analyzed data from task 3
df=pd.read_csv("data/trends_analysed.csv")

# create outputs folder if it does not already exist
os.makedirs("outputs",exist_ok=True)

print("Data Loaded successfully")
print(f"Total stories: {len(df)}")


# select 1 stories with the highest scores

top_stories=df.nlargest(10,"score").copy()

# shorten long titles so they fit better on the chart

top_stories["short_title"]=top_stories["title"].apply(lambda title:title[:50]+"..." if len(title)>50 else title)

# create horizontal bar chart

plt.figure(figsize=(10,6))
plt.barh(top_stories["short_title"],top_stories["score"])
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

# put the highest score at the top of the chart
plt.gca().invert_yaxis()
# Save before show

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")

plt.close()
print("Chart 1 saved: outputs/chart1_top_stories.png")


# count the number of stories in each category
category_counts=df["category"].value_counts()

# create bar chart
plt.figure(figsize=(8,5))
plt.bar(category_counts.index,category_counts.values,color=["blue","green","orange","red","purple"])

plt.title("Stories per category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")

plt.close()
print("Chart 2 saved: outputs/chart2_categories.png")


# separate popular and non-popular stories

popular=df[df["is_popular"]==True]
not_popular=df[df["is_popular"]==False]

# create scatter plot
plt.figure(figsize=(10,6))

plt.scatter(popular["score"],popular["num_comments"],color="red",label="Popular Stories")
plt.scatter(not_popular["score"],not_popular["num_comments"],color="blue",label="Non-Popular Stories")

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")

plt.close()
print("Chart 3 saved: outputs/chart3_scatter.png")


# create dashboard with 2 rows and 2 columns
fig,axes=plt.subplots(2,2,figsize=(16,10))

# Dashboard Chart 1

axes[0,0].barh(top_stories["short_title"],top_stories["score"])

axes[0,0].set_title("Top 10 Stories by Score")
axes[0,0].set_xlabel("Score")
axes[0,0].set_ylabel("Story Title")
axes[0,0].invert_yaxis()


# dashboard Chart 2
axes[0,1].bar(category_counts.index,category_counts.values,color=["blue","green","orange","red","purple"])
axes[0,1].set_title("Stories per Category")
axes[0,1].set_xlabel("Category")
axes[0,1].set_ylabel("Number of Stories")

# dashboard Chart 3
axes[1,0].scatter(popular["score"],popular["num_comments"],color="red",label="Popular Stories")
axes[1,0].scatter(not_popular["score"],not_popular["num_comments"],color="blue",label="Non-Popular Stories")
axes[1,0].set_title("Score vs Comments")
axes[1,0].set_xlabel("Score")
axes[1,0].set_ylabel("Number of Comments")
axes[1,0].legend()

# remove unused subplot (bottom right)
fig.delaxes(axes[1,1])

# overall dashboard title
fig.suptitle("TrendPulse Dashboard",fontsize=16)

plt.tight_layout()

# save the dashboard
plt.savefig("outputs/dashboard.png")

plt.close()

print("Dashboard saved: outputs/dashboard.png")

print("\nAll charts created successfully!")