# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:33:29 2020

@author: Joe

UKBiobank data loading utilities
"""
import pandas as pd
import re
import numpy as np
import csv
import ukbiobank
import ukbiobank.filtering

        
        

def getFieldsInstancesArrays(ukb_csv=None, data_dict=None):
    """
    
    Parameters
    ----------
    ukbcsv : String path to ukbiobank csv file
         The default is None.
  
    data_dict :Pandas dataframe.
          Uk biobank data dictionary
        


    Returns
    -------
    field_instance_array pandas dataframe.        
    
    This is used as a reference for decoding columns heads & filtering based on column, instance etc

    """
    
    
    # Gathering available fields and instances
    with open(ukb_csv, 'r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        

    
    fieldnames = list(fieldnames)
        
    field_instance_array_df=pd.DataFrame()
    
    #TODO: make for loop more efficient (takes ~15s)
    for f in fieldnames:
        
        if f=='eid':
            pass
        else:
            field_instance, array_n = re.split('\.',f)#array_n is the number after the '.' (some fields have multiple measurements, e.g. multiple reported illnesses)
            field, instance = re.split('-',field_instance)
            temp_df=pd.DataFrame({'field':field, 'instance':instance, 'array':array_n},index=[0])
           
            field_instance_array_df=field_instance_array_df.append(temp_df)
        

    field_instance_array_df[["field","instance","array"]]=field_instance_array_df[["field","instance","array"]].apply(pd.to_numeric)
    
    
    result=pd.merge(field_instance_array_df,data_dict[['FieldID','Field']],left_on='field',right_on='FieldID')
        
    
    #tidying df
    result.drop(labels=['FieldID'],axis=1,inplace=True)
    result.rename(columns={'field':'field_id','Field':'field_name'}, inplace=True)

    #creating field_id_instance_array column
    result['id_instance_array']=result['field_id'].astype(str)+'-'+result['instance'].astype(str)+'.'+result['array'].astype(str)

    
    #Renaming duplicate fieldnames (inserting fieldID into name.)
    
    #get unique IDs
    uniq_ids=result.drop_duplicates(subset=['field_id'])
    duplicate_names=uniq_ids[uniq_ids.duplicated(subset=['field_name'],keep=False)]
    duplicate_names_ids=duplicate_names.field_id.unique().tolist()

    
    #Splitting duplicated from non-duplicate in order to append name column for duplicate
    result_duplicate=result[result['field_id'].isin(duplicate_names_ids)]
    result_non_duplicate=result[~result['field_id'].isin(duplicate_names_ids)]
    
    
    result_duplicate = result_duplicate.copy()
    result_duplicate['new_field_name'] = result_duplicate['field_name'].astype(str) + ' (Field ID: ' + result_duplicate['field_id'].astype(str)+ ')'
    result_duplicate.drop(labels=['field_name'],axis=1,inplace=True)
    result_duplicate.rename(columns={'new_field_name':'field_name'}, inplace=True)
    
    result2=result_duplicate.append(result_non_duplicate)
    result2['field_name_instance_array'] = result2['field_name'].astype(str)+'-'+result2['instance'].astype(str)+'.'+result2['array'].astype(str)


    return result2


def getFieldnames(ukbio):
    """
    

    Parameters
    ----------
    ukbio : ukbio object

    Returns
    -------
    List
        List of available ukbiobank fieldnames.

    """
   
    return ukbio.field_instance_array_df['field_name'].unique().tolist()




def getFieldIdsInstancesFromCategoryId(ukbio, field_ids=None):
    """
    

    Parameters
    ----------
    ukbio : ukbio object
    fieldNames : List of integers, mandatory
        Ukbiobank field category ids.

    Returns
    -------
    List of ALL ukbiobank fieldId_instance_array's associated with given field category id.

    """

    field_instance_array_df_temp=ukbio.field_instance_array_df.copy()    
    field_ids=field_instance_array_df_temp[field_instance_array_df_temp['field_id'].isin(field_ids)]['id_instance_array'].tolist()

    return field_ids

def getFieldIdsInstancesFromNamesInstances(ukbio, field_names=None):
    """
  
    Parameters
    ----------
    ukbio : ukbio object
    fieldNames : List of strings e.g. 'Sex-0.0' 

    Returns
    -------
    List of ALL ukbiobank fieldId_instance_array's associated with given field category 'id-instance.array' .

    """

    field_instance_array_df_temp=ukbio.field_instance_array_df.copy()    
    field_ids=field_instance_array_df_temp[field_instance_array_df_temp['field_name_instance_array'].isin(field_names)]['id_instance_array'].tolist()

    return field_ids




def getFieldIdsFromNames(ukbio, field_names=None):
    """
    

    Parameters
    ----------
    ukbio : ukbio object
    fieldNames : List of strings, mandatory
        Ukbiobank field_names.

    Returns
    -------
    List of ALL ukbiobank fieldId_instance_array's associated with given fieldname.

    """

    field_instance_array_df_temp=ukbio.field_instance_array_df.copy()    
    field_ids=field_instance_array_df_temp[field_instance_array_df_temp['field_name'].isin(field_names)]['id_instance_array'].tolist()

    return field_ids

def loadCsv(ukbio=None, fields=None, n_rows=None, instance=None):
    """
    
    Parameters
    ----------
    ukbio : ukbio object
    
    fields : List of strings, Mandatory
        Accepts UKB field category, ID or text string (or mixed), e.g. 21, '21-0.0' or 'Sex'.
    
    instance: Integer (either 0,1,2,3), optional.
        Performs filtering of columns by instance

    Returns
    -------
    df : Pandas dataframe
        df containing all instances of chosen fields.

    """
    
    
    #Testing for existence of all fields in ukbio object
    not_found=[]
    all_field_names_and_ids=ukbio.field_instance_array_df['field_name'].unique().tolist()
    all_field_names_and_ids.extend(ukbio.field_instance_array_df['id_instance_array'].tolist())
    all_field_names_and_ids.extend(ukbio.field_instance_array_df['field_id'].tolist())    
    all_field_names_and_ids.extend(ukbio.field_instance_array_df['field_name'].tolist())
    all_field_names_and_ids.extend(ukbio.field_instance_array_df['field_name_instance_array'].tolist())
    
    
    for f in fields:
        if f not in all_field_names_and_ids and f!='eid':
            not_found.append(f)
    
    if len(not_found)>0:
        print('The following variables were not found:\n {0}. \n\n This may be because the same fieldname is used across multiple field IDs.\n\n Either check the spelling of the variables or alternatively try using the field ID'.format(not_found))
    
    
    #Checking if field is text (new_fields will be a list of all field IDs after conversion from text)
    new_fields, fieldname_to_convert, field_id_to_convert = [], [], []
    for f in fields:
        
        #if string
        if isinstance(f, str) and f!='eid':
            fieldname_to_convert.append(f)
        
        #if category id but not field-instance-array
        elif re.match("^[0-9]*-", str(f)) is None and f!='eid' and isinstance(f, int):
            field_id_to_convert.append(f)
        
        
        else:
            new_fields.append(f)
    
    
    
    
    #Converting field cat to id-instance-arrays (e.g. '31' -> '31-0.0')
    if len(field_id_to_convert)>0:
        new_fields.extend(getFieldIdsInstancesFromCategoryId(ukbio, field_ids=field_id_to_convert))

    
    #Converting text to id (e.g. 'Sex' ->'31-0.0')
    if len(fieldname_to_convert)>0:
        new_fields.extend(getFieldIdsFromNames(ukbio, field_names=fieldname_to_convert))
    
    
    #Converting fieldname-instance.array format to fieldID-instance.array format (e.g. 'Sex-0.0' -> '31-0.0')
    if len (fieldname_to_convert)>0:
        new_fields.extend(getFieldIdsInstancesFromNamesInstances(ukbio, field_names=fieldname_to_convert))
    
    
    
    if 'eid' not in fields:
        new_fields.append('eid')
    
  
    if n_rows is not None:
        df=pd.read_csv(ukbio.csv_path, usecols=new_fields, nrows=n_rows)
    else:
        df=pd.read_csv(ukbio.csv_path, usecols=new_fields)
    
    if instance is not None:
        df = ukbiobank.filtering.filterInstancesArrays(ukbio=ukbio, df=df, instances=instance)

    return df



def fieldIdsToNames(ukbio=None, df=None, ids=None):
    """
    

    Parameters
    ----------
    ukbio : ukbio object, mandatory
        
    df : pandas dataframe (generated using ukbio loadCsv), optional
        
    ids: a list of ids (can be mixed text & id) to be converted to text, optional

    Returns
    -------
    Pandas dataframe (column names converted to text names)

    or
    
    List of fieldnames

    """

    if df is not None and ids is not None:
        print('Either specify df or ids, not both!')
        
    
    fieldID_fieldName_df=ukbio.field_instance_array_df.copy()

    
    if ids is not None:
        out=[]
        for i in ids:
            #if string with instance-array appendige
            if isinstance(i, str) and re.match(".*-[0-9]*\.[0-9]*$", i) is not None :             
               out.append(i)
            #if string without instance-array appendige, then add appendages
            elif isinstance(i, str) and re.match(".*-[0-9]*\.[0-9]*$", i) is None :
                field_names=fieldID_fieldName_df[fieldID_fieldName_df['field_name']==i]['field_name']              
                field_instances=fieldID_fieldName_df[fieldID_fieldName_df['field_name']==i]['instance']      
                field_arrays=fieldID_fieldName_df[fieldID_fieldName_df['field_name']==i]['array']    
                fieldnames_instance_array=field_names+'-'+field_instances.astype(str)+'.'+field_arrays.astype(str)
                out.extend(fieldnames_instance_array.tolist())
               
            #else if field ID (int) and Field ID exists, then convert to name and add appendage
            elif isinstance(i, int) and i in fieldID_fieldName_df['field_id'].values:
                field_names=fieldID_fieldName_df[fieldID_fieldName_df['field_id']==int(i)]['field_name']              
                field_instances=fieldID_fieldName_df[fieldID_fieldName_df['field_id']==int(i)]['instance']      
                field_arrays=fieldID_fieldName_df[fieldID_fieldName_df['field_id']==int(i)]['array']    
                
                fieldnames_instance_array=field_names+'-'+field_instances.astype(str)+'.'+field_arrays.astype(str) 
                out.extend(fieldnames_instance_array.tolist())
          
            else:
                print('Could not find field ID: {0}'.format(i))
            
    
    

    elif df is not None:
        cols=df.columns.tolist()    
        new_fields = []
        #Check if field is ID, if so, gather fieldname
        for c in cols:
            if re.match("^[0-9]*-", c) is not None and c!='eid':
               
                fieldID=c.split('-')[0]
                
                fieldName=fieldID_fieldName_df[fieldID_fieldName_df['field_id']==int(fieldID)]['field_name'].iloc[0]
                
                converted=re.sub("^([0-9])*-",fieldName+'-',c)
                
                new_fields.append(converted)
            else:
                new_fields.append(c)
        out=df.copy()
        out.columns=new_fields
    
    
    return out

def fieldNamesToIds(ukbio=None, df=None):
    """
    

    Parameters
    ----------
    ukbio : ukbio object, mandatory
        
    df : pandas dataframe with column headers containing text name (e.g. Illness Code-2.0')
        

    Returns
    -------
    Pandas dataframe (column text names converted to ukbio id (e.g. 'Illness Code-2.0' -> 20002-2.0)

    """
    
    cols=df.columns.tolist()    
    fieldID_fieldName_df=ukbio.field_instance_array_df.copy()
    
    
    new_fields = []
    #Check if field is a series of integers in '(field)-(instance).(array)' format, if so 
    for c in cols:
        if re.match("[0-9]*-[0-9]*\.[0-9]*$", c) is None and c!='eid':
           
            
            fieldNameParts=c.split('-')[:-1] # get all parts of string up until the final '-' (i.e. the name)
            
            fieldName='-'.join(fieldNameParts)#
            instanceArray=c.split('-')[-1]
            
            fieldID=fieldID_fieldName_df[fieldID_fieldName_df['field_name']==fieldName]['field_id'].iloc[0]
            
            converted=re.sub("(.*)-[0-9]*\.[0-9]*$",str(fieldID)+'-'+instanceArray,c)
            
            new_fields.append(converted)
        else:
            new_fields.append(c)
   
    
    new_df=df.copy()
    new_df.columns=new_fields
    
    
    return new_df


def illnessCodesToText(ukbio=None, df=None):
    """
    Parameters
    ----------
    ukbio : ukbio object, mandatory
        
    df : pandas dataframe (generated using ukbio loadCsv)

    Returns
    -------
    Pandas dataframe (column names converted to text names)


    """

    
    #At this stage the input_df columns are expected to be fieldIDs (not text)
    
    #If all columns contain alphanumeric characters then convert to field ID ('Sex-0.0' -> '23-0.0')
    if df.columns.str.contains('[a-z]').all():
        df=fieldNamesToIds(ukbio,df)



    #Decode self-reported illness (non-cancer)
    nonCancerIllness=df.filter(regex='^(20002)|(eid)')
    nonCancerIllness.replace(to_replace=ukbio.nonCancerIllnessCoding.coding.tolist(),value=ukbio.nonCancerIllnessCoding.meaning.tolist(), inplace=True)   
    
    #Decode ICD9 illness
    icd9=df.filter(regex='^(40013)|^(40017)|^(41271)|^(41203)|^(41205)')
    icd9.replace(to_replace=ukbio.icd9Coding.coding.tolist(),value=ukbio.icd9Coding.meaning.tolist(), inplace=True)   


    #Decode ICD10 illness
    icd10=df.filter(regex='^(40002)|^(41270)|^(41202)|^(41204)|^(41201)|^(40006)|^(40001)')
    icd10.replace(to_replace=ukbio.icd10Coding.coding.tolist(),value=ukbio.icd10Coding.meaning.tolist(), inplace=True)   

    
    #merging decoded illness dataframes
    concatenated=pd.concat([nonCancerIllness,icd9,icd10],axis=1)
    # merged = reduce(lambda  left,right: pd.merge(left,right,on=['eid'],
    #                                         how='outer'), to_merge)


    columns_to_use = df.columns.difference(concatenated.columns).tolist()
    columns_to_use.append('eid')
    df_out=df[columns_to_use].merge(concatenated, on='eid')
    

    return df_out


def addFields(ukbio=None, df=None, fields=None):
    """
    
    Parameters
    ----------
    ukbio : ukbio object
        ukbiobank.ukbio object
    
    df : pandas dataframe
        df containing ukbiobank data 
    
    fields : List, Mandatory
        Accepts UKB field ID or text string (or mixed), e.g. '31-0.0' or 'Sex'.
        
    Example usage::
        
        df = ukbiobank.utils.addFields(ukbio = ukb, df = df, fields = ['Sex'])
    

    Returns
    -------
    df : Pandas dataframe
        df containing all instances of chosen fields.

    """
    
    # Convert to list
    if not isinstance(fields,list):
        fields = [fields]
    
    
    # If no df passed, then initiliase empty df
    if df is None:
        in_df = False
        df = pd.DataFrame()
    else:
        in_df = True
    
    # Convert input to df if not (e.g. if just a series of eids)
    if not isinstance(df, pd.DataFrame):
        df = df.to_frame()

    
    # Append 'eid' to list of required fields
    if 'eid' not in fields:
        fields = list(fields)
        fields.append('eid')
    
    # Get extra fields
    new_df = loadCsv(ukbio, fields=fields)
        
    
    # Merge dataframes
    if  in_df is True:
        # Ignoring duplicate columns
        cols_to_use = new_df.columns.difference(df.columns)
        cols_to_use = cols_to_use.tolist()
        cols_to_use.append('eid')
        
        # Merging
        out_df=df.merge(new_df[cols_to_use], on='eid', how='inner')
    else:
        out_df = new_df.copy()
        
    return out_df




def calculateHealthySleepScore(ukbio=None, df=None):
    """
    Generates a composite healthy sleep score (0-5) accoring the methods used: 
        https://academic.oup.com/eurheartj/article/41/11/1182/5678714#200787415


    Parameters
    ----------
    ukbio : ukbio object.  Mandatory.
    
    df : pandas df loaded using ukbiobank-tools. Mandatory.

    Returns
    -------
    out_df : pandas df containing healthy sleep score (0-5)

    """
    
    #Check that vars exist in df


    #sleep_vars=['Morning/evening person (chronotype)-{0}.0', 'Sleep duration-{0}.0',  'Sleeplessness / insomnia-{0}.0', 'Snoring-{0}.0' ,  'Daytime dozing / sleeping (narcolepsy)-{0}.0']
    
    for instance in ['2', '3']:
        
        
        hss='healthy_sleep_score-{0}.0'.format(instance) #(hss : healthy sleep score)
        
        #Score starts at zero (+1 is added depending upon question response)
        df[hss] = 0
        
        #Chronotype score
        v = 'Morning/evening person (chronotype)-{0}.0'.format(instance)
        df.loc[(df[v] == 1) | (df[v] == 2) , hss] = df[hss] + 1
        
        #Sleep duration score
        v = 'Sleep duration-{0}.0'.format(instance)
        df.loc[(df[v] == 7) | (df[v] == 8) , hss] = df[hss] + 1
        
        #Insomnia score
        v =  'Sleeplessness / insomnia-{0}.0'.format(instance)
        df.loc[(df[v] == 1) , hss] = df[hss] + 1
        
        #Snore score
        v = 'Snoring-{0}.0'.format(instance)
        df.loc[(df[v] == 2) , hss] = df[hss] + 1
        
        #Daytime dozing score
        v = 'Daytime dozing / sleeping (narcolepsy)-{0}.0'.format(instance)
        df.loc[(df[v] == 0) | (df[v] == 1) , hss] = df[hss] + 1
        
        
    # Assign score
    
    
    

    
    
    #Methods below:
    """
    
    We included five sleep factors (chronotype, duration, insomnia, snoring, and excessive daytime sleepiness) to generate a healthy sleep score. Low-risk sleep factors were defined as follows: early chronotype (‘morning’ or ‘morning than evening’); sleep 7–8 h per day; reported never or rarely insomnia symptoms; no self-reported snoring; and no frequent daytime sleepiness (‘never/rarely’ or ‘sometimes’). For each sleep factor, the participant received a score of 1 if he or she was classified as low risk for that factor or 0 if at high risk for that factor. All component scores were summed to obtain a healthy sleep score ranging from 0 to 5, with higher scores indicating a healthier sleep pattern. We then define the overall sleep patterns as ‘healthy sleep pattern’ (healthy sleep score ≥4), ‘intermediate sleep pattern’ (2≤healthy sleep score ≤3), and ‘poor sleep pattern’ (healthy sleep score ≤1) based on the healthy sleep score.

In sensitive analysis, we further constructed a weighted sleep score based on the five sleep factors by using the equation: weighted sleep score = (β1×factor1 +β2 ×factor 2 +…+β5×factor 5) × (5/sum of the β coefficients). This weighted score also ranges from 0 to 5 points but considers magnitudes of the adjusted relative risk for each factor in each sleep pattern as a combination of five factors.


    """

    out_df=df.copy()
    
    
    return out_df
    
    
    

        
def removeOutliers(df = None, std = 3, cols = None):
    """
    
    Parameters
    ---------
    
    df: pandas dataframe
    
    std : int, defauult 3. Number of standard deviations threshold to exclude outliers.

    cols : columns in pandas df to exlcude outliers.

    Returns
    -------
    df : Pandas dataframe
     
    """    
    
    for c in cols:
        upper_limit, lower_limit = (df[c].mean() + 3*df[c].std()), (df[c].mean() - 3*df[c].std())
        
        
        df.loc[(df[c] > upper_limit), c] = np.nan
        df.loc[(df[c] < lower_limit), c] = np.nan
    
    return df





def  calculateChangeInCognitiveScores(ukbio=None, df=None):
    """    
    Parameters
    ----------
    ukbio : ukbio object.  Mandatory.
    
    df : pandas df loaded using ukbiobank-tools. Mandatory.

    Returns
    -------
    out_df : pandas df containing cognitive decline score
    
    Currently subtracts cognitive test score at instance 3 from instance 2 for the tests listed below. Output variables are labelled as 'change in x':
        
        
     - 'Mean time to correctly identify matches'->'Change in Mean time to correctly identify matches 
     - 'Maximum digits remembered correctly (Field ID: 4282) ->  'Change in x
     - Fluid intelligence score (Field ID: 20016) -> 'Change in x
     - 'Number of incorrect matches in round (Field ID: 399) -> 'Change in x
     - 'Number of puzzles correctly solved -> 'Change in x
     - 'Number of puzzles correct -> 'Change in x
     - 'Number of word pairs correctly associated -> Change in x
     - Duration to complete alphanumeric path (trail #2) (Field ID: 6350)  -> Change in x
     - 'Number of symbol digit matches made correctly (Field ID: 23324) -> Change in x
        
    
    
    """

    out_df=df.copy()
    
    # List of pairs of cognitive vars to calculate change between (first - second) 
    
    cog_vars = [('Mean time to correctly identify matches-3.0','Mean time to correctly identify matches-2.0'),
                ('Maximum digits remembered correctly (Field ID: 4282)-3.0','Maximum digits remembered correctly (Field ID: 4282)-2.0'),
                ('Fluid intelligence score (Field ID: 20016)-3.0','Fluid intelligence score (Field ID: 20016)-2.0'),
                ('Number of incorrect matches in round (Field ID: 399)-3.2','Number of incorrect matches in round (Field ID: 399)-2.2'),
                ('Number of puzzles correctly solved-3.0','Number of puzzles correctly solved-2.0'),
                ('Number of puzzles correct-3.0','Number of puzzles correct-2.0'),                
                ('Number of word pairs correctly associated-3.0','Number of word pairs correctly associated-2.0'),
                ('Duration to complete alphanumeric path (trail #2) (Field ID: 6350)-3.0','Duration to complete alphanumeric path (trail #2) (Field ID: 6350)-2.0'),
                 ('Number of symbol digit matches made correctly (Field ID: 23324)-3.0','Number of symbol digit matches made correctly (Field ID: 23324)-2.0')]
    
    
    
    for pair in cog_vars:
        
        
        #Calculating raw change in cog pair
        v = 'Change in {0}'.format(pair[0].rsplit('-')[0])
        out_df[v]  = out_df[pair[0]] - out_df[pair[1]]
        
        #Calculating percentage change in cog pair
        v = 'Percentage Change in {0}'.format(pair[0].rsplit('-')[0])
        out_df[v]  = ( ((out_df[pair[0]] - out_df[pair[1]]) /  (out_df[pair[0]]))  *100 ) 


    return out_df



def calculateCognitiveDeclineScore(ukbio=None, df=None, percentage_thresh=0, missing_tolerance=0):
    """
    Currently generates a composite 'cognitive_decline_score-3.0' between instances 2 & 3 (imaging visits)
    +1 point is added if the score on a test changed by a given percentage' between instances 2 & 3. 
    Deafult percentage is '0', i.e. any decline in a score will count, if '+20, improvements of 19% and any decrease in performance will count.
    
    Future to do's
   
    -include additional tests, instances etc
    -account for age. .
   
    Parameters
    ----------
    ukbio : ukbio object.  Mandatory.
    
    df : pandas df loaded using ukbiobank-tools. Mandatory.
    
    percentage_thresh: int. Optional. Default: 0.
    
        This parameter determines how much of a percentage change in scoring is required before a '+1' cognitive decline score is to be added for that test.
        E.g. if set to '-50', then the RT must have gotten worse by 50%, or the number of items remembered must have dropped by 50% ..

    missing_thresh: int. optional, default 0.
        
        This parameter determine how many mising tests the calculation will tolerate.
        E.g. if scores are missing for all tests, then a subject will by default recieve an overall score of 0. 
        However, if the missing tolerance is 0, then any missing test will assign a NaN score to this subject.

    Returns
    -------
    out_df : pandas df containing cognitive decline score
    """
    



    cog_vars = ['Percentage Change in Maximum digits remembered correctly (Field ID: 4282)',
                'Percentage Change in Fluid intelligence score (Field ID: 20016)',
                'Percentage Change in Number of puzzles correctly solved',
                'Percentage Change in Number of puzzles correct',
                'Percentage Change in Number of word pairs correctly associated',
                'Percentage Change in Number of symbol digit matches made correctly (Field ID: 23324)']

    
    #These are the cognitive vars for which a higher score means worse performance (e.g. reaction time / number of errors made). They are treated separately during the score calculation
    cog_vars_inverted = ['Percentage Change in Mean time to correctly identify matches',
                         'Percentage Change in Number of incorrect matches in round (Field ID: 399)',
                         'Percentage Change in Duration to complete alphanumeric path (trail #2) (Field ID: 6350)']
        
    
    # Check that 'Change in' cognitive vars exist in df, if not then run calculateChangeInCognitiveScore
    if not pd.Series(cog_vars+cog_vars_inverted).isin(df.columns).all():
        raise ValueError('Change in cognitive scores not found in dataframe, try running calculateChangeInCognitiveScores() first')

                  
    #Score starts at zero (+1 is added depending upon question response)
    cds='cognitive_decline_score-3.0' #(cds : cognitive decline score)
    df[cds] = 0
    
    # Setting cognitive score to nan based on tolerance
    all_cog_vars= cog_vars+cog_vars_inverted
    df['NumberOfNans'] = 0
    for v in all_cog_vars:
        df.loc[(df[v].isnull()), 'NumberOfNans'] = df['NumberOfNans'] + 1
        
    df.loc[(df['NumberOfNans'] > missing_tolerance) , cds] = np.nan
    
    
    #Assigning cognitive decline points
    for v in cog_vars:   
        df.loc[(df[v] < percentage_thresh), cds] = df[cds] + 1
        
    
    for v in cog_vars_inverted:
        df.loc[(df[v] > -percentage_thresh) , cds] = df[cds] + 1
         

    
    out_df=df.copy()
    
    
    return out_df
    






def meltByInstance(ukbio=None, df=None):
    """
    

    Parameters
    ----------
    ukbio : ukbio object.  Mandatory.
    
    df : pandas df loaded using ukbiobank-tools. Mandatory.

    Returns
    -------
    out_df : pandas df which has been re-fromatted to include the following columns: "Variable | Instance | Value"
    """
    
    df = df.melt(id_vars='eid')
    
    df[['variable','instance','array']]=df.variable.str.extract(pat='^(.*)-(.*)\.(.*)$')



    return df