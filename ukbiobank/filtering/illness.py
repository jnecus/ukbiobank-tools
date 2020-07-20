# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:33:29 2020

@author: jnecus

UKBiobank data filtering utilities
"""
import pandas as pd
import re
import ukbiobank

def healthy_unhealthy_split(ukbio=None, df=None, instances=[0,1,2,3], return_filter_fields=False):
    """
    Splits dataframe into healthy_df and unhealthy_df based upon exclusion criteria used in Cole 2020 
    https://www.sciencedirect.com/science/article/pii/S0197458020301056

    Exclusion critera were:
    An ICD-10 diagnosis (#41270),
    Self-reported long-standing illness disability or infirmity (UK Biobank data field #2188), 
    Self-reported diabetes (field #2443)
    Stroke history (field #4056), 
    Not having good or excellent self-reported health (field #2178).    
    
   *Note: According to these criteria, around ~20% of the data are 'healthy', with 80% deemed 'unhealthy'*

    Parameters
    ----------
    ukbio : ukbio object, mandatory
    
    df : pandas dataframe (generated using ukbio loadCsv). Mandatory
    
    instances : list of integers, Default is [0,1,2,3] (include all instances)
    
    return_filter_fields : Boolean, default False.
        If True, the fields used to filter according to healthy/unhealthy criteria are included in return dataframes (this can be useful for validation and see investigate the cause of healthy/unhealthy classification).
        If False, returned dataframes contain the same fields as the input dataframe.


    Returns
    -------
    healthy_df, dataframe with individuals not matching exclusion criteria : Pandas dataframe
    
    unhealthy_df, dataframe with individuals containing one or more matching exclusion criteria : Pandas dataframe

    """
    
    # Make copy of input dataframe
    in_df = df.copy()
    
    # Add fields required for exclusion criteria
    fields = [2188,2443,4056,2178]
    df = ukbiobank.utils.addFields(ukbio=ukbio,df=df,fields=fields,instances=instances)
    
    # ICD-10 diagnosis information is tied to instance '0', & added seperately
    fields=[41270]
    df = ukbiobank.utils.addFields(ukbio=ukbio,df=df,fields=fields, instances=0)
    
    # Gathering exclusion criteria columns and appending 'eid'
    excl_cols=list(df.columns.difference(in_df.columns))
    excl_cols.append('eid')
    
    df_excl_criteria = df[excl_cols]

    unhealthy_eids = [] # List to collect eids of individuals identified as 'unhealthy'
    
    
    # Filtering those with ICD-10 diagnosis #41270 (collecting eid for individuals with not any 'non-nan', i.e. containing a diagnosis) 
    col = list(df_excl_criteria.columns[df_excl_criteria.columns.str.match('^41270-')])
    uh_eids = df_excl_criteria.loc[ (df_excl_criteria[col].notna().any(axis=1)) , 'eid'] 
    unhealthy_eids.extend(list(uh_eids)) #extending list of unhealthy eid's
    
    # Filtering those with self reported illness/disability #2188
    responses_to_match = [1,-1,-3] # Will collecting eids with response '1' = 'yes',  '-1' (do not know) and '-3' (prefer not to answer)
    col = list(df_excl_criteria.columns[df_excl_criteria.columns.str.match('^2188-')])
    uh_eids = df_excl_criteria.loc[ (df_excl_criteria[col].isin(responses_to_match).all(axis=1)) , 'eid'] 
    unhealthy_eids.extend(list(uh_eids))
    
    # Filtering those with self reported diabetes #2443
    responses_to_match = [1,-1,-3] # Will collecting eids with response '1' = 'yes' to this field,  '-1' (do not know) and '-3' (prefer not to answer)
    col = list(df_excl_criteria.columns[df_excl_criteria.columns.str.match('^2443-')])
    uh_eids = df_excl_criteria.loc[ (df_excl_criteria[col].isin(responses_to_match).all(axis=1)) , 'eid'] 
    unhealthy_eids.extend(list(uh_eids))
    

    # Filtering those with age stroke diagnosed #4056   (collecting eid for individuals with not any 'non-nan', i.e. containing an age of stroke diagnosis or a -1/-3 (do not know/prefer not to answer)) 
    col = list(df_excl_criteria.columns[df_excl_criteria.columns.str.match('^4056-')])
    uh_eids = df_excl_criteria.loc[ (df_excl_criteria[col].notna().any(axis=1)) , 'eid'] 
    unhealthy_eids.extend(list(uh_eids)) #extending list of unhealthy eid's
    
    
    # Filtering those not responding as having 'good' or 'excellent' health #2178
    responses_to_match = [-3,-1,3,4] # Collecting eids with response '-3,-1, 3, 4' = 'Do not know, no answer, fair, poor' (all but good or excellent) to this field
    col = list(df_excl_criteria.columns[df_excl_criteria.columns.str.match('^2178-')])
    uh_eids = df_excl_criteria.loc[ (df_excl_criteria[col].isin(responses_to_match).all(axis=1)), 'eid'] 
    unhealthy_eids.extend(list(uh_eids))
    
    
    # Splitting original df by 'healthy' vs. 'unhealthy' eids 
    unhealthy_eids = list(set(unhealthy_eids)) #unique unhealthy eids
    
   
    df_unhealthy = in_df.loc[in_df['eid'].isin(unhealthy_eids)]
    df_healthy = in_df.loc[~in_df['eid'].isin(unhealthy_eids)]

    # Including criteria fields if requested
    if return_filter_fields == True:
        df_unhealthy = pd.merge(df_unhealthy,df_excl_criteria, on='eid')
        df_healthy = pd.merge(df_healthy,df_excl_criteria, on='eid')


    return df_healthy, df_unhealthy








