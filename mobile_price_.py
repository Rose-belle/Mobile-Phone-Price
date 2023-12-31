# -*- coding: utf-8 -*-
"""Mobile Price .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FhKUkBx6T69KZ5gGrSZpZl5WEQxxhsXi
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the dataset from the file
data = pd.read_csv('Mobile phone price.csv')
data.head()

data.columns

# Renaming the columns
data = data.rename({'Brand':'brand',
             'Model':'model',
             'Storage ':'storage',
             'RAM ':'ram',
             'Screen Size (inches)':'screen_size',
             'Camera (MP)':'camera',
             'Battery Capacity (mAh)':'battery',
             'Price ($)':'price'},axis=1)

data.head()

data.info()

# converting the barnd and model to lowercase

data['brand'] = data['brand'].str.lower()
data['model'] = data['model'].str.lower()

#Removing the 'BG from the storage and ram

data['storage'] = data['storage'].str.replace('GB','')
data['ram'] = data['ram'].str.replace('GB','')

#Creating a new feature from camera: Number of cameras

data['n_cameras'] = data['camera'].str.count('\\+') + 1
data['n_cameras'].unique()

data.head()

# Creating four new feature and removing camera

res1 = []
res2 = []
res3 = []
res4 = []
for x in data['camera']:
    resolutions = x.split('+')
    tam = len(resolutions)

    if tam == 1:
        res1.append(resolutions[0])
        res2.append('0')
        res3.append('0')
        res4.append('0')

    if tam == 2:
        res1.append(resolutions[0])
        res2.append(resolutions[1])
        res3.append('0')
        res4.append('0')

    if tam == 3:
        res1.append(resolutions[0])
        res2.append(resolutions[1])
        res3.append(resolutions[2])
        res4.append('0')

    if tam == 4:
        res1.append(resolutions[0])
        res2.append(resolutions[1])
        res3.append(resolutions[2])
        res4.append(resolutions[3])

data['res1'] = res1
data['res2'] = res2
data['res3'] = res3
data['res4'] = res4

data = data.drop(columns='camera')

data.head()

# Cleaning data

for x in data:
    print(f' Type of {x} : {data[x].dtype}\n')

data['res3'].unique()

data['res1'] = data['res1'].str.replace('MP','')
data['res2'] = data['res2'].str.replace('MP','')
data['res3'] = data['res3'].str.replace('MP','')
data['res4'] = data['res4'].str.replace('MP','')
data['price'] = data['price'].str.replace('$','')
data['price'] = data['price'].str.replace(',','.')
data.loc[88,'screen_size'] = '6.8'
data.loc[373,'screen_size'] = '7.6'
data.loc[342,'res4'] = 0
data.loc[342,'n_cameras'] = 3
data.loc[292,'res4'] = 0
data.loc[292,'n_cameras'] = 3
data.loc[312,'res4'] = 2
data.loc[312,'n_cameras'] = 4
data.loc[330,'res4'] = 0
data.loc[330,'n_cameras'] = 3
data.loc[361,'res4'] = 8
data.loc[361,'res3'] = 8
data.loc[361,'n_cameras'] = 4
data.loc[367,'res4'] = 0
data.loc[367,'n_cameras'] = 3
data.loc[376,'res4'] = 2
data.loc[376,'n_cameras'] = 4

# Casting the features to numeric type

for feature in data:
    print(f'Type of {feature}: {data[feature].dtype}')

data['storage'] = pd.to_numeric(data['storage'])

data['ram'] = pd.to_numeric(data['ram'])

data['screen_size'] = pd.to_numeric(data['screen_size'])

data['price'] = pd.to_numeric(data['price'])

data['res1'] = pd.to_numeric(data['res1'])

data['res2'] = pd.to_numeric(data['res2'])

data['res3'] = pd.to_numeric(data['res3'])

data['res4'] = pd.to_numeric(data['res4'])

for feature in data:
    print(f'Type of {feature}: {data[feature].dtype}')

data.head()

# Missing values and duplicate values

data.info()

data.isna().sum(),data.isna().mean()     #Alternatively, we can use data.isna().sum() for absolute values or data.isna().mean() for percentage values.

#49 rows of our data are duplicates, and that's 12% of all our data

absolute = data.duplicated().sum()

relative = data.duplicated().mean()*100

print(f'Duplicated:\n\ndata(#): {absolute}\n\nRelative: {round(relative,2)} %')

# Removing duplicates.

dup = data[data.duplicated()]

data_without_dup = data.drop_duplicates()

data_without_dup.reset_index()

# Here you can see all duplicate data
dup

# The difference of price distribution with duplicate data and without duplicate data

sns.histplot(data=data,x='price',label='with duplicate data', stat='density')
sns.histplot(data=data_without_dup,x='price',label='without duplicate data',stat='density')
plt.legend();

data.shape , data_without_dup.shape

407 - 358

# EDA
# I'll start with describe method
# We see that the minimum price is a mistake. A cell phone never costs 1 dollar

data_without_dup.describe().T

# Let's see the price distribution with plotly

# The data set has three cell phones priced between 0 and 19 dollars. This is an error and we will remove these rows

px.histogram(data_without_dup,x='price',nbins=100)

index = data_without_dup.query('price < 20').index
data_without_dup = data_without_dup.drop(index)
data_without_dup.shape

# The most expensive cell phone
#We can see the 10 most expensive cell phones and the most expensive cell phone is galaxy z fold2 5g from Samsung costing $1999.
#Samsung accounts for 60% of the most expensive phones in the top 10
#Huawei corresponds to 20%
#The others corresponds to 30%


data_without_dup.sort_values(by='price',ascending=False).head(10)

# The most frequent brand
#Samsung accounts for 17.75% of the entire dataset and is the most frequent brand.
#The second most frequent brand is Xiaomi which corresponds to 15.77%
#Third is Oppo with 14.37%


most_frequent = data_without_dup.groupby('brand').size().sort_values(ascending=False)

total_of_mobiles = 355

for brand,quant in most_frequent.items():
    print(f"{brand.capitalize()} has {quant} mobiles and corresponds to {round(quant/total_of_mobiles * 100,2)}% of the entire dataset\n")

#fig ,ax = plt.subplots(1,1,constrained_layout=True,figsize=(20,10))
plt.figure(figsize=(10,8))
ex = most_frequent.keys()
ey = most_frequent.values

plt.barh(y=ex,width=ey)
plt.xlabel('Count (#)',fontsize=12)
plt.ylabel('Brand',fontsize=12);


#ax[0].barh(y=ex,width=ey)
#ax[0].set_xlabel('Count (#)',fontsize=12)
#ax[0].set_ylabel('Brand',fontsize=12)

#ax[1].plot(ey,ex)
#ax[1].set_xlabel('Count (#)',fontsize=12)

#Which is the most expensive and cheapest brand?
#The most expensive brand is Asus and the cheapest is Realme
#Perhaps it would be more interesting to consider only brands with more cell phones. But we can leave that for later.

costs = data_without_dup.groupby('brand')['price'].mean().sort_values(ascending=False)

for brand,price in costs.items():
    print(f"On average {brand.capitalize()} costs ${round(price,2)}\n")

#The most expensive and cheapest cell phone for the top 10 most frequent brands

top10 = most_frequent.head(10)
print('To remember, the top10 brands are: \n')
for brand in top10.keys():
    print(brand,'\n')

#We will start with the distribution of prices for each top10 brand

top10 = data_without_dup.query(f'brand == {top10.keys().tolist()}')

sns.boxplot(data=top10,x='price',y='brand')

print('The expensive cell phones of each brand')
top10.groupby('brand')[['model','price']].max().sort_values(by='price',ascending=False)

print('The cheapest cell phones of each brand')
top10.groupby('brand')[['model','price']].min().sort_values(by='price',ascending=False)

#What are the features that have some correlation with the price?

#First strategy: Plot each feature with price.

#Second strategy: Calculate the correlation coefficient to measure a linear correlation.

#Most features have a linear correlation with price. However, we also observe linear correlation between features, for example: Storage and Ram have 0.68 correlation and so on.

#We can also calculate the VIF (variance inflation factor) to measure the degree of multicollinearity.

#Correlation of features with price:

#storage: 0.729
#res3: 0.632
#res2: 0.631
#ram: 0.630
#res4: 0.202
#res1: 0.127
#screen_size: 0.082
#n_cameras: 0.056
#battery: -0.409

for feature in data_without_dup:
    if feature in ['brand','model','price']:
        continue

    sns.regplot(y=data_without_dup['price'],x=data_without_dup[feature])
    plt.show()

correlation = data_without_dup.corr()

sns.heatmap(correlation,annot=True,fmt='.2f',linecolor='black', linewidths=2, cmap='inferno')

#More Questions and new features
#Our dataset has some brands from different continents and countries, for example:

#Apple - United States - North America

#Samsung - South Korea - Asia

#Xiaomi - China - Asia

#etc...

#Is there any difference about country or continent? If yes, what are the differences? Are price and other variables affected by country or continent?

#To answer these questions we need to add two new features: Country and Continente. So let's go!

print('The brands are: \n')
for brands in data_without_dup['brand'].unique():
    print(brands.capitalize(),'\n')

data_without_dup.reset_index(inplace=True)

data_without_dup[['country','continent']] = np.nan

for index,brand in enumerate(data_without_dup['brand']):

    if brand in ['apple','cat','google', 'motorola']:
        data_without_dup.loc[index,'country'] = 'united states'
        data_without_dup.loc[index,'continent'] = 'north america'

    elif brand in ['blackberry']:
        data_without_dup.loc[index,'country'] = 'canada'
        data_without_dup.loc[index,'continent'] = 'north america'

    elif brand in ['nokia']:
        data_without_dup.loc[index,'country'] = 'finland'
        data_without_dup.loc[index,'continent'] = 'europa'

    elif brand in ['samsung','lg']:
        data_without_dup.loc[index,'country'] = 'south korean'
        data_without_dup.loc[index,'continent'] = 'asia'

    else:
        data_without_dup.loc[index,'country'] = 'china'
        data_without_dup.loc[index,'continent'] = 'asia'

data_without_dup.head(10)

#Let's do a basic exploration on Contry and Continent features

# 1. Continent Statistics:

# 77.46% of cell phones are from Asia
# 15.77% of cell phones are from North america
# 6.76% of cell phones are from Europa
# 2. Country Statistics:

# 58.87% of cell phones are from China
# 18.59% of cell phones are from South korean
# 14.93% of cell phones are from United states
# 6.76% of cell phones are from Finland
# 0.85% of cell phones are from Canada
# Samsung is the most frequent brand, however Chinese brands together dominate our dataset.

# On average/median, North American cell phones are more expensive than Asian cell phones. And US cell phone prices are more dispersed than Asian ones.

most_frequent_country = data_without_dup.groupby('country').size().sort_values(ascending=False)
most_frequent_continent = data_without_dup.groupby('continent').size().sort_values(ascending=False)

total_of_mobiles = 355

for continent,quant in most_frequent_continent.items():
    print(f'{round(quant/total_of_mobiles*100,2)}%  ({quant}) of cell phones are from {continent.capitalize()}')

print()
for country,quant in most_frequent_country.items():
    print(f'{round(quant/total_of_mobiles*100,2)}%  ({quant}) of cell phones are from {country.capitalize()}')

plt.figure(figsize=(10,8))
sns.barplot(x=most_frequent_continent.values, y=most_frequent_continent.keys())

plt.ylabel('Continent',fontsize=12)
plt.xlabel('#',fontsize=12);

plt.figure(figsize=(10,8))
sns.barplot(x=most_frequent_country.values, y=most_frequent_country.keys())

plt.ylabel('Country',fontsize=12)
plt.xlabel('#',fontsize=12);

plt.figure(figsize=(10,7))
sns.boxplot(data=data_without_dup,x='price',y='country')

plt.figure(figsize=(10,7))
sns.boxplot(data=data_without_dup,x='price',y='continent')

statistics_price = data_without_dup.groupby('continent')['price'].agg(['mean','median','std']).sort_values(by='mean',ascending=False)

statistics_price['Coefficient_of_variation'] = statistics_price['std'] / statistics_price['mean']

statistics_price

# What are the differences between North American cell phones and Asian cell phones

# The strategy for analyzing this is to calculate the base statistic for each feature for each continent. We observed, on average, that Asian cell phones have better values ​​than North American ones.

# Let's calculate the total resolution (res1 + res2 + res3 + res4) to simplify the analysis

data_without_dup['total_resolution'] = data_without_dup['res1'] + data_without_dup['res2'] + data_without_dup['res3'] + data_without_dup['res4']
data_without_dup.head()

# Mean and standard deviation for multiple features
data_without_dup.groupby('continent')[['storage','ram','screen_size','battery','n_cameras','total_resolution']].agg(['mean','std','median'])

# Is there any difference between Asian phones?

#The strategy is the same as in the previous analysis.

# We can see that South Korean cell phones are a little more expensive than Chinese ones. The two countries have similar cell phones, however, the number of cameras and the battery are better for the South Korean.

asia = data_without_dup.query('continent == "asia"')

asia.groupby('country')[['storage','ram','screen_size','battery','n_cameras','total_resolution','price']].agg(['mean','std'])

# EDA Conclusion
# We saw that Samsung has the most expensive cell phone, and Samsung makes up (proportionally) 60% of the most expensive top 10 brands.

# Samsung is also the most frequent brand in our dataset, accounting for 17.75% of all data.

# The most expensive brand is Asus (on average 874 dollars) and Realme the cheapest (on average 208 dollars). Asus only has a four cell phones in our dataset, so it might be interesting to consider more frequent brands.

# We saw that most features have some linear correlation with price, however, some features are correlated with others and this may indicate multicollinearity. We can measure this with the Variation Inflation Error.

# Continent Statistics:
# 77.46% of cell phones are from Asia
# 15.77% of cell phones are from North America
# 6.76% of cell phones are from Europa
# Country Statistics:
# 58.87% of cell phones are from China
# 18.59% of cell phones are from South korean
# 14.93% of cell phones are from United states
# 6.76% of cell phones are from Finland
# 0.85% of cell phones are from Canada
# Samsung is the most frequent brand, however Chinese brands together dominate our dataset.

# On average/median, North American cell phones are more expensive than Asian cell phones. And US cell phone prices are more dispersed than Asian ones.

# We observed, on average, that Asian cell phones have better values than North American ones.

# We saw that South Korean cell phones are a little more expensive than Chinese ones. The two countries have similar cell phones, however, the number of cameras and the battery are better for the South Korean.