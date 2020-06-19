# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:33:29 2020

@author: Joe

UKBiobank data loading utilities
"""
import pandas as pd
import re

import wx
import ukbiobank
import ukbiobank.filtering 
from .select_variables import SelectVariablesFrame
from .select_illness import SelectIllnessFrame
from .output_csv import OutputCsvFrame

#MenuFrame (frame containing all options)
class MenuFrame(wx.Frame, ukbiobank.ukbio):
    
    def __init__(self, frame, ukb):
        super().__init__(parent=None,title='UKBiobank-tools menu', size=wx.DefaultSize)
        self.ukb_object = ukb
        self.ukb_object.SELECTIONS = None #initialising variable/filter selections to None 
        
        
        panel = wx.Panel(self)        
        my_sizer = wx.GridSizer(4, 1, 10, 10)  # rows, cols, vgap, hgap
        
        # Select variables from checkbox
        self.selectVariablesPressed = False
        checkbox_btn = wx.Button(panel, label='Select desired variables')
        checkbox_btn.Bind(wx.EVT_BUTTON,lambda evt, ukb=ukb: self.SelectVariablesFrameButton(evt, self.ukb_object))#for explanation see: https://wiki.wxpython.org/Passing%20Arguments%20to%20Callbacks
        my_sizer.Add(checkbox_btn, 0, wx.EXPAND, 0)
        
        
        # Select illnesses from checkbox
        self.selectIllnessPressed = False
        select_illness_btn = wx.Button(panel, label='Select illnesses')
        select_illness_btn.Bind(wx.EVT_BUTTON,lambda evt, ukb=ukb: self.SelectIllnessFrameButton(evt, self.ukb_object))
        my_sizer.Add(select_illness_btn, 0, wx.EXPAND, 0)
        
        
        # View selections
        view_btn = wx.Button(panel, label='View Selections')
        view_btn.Bind(wx.EVT_BUTTON, self.selectionsGetter) 
        my_sizer.Add(view_btn, 0, wx.EXPAND, 0) 
        
    
        # Output CSV 
        output_btn = wx.Button(panel, label='Output CSV')
        output_btn.Bind(wx.EVT_BUTTON,lambda evt, ukb=ukb: self.OutputCsvFrameButton(evt, self.ukb_object)) 
        my_sizer.Add(output_btn, 0, wx.EXPAND, 0) 

        panel.SetSizer(my_sizer)        
        self.Show()
        

    
        

    # Loading SelectVariablesFrame
    def SelectVariablesFrameButton(self, event, ukb):        
        if self.selectVariablesPressed == False:
            self.SelectVariablesFrame = SelectVariablesFrame(self, ukb)
            self.selectVariablesPressed = True
        else:     
            self.SelectVariablesFrame.Show()
        
        
        return
    
    
    #L oading SelectIllnessFrame
    def SelectIllnessFrameButton(self, event, ukb):
        if self.selectIllnessPressed == False:
            self.selectIllnessFrame = SelectIllnessFrame(self, ukb)
            self.selectIllnessPressed = True
        else:     
            self.selectIllnessFrame.Show()
        
        
        return
    
    # Function to gather all options selected
    def selectionsGetter(self, event):       
        print(self.ukb_object.SELECTIONS)
        return 
    
    
    #Function to set options selected (options should be submitted as a key-value pair)
    #e.g {'include_illness': [x,y,z]}
    def selectionsSetter(self, arg1=None):
        
        if self.ukb_object.SELECTIONS is not None:
            self.ukb_object.SELECTIONS.update(arg1)
          
        else:               
            self.ukb_object.SELECTIONS = arg1
        return 
    
    
        
        
        
    
    def OutputCsvFrameButton(self, event, ukb):
        
        OutputCsvFrame(self, ukb)
        
        return
    
        
        # with wx.FileDialog(self, "Save output as csv", wildcard="csv files (*.csv)|*.csv",
        #                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
    
        #     if fileDialog.ShowModal() == wx.ID_CANCEL:
        #         return     # the user changed their mind
    
        #     # Getting filepath
        #     pathname = fileDialog.GetPath()
            
        #     # Getting selections 
        #     s = self.ukb_object.SELECTIONS 
            
        #     if s == None:
        #         print('No selections were made!')
            
        #     else:
            
        #         # Adding fields to dataframe
        #         if 'include_variables' in s and len(s['include_variables']) > 0:
        #             df = ukbiobank.utils.addFields(ukbio=self.ukb_object, fields=s['include_variables'])
                
        #         # Filtering dataframe according to 'include_illness' selections
        #         if 'include_illnesses' in s and len(s['include_illnesses_coded']) > 0:                
        #             df = ukbiobank.filtering.filterByField(ukbio=self.ukb_object, df=df, fields_to_include=s['include_illnesses_coded'])
                
                
        #         try:
        #             # Saving
        #             df.to_csv(pathname)
    
        #         except IOError:
        #             wx.LogError("Cannot save current data in file '%s'." % pathname)
                
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        