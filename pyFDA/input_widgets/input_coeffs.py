# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:57:30 2013

@author: Christian Muenker

Tab-Widget for displaying and modifying filter coefficients
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import sys, os
from PyQt4 import QtGui
#import scipy.io
import numpy as np

# import filterbroker from one level above if this file is run as __main__
# for test purposes
if __name__ == "__main__": 
    __cwd__ = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(__cwd__ + '/..')

import filterbroker as fb # importing filterbroker initializes all its globals

# TODO: saveCoeffs() is triggered multiple times when table entries are changed
#       not by user but by e.g. a changed filter design
class InputCoeffs(QtGui.QWidget):
    """
    Create the window for entering exporting / importing and saving / loading data
    """
    def __init__(self, DEBUG = True):
        self.DEBUG = DEBUG
        super(InputCoeffs, self).__init__()

        self.initUI()
        self.showCoeffs()
        
    def initUI(self): 
        """
        Intitialize the widget, consisting of:
        - 
        - 
        """
        # widget / subwindow for coefficient display / entry

        self.chkCoeffList =  QtGui.QCheckBox()
        self.chkCoeffList.setChecked(True)
        self.chkCoeffList.setToolTip("Show filter coefficients as an editable list.")
        self.lblCoeffList = QtGui.QLabel()
        self.lblCoeffList.setText("Show Coefficients")
       
        self.tblCoeff = QtGui.QTableWidget()
        self.tblCoeff.setEditTriggers(QtGui.QTableWidget.AllEditTriggers)
        self.tblCoeff.setAlternatingRowColors(True)
#        self.tblCoeff.itemEntered.connect(self.saveCoeffs) # nothing happens
#        self.tblCoeff.itemActivated.connect(self.saveCoeffs) # nothing happens
#        self.tblCoeff.itemChanged.connect(self.saveCoeffs) # works but fires multiple times
        self.tblCoeff.selectionModel().currentChanged.connect(self.saveCoeffs) 
        self.tblCoeff.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                          QtGui.QSizePolicy.MinimumExpanding)

        self.butAddRow = QtGui.QPushButton()
        self.butAddRow.setToolTip("Add row to coefficient table.\nSelect n existing rows to append n new rows.")
        self.butAddRow.setText("Add")
        
        self.butDelRow = QtGui.QPushButton()
        self.butDelRow.setToolTip("Delete selected row(s) from coefficient table.")
        self.butDelRow.setText("Delete")
        
        self.butUpdate = QtGui.QPushButton()
        self.butUpdate.setToolTip("Update filter info and plots.")
        self.butUpdate.setText("Update")
 
        # ============== UI Layout =====================================
        self.layHChkBoxes = QtGui.QHBoxLayout()
        self.layHChkBoxes.addWidget(self.chkCoeffList)
        self.layHChkBoxes.addWidget(self.lblCoeffList)
        self.layHChkBoxes.addStretch(1)        
#        self.layHChkBoxes.addStretch(10)
        
        self.layHButtonsCoeffs = QtGui.QHBoxLayout()
        self.layHButtonsCoeffs.addWidget(self.butAddRow)
        self.layHButtonsCoeffs.addWidget(self.butDelRow)
        self.layHButtonsCoeffs.addWidget(self.butUpdate)
        self.layHButtonsCoeffs.addStretch()


        layVMain = QtGui.QVBoxLayout()
        layVMain.addLayout(self.layHChkBoxes)
        layVMain.addWidget(self.tblCoeff)
        layVMain.addLayout(self.layHButtonsCoeffs)
#        layVMain.addStretch(1)
        self.setLayout(layVMain)
        
        # ============== Signals & Slots ================================
        self.chkCoeffList.clicked.connect(self.showCoeffs)        
        self.butUpdate.clicked.connect(self.showCoeffs)        
        self.butDelRow.clicked.connect(self.deleteRows) 
        self.butAddRow.clicked.connect(self.addRows) 

        
    def saveCoeffs(self):
        """
        Read out table and save the values to the filter coeff dict
        """
        coeffs = []
        num_rows, num_cols = self.tblCoeff.rowCount(),\
                                        self.tblCoeff.columnCount()
        if self.DEBUG: print(num_rows, num_cols)
        if num_cols > 1: # IIR
            for col in range(num_cols):
                rows = []
                for row in range(num_rows):
                    item = self.tblCoeff.item(row, col)
                    rows.append(float(item.text()) if item else 0.)
                coeffs.append(rows)
        else: # FIR
            col = 0
            for row in range(num_rows):
                item = self.tblCoeff.item(row, col)
                coeffs.append(float(item.text()) if item else 0.)            
        
        fb.fil[0]['coeffs'] = coeffs
        if self.DEBUG: print ("coeffs updated!")
        
    def showCoeffs(self):
        """
        Read out table and save the values to the filter coeff dict
        """            
        coeffs = fb.fil[0]["coeffs"]
        self.tblCoeff.setVisible(self.chkCoeffList.isChecked())

        self.tblCoeff.clear()
        self.tblCoeff.setRowCount(max(np.shape(coeffs)))


        if self.DEBUG:
            print("=====================\nInputInfo.showCoeffs")
            print("Coeffs:\n",coeffs)
            print ("shape", np.shape(coeffs))
            print ("len", len(coeffs))
            print("ndim", np.ndim(coeffs))
            
#        if np.ndim(fb.fil[0]['coeffs']) == 1: # FIR
#            self.bb = fb.fil[0]['coeffs']
#            self.aa = 1.
#        else: # IIR
#            self.bb = fb.fil[0]['coeffs'][0]
#            self.aa = fb.fil[0]['coeffs'][1]

        if np.ndim(coeffs) == 1: # FIR
            self.tblCoeff.setColumnCount(1)
            self.tblCoeff.setHorizontalHeaderLabels(["b"])
            for i in range(len(coeffs)):
                if self.DEBUG: print(i, coeffs[i])
                item = QtGui.QTableWidgetItem(str(coeffs[i]))
                self.tblCoeff.setItem(i,0,item)
        else: # IIR
            self.tblCoeff.setColumnCount(2)
            self.tblCoeff.setHorizontalHeaderLabels(["b", "a"])
            for i in range(np.shape(coeffs)[1]):
#                print(i, fb.fil[0]["coeffs"][0][i])
#                item = QtGui.QTableWidgetItem(coeffs[0][i])
#                bCoeffs.append(str(coeffs[0][i]))
#                aCoeffs.append(str(coeffs[1][i]))
                self.tblCoeff.setItem(i,0,QtGui.QTableWidgetItem(str(coeffs[0][i])))
                self.tblCoeff.setItem(i,1,QtGui.QTableWidgetItem(str(coeffs[1][i])))

        self.tblCoeff.resizeColumnsToContents()
        
    def deleteRows(self):
        # returns index to rows where _all_ columns are selected
        rows = self.tblCoeff.selectionModel().selectedRows() 
        rows = rows[::-1] # revert order of rows before running the loop
        print (rows)
        for r in rows:
            self.tblCoeff.removeRow(r.row())
        
        self.saveCoeffs()
        
    def addRows(self):
        nrows = len(self.tblCoeff.selectionModel().selectedRows())
        if nrows == 0: 
            nrows = 1 # add at least one row
        ncols = self.tblCoeff.columnCount()
        

        if ncols == 1: # FIR
            fb.fil[0]["coeffs"].extend(list(np.zeros(nrows)))
        else:
            z = np.zeros((ncols, nrows))
            fb.fil[0]["coeffs"] = np.hstack((fb.fil[0]["coeffs"],z))
            
        self.showCoeffs() 

#------------------------------------------------------------------------------
   
if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    form = InputCoeffs()
    form.show()
   
    app.exec_()