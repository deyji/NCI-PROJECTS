#!/usr/bin/env python
# coding: utf-8

# In[5]:


#Question 1a
import xml.etree.ElementTree as ET
#funtion to import xml file

def importxml(file):
    try:
        with open(file, 'r') as file:
            tree = ET.parse(file)
            root = tree.getroot()
    except:
        print('Error reading file')

#xml file was saved to jupyter notebook root folder
importxml('theoDataset.xml')


# In[6]:


#Question 1b
#Use the print function to display the ‘id’, ‘weight’ and ‘conc’ of the first, fifth, ninth, thirteenth and eighteeth records
with open('theoDataset.xml') as file:
    tree = ET.parse(file)
    root = tree.getroot()
    
#to find all the elements with the subject tag
mysubjects = root.findall('subject')

#iterating over a list of the subjects to find ID, Weight and Conc
for i in [0,4,8,12,17]: 
    print('ID : ', mysubjects[i].find('id').text)
    print('Weight : ',mysubjects[i].find('weight').text )
    print('Conc : ',mysubjects[i].find('conc').text )
    print('')


# In[12]:


#Question 1c
#Writing the entire xml script to a csv file
with open('theoDataset.xml') as file:
    tree = ET.parse(file)
    root = tree.getroot()

    #create empty lists to append the xml tags as headers
    subject = []
    main = []
    count = 0
    
    # to append the header tags as column names in the csv file
    for x in root[0]:
        subject.append(x.tag)
    main.append(subject)
    
    #reassign subject as empty list for reuse in populating table
    #get all element entries as a list and append to main list
    subject = []
    for item in root:
        subject.append(item.find('id').text)
        subject.append(item.find('weight').text) 
        subject.append(item.find('dose').text)
        subject.append(item.find('time').text)
        subject.append(item.find('conc').text)
        main.append(subject)
        subject =[]

#write the list to csv using csv.writer function in python
import csv
with open('course.csv', 'w') as f:
    for rows in main:
        myfile = csv.writer(f)
        myfile.writerow(rows)


# In[8]:


#Question 2
#Question 2a
import numpy as np
#numpy array filled with 1000 numbers
array1 = np.arange(1000).reshape(250,4)

#Question 2b
#split array1 into 5 arrays of size 50 by 4
array2 = array1[0:50]
array3 = array1[50:100]
array4 = array1[100:150]
array5 = array1[150:200]
array6 = array1[200:250]

#Question 2c
#reshape into different dimensions of (100 by 2), (200 by 1) and (20 by 10) respectively
array7 = array2.reshape(100,2)
array8 = array3.reshape(200,1)
array9 = array4.reshape(20,10)

#Question 2d
#split two of these arrays horizontally
array10 = np.split(array8, 2, axis = 0)
array11 = np.split(array9, 2, axis = 0)


# In[9]:


import re
#Question 3
txt = '''All I want is a proper cup of coffee
Made in a proper copper coffee pot
I may be off my dot
But I want a cup of coffee
From a proper coffee pot
Tin coffee pots and iron coffee pots
They’re no use to me
If I can’t have a proper cup of coffee
In a proper copper coffee pot
I’ll have a cup of tea.'''

#Function written to print the string matched to a pattern using rstrip. \g is a method in re too quote a match
def match(pattern, string):
    print(re.compile(pattern, re.M).sub("{\g<0>}",string.rstrip()))

#matches (coffee, pot and pots) at the end of the lines
#Question 3a
match('(coffee|pot|pots)$', txt)
print('\n')

#matches (coffee, pot and pots) at the end of the lines and proper anywhere within the lines
#Question 3b
match('((coffee|pot|pots)$)|(proper)', txt)


# In[ ]:




