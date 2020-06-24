# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:33:29 2020

@author: Joe

UKBiobank data loading utilities
"""
import wx
import ukbiobank 
from wx.lib.agw import pybusyinfo
from ukbiobank.gui.menu_frame import MenuFrame

#Load path to ukbiobank csv file, initialise ukbiobank.ukbio.ukbio() object..
class LoadFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='UKBiobank-tools')
        panel = wx.Panel(self)        
        
        my_sizer = wx.BoxSizer(wx.VERTICAL)        
        
        self.my_csv =  wx.FilePickerCtrl(panel)
        my_sizer.Add(self.my_csv, 0, wx.EXPAND, 5)  
                
        
        my_btn = wx.Button(panel,label='Load CSV')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.EXPAND, 5)        
        panel.SetSizer(my_sizer)        
        
        
        self.Show()
        
    #on_press: load ukb object with csv path
    def on_press(self, event):
        value = self.my_csv.GetPath()
        if not value:
            wx.MessageDialog(self, message="You didn't enter anything!").ShowModal()
        else:           
            #Loading menu...
            self.Close()
            busy =  pybusyinfo.PyBusyInfo(message='Loading csv, please wait...')
            ukb=ukbiobank.ukbio.ukbio(ukb_csv=value)
            busy.Show(show=False)
            MenuFrame(self, ukb)
       






