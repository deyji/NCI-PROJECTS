#!/usr/bin/env python
# coding: utf-8

# In[106]:


#Parse API content
import urllib, json, pymongo

url = "https://chronicdata.cdc.gov/api/views/wsas-xwh5/rows.json?accessType=DOWNLOAD"

try:
    with urllib.request.urlopen(url) as response:
        html = response.read()
except:
    print("Error opening URL")


# In[107]:


#Parse api content as a json object
#filtering the json file before uploading to mongodb
#MongoDB has a file size limit of 16MB
data = json.loads(html)
for i in data['data']:
    del i[0:8]
    #del i[23:28]
    
new_data = []
data2 = {}

for i in data['data']:
    if i[0] in ['2016']: 
        new_data.append(i)

data2.update({'data': new_data})


# In[108]:


# Transform python object back into json
#Insert into MongoDB
#output_json = json.dumps(output_dict)

#Connection to mongodb
from pymongo import MongoClient
try:
    client = MongoClient('localhost', 27017)
except:
    print("Error connecting to MongoDB")
Project = client['DIA_PRO_DB']
col_name = 'TOBACCO_USE'
myCollection = Project[col_name]
myCollection.insert_one(data2)


# In[109]:


#Retrieve data from MongoDB Collection
a = myCollection.find_one()


# In[110]:


#Convert json object to csv object
import csv

with open('csv_file', 'w+') as file:
    for i in a['data']:
        write = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    write.writerow(a['data'])


# In[111]:


#load csv object to a dataframe for manipulation
import pandas as pd
y = a['data']
file = pd.DataFrame.from_records(y)


# In[112]:


#Name columns of the dataframe
file.columns = ['YEAR','LocationAbbr','LocationDesc','TopicType','TopicDesc','MeasureDesc','DataSource','Response','Data_Value_Unit','Data_Value_Type','Data_Value','Data_Value_Footnote_Symbol','Data_Value_Footnote','Data_Value_Std_Err','Low_Confidence_Limit','High_Confidence_Limit','Sample_Size','Gender','Race','Age','Education','GeoLocation','TopicTypeId','TopicId','MeasureId','StratificationID1','StratificationID2','StratificationID3','StratificationID4','SubMeasureID','DisplayOrder','a','b']


# In[113]:


#Drop unneeded columns
file_Current_Smoking = file[['YEAR', 'LocationAbbr','LocationDesc', 'TopicDesc','MeasureDesc','Gender','Race','Age', 'Data_Value']]
file_Current_Smoking = file_Current_Smoking.reset_index(drop = True)


# In[114]:


#Filter dataframe to get required data for table 1
file_Current_Smoking = file_Current_Smoking[file_Current_Smoking['TopicDesc'] == 'Cigarette Use (Adults)']
file_Current_Smoking = file_Current_Smoking[file_Current_Smoking['MeasureDesc'] == 'Current Smoking']
file_Current_Smoking = file_Current_Smoking[file_Current_Smoking['Gender'] == 'Overall']
file_Current_Smoking = file_Current_Smoking[file_Current_Smoking['Race'] == 'All Races']
file_Current_Smoking = file_Current_Smoking[file_Current_Smoking['Age'] == 'All Ages']


# In[115]:


#Filter dataframe to get required data for table 2
file_Smoking_Status = file[['YEAR', 'LocationAbbr','LocationDesc','MeasureDesc', 'Response', 'TopicDesc','Gender','Race','Age', 'Data_Value']]
file_Smoking_Status = file_Smoking_Status[file_Smoking_Status['MeasureDesc'] == 'Smoking Status']
file_Smoking_Status = file_Smoking_Status[file_Smoking_Status['TopicDesc'] == 'Cigarette Use (Adults)']
file_Smoking_Status = file_Smoking_Status[file_Smoking_Status['Gender'] == 'Overall']
file_Smoking_Status = file_Smoking_Status[file_Smoking_Status['Race'] == 'All Races']
file_Smoking_Status = file_Smoking_Status[file_Smoking_Status['Age'] == 'All Ages']
file_Smoking_Status = file_Smoking_Status.drop(columns = ['TopicDesc','Gender','Race','Age'])
file_Smoking_Status['Response1'] = 0
file_Smoking_Status['Response2'] = 0
file_Smoking_Status['Response3'] = 0
countries = ['KY', 'GA', 'AK', 'AK', 'AR', 'AR', 'DE', 'DC', 'IA', 'CO', 'GA', 'IN', 'KY', 'GA', 'DE', 'AR', 'ID', 'AZ', 'CT', 'CA', 'AZ', 'GU', 'CO', 'AK', 'GU', 'CT', 'IL', 'FL', 'IA', 'KS', 'IL', 'KY', 'HI', 'LA', 'ID', 'AL', 'IA', 'AL', 'DC', 'CA', 'HI', 'CA', 'KS', 'HI', 'IN', 'FL', 'DE', 'FL', 'AL', 'IL', 'LA', 'ID', 'CO', 'KS', 'IN', 'LA', 'AZ', 'DC', 'CT', 'GU', 'NY', 'MI', 'VT', 'MS', 'RI', 'NY', 'TX', 'MN', 'NE', 'PA', 'PR', 'NH', 'NE', 'OH', 'WV', 'US', 'SC', 'MS', 'ME', 'WI', 'MD', 'NJ', 'MN', 'WI', 'MO', 'NM', 'OH', 'TN', 'MI', 'NJ', 'UT', 'WA', 'SD', 'MS', 'SC', 'OK', 'OR', 'OH', 'PR', 'WA', 'MA', 'MT', 'NC', 'NM', 'ND', 'VA', 'NY', 'WY', 'NH', 'NH', 'WA', 'UT', 'MD', 'MA', 'VT', 'MT', 'NV', 'NJ', 'MN', 'MD', 'RI', 'VA', 'ME', 'MO', 'WV', 'TX', 'MO', 'MI', 'TN', 'PR', 'US', 'OK', 'ME', 'RI', 'OR', 'NV', 'ND', 'WY', 'SD', 'WY', 'WV', 'NC', 'PA', 'MT', 'PA', 'NC', 'MA', 'TX', 'OR', 'SC', 'US', 'NV', 'OK', 'NM', 'ND', 'VT', 'TN', 'SD', 'WI', 'VA', 'NE', 'UT']
for i in countries:
    for j in range(file_Smoking_Status.shape[0]):
        if (file_Smoking_Status.iloc[j,1] == i):
            if(file_Smoking_Status.iloc[j,4] == 'Current'):
                file_Smoking_Status.iloc[j,6] = file_Smoking_Status.iloc[j,5]
            elif(file_Smoking_Status.iloc[j,4] == 'Never'):
                file_Smoking_Status.iloc[j,7] = file_Smoking_Status.iloc[j,5]
            elif(file_Smoking_Status.iloc[j,4] == 'Former'):
                file_Smoking_Status.iloc[j,8] = file_Smoking_Status.iloc[j,5]


# In[124]:


New_Smoking_Status = file_Smoking_Status.drop(columns = ['Data_Value','Response', 'Response1', 'Response2', 'Response3'], inplace = False)
New_Smoking_Status = New_Smoking_Status.drop_duplicates(inplace = False)
New_Smoking_Status['Response1'] = 0
New_Smoking_Status['Response2'] = 0
New_Smoking_Status['Response3'] = 0


# In[154]:


#aggregate data to collapse data in the response columns into a new dataframe New_Smoking_status
for i in countries:
    a = 0.0
    b = 0.0
    c = 0.0
    for j in range(file_Smoking_Status.shape[0]):
        if (file_Smoking_Status.iloc[j,1] == i):
            if(file_Smoking_Status.iloc[j,4] == 'Current'):
                a += float(file_Smoking_Status.iloc[j,6])
            elif(file_Smoking_Status.iloc[j,4] == 'Never'):
                b+=float(file_Smoking_Status.iloc[j,7])
            elif(file_Smoking_Status.iloc[j,4] == 'Former'):
                c+=float(file_Smoking_Status.iloc[j,8])
        for x in range(New_Smoking_Status.shape[0]):
            if (New_Smoking_Status.iloc[x,1] == i):
                New_Smoking_Status.iloc[x,4] = a
                New_Smoking_Status.iloc[x,5] = b
                New_Smoking_Status.iloc[x,6] = c


# In[155]:


#file_Smoking_Status
New_Smoking_Status.columns = ['YEAR', 'LocationAbbr', 'LocationDesc', 'MeasureDesc', 'Response_Current', 'Response_Never', 'Response_Former']


# In[157]:


#Connect to postgres
import psycopg2

try:
    dbConnection = psycopg2.connect(
        user = "dap",
        password = "dap",
        host = "192.168.56.30",
        port = "5432",
        dbname = "dia_project")
    dbConnection.set_isolation_level(0) #AUTOCOMMIT
    dbCursor = dbConnection.cursor()
except:
    print('Error')


# In[160]:


#Create tables in postgres
try:
    dbCursor.execute("""
            
    CREATE TABLE IF NOT EXISTS Tobacco_Current_Smoking(

            YEAR VARCHAR,
            LocationAbbr VARCHAR PRIMARY KEY,
            LocationDesc VARCHAR,
            TopicDesc VARCHAR,
            MeasureDesc VARCHAR,
            Gender VARCHAR,
            Race VARCHAR,
            Age VARCHAR,
            Data_Value numeric
            );
            
            CREATE TABLE IF NOT EXISTS Tobacco_Smoking_Status(

            YEAR VARCHAR,
            LocationAbbr VARCHAR,
            LocationDesc VARCHAR,
            MeasureDesc VARCHAR,
            Response_Current numeric,
            Response_Never numeric,
            Response_Former numeric,
            CONSTRAINT PKSStatus PRIMARY KEY (LocationAbbr)
            );
    """)
except (Exception, psycopg2.Error) as dbError:
    print("Error while connecting to PostgreSQL", dbError)


# In[161]:


#Import dataframes from python to postgres
from sqlalchemy import create_engine
import io

engine = create_engine('postgresql+psycopg2://dap:dap@192.168.56.30:5432/dia_project')
conn = engine.raw_connection()
cur = conn.cursor()
output = io.StringIO()
New_Smoking_Status.to_csv(output, sep = '\t', header = False, index = False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'Tobacco_Smoking_Status', null = "")
conn.commit()
conn.close()

engine = create_engine('postgresql+psycopg2://dap:dap@192.168.56.30:5432/dia_project')
conn = engine.raw_connection()
cur = conn.cursor()
output = io.StringIO()
file_Current_Smoking.to_csv(output, sep = '\t', header = False, index = False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'Tobacco_Current_Smoking', null = "")
conn.commit()
conn.close()


# In[162]:


#file_Current_Smoking.shape


# In[163]:


#Close connection
dbCursor.close()


# In[ ]:





# In[164]:


#Parse API content
import urllib, json, pymongo

url = "https://chronicdata.cdc.gov/views/hn4x-zwk7/rows.json?accessType=DOWNLOAD"

try:
    with urllib.request.urlopen(url) as response:
        html = response.read()
except:
    print("Error opening URL")


# In[165]:


#Filter api content and parse as python json object
data = json.loads(html)
for i in data['data']:
    del i[0:8]
    
new_data = []
data2 = {}

for i in data['data']:
    if i[0] in ['2016']: 
        if i[5] in ['Obesity / Weight Status']:
            if i[7] in ['Percent of adults aged 18 years and older who have obesity']:
                if i[29] in ['Total']:
                    new_data.append(i)

data2.update({'data': new_data})


# In[166]:


#Connect and Export to MongoDB
from pymongo import MongoClient
try:
    client = MongoClient('localhost', 27017)
except:
    print("Error connecting to MongoDB")
Project = client['DIA_PRO_DB']
col_name = 'OBESITY'
myCollection = Project[col_name]
myCollection.insert_one(data2)


# In[167]:


#Retrieve data from mongodb
a = myCollection.find_one()


# In[168]:


#Export data to a csv
import csv

with open('csv_file', 'w+') as file:
    for i in a['data']:
        write = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    write.writerow(a['data'])
    
#Convert csv to a pandas dataframe
import pandas as pd
y = a['data']
file = pd.DataFrame.from_records(y)


# In[170]:


#Rename columns
file.columns = ['Year','YearEnd','LocationAbbr','LocationDesc','Datasource','Class','Topic','Question','Data_Value_Unit','Data_Value_Type','Data_Value','Data_Value_Alt','Data_Value_Footnote_Symbol','Data_Value_Footnote','Low_Confidence_Limit','High_Confidence_Limit ','Sample_Size','Total','Age_years','Education','Gender','Income','Race_Ethnicity','GeoLocation','ClassID','TopicID','QuestionID','DataValueTypeID','LocationID','StratificationCategory1','Stratification1','StratificationCategoryId1','StratificationID1','a','b']


# In[172]:


#Drop unwanted columns
file_obesity = file[['Year', 'LocationAbbr', 'Topic', 'Question', 'Data_Value']]
for i in range(file_obesity.shape[0]):
    file_obesity.iloc[i,4] = float(file_obesity.iloc[i,4])


# In[173]:


#Connect to postgres
import psycopg2

try:
    dbConnection = psycopg2.connect(
        user = "dap",
        password = "dap",
        host = "192.168.56.30",
        port = "5432",
        dbname = "dia_project")
    dbConnection.set_isolation_level(0) #AUTOCOMMIT
    dbCursor = dbConnection.cursor()
except:
    print('Error')


# In[177]:


#Create tables in postgres
try:
    dbCursor.execute("""
    CREATE TABLE IF NOT EXISTS Obesity(
            Year VARCHAR,
            LocationAbbr VARCHAR,
            Topic VARCHAR,
            Question VARCHAR,
            Data_Value numeric,
            CONSTRAINT PKObesity PRIMARY KEY (LocationAbbr)
            );
            
    """)
except (Exception, psycopg2.Error) as dbError:
    print("Error while connecting to PostgreSQL", dbError)


# In[178]:


#Import dataframes to postgres
from sqlalchemy import create_engine
import io

engine = create_engine('postgresql+psycopg2://dap:dap@192.168.56.30:5432/dia_project')
conn = engine.raw_connection()
cur = conn.cursor()
output = io.StringIO()
file_obesity.to_csv(output, sep = '\t', header = False, index = False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'OBESITY', null = "")
conn.commit()
conn.close()


# In[179]:


#Close connection
dbCursor.close()


# In[ ]:





# In[180]:


#Parse API content
import urllib, json, pymongo

url = "https://chronicdata.cdc.gov/views/mfvi-hkb9/rows.json?accessType=DOWNLOAD"

try:
    with urllib.request.urlopen(url) as response:
        html = response.read()
except:
    print("Error opening URL")


# In[181]:


#Parse API to json file
data = json.loads(html)
for i in data['data']:
    del i[0:8]
    
new_data = []
data2 = {}

for i in data['data']:
    if i[0] in ['2016']: 
        if i[3] in ['State']:
            if i[13] in ['Overall']:
                if i[15] in ['Overall']:
                    new_data.append(i)

data2.update({'data': new_data})


# In[182]:


#Connect to MongoDB
from pymongo import MongoClient
try:
    client = MongoClient('localhost', 27017)
except:
    print("Error connecting to MongoDB")
Project = client['DIA_PRO_DB']
col_name = 'HEART_DISEASE'
myCollection = Project[col_name]
myCollection.insert_one(data2)


# In[183]:


#Retrieve Data from MongoDB and convert to Dataframe
a = myCollection.find_one()
import csv

with open('csv_file', 'w+') as file:
    for i in a['data']:
        write = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    write.writerow(a['data'])
    
import pandas as pd
y = a['data']
file = pd.DataFrame.from_records(y)


# In[184]:


#rename columns
file.columns = ['Year','LocationAbbr','LocationDesc','GeographicLevel','DataSource','Class','Topic','Data_Value','Data_Value_Unit','Data_Value_Type','Data_Value_Footnote_Symbol','Data_Value_Footnote','StratificationCategory1','Stratification1','StratificationCategory2','Stratification2','TopicID','LocationID','Y_lat','X_lon','Georeference_Column','States','Counties']


# In[185]:


#Filter unwanted columns from dataframe 
file_Heart_Disease = file[['Year', 'GeographicLevel', 'Stratification1', 'Stratification2', 'LocationAbbr', 'LocationDesc', 'Data_Value']]


# In[196]:


#Connect to Postgres
import psycopg2

try:
    dbConnection = psycopg2.connect(
        user = "dap",
        password = "dap",
        host = "192.168.56.30",
        port = "5432",
        dbname = "dia_project")
    dbConnection.set_isolation_level(0) #AUTOCOMMIT
    dbCursor = dbConnection.cursor()
except:
    print('Error')


# In[197]:


#Connect ot Postgres
try:
    dbCursor.execute("""
    CREATE TABLE IF NOT EXISTS heart_disease(
        Year VARCHAR,
        GeographicLevel VARCHAR,
        Stratification1 VARCHAR,
        Stratification2 VARCHAR,
        LocationAbbr VARCHAR,
        LocationDesc VARCHAR,
        Data_Value numeric,
        CONSTRAINT PKHDisease PRIMARY KEY (LocationAbbr)
        );
    """)
except (Exception, psycopg2.Error) as dbError:
    print("Error while connecting to PostgreSQL", dbError)


# In[199]:


#Export to postgres table
from sqlalchemy import create_engine
import io

engine = create_engine('postgresql+psycopg2://dap:dap@192.168.56.30:5432/dia_project')
conn = engine.raw_connection()
cur = conn.cursor()
output = io.StringIO()
file_Heart_Disease.to_csv(output, sep = '\t', header = False, index = False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'heart_disease', null = "")
conn.commit()
conn.close()


# In[200]:


#Close connection
dbCursor.close()


# In[ ]:





# In[201]:


#Parse API Content
import urllib, json, pymongo

url = "https://chronicdata.cdc.gov/views/v246-z5tb/rows.json?accessType=DOWNLOAD"

try:
    with urllib.request.urlopen(url) as response:
        html = response.read()
except:
    print("Error opening URL")


# In[202]:


#Load into json format
data = json.loads(html)
for i in data['data']:
    del i[0:8]
    
new_data = []
data2 = {}

for i in data['data']:
    if i[0] in ['2016']: 
        if i[3] in ['State']:
            if i[13] in ['Overall']:
                if i[15] in ['Overall']:
                    new_data.append(i)

data2.update({'data': new_data})


# In[203]:


#Connect and Export to mongodb 
from pymongo import MongoClient
try:
    client = MongoClient('localhost', 27017)
except:
    print("Error connecting to MongoDB")
Project = client['DIA_PRO_DB']
col_name = 'STROKE_MORTALITY'
myCollection = Project[col_name]
myCollection.insert_one(data2)


# In[204]:


#Retrieve data from mongodb and convert to csv
a = myCollection.find_one()
import csv

with open('csv_file', 'w+') as file:
    for i in a['data']:
        write = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    write.writerow(a['data'])
    
import pandas as pd
y = a['data']
file = pd.DataFrame.from_records(y)


# In[205]:


#Rename columns and filter table for unwanted columns
file.columns = ['Year','LocationAbbr','LocationDesc','GeographicLevel','DataSource','Class','Topic','Data_Value','Data_Value_Unit','Data_Value_Type','Data_Value_Footnote_Symbol','Data_Value_Footnote','StratificationCategory1','Stratification1','StratificationCategory2','Stratification2','TopicID','LocationID','Y_lat','X_lon','Georeference_Column','States','Counties']
file_Stroke_Mortality = file[['Year', 'GeographicLevel', 'Stratification1', 'Stratification2', 'LocationAbbr', 'LocationDesc', 'Data_Value']]


# In[207]:


#Connect to postgres
import psycopg2

dbConnection = psycopg2.connect(
        user = "dap",
        password = "dap",
        host = "192.168.56.30",
        port = "5432",
        dbname = "dia_project")
dbConnection.set_isolation_level(0) #AUTOCOMMIT
dbCursor = dbConnection.cursor()


# In[208]:


#Create tables in postgres
try:
    dbCursor.execute("""
    CREATE TABLE IF NOT EXISTS stroke_mortality(
        Year VARCHAR,
        GeographicLevel VARCHAR,
        Stratification1 VARCHAR,
        Stratification2 VARCHAR,
        LocationAbbr VARCHAR,
        LocationDesc VARCHAR,
        Data_Value numeric,
        CONSTRAINT PKSMortality PRIMARY KEY (LocationAbbr)
            );
    """)
except (Exception, psycopg2.Error) as dbError:
    print("Error while connecting to PostgreSQL", dbError)


# In[209]:


#Export dataframe to postgres
from sqlalchemy import create_engine
import io

engine = create_engine('postgresql+psycopg2://dap:dap@192.168.56.30:5432/dia_project')
conn = engine.raw_connection()
cur = conn.cursor()
output = io.StringIO()
file_Stroke_Mortality.to_csv(output, sep = '\t', header = False, index = False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'stroke_mortality', null = "")
conn.commit()
conn.close()


# In[210]:


#Close connection
dbCursor.close()


# In[ ]:





# In[5]:


#Connect to postgres
import psycopg2

dbConnection = psycopg2.connect(
        user = "dap",
        password = "dap",
        host = "192.168.56.30",
        port = "5432",
        dbname = "dia_project")
dbConnection.set_isolation_level(0) #AUTOCOMMIT
dbCursor = dbConnection.cursor()


# In[6]:


#Create a table from all tables pushed into postgres using join statements
import pandas as pd
import pandas.io.sql as sqlio

sql = """
SELECT obesity.locationabbr, obesity.data_value, tobacco_current_smoking.data_value, stroke_mortality.data_value, heart_disease.data_value
FROM obesity 
INNER JOIN tobacco_current_smoking ON obesity.locationabbr = tobacco_current_smoking.locationabbr
INNER JOIN stroke_mortality ON obesity.locationabbr = stroke_mortality.locationabbr
INNER JOIN heart_disease ON obesity.locationabbr = heart_disease.locationabbr;
"""
ObesityTobaccoDF = sqlio.read_sql_query(sql, dbConnection)


# In[7]:


#Rename columns
ObesityTobaccoDF.columns = ['Location', 'Obesity_Value', 'Tobacco_Value', 'Stroke_Mortality', 'HeartDisease_Mortality']


# In[214]:


#Create table for join table in postgres
try:
    dbCursor.execute("""
    CREATE TABLE IF NOT EXISTS COMBINED_DF(
        Location VARCHAR PRIMARY KEY,
        Obesity_Value numeric,
        Tobacco_Value numeric,
        Stroke_Mortality numeric,
        HeartDisease_Mortality numeric
            );
    """)
except (Exception, psycopg2.Error) as dbError:
    print("Error while connecting to PostgreSQL", dbError)

#Push join table to postgres
from sqlalchemy import create_engine
import io

engine = create_engine('postgresql+psycopg2://dap:dap@192.168.56.30:5432/dia_project')
conn = engine.raw_connection()
cur = conn.cursor()
output = io.StringIO()
ObesityTobaccoDF.to_csv(output, sep = '\t', header = False, index = False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'combined_df', null = "")
conn.commit()
conn.close()


# In[215]:


#Close connection
dbCursor.close()


# In[ ]:





# In[8]:


#load necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


# In[9]:


#Calculate correlation between attributes
ObeCorr = (ObesityTobaccoDF.drop(columns = 'Location')).corr(method='pearson')


# In[10]:


#Show correlation
ObeCorr


# In[11]:


#Plot heatmap for correlation
sb.heatmap(ObeCorr, 
xticklabels=ObeCorr.columns,
yticklabels=ObeCorr.columns,
cmap='RdBu_r',
annot=True,
square = True,
linewidth=1.0)


# In[17]:


#Sort data in descending order and create dataframe for first and last five
y = ObesityTobaccoDF.sort_values(['Tobacco_Value'], ascending = False)
y2 = y.iloc[[0,1,2,3,4,-1,-2,-3,-4],:]
z = ObesityTobaccoDF.sort_values(['Obesity_Value'], ascending = False)
z2 = z.iloc[[0,1,2,3,4,-1,-2,-3,-4],:]
a = ObesityTobaccoDF.sort_values(['HeartDisease_Mortality'], ascending = False)
a2 = a.iloc[[0,1,2,3,4,-1,-2,-3,-4],:]
b = ObesityTobaccoDF.sort_values(['Stroke_Mortality'], ascending = False)
b2 = b.iloc[[0,1,2,3,4,-1,-2,-3,-4],:]
y2


# In[20]:


import matplotlib.pylab as plt 
plt.xticks(rotation = 45)
sb.set(rc={'figure.figsize':(14,8.50)})
clrs = ['blue' if (x < y2.iloc[4,2]) else 'red' for x in y2['Tobacco_Value'] ]
sb.barplot(x = "Location", y = "Tobacco_Value", data = y2, palette=clrs);


# In[26]:


plt.xticks(rotation = 45)
sb.set(rc={'figure.figsize':(14,8.50)})
clrs = ['blue' if (x < z2.iloc[4,1]) else 'red' for x in z2['Obesity_Value'] ]
sb.barplot(x = "Location", y = "Obesity_Value", data = z2, palette = clrs);


# In[27]:


plt.xticks(rotation = 45)
sb.set(rc={'figure.figsize':(14,8.50)})
clrs = ['blue' if (x < b2.iloc[4,3]) else 'red' for x in b2['Stroke_Mortality'] ]
sb.barplot(x = "Location", y = "Stroke_Mortality", data = b2, palette = clrs);


# In[29]:


plt.xticks(rotation = 45)
sb.set(rc={'figure.figsize':(14,8.50)})
clrs = ['blue' if (x < a2.iloc[4,4]) else 'red' for x in a2['HeartDisease_Mortality'] ]
sb.barplot(x = "Location", y = "HeartDisease_Mortality", data = a2, palette = clrs);


# In[12]:


from sklearn.preprocessing import normalize


# In[13]:


df1 = pd.melt(ObesityTobaccoDF, id_vars=['Location']).sort_values(['variable','value'])
for i in range(df1.shape[0]):
    df1.iloc[i,2] = (df1.iloc[i,2] - min(df1['value']))/(max(df1['value']) - min(df1['value']))


# In[14]:


plt.xticks(rotation = 45)
sb.set(rc={'figure.figsize':(35,13)})
sb.barplot(x='Location', y='value', hue='variable', data=df1)
plt.xticks(rotation=45)
plt.ylabel('Values')
plt.title('Plots Per State');


# In[37]:


from pandas import DataFrame
from sklearn import linear_model
import statsmodels.api as sm

X = ObesityTobaccoDF[['Obesity_Value', 'Tobacco_Value']]
Y = ObesityTobaccoDF[['Stroke_Mortality']]
Z = ObesityTobaccoDF[['HeartDisease_Mortality']]
 
#Create a model to identify the coefficients of each variable in a predictive model 
model = sm.OLS(Y, X).fit()

# Print out the statistics
model.summary()


# In[38]:


regr = linear_model.LinearRegression()
model = sm.OLS(Z, X).fit()
#predictions = model.predict(X) # make the predictions by the model

# Print out the statistics
model.summary()


# In[15]:


from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# In[16]:


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state= 0)
A_train, A_test, B_train, B_test = train_test_split(A, B, test_size=0.2, random_state= 0)


# In[17]:


model1 = regr.fit(X_train, Y_train)
model2 = regr.fit(A_train, B_train)


# In[18]:


pred1 = model1.predict(X_test)
pred2 = model2.predict(A_test)


# In[ ]:




