# Import librairies
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import missingno as msno 
from collections import Counter 

!pip install missingno

#Loading Dataset
df = pd.read_csv("Dune Sales Data.csv")

# print the first rows
df.head(10) 

#Print the bottom 10 row
df.tail(10)

#Dimensionality of the data-the number of rows and colunms
df.shape

(34867, 12)
#Examine the columns /features
df.columns

# Investigate the dataset for anomalies and data types
df.info()

# Numerical statistical analysis
df.describe()

# Categorical statistical analysis
df.describe(include=["object", "bool"])

# Categorical statistical analysis
df.describe(include=["object", "bool"])

# Investigating the missing data
null_vals = df.isnull().sum()
null_vals

# visualizing missing data
plt.figure(figsize = (8,5))
sns.heatmap(df.isnull(), cbar=True, cmap="magma");

msno.bar(df, color="blue");

#Displaying mssing data in the dataset
df[df.isnull().any(axis=1)]

# Convert the date colunm into a pandas date time object
df["Date"] = pd.to_datetime(df["Date"])

df.head()

# Extract the year and the month, quater (feature engineering)
df['year'] = df["Date"].dt.year
df['month'] = df["Date"].dt.month
df['month_name'] = df["Date"].dt.month_name()
df['quarter'] = df["Date"].dt.quarter 

df.head(2)

# Categorize or group Customer age into age bracket
def age_group(x):
    if x <= 25:
        return "<=  25 Young Adult"
    elif x <= 40:
        return "20-40 Adult"
    elif x < 50:
        return "41-50 old Adult"
    else:
        return ">=51 Elder"
#Apply function to the date
df["age_group"] = df["Customer_Age"].apply(age_group)
df.head(3)

# Calculate cost, revenue
df["Cost"] = df["Quantity"] * df["Unit_Cost"]
df["Revenue"] = df["Quantity"] * df["Unit_Price"]
df["Profit"] = df["Revenue"] - df["Cost"]
df.head(2)

#Profit/loss grouping
def profitol(x):
    if x >= 0:
        return "Profit"
    else:
        return "Loss"
df["Profit_label"] = df["Profit"].apply(profitol)
df.head(3)

# Univeriate analysis
# How many customers belong to each customer spec
sns.countplot(x="Customer", data=df);

# Investigate the columns affected with different types of spellings
df[df["Customer"] == "Hign"].head(3)

#correct the spelling Hign
df.loc[df["Customer"] == "Hign", "Customer"] = "High"
sns.countplot(x="Customer", data=df);

df["Customer"].value_counts()

# sales Persons, How many transactions by sales person
ax = sns.countplot(x =df["Sales Person"], order=df["Sales Person"].value_counts(ascending=False).index)
ax
values= df["Sales Person"].value_counts(ascending=False).values 
ax.bar_label(container=ax.containers[0], labels=values);

Compared to other sales person, Remota has the highest number of tansaction while Kenny has the lowest number of transactions.

# Cont the number of male and female customers 
df["Customer_Gender"].value_counts()

# count of product in each category
df["Product_Category"].value_counts()

#Total transaction by customer age group
ay = sns.countplot(x =df["age_group"], order=df["age_group"].value_counts(ascending=False).index)
ay
values= df["age_group"].value_counts(ascending=False).values 
ax.bar_label(container=ax.containers[0], labels=values);

##Total Transaction by customer gender

fig,ax = plt.subplots(figsize=(5,5))
count = Counter(df["Customer_Gender"])
ax.pie(count.values(), labels=count.keys(), autopct=lambda p:f'{p:.2f}%')
ax.set_title("Percentage of transaction by Gender")
plt.show();

#Data looks messy, visualize just top 10
plt.figure(figsize=(20,5))
topten = df["State"].value_counts().head(10)
sns.countplot(x="State", data=df, order=topten.index);
print(topten)

#Total Transaction by Profit or loss
fig,ax = plt.subplots(figsize=(5,5))
count = Counter(df["Profit_label"])
ax.pie(count.values(), labels=count.keys(), autopct=lambda p:f'{p:.2f}%')
ax.set_title("Percentage of transaction by Profit or Loss")
plt.show();

#86.08% of the transaction resulted in a profit

#Numerical data Visualization
#Qauntity,cost and revenue-subplot
fig,axs = plt.subplots(nrows=2,ncols=2, figsize=(15,10))

sns.boxplot(x="Quantity", data=df,ax=axs[0,0])
axs[0,0].set_title("Boxplot on Qauntity sold")

sns.boxplot(x="Cost", data=df,ax=axs[0,1])
axs[0,1].set_title("Boxplot on cost")

sns.boxplot(x="Revenue", data=df,ax=axs[1,0])
axs[1,0].set_title("Boxplot on revenue")

sns.histplot(x="Profit", data=df,ax=axs[1,1])
axs[1,1].set_title("Histogram on profit");

##The distribution of Quantity sold shows low variability, indicating that most customers purchase one to two items per transaction. Cost and Revenue distributions are right-skewed with several high-value outliers, suggesting the presence of premium products. The Profit distribution is centered around zero with a higher concentration of profitable transactions, confirming overall business profitability.
