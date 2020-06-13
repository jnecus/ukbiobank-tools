# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:33:29 2020

@author: Joe

UKBiobank data loading utilities
"""
import wx
#import ukbiobank 
#import ukbiobank.gui
from ukbiobank.gui import LoadFrame




#Open GUI
def open():    
    app = wx.App()
    frame = LoadFrame()
    app.MainLoop()
    return










#OLD code whereby all classes in same file below (incase new method breaks . . )

# #Load path to ukbiobank csv file, initialise ukbiobank.ukbio() object..
# class LoadFrame(wx.Frame):    
#     def __init__(self):
#         super().__init__(parent=None, title='UKBiobank-tools')
#         panel = wx.Panel(self)        
        
#         my_sizer = wx.BoxSizer(wx.VERTICAL)        
        
#         self.my_csv =  wx.FilePickerCtrl(panel)
#         my_sizer.Add(self.my_csv, 0, wx.EXPAND, 5)  
        
#         #self.my_csv = wx.FilePickerCtrl(panel)
        
        
#         my_btn = wx.Button(panel,label='Load CSV')
#         my_btn.Bind(wx.EVT_BUTTON, self.on_press)
#         my_sizer.Add(my_btn, 0, wx.EXPAND, 5)        
#         panel.SetSizer(my_sizer)        
        
        
#         self.Show()
        
#     #on_press: load ukb object with csv path
#     def on_press(self, event):
#         value = self.my_csv.GetPath()
#         if not value:
#             print("You didn't enter anything!")
#         else:
#             print(f'You typed: "{value}"')
#             #Loading menu...
#             self.Close()
#             ukb=ukbiobank.ukbio(ukb_csv=value)
#             MenuFrame(self, ukb)


# #MenuFrame: Panel containing all options
# class MenuFrame(wx.Frame, ukbiobank.ukbio):
    
#     def __init__(self, frame, ukb):
#         super().__init__(parent=None,title='UKBiobank-tools menu', size=wx.DefaultSize)
#         self.ukb_object = ukb
        
        
#         panel = wx.Panel(self)        
#         #my_sizer = wx.BoxSizer(wx.VERTICAL)        
#         my_sizer = wx.GridSizer(3, 1, 10, 10)  # rows, cols, vgap, hgap
        
#         #Select variables from checkbox
#         checkbox_btn = wx.Button(panel, label='Select desired variables')
#         checkbox_btn.Bind(wx.EVT_BUTTON,lambda evt, ukb=ukb: self.checkboxFrameButton(evt, self.ukb_object))#for explanation see: https://wiki.wxpython.org/Passing%20Arguments%20to%20Callbacks
#         my_sizer.Add(checkbox_btn, 0, wx.EXPAND, 0)
        
        
#         #Print selections
#         view_btn = wx.Button(panel, label='View Selections')
#         view_btn.Bind(wx.EVT_BUTTON, self.selectionsGetter) # to do : add data here as functionality increases
#         my_sizer.Add(view_btn, 0, wx.EXPAND, 0) 
        
    
#         #Output CSV 
#         output_btn = wx.Button(panel, label='Output CSV')
#         output_btn.Bind(wx.EVT_BUTTON, self.outputCSV) # to do : add data here as functionality increases
#         my_sizer.Add(output_btn, 0, wx.EXPAND, 0) 

#         #my_sizer.SetSizeHints(self)  
#         panel.SetSizer(my_sizer)        
#         self.Show()
        

#     #Outputting CSV with given selections
#     def outputCSV(self, event):
        
#         # Adding desired fields
#         df = ukbiobank.utils.addFields(ukbio=self.ukb_object, df=None, fields=list(self.ukb_object.SELECTIONS))
        
#         # Saving to desktop.. 
#         df.to_csv('C:/Users/Joe/Desktop/output_csv_temp.csv')
        
        

#     #Loading CheckBoxFrame
#     def checkboxFrameButton(self, event, ukb):
#         CheckBoxFrame(self, ukb)
#         return
    
    
#     #Function to gather all options selected
#     def selectionsGetter(self, event):       
#         #Add selections from other frame
#         print(self.ukb_object.SELECTIONS)
#         return 
    
    
#     #Function to set options selected
#     def selectionsSetter(self, arg1=None):       
#         #Add selections from other frame
#         self.ukb_object.SELECTIONS = arg1
#         return 
    
    
        

    
# class CheckBoxFrame(wx.Frame, ukbiobank.ukbio):
        
#     def __init__(self, parent, ukb):
#         super().__init__(parent=None, title='UKBiobank-tools checkbox')
#         panel = wx.Panel(self)        
        
#         my_sizer = wx.BoxSizer(wx.VERTICAL)      
        
        
#         #Variables checkbox
#         self.checkbox = wx.CheckListBox(panel,choices=ukbiobank.utils.getFieldnames(ukb))
        
#         #Description
#         desc=wx.TextCtrl(panel,value='Select desired variables',style=wx.TE_READONLY)
        
#         # #Submit button
#         submit=wx.Button(panel,label='Submit')
#         submit.Bind(wx.EVT_BUTTON, lambda evt, ukb=ukb: self.submit(evt, parent, ukb))
        
        
#         my_sizer.Add(desc,1, wx.CENTER | wx.EXPAND)
#         my_sizer.Add(self.checkbox,1, wx.EXPAND)       
#         my_sizer.Add(submit,1,wx.EXPAND)
         
#         panel.SetSizer(my_sizer)           
#         self.Show()


#     #set selections
#     def submit(self, event, parent, ukb):
        
#         selections = self.checkbox.GetCheckedStrings()
        
#         #Setting selections, passing through parent MenuFrame
#         MenuFrame.selectionsSetter(parent, arg1 = selections)

        
#         self.Close()
#         return 