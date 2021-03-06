# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 12:38:10 2020

@author: jnecus
"""

import os

import pandas as pd

import ukbiobank


class ukbio:
    """

    Parameters
    ----------
    ukb_csv : String, mandatory
       Path to ukbiobank csv file. ipthon


    Example usage::

        import ukbiobank
        ukb = ukbiobank.ukbio(ukb_csv='path/to/ukbiobank_data.csv')



    Returns
    -------
    ukbio object.
        ukbio objects are required as an input when using ukbiobank-tools functions.
        ukbio objects contain import information such as:
                - variable codings
                - path to ukbiobank csv file

    """

    def __init__(self, ukb_csv=None):

        file_path = os.path.dirname(__file__)
        self.csv_path = ukb_csv

        self.data_dict = pd.read_csv(
            os.path.join(file_path, "data_coding", "Data_Dictionary_Showcase.csv")
        )

        # Illness/medication codings
        # TODO continue insert coding dictionaries.. (for medications etc..)
        self.nonCancerIllnessCoding = pd.read_table(
            os.path.join(file_path, "data_coding", "coding6.tsv")
        )
        self.icd9Coding = pd.read_table(
            os.path.join(file_path, "data_coding", "coding87.tsv")
        )
        self.icd10Coding = pd.read_table(
            os.path.join(file_path, "data_coding", "coding19.tsv")
        )

        # Variable/instance codings
        self.field_instance_array_df = ukbiobank.utils.getFieldsInstancesArrays(
            ukb_csv=self.csv_path, data_dict=self.data_dict
        )
