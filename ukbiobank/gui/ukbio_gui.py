# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:33:29 2020

@author: Joe

UKBiobank data loading utilities
"""
import pandas as pd
import re

import wx



#wxpython code taken from https://realpython.com/python-gui-with-wxpython/
def open():    
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
    return

    

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Hello World')
        panel = wx.Panel(self)

        self.text_ctrl = wx.TextCtrl(panel, pos=(5, 5))
        my_btn = wx.Button(panel, label='Press Me', pos=(5, 55))

        self.Show()


    
  # return


#ukbio_utils functions below...

# def getFieldsInstancesArrays(ukb_csv=None, data_dict=None):
#     """
#     Parameters
#     ----------
#     ukbcsv : String path to ukbiobank csv file
#          The default is None.
  
#     data_dict :Pandas dataframe.
#           Uk biobank data dictionary
        


#     Returns
#     -------
#     field_instance_array pandas dataframe        

#     """
    
#     #Gathering available fields and instances
#     fieldnames=pd.read_csv(ukb_csv,nrows=0).columns.tolist()

    
    
#     field_instance_array_df=pd.DataFrame()
    
#     for f in fieldnames:
        
#         if f=='eid':
#             pass
#         else:
#             field_instance, array_n = re.split('\.',f)#array_n is the number after the '.' (some fields have multiple measurements, e.g. multiple reported illnesses)
#             field, instance = re.split('-',field_instance)
#             temp_df=pd.DataFrame({'field':field, 'instance':instance, 'array':array_n},index=[0])
           
#             field_instance_array_df=field_instance_array_df.append(temp_df)
        

#     field_instance_array_df[["field","instance","array"]]=field_instance_array_df[["field","instance","array"]].apply(pd.to_numeric)
#     result=pd.merge(field_instance_array_df,data_dict[['FieldID','Field']],left_on='field',right_on='FieldID')
        
    
#     #tidying df
#     result.drop(labels=['FieldID'],axis=1,inplace=True)
#     result.rename(columns={'field':'field_id','Field':'field_name'}, inplace=True)

#     #creating field_id_instance_array column
#     result['id_instance_array']=result['field_id'].astype(str)+'-'+result['instance'].astype(str)+'.'+result['array'].astype(str)

#     return result


# def getFieldIDFieldNameDf(field_instance_array_df=None):
#     """
    

#     Parameters
#     ----------
#     field_instance_array_df : ukbio field_instance_arraypandas df

#     Returns
#     -------
#     fieldID_fieldName_df : shortened 'reference df' (index='field ID', 'field_name'=fieldname
#                                                    e.g index=21, 'field_name'='Sex')

#     """
#     fieldID_fieldName_df=field_instance_array_df.copy()
    
 
#     fieldID_fieldName_df.set_index('field_id',inplace=True)    
#     fieldID_fieldName_df = fieldID_fieldName_df.loc[~fieldID_fieldName_df.index.duplicated(keep='first')]


#     return fieldID_fieldName_df

# def getFieldnames(ukbio):
#     """
    

#     Parameters
#     ----------
#     ukbio : ukbio object

#     Returns
#     -------
#     List
#         List of available ukbiobank fieldnames.

#     """
   
#     return ukbio.field_instance_array_df['field_name'].unique().tolist()


# def getFieldIdsFromNames(ukbio, field_names=None):
#     """
    

#     Parameters
#     ----------
#     ukbio : ukbio object
#     fieldNames : List of strings, mandatory
#         Ukbiobank field_names.

#     Returns
#     -------
#     List of ALL ukbiobank fieldId_instance_array's associated with given fieldname.

#     """

#     field_instance_array_df_temp=ukbio.field_instance_array_df.copy()    
#     field_ids=field_instance_array_df_temp[field_instance_array_df_temp['field_name'].isin(field_names)]['id_instance_array'].tolist()

#     return field_ids

# def loadCsv(ukbio, fields=None):
#     """
    
#     Parameters
#     ----------
#     ukbio : ukbio object
    
#     fields : List of strings, Mandatory
#         Accepts UKB field ID or text string (or mixed), e.g. '21-0.0' or 'Sex'.


#     Returns
#     -------
#     df : Pandas dataframe
#         df containing all instances of chosen fields.

#     """
    
        
#     #Checking if field is text
#     new_fields, to_convert = [], []
#     for f in fields:
#         if re.match("^[0-9]*-", f) is None and f!='eid':
#              to_convert.append(f)
#         else:
#             new_fields.append(f)
#     #Converting text to id
#     if len(to_convert)>0:
#         new_fields.extend(getFieldIdsFromNames(ukbio, field_names=to_convert))
    
    
#     if 'eid' not in fields:
#         new_fields.append('eid')
    
    
    
#     #Checking for number of fields to be loaded (assessing memory required)
#     if len(new_fields)> 600:
#         cont=input('The number of identified field instances will require {0}mb of  memory, do you want to continue to load? (y/n): '.format(((500000*8)/1e+6)*len(new_fields)))
#         if cont=='y':
#             df=pd.read_csv(ukbio.csv_path, usecols=new_fields)
#         else:
#             return None
#     else:
#         df=pd.read_csv(ukbio.csv_path, usecols=new_fields)
    


#     return df

# def loadSampleCsv(ukbio, fields=None, n_rows=0):
#     """
    
#     Parameters
#     ----------
#     ukbio : ukbio object
    
#     fields : List of strings, Mandatory
#         Accepts UKB field ID or text string (or mixed), e.g. '21-0.0' or 'Sex'.
        
#     n_rows: int
#         Number of rows of ukb csv file to read

#     Returns
#     -------
#     df : Pandas dataframe
#         df containing all instances of chosen fields.

#     """
    
        
#     #Checking if field is text
#     new_fields, to_convert = [], []
#     for f in fields:
#         if re.match("^[0-9]*-", f) is None and f!='eid':
#              to_convert.append(f)
#         else:
#             new_fields.append(f)
#     #Converting text to id
#     if len(to_convert)>0:
#         new_fields.extend(getFieldIdsFromNames(ukbio, field_names=to_convert))
    
    
#     if 'eid' not in fields:
#         new_fields.append('eid')
    

    
#     df=pd.read_csv(ukbio.csv_path, usecols=new_fields, nrows=n_rows)

#     return df


# def fieldIdsToNames(ukbio=None, df=None):
#     """
    

#     Parameters
#     ----------
#     ukbio : ukbio object, mandatory
        
#     df : pandas dataframe (generated using ukbio loadCsv)
        

#     Returns
#     -------
#     Pandas dataframe (column names converted to text names)

#     """
    
#     cols=df.columns.tolist()
#     fieldID_fieldName_df=ukbio.fieldID_fieldName_df.copy()

    
    
#     new_fields = []
#     #Check if field is ID, if so, gather fieldname
#     for c in cols:
#         if re.match("^[0-9]*-", c) is not None and c!='eid':
           
#             fieldID=c.split('-')[0]
            
#             fieldName=fieldID_fieldName_df.loc[int(fieldID)]['field_name']
            
#             converted=re.sub("^([0-9])*-",fieldName+'-',c)
            
#             new_fields.append(converted)
#         else:
#             new_fields.append(c)
   
    
#     new_df=df.copy()
#     new_df.columns=new_fields
    
    
#     return new_df

# def fieldNamesToIds(ukbio=None, df=None):
#     """
    

#     Parameters
#     ----------
#     ukbio : ukbio object, mandatory
        
#     df : pandas dataframe with column headers containing text name (e.g. Illness Code-2.0')
        

#     Returns
#     -------
#     Pandas dataframe (column text names converted to ukbio id (e.g. 'Illness Code-2.0' -> 20002-2.0)

#     """
    
#     cols=df.columns.tolist()    
#     fieldID_fieldName_df=ukbio.fieldID_fieldName_df.copy()
#     fieldID_fieldName_df['field_id']=fieldID_fieldName_df.index
#     fieldID_fieldName_df.set_index('field_name', inplace=True)

    
#     new_fields = []
#     #Check if field finishes with '-(instance).(array)' format, if so 
#     for c in cols:
#         if re.match(".*-[0-9]*\.[0-9]*$", c) is not None and c!='eid':
           
#             fieldNameParts=c.split('-')[:-1] # get all parts of string up until the final '-'
#             fieldName='-'.join(fieldNameParts)#
#             fieldID=fieldID_fieldName_df.loc[fieldName]['field_id']
            
#             instanceArray=c.split('-')[-1]
            
#             converted=re.sub("(.*)-[0-9]*\.[0-9]*$",str(fieldID)+'-'+instanceArray,c)
            
#             new_fields.append(converted)
#         else:
#             new_fields.append(c)
   
    
#     new_df=df.copy()
#     new_df.columns=new_fields
    
    
#     return new_df


# def illnessCodesToText(ukbio=None, df=None):
#     """
#     Parameters
#     ----------
#     ukbio : ukbio object, mandatory
        
#     df : pandas dataframe (generated using ukbio loadCsv)

#     Returns
#     -------
#     Pandas dataframe (column names converted to text names)


#     """

    
#     #At this stage the input_df columns are expected to be fieldIDs (not text)
    
#     #If all columns contain alphanumeric characters then convert to field ID ('Sex-0.0' -> '23-0.0')
#     if df.columns.str.contains('[a-z]').all():
#         df=fieldNamesToIds(ukbio,df)



#     #Decode self-reported illness (non-cancer)
#     nonCancerIllness=df.filter(regex='^(20002)|(eid)')
#     nonCancerIllness.replace(to_replace=ukbio.nonCancerIllnessCoding.coding.tolist(),value=ukbio.nonCancerIllnessCoding.meaning.tolist(), inplace=True)   
    
#     #Decode ICD9 illness
#     icd9=df.filter(regex='^(40013)|^(40017)|^(41271)|^(41203)|^(41205)')
#     icd9.replace(to_replace=ukbio.icd9Coding.coding.tolist(),value=ukbio.icd9Coding.meaning.tolist(), inplace=True)   


#     #Decode ICD10 illness
#     icd10=df.filter(regex='^(40002)|^(41270)|^(41202)|^(41204)|^(41201)|^(40006)|^(40001)')
#     icd10.replace(to_replace=ukbio.icd10Coding.coding.tolist(),value=ukbio.icd10Coding.meaning.tolist(), inplace=True)   

    
#     #merging decoded illness dataframes
#     concatenated=pd.concat([nonCancerIllness,icd9,icd10],axis=1)
#     # merged = reduce(lambda  left,right: pd.merge(left,right,on=['eid'],
#     #                                         how='outer'), to_merge)


#     columns_to_use = df.columns.difference(concatenated.columns).tolist()
#     columns_to_use.append('eid')
#     df_out=df[columns_to_use].merge(concatenated, on='eid')
    

#     return df_out

# def getFieldname(fieldId=None):
#     """
    
