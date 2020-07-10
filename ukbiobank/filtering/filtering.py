# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:33:29 2020

@author: jnecus

UKBiobank data filtering utilities
"""
import pandas as pd
import re
import ukbiobank
import ukbiobank.utils

#from ukbiobank.utils import fieldNamesToIds, addFields


def filterInstancesArrays(ukbio=None, df=None, instances=None, arrays=None):
    """
    

    Parameters
    ----------
    ukbio : ukbio object, mandatory
    
    df : pandas dataframe (generated using ukbio loadCsv)
    
    instances : List of integers. Default is none (include all instances)
        
    arrays : List of integers.  Default is none (include all arrays)
        

    Returns
    -------
    Dataframe with datafields filtered for selected instances/arrays : Pandas dataframe

    """
    
    # Check instances is list, if not convert to list
    if not isinstance(instances, list):
        instances = [instances]
    
    #if all columns contain alphanumeric characters then convert to field ID 
    if df.columns.str.contains('[a-z]').all():
        df=ukbiobank.utils.fieldNamesToIds(ukbio,df)
    
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





def filterByField(ukbio=None, df=None, fields_to_include=None, instances=[0,1,2,3], arrays=None):
    """  
    Parameters
    ----------
    ukbio : ukbio object, mandatory
    
    df : pandas dataframe (currently only accepts FieldID headers as column headers)
                           
    fields_to_include: Dictionary whereby keys: 'fields to include', values:'values to include'
    *FIELDS IN FIELDS_TO_INCLUDE MUST BE IN FIELD_ID FORM* e.g. '20002' (not 'Self-reported Illness') *
    *VALUES IN FIELDS_TO_INCLUDE MUST BE IN CODED FORM* e.g. '1074', (not 'angina') *
   
    instances : list of integers
    
    arrays : list of integers
        

    Returns
    -------
    Pandas dataframe with data-fields filtered for selected fields, values, instances, arrays.
    
    *This function uses 'OR' logic, i.e. if any of the values/fields included are present then they will be included*
    
    """
    
    # Account for df = None, or if fields are not found in df, then add them
    if df is None:
        # Add all fields_to include
        df = ukbiobank.utils.addFields(ukbio=ukbio, fields=list(fields_to_include.keys()))
    else:
        
        # Convert df headings to fieldid-instance.array
        df = ukbiobank.utils.fieldNamesToIds(ukbio=ukbio, df=df)
        
        # Checking for missing fields
        df_fields = []
        for f in df.columns.tolist():
            df_fields.append(f.split('-')[0])
            
        unique_df_fields = list(set(df_fields))
            
        fields_to_add = []
        for f in list(fields_to_include.keys()):
            if f not in unique_df_fields:
                fields_to_add.append(f)
            
        if len(fields_to_add)>0:
            df = ukbiobank.utils.addFields(ukbio=ukbio, df=df, fields=fields_to_add)
 
    
 
    #TODO (account for text/ids/mixture etc...)
    #convert keys/values from text --> id 
    
    
    
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
                
                if not isinstance(value, list):
                    value = [value]
                
                temp_df=df[field_instance_arrays].isin(value)
                
                #If any column is true, then keep that row (i.e. that 'eid' row)
                temp_df=df[field_instance_arrays][temp_df.any(axis=1)]
                
                matched_eids.extend(temp_df['eid'].tolist())
                
    
    
    return df[df['eid'].isin(matched_eids)]











