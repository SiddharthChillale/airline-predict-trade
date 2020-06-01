#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import tabula
import pandas as pd
import os
import itertools


# In[ ]:


import logging
logging.basicConfig(level=logging.INFO,
                    filename='../logs/test.log',
                    format="%(levelname)s:%(message)s")
import warnings
warnings.filterwarnings("ignore")


# In[ ]:




url_head = "https://www.aai.aero/sites/default/files/traffic-news/"

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


cent = '2k'


years = [16, 17, 18, 19, 20]

annexes = ['annex5']

C_annexes = ['Annex5']

           
error_filenames_cor = [
       'Mar2k15annex5_',  'apr2k16annex5R', 'Mar2k17annex5R', 'OCT2k17annex5', 'Dec2k18Annex5', 'Feb2k19Annex5_0', 'Mar2K19Annex5', 'June2k19Annex5', 'Dec2k19Annex5_0', 'Jan2k20Annex5_0'
   ]

error_filenames = [
       'Mar2k16annex5',  'Apr2k16annex5', 'Mar2k17annex5', 'Oct2k17annex5', 'Dec2k18annex5', 'Feb2k19Annex5', 'Mar2k19Annex5', 'Jun2k19Annex5', 'Dec2k19Annex5', 'Jan2k20Annex5'
   ]
files = []
outputfiles=[]

# In[ ]:


allFiles = {}


# In[ ]:


for year in years:
    for ind,month in enumerate(months):
        for annex in annexes:
            url = url_head + month + cent + str(year) + annex + ".pdf"
            
            filename = month + cent + str(year) + annex
            allFiles[filename.lower()] = filename


# In[ ]:



for year in years[3:]:
    for ind,month in enumerate(months):
        for annex in C_annexes:
            url = url_head + month + cent + str(year) + annex + ".pdf"
            
            filename = month + cent + str(year) + annex
            allFiles[filename.lower()] = filename
    


# In[ ]:


unwanted_months = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
allFiles = dict(itertools.islice(allFiles.items(), len(years)*len(months)-len(unwanted_months)))
len(allFiles)


# In[ ]:


for x,y in zip(error_filenames,error_filenames_cor):
    allFiles[x.lower()] = y
    


# In[ ]:


# allFiles


# In[ ]:


os.mkdir("../assets")
os.chdir("../assets")
for year in years:
    os.mkdir(f'{str(20) + str(year)}')
    os.chdir(f'{str(20) + str(year)}')
    for ind,month in enumerate(months):
        ind = str(ind).zfill(2)
        for annex in annexes:
            
            filename = (month + cent + str(year) + annex).lower()
            
            url = url_head + allFiles[filename] + ".pdf"
            
            
            
            try:
                response = requests.get(url, verify=False)
            except:
                logging.error(":Not available online. Try manually: "+filename)

            with open(ind+filename+".pdf", 'wb') as f:
                print("saving")
                try:
                    f.write(response.content)
                    logging.info("Written to PDF:"+filename)
                    files.append(filename)
                except:
                    logging.critical("Failed to write to " + filename)
            
            try:
                out = "output-"+ind+filename+".csv"
                tabula.convert_into(ind+str(filename+".pdf"), out, output_format="csv", pages='all')
                outputfiles.append(out)
            except:
                logging.critical("Failed to save output to " + filename)
                error_filenames.append(filename)

            
            # try:
            #     os.remove(filename+".pdf")
            # except:
            #     logging.error("Could not delete " + filename + ".pdf")

        
    os.chdir("../")
                


# In[ ]:




