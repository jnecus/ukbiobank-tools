# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:33:29 2020

@author: Joe

UKBiobank data loading utilities
"""
import wx
import ukbiobank
import ukbiobank.filtering 
from ukbiobank.gui.select_variables import SelectVariablesFrame
from ukbiobank.gui.select_illness import SelectIllnessFrame
from ukbiobank.gui.output_csv import OutputCsvFrame

class M_AM_B(wx.Frame, ukbiobank.ukbio.ukbio): pass

#MenuFrame (frame containing all options)
class MenuFrame(wx.Frame, ukbiobank.ukbio.ukbio):
    __metaclass__ = M_AM_B
    
    def __init__(self, frame, ukb):
        super().__init__(parent=None,title='UKBiobank-tools menu', size=wx.DefaultSize)
        self.ukb_object = ukb
        self.ukb_object.SELECTIONS = None #initialising variable/filter selections to None 
        
        # Close all chidren on MenuFrame close.
        self.Bind( wx.EVT_CLOSE, self.ParentFrameOnClose )
        
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
        
    
    
    def ParentFrameOnClose(self, event):
            self.DestroyChildren()  ## Destroy the children first
            self.Destroy()    ## Destroy the parent then.

    # Loading SelectVariablesFrame
    def SelectVariablesFrameButton(self, event, ukb):        
        if self.selectVariablesPressed == False:
            self.SelectVariablesFrame = SelectVariablesFrame(self, ukb)
            self.selectVariablesPressed = True
        else:     
            self.SelectVariablesFrame.Show()
        
        
        return
    
    
    # Loading SelectIllnessFrame
    def SelectIllnessFrameButton(self, event, ukb):
        if self.selectIllnessPressed == False:
            self.selectIllnessFrame = SelectIllnessFrame(self, ukb)
            self.selectIllnessPressed = True
        else:     
            self.selectIllnessFrame.Show()
        
        
        return
    
    # Function to gather all options selected
    def selectionsGetter(self, event):
        wx.MessageDialog(self, message="This function is not yet available").ShowModal()
        #print(self.ukb_object.SELECTIONS)
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
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        