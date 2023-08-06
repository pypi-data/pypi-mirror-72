# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tcp_scan_dialog.ui',
# licensing of 'tcp_scan_dialog.ui' applies.
#
# Created: Mon Apr 20 16:45:34 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_TCPScanDialog(object):
    def setupUi(self, TCPScanDialog):
        TCPScanDialog.setObjectName("TCPScanDialog")
        TCPScanDialog.resize(915, 445)
        self.verticalLayout = QtWidgets.QVBoxLayout(TCPScanDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(TCPScanDialog)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.automaticRescan = QtWidgets.QCheckBox(TCPScanDialog)
        self.automaticRescan.setObjectName("automaticRescan")
        self.verticalLayout.addWidget(self.automaticRescan)
        self.buttonBox = QtWidgets.QDialogButtonBox(TCPScanDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TCPScanDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), TCPScanDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), TCPScanDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TCPScanDialog)

    def retranslateUi(self, TCPScanDialog):
        TCPScanDialog.setWindowTitle(QtWidgets.QApplication.translate("TCPScanDialog", "TCP Devices", None, -1))
        self.tableWidget.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("TCPScanDialog", "Serial", None, -1))
        self.tableWidget.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("TCPScanDialog", "Tag 1", None, -1))
        self.tableWidget.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("TCPScanDialog", "Tag 2", None, -1))
        self.tableWidget.horizontalHeaderItem(3).setText(QtWidgets.QApplication.translate("TCPScanDialog", "Board Info", None, -1))
        self.tableWidget.horizontalHeaderItem(4).setText(QtWidgets.QApplication.translate("TCPScanDialog", "Build Info", None, -1))
        self.tableWidget.horizontalHeaderItem(5).setText(QtWidgets.QApplication.translate("TCPScanDialog", "Build Date", None, -1))
        self.tableWidget.horizontalHeaderItem(6).setText(QtWidgets.QApplication.translate("TCPScanDialog", "Bootloader", None, -1))
        self.tableWidget.horizontalHeaderItem(7).setText(QtWidgets.QApplication.translate("TCPScanDialog", "Available", None, -1))
        self.automaticRescan.setText(QtWidgets.QApplication.translate("TCPScanDialog", "Automatic Rescan", None, -1))

