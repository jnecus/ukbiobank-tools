# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:33:29 2020

@author: Joe

UKBiobank data filtering utilities
"""
import pandas as pd
import re
from ukbiobank.utils import fieldNamesToIds

def filterInstancesArrays(ukbio=None, df=None, instances=None, arrays=None):
    """
    

    Parameters
    ----------
    ukbio : ukbio object, mandatory
    
    df : pandas dataframe (generated using ukbio loadCsv)
    
    instances : List of integers
        
    arrays : List of integers
        

    Returns
    -------
    Pandas dataframe with datafields filtered for selected instances/arrays.

    """
    
    
    #This function expects column heading to be in the format 'fieldID-instance.array'
    
    #test columns 
    #xx.columns.str.contains('[a-z]').any()
    
    #if any column contains alphanumeric characters, (TODO: include functionality to ignore 'eid'..this will currently convert to ID every time)
    
    
    #if all columns contain alphanumeric characters then convert to field ID 
    if df.columns.str.contains('[a-z]').all():
        df=fieldNamesToIds(ukbio,df)
    
    field_instance_array_df_temp=ukbio.field_instance_array_df.copy()
    
    #filtering by instances
    if instances is not None:
        field_instance_array_df_temp=field_instance_array_df_temp[field_instance_array_df_temp['instance']
                                                     .isin(instances)]
    #filtering by arrays
    if arrays is not None:
        field_instance_array_df_temp=field_instance_array_df_temp[field_instance_array_df_temp['array']
                                                     .isin(arrays)]



    #Finding intersection of "Dataframe" field_instance_arrays &  "ALL" field_instance_arrays
    cols=list( set(df.columns.tolist())  & set(field_instance_array_df_temp['id_instance_array'].tolist()) )
    
    if 'eid' not in cols:
        cols.append('eid')          
    
 

    return df[cols]





def filterByField(ukbio=None, df=None, fields_to_include=None, instances=None, arrays=None):
    """  
    Parameters
    ----------
    ukbio : ukbio object, mandatory
    
    df : pandas dataframe (currently only accepts FieldID headers ased column headers)
                           
    fields_to_include: Dictionary whereby keys: 'fields to include', values:'values to include'
    
    instances : list of integers
    
    arrays : list of integers
        

    Returns
    -------
    Pandas dataframe with data-fields filtered for selected fields, values, instances, arrays.
    
    *This function uses 'OR' logic, i.e. if any of the values/fields included are present then they will be included*
    
    """
    
    #todo (account for text/ids/mixture etc...)
    #convert keys/values from text --> id 
    
    
    #Generate list of columns to iterate (i.e. accounting for field-instance.array)
    
    
    #Once all headers are raw Field IDs, and table values are encoded IDs..
    """Below here expected format is e.g.      'eid'      '20002-1.0'
                                                1437784     12633

    """
    
    matched_eids=[] #list to collect eids for which a match is found
    
    for field, value in fields_to_include.items():
      
        for instance in instances:
            field_instance=str(field)+'-'+str(instance)
            
            #matching all columns with field/instance
            field_instance_arrays=[col for col in df if col.startswith(field_instance)]
            
            if len(field_instance_arrays)>0:
                field_instance_arrays.append('eid')
            
                
                #Is there a matching value in any column given the list of values
                temp_df=df[field_instance_arrays].isin(value)
                
                #If any column is true, then keep that row (i.e. that 'eid' row)
                temp_df=df[field_instance_arrays][temp_df.any(axis=1)]
                
                matched_eids.extend(temp_df['eid'].tolist())
                
    
    
    return df[df['eid'].isin(matched_eids)]









def getAlgorithmicAllCauseDementia(ukbio=None, df=None):
    """
    An implementation of Ukbiobank algorithmic health outcome, specifically 'All cause dementia' using the 
    criteria defined in https://biobank.ndph.ox.ac.uk/showcase/showcase/docs/alg_outcome_dementia.pdf

    Parameters
    ----------
    ukbio : ukbio object, mandatory
    
    df : pandas dataframe (generated using ukbio loadCsv)
   
    *Note* Input dataframe must contain fields pertaining to ICD9, ICD10, 
    Non-Cancer Illness codes and corresponding dates
           
    Returns
    -------
    Pandas dataframe manually generated all cause dementia fields.

    """





    #Defining fields & values corresponding to all cause dementia
    icd_10_main_field=41202
    icd_10_secondary_field=41204
    icd_10_all_dementia=['A810','F00','F000','F001','F002','F009','F01','F010','F011','F012','F013','F018','F019','F02','F020','F021','F022','F023','F024','F028','F03','F051','F106','G30','G300','G301','G308','G309','G310','G311','G318','I673']
    
    icd_10_primary_death_field=40001    
    icd_10_secondary_death_field=40002
    
    icd_9_main_field=41203
    icd_9_secondary_field=41205
    icd_9_all_dementia=[290.2, 290.3, 290.4, 291.2, 294.1, 331.0, 331.1, 331.2, 331.5]
    
    
    #Self reported illness
    self_reported_illness_field=20002
    self_reported_illness_dementia=[1263]
    
    #Gathering df containing eids with a record of dementia
    my_dementia_df=filterByField(ukbio, df=df, fields_to_include={
                                     self_reported_illness_field: self_reported_illness_dementia,
                                     icd_10_main_field: icd_10_all_dementia,
                                     icd_10_secondary_field: icd_10_all_dementia,
                                     icd_10_primary_death_field:icd_10_all_dementia,
                                     icd_10_secondary_death_field:icd_10_all_dementia,
                                     icd_9_secondary_field: icd_9_all_dementia,
                                     icd_9_main_field: icd_9_all_dementia},
                                     instances=[0,1,2,3])


    
    my_dementia_df.dropna(axis=1,how='all', inplace=True) #dropping cols with all Nan
    
    #Selecting only the columns corresponding to illness code and year occurred
    icd10_illnesses='^(40002)|^(41270)|^(41202)|^(41204)|^(41201)|^(40006)|^(40001)'
    icd10_dates='^(41280)|^(41262)|'
    icd9_illnesses='^(40013)|^(40017)|^(41271)|^(41203)|^(41205)'
    icd9_dates='^(41281)|^(41263)|'
    nonCancer_illnesses='^(20002)|'
    nonCancer_years='^(20008)|'
    
    
    #TODO continue to implement this once ICD9/10 diagnosis *date* variables have been obtained.
    my_dementia_df.filter(icd10_illnesses )#...
    
    #melt df
    df_melted=my_dementia_df.melt(id_vars='eid',var_name='field_instance_array',value_name='code')
    
    #per subject
    # for subj in df_melted.groupby('eid'):
        #filter for dementia codes only
        #xx=df_melted[df_melted['code'].isin(list_of_dementia_codes)]
        #filter for source & earliest date
        #save log of source and earliest date
        
    
    #requires implementing the various logic included in the pdf doc mentioning in docstring.
    return my_dementia_df















