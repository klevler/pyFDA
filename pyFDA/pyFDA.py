# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:57:30 2013

@author: Julia Beike, Christian Muenker

Main file for the pyFDA app, initializes UI
"""

import sys
from PyQt4 import QtGui
#from PyQt4.QtCore import SIGNAL
import scipy.io
import numpy as np

import databroker as db # importing databroker initializes all its globals
from FilterFileReader import FilterFileReader
from inputWidgets import ChooseParams
#from filterDesign import cheby1 #, design_selector
from plotWidgets import plotAll

DEBUG = True

class pyFDA(QtGui.QWidget):
    PLT_SAME_WINDOW =  True
    """
    Create the main window for entering the filter specifications
    """
    def __init__(self):
        super(pyFDA, self).__init__()
        # read directory with filterDesigns and construct filter Tree from it
        self.ffr = FilterFileReader('Init.txt', 'filterDesign', commentCh = '#', DEBUG = True) # 
        
#        db.gD['zpk'] = ([1], 0, 0.5)
        # initialize filter coefficients b, a :
#        db.gD['coeffs'] = [db.gD['zpk'][2]*np.poly(db.gD['zpk'][0]), 
#                                       np.poly(db.gD['zpk'][1])]
        #self.em = QtGui.QFontMetricsF(QtGui.QLineEdit.font()).width('m')
       
#        self.myFilter = cheby1.cheby1()
        self.initUI()     
        
    def initUI(self): 
        """
        Intitialize the main GUI, consisting of:
        - Subwindow for parameter selection [-> ChooseParams.ChooseParams()]
        - Filter Design button [-> self.startDesignFilt()] 
        - Plot Window [-> plotAll.plotAll()]
        """
        # widget / subwindow for parameter selection
        self.widgetChooseParams = ChooseParams.ChooseParams() 
        self.widgetChooseParams.setMaximumWidth(250)
        self.butDesignFilt = QtGui.QPushButton("DESIGN FILTER", self)
        self.butExportML = QtGui.QPushButton("Export -> ML", self)
        self.butExportCSV = QtGui.QPushButton("Export -> CSV", self)
        self.pltAll = plotAll.plotAll() # instantiate tabbed plot widgets        
        # ============== UI Layout =====================================
        self.grLayout = QtGui.QGridLayout()
        self.grLayout.addWidget(self.widgetChooseParams,0,0) # parameter select widget
        self.grLayout.addWidget(self.butDesignFilt,1,0) # filter design button
        self.grLayout.addWidget(self.butExportML,2,0) # filter export button
        self.grLayout.addWidget(self.butExportCSV,3,0) # filter export button
       #print(self.grLayout.columnMinimumWidth(0))# .setSizePolicy(QtGui.QSizePolicy.Expanding, 
#                                   QtGui.QSizePolicy.Expanding)
#        self.grLayout.updateGeometry()

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(self.grLayout)
#        hbox.addWidget(self.pltAll)

        if self.PLT_SAME_WINDOW:
            # Plot window docked in same window:
#            self.layout.addWidget(self.pltAll,0,1) 
            hbox.addWidget(self.pltAll) 
        self.setLayout(hbox)
#        self.setLayout(self.layout)
        # ============== Signals & Slots ================================

        self.butDesignFilt.clicked.connect(self.startDesignFilt)
        self.butExportML.clicked.connect(self.exportML)
        self.butExportCSV.clicked.connect(self.exportCSV)        

    def startDesignFilt(self):
        """
        Design Filter
        """
        params = self.widgetChooseParams.get() 
        if DEBUG: print("db.gD['curFilter']['dm']", db.gD['curFilter']['dm'])
        self.myFilter = self.ffr.objectWizzard(db.gD['curFilter']['dm'])
        # Now design the filter by passing params to the filter instance ...
        myFilt = getattr(self.myFilter, db.gD['curFilter']['rt'])(params)
        # ... and reading back filter coefficients and (zeroes, poles, k):
        db.gD['zpk'] = self.myFilter.zpk # read (zeroes, poles, k)
        print('ndim coeffs:', np.ndim(self.myFilter.coeffs))
        if np.ndim(self.myFilter.coeffs) == 1: # FIR-Filter - only b coeffs
            db.gD['coeffs'] = (self.myFilter.coeffs, [1]) # and filter coefficients
            print('FIR!')
        else:                                 # IIR-Filter - [b, a]
            db.gD['coeffs'] = self.myFilter.coeffs # and filter coefficients
            print('IIR!')
        if DEBUG:
            print("--- pyFDA.py : startDesignFilter ---")
            print("zpk:" , db.gD['zpk'])
            print('ndim gD:', np.ndim(db.gD['coeffs']))
            print("b,a = ", db.gD['coeffs'])

        if self.PLT_SAME_WINDOW:       
            self.pltAll.update()
        else:
            # Separate window for plots:
            self.pltAll.update()
            self.pltAll.show()

        
    def exportML(self):
        """
        Export filter coefficients to a file that can be imported into 
        Matlab workspace
        """
        
        scipy.io.savemat('d:/Daten/filt_coeffs.mat', 
                         mdict={'filt_coeffs': db.gD['coeffs']})
        print("exportML: Matlab workspace exported!")
        
    def exportCSV(self):
        """
        Export filter coefficients to a CSV-file 
        """
        
        np.savetxt('d:/Daten/filt_coeffs.csv', db.gD['coeffs'])
        print("exportCSV: CSV - File exported!")
#------------------------------------------------------------------------------
   
if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    form = pyFDA()
    form.show()
   
    app.exec_()