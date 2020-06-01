#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd


# In[44]:


import os
import re

allFilePaths = []

yearList = [int(x) for x in os.listdir('../assets')]

yearList.sort()

yearList = yearList[:3]


# In[45]:



for year in yearList:
    with os.scandir('../assets/'+str(year)) as it:
        for entry in it:
            if entry.name.endswith('.csv') and entry.is_file():
                filename = entry.name
                path = '../assets/'+str(year)+'/'+filename
                print(path)
                allFilePaths.append(path)
    


# In[46]:


regions = ['EASTERN', 'WESTERN', 'SOUTHERN', 'NORTHEN', 'NORTH EAST']


# In[47]:


headers = [x for x in range(19)]


# In[48]:


ix_to_month = {
    0:"Jan",
    1:"Feb",
    2:"Mar",
    3:"Apr",
    4:"May",
    5:"Jun",
    6:"Jul",
    7:"Aug",
    8:"Sep",
    9:"Oct",
    10:"Nov",
    11:"Dec"
    
}


# In[54]:


def separate_csv(path, col):
    df = pd.read_csv(path, names = headers )
    movement = df.iloc[4:4+len(regions)]
    passengers = df.iloc[11:11+len(regions)]
    freight = df.iloc[18:18+len(regions)]

    movement = cleanup(movement, "m", col)
    passengers = cleanup(passengers, "p", col)
    freight = cleanup(freight, "f", col)
    
    return movement,passengers,freight
#     print(movement.shape)
#     print(passengers.shape)
#     print(freight.shape)


# In[55]:


def cleanup(dataframe, name, alt):
    dataframe = dataframe.loc[:,[0,1,7]]
    dataframe.set_index(0, inplace=True)
    dataframe.rename(columns={1:alt+"_I", 7:alt+"_D"})
    if name=="m":
        print(dataframe.head(2))
        
    return dataframe


# ../assets/2017/output-9oct2k17annex5.csv

# In[74]:


movement_df = pd.DataFrame(index=regions, columns = ['hi', 'bi'])
passengers_df = pd.DataFrame(index=regions, columns = ['hi', 'bi'])
freight_df = pd.DataFrame(index=regions, columns = ['hi', 'bi'])



# In[71]:



for filepath in allFilePaths:
    filename = filepath[15:]
#     print(filename)
    year = filepath[10:14]
#     print(year)
    month = ix_to_month[int(filepath[22])]
    col = month+year
#     print(col)
    movement, passengers, freight  = separate_csv(filepath, col)
    
    print(movement.shape)
#     movement_df.join(movement)
    pd.concat([movement_df,movement])
    pd.concat([passengers_df,passengers])
    pd.concat([freight_df,freight])
    


# In[72]:


print(movement_df.shape)


# In[70]:


print(movement)


# In[ ]:




