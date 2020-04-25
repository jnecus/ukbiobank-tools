# -*- coding: utf-8 -*-
"""
Quick testing gui edits . . .
"""



import ukbiobank.gui as gui
import wx
import ukbiobank

ukb=ukbiobank.ukbio(ukb_csv='C:/Users/Joe/Google Drive/Post Doc Dementia/UK Biobank/March2020_data_refreshes/ukb41344/ukb41344.csv')

app = wx.App(0)
app.MainLoop()



#Testing MenuFrame
gui.MenuFrame(wx.Frame,ukb)


#app.Destroy()
