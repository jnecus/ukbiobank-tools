# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 12:38:10 2020

@author: Joe
"""


from .utils import getFieldsInstancesArrays,getFieldIDFieldNameDf
import pandas as pd
import os


class ukbio():

    
    def __init__(self, ukb_csv=None):
        """
        
        
        Parameters
        ----------
        ukb_csv : String, mandatory
           Path to ukbiobank csv file. .
        
        Returns
        -------
        ukbio object.
        
        """
        
        
        file_path = os.path.dirname(__file__)       
        self.csv_path=ukb_csv
        
        
        
        #Paths may fail between unix / windows due to hard-coded backslash below
        self.data_dict=pd.read_csv(file_path+'\data_coding\Data_Dictionary_Showcase.csv')
        
        
        #TODO continue insert coding dictionaries.. (for medications etc..)
        self.nonCancerIllnessCoding=pd.read_table(file_path+'\data_coding\coding6.tsv')
        self.icd9Coding=pd.read_table(file_path+'\data_coding\coding87.tsv')
        self.icd10Coding=pd.read_table(file_path+'\data_coding\coding19.tsv')


        
        self.field_instance_array_df=getFieldsInstancesArrays(ukb_csv=self.csv_path, data_dict=self.data_dict)        
        self.fieldID_fieldName_df=getFieldIDFieldNameDf(field_instance_array_df=self.field_instance_array_df)
        
