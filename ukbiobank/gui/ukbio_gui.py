# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:33:29 2020

@author: Joe

UKBiobank data loading utilities
"""
import wx
from ukbiobank.gui.load_frame import LoadFrame




#Open GUI
def open():    
    app = wx.App()
    LoadFrame()
    app.MainLoop()
    return

