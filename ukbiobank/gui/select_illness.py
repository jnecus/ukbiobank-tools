# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 17:45:15 2020

@author: Joe
"""


import wx
import ukbiobank 

class M_AM_B(wx.Frame, ukbiobank.ukbio.ukbio): pass

class SelectIllnessFrame(wx.Frame, ukbiobank.ukbio.ukbio):
    __metaclass__ = M_AM_B
    def __init__(self, parent, ukb):
        super().__init__(parent=parent, title='Select Illness', size=wx.DefaultSize)

        # Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)
        
        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 1, wx.EXPAND)

        # Create the tab windows
        self.tab1 = Tab(nb, ukb, diagnosisType='self')
        self.tab2 = Tab(nb, ukb, diagnosisType='ICD9')
        self.tab3 = Tab(nb, ukb, diagnosisType='ICD10')


        # Add the windows to tabs and name them.
        nb.AddPage(self.tab1, "Self-Reported Non-Cancer Illnesses")
        nb.AddPage(self.tab2, "ICD 9 Main Diagnosis")
        nb.AddPage(self.tab3, "ICD 10 Main Diagnosis")
        
        
        #Submit button
        submit=wx.Button(p, label='Submit')
        submit.Bind(wx.EVT_BUTTON, lambda evt, ukb=ukb: self.submit(evt, parent, ukb))
        
        
        sizer.Add(submit,1,wx.EXPAND)
        p.SetSizer(sizer)
        
        
        self.Show()
        
        
        
    #set selections
    def submit(self, event, parent, ukb):
        
        self_reported = list(self.tab1.getSelections())
        icd9 = list(self.tab2.getSelections())
        icd10 = list(self.tab3.getSelections())
    
        selections = {}
        
        # Selections are saved as a key value pair whereby:
            #key:  ukbiobank field ID (correspinding to self-report/icd9/icd10 column)
            #values: selected illnessess
            
        #TODO: Include 'Secondary diagnoses', cancer illnesses, cause of death etc etc...
        selections['include_illnesses'] = {'Non-cancer illness code, self-reported': self_reported,
                                           'Diagnoses - main ICD9': icd9,
                                           'Diagnoses - ICD10': icd10}
        
                                       
        selections['include_illnesses_coded'] = {20002: ukb.nonCancerIllnessCoding['coding'][ukb.nonCancerIllnessCoding['meaning'].isin(self_reported)].tolist(),
                                           41203: ukb.icd9Coding['coding'][ukb.icd9Coding['meaning'].isin(icd9)].tolist(),
                                           41270: ukb.icd10Coding['coding'][ukb.icd10Coding['meaning'].isin(icd10)].tolist()}
                                           
                                          
                                           
        #Setting selections, passing through parent MenuFrame
        parent.selectionsSetter(arg1 = selections)

        self.Hide()
        
        return 
            
        

# Define the tab content as classes (in this case each tab will have the same structure so base 'Tab' class will suffice)
class Tab(wx.Panel, ukbiobank.ukbio.ukbio):
    def __init__(self, parent, ukb, diagnosisType):
        wx.Panel.__init__(self, parent)
        #wx.StaticText(self, -1, "This is the first tab", (20,20))
        
        p = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)      
        
        if diagnosisType=='self':
            #Getting list of illnesses
            df = ukb.nonCancerIllnessCoding
            illness_list = (df.loc[ (df['coding'] !=-1)  & (df['coding'] !=99999),'meaning']).tolist()
            illness_list.sort()
        
        elif diagnosisType=='ICD9':
            illness_list = ukb.icd9Coding.meaning.tolist()
            
        elif diagnosisType=='ICD10':
            illness_list = ukb.icd10Coding.meaning.tolist()
        
        # Variables checkbox
        self.checkbox = wx.CheckListBox(self, choices=illness_list)
        

        my_sizer.Add(self.checkbox,1, wx.EXPAND)    
        p.SetSizer(my_sizer)       
        
    def getSelections(self):
        return self.checkbox.GetCheckedStrings()
    
