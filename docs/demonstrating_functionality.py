# -*- coding: utf-8 -*-
"""

Loading and testing ukbio features with ukbiobank data.


***THIS ALL NEEDS RE-WRITING WITH NEW MODULAR STRUCTURE . . ***

E.G. import ukbiobank.filtering
    ukbiobank.filtering.filterByField() . . 



"""


#import pandas as pd
from ukbio import ukbio
from ukbio.ukbio_utils import getFieldnames, loadCsv, illnessCodesToText


""" FIRST STEP. Loading ukbiobank data into ukbio object"""
#path to ukb csv file
ukb_csv = 'C:/Users/Joe/Google Drive/Post Doc Dementia/UK Biobank/March2020_data_refreshes/ukb41344/ukb41344.csv'
ukb=ukbio.ukbio(ukb_csv=ukb_csv)

#This can also accept a zipped csv file (some ukbiobank csv files are very large so zipped files are useful to save disk space), .e.g. :
ukb_csv = 'C:/Users/Joe/Google Drive/Post Doc Dementia/UK Biobank/March2020_data_refreshes/ukb41344/ukb41344.zip'
ukb=ukbio.ukbio(ukb_csv=ukb_csv)

#Gathering fieldnames
fieldnames=getFieldnames(ukb)
 
#loading csv with fields
#df=loadCsv(ukb,fields=['eid','Non-cancer illness code, self-reported','Date of all cause dementia report','Source of all cause dementia report', 'Diagnoses - main ICD10','Diagnoses - main ICD9'])

#loading a sample of df for testing purposes
df=loadSampleCsv(ukb,fields=['eid','Non-cancer illness code, self-reported','Date of all cause dementia report','Source of all cause dementia report', 'Diagnoses - main ICD10','Diagnoses - main ICD9'],n_rows=2000)






"""Filtering fields based upon Instances/Arrays"""
from ukbio.ukbio_filtering import filterInstancesArrays
df2=filterInstancesArrays(ukbio=ukb,df=df,instances=[0])


#Convert column field Ids to names
from ukbio.ukbio_utils import fieldIdsToNames
df3=fieldIdsToNames(ukbio=ukb,df=df2)



#Filtering by field
#defining fields and values to filter on
field1=20002 #self reported illness field
values1=[1263,1111] # dementias & asthma
fields_to_include={field1:values1} #create dictionary of fields/values to filter on

#Perform filterByField
from ukbio.ukbio_filtering import filterByField
from ukbio.ukbio_utils import fieldNamesToIds
df3=fieldNamesToIds(ukb,df)#converting back to ids as filterByFields currently only accepts fieldID column headings
df4=filterByField(ukbio=ukb,df=df3,fields_to_include=fields_to_include, instances=[0,1,2,3])


#Convert illness codes to text
df5=illnessCodesToText(ukb, df4)


""" To Do"""
#df6=addFields(ukb, df, fields=[])





#1. How many people have a diagnosis of dementia and one scan or two scans?


#Generating 'Date of all cause dementia report' in separate script : 'generatingAllCauseDementiaReport20200401.py'




















