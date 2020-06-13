# -*- coding: utf-8 -*-
"""
Quick testing gui edits . . .
"""



import ukbiobank.gui as gui
import wx
import pickle
# ukb=ukbiobank.ukbio(ukb_csv='C:/Users/Joe/Google Drive/Post Doc Dementia/UK Biobank/March2020_data_refreshes/ukb41831/all_ScanRescanSubjects_UKB_format.csv')

x = open('C:/Users/Joe/Google Drive/Post Doc Dementia/UK Biobank/March2020_data_refreshes/ukb_pickle', 'rb')

#loading pickled ukbio object
ukb = pickle.load(x)
x.close()

app = wx.App(0)
app.MainLoop()



#Testing MenuFrame
gui.MenuFrame(wx.Frame,ukb)

#.SelectIllnessFrame(wx.Frame,ukb)

#Testing loadframe
#gui.LoadFrame()


#to kill
#app.Destroy()

