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
from .select_variables import SelectVariablesFrame
from .select_illness import SelectIllnessFrame

#MenuFrame: Panel containing all options
class MenuFrame(wx.Frame, ukbiobank.ukbio):
    
    def __init__(self, frame, ukb):
        super().__init__(parent=None,title='UKBiobank-tools menu', size=wx.DefaultSize)
        self.ukb_object = ukb
        self.ukb_object.SELECTIONS = None #initialising variable/filter selections to None 
        
        
        panel = wx.Panel(self)        
        #my_sizer = wx.BoxSizer(wx.VERTICAL)        
        my_sizer = wx.GridSizer(4, 1, 10, 10)  # rows, cols, vgap, hgap
        
        #Select variables from checkbox
        self.selectVariablesPressed = False
        checkbox_btn = wx.Button(panel, label='Select desired variables')
        checkbox_btn.Bind(wx.EVT_BUTTON,lambda evt, ukb=ukb: self.SelectVariablesFrameButton(evt, self.ukb_object))#for explanation see: https://wiki.wxpython.org/Passing%20Arguments%20to%20Callbacks
        my_sizer.Add(checkbox_btn, 0, wx.EXPAND, 0)
        
        
        
        
        
         #Select illnesses from checkbox
        self.selectIllnessPressed = False
        select_illness_btn = wx.Button(panel, label='Select illnesses')
        select_illness_btn.Bind(wx.EVT_BUTTON,lambda evt, ukb=ukb: self.SelectIllnessFrameButton(evt, self.ukb_object))
        my_sizer.Add(select_illness_btn, 0, wx.EXPAND, 0)
        
        
        
        
        #Print selections
        view_btn = wx.Button(panel, label='View Selections')
        view_btn.Bind(wx.EVT_BUTTON, self.selectionsGetter) # to do : add data here as functionality increases
        my_sizer.Add(view_btn, 0, wx.EXPAND, 0) 
        
    
        #Output CSV 
        output_btn = wx.Button(panel, label='Output CSV')
        output_btn.Bind(wx.EVT_BUTTON, self.outputCSV) # to do : add data here as functionality increases
        my_sizer.Add(output_btn, 0, wx.EXPAND, 0) 

        #my_sizer.SetSizeHints(self)  
        panel.SetSizer(my_sizer)        
        self.Show()
        

    #Outputting CSV with given selections
    def outputCSV(self, event):
        
        # Adding desired fields
        df = ukbiobank.utils.addFields(ukbio=self.ukb_object, df=None, fields=list(self.ukb_object.SELECTIONS))
        
        # Saving to desktop.. 
        df.to_csv('C:/Users/Joe/Desktop/output_csv_temp.csv')
        
        

    #Loading SelectVariablesFrame
    def SelectVariablesFrameButton(self, event, ukb):        
        if self.selectVariablesPressed == False:
            self.SelectVariablesFrame = SelectVariablesFrame(self, ukb)
            self.selectVariablesPressed = True
        else:     
            self.SelectVariablesFrame.Show()
        
        
        return
    
    
    #Loading SelectIllnessFrameButton
    def SelectIllnessFrameButton(self, event, ukb):
        if self.selectIllnessPressed == False:
            self.selectIllnessFrame = SelectIllnessFrame(self, ukb)
            self.selectIllnessPressed = True
        else:     
            self.selectIllnessFrame.Show()
        
        
        return
    
    #Function to gather all options selected
    def selectionsGetter(self, event):       
        #Add selections from other frame
        print(self.ukb_object.SELECTIONS)
        return 
    
    
    #Function to set options selected (options should be submitted as a key-value pair)
    #e.g {'include_illness': [X,y,z]}
    def selectionsSetter(self, arg1=None):
        
        if self.ukb_object.SELECTIONS is not None:
            self.ukb_object.SELECTIONS.update(arg1)
          
        else:               
            self.ukb_object.SELECTIONS = arg1
        return 
    
    
