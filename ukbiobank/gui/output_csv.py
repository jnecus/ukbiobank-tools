# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 17:45:15 2020

@author: Joe
"""


import wx
import ukbiobank 
from wx.lib.agw import pybusyinfo

class OutputCsvFrame(wx.Frame, ukbiobank.ukbio):
    def __init__(self, parent, ukb):
        super().__init__(parent=parent, title='Output CSV', size=wx.DefaultSize)



        
        with wx.FileDialog(self, "Save output as csv", wildcard="csv files (*.csv)|*.csv",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
    
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
    
            # Getting filepath
            pathname = fileDialog.GetPath()
            
            # Getting selections 
            s = ukb.SELECTIONS 
            
            if s is None:
                print("No selections were made")
                return
            
            else:
            
                busy =  pybusyinfo.PyBusyInfo(message='Saving csv, please wait...')
                
                # Adding fields to dataframe
                if 'include_variables' in s and len(s['include_variables']) > 0:
                    df = ukbiobank.utils.addFields(ukbio=ukb, fields=s['include_variables'])
                
                # Filtering dataframe according to 'include_illness' selections
                if 'include_illnesses' in s and len(s['include_illnesses_coded']) > 0:                
                    df = ukbiobank.filtering.filterByField(ukbio=ukb, df=df, fields_to_include=s['include_illnesses_coded'])
                
                
                try:
                    # Saving
                    df.to_csv(pathname,index=False)
    
                except IOError:
                    wx.LogError("Cannot save current data in file '%s'." % pathname)
            
                
                busy.Show(show=False)
                wx.MessageBox('CSV saved to: {0}'.format(pathname), 'Info', wx.OK | wx.ICON_INFORMATION)
           
        
        
