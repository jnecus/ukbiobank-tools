# -*- coding: utf-8 -*-

import wx
import ukbiobank 


class M_AM_B(wx.Frame, ukbiobank.ukbio.ukbio): pass

class SelectVariablesFrame(wx.Frame, ukbiobank.ukbio.ukbio):
    __metaclass__ = M_AM_B
        
    def __init__(self, parent, ukb):
        super().__init__(parent=parent, title='UKBiobank-tools checkbox')
        panel = wx.Panel(self)        
        
        my_sizer = wx.BoxSizer(wx.VERTICAL)      
        
        
        #Variables checkbox
        self.checkbox = wx.CheckListBox(panel,choices=ukbiobank.utils.utils.getFieldnames(ukb))
        
        #Description
        desc=wx.TextCtrl(panel,value='Select desired variables',style=wx.TE_READONLY)
        
        # #Submit button
        submit=wx.Button(panel,label='Submit')
        submit.Bind(wx.EVT_BUTTON, lambda evt, ukb=ukb: self.submit(evt, parent, ukb))
        
        
        my_sizer.Add(desc,1, wx.CENTER | wx.EXPAND)
        my_sizer.Add(self.checkbox,1, wx.EXPAND)       
        my_sizer.Add(submit,1,wx.EXPAND)
         
        panel.SetSizer(my_sizer)           
        self.Show()


    #set selections
    def submit(self, event, parent, ukb):
        
        selections = {}
        selections['include_variables'] = list(self.checkbox.GetCheckedStrings())
                
        #Setting selections, passing through parent MenuFrame
        parent.selectionsSetter(arg1 = selections)

        
        self.Hide()
        return 





















