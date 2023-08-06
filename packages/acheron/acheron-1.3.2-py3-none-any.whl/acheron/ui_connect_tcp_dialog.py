# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_tcp_dialog.ui',
# licensing of 'connect_tcp_dialog.ui' applies.
#
# Created: Mon Apr 20 10:50:17 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ConnectTCPDialog(object):
    def setupUi(self, ConnectTCPDialog):
        ConnectTCPDialog.setObjectName("ConnectTCPDialog")
        ConnectTCPDialog.resize(341, 119)
        self.formLayout = QtWidgets.QFormLayout(ConnectTCPDialog)
        self.formLayout.setObjectName("formLayout")
        self.hostnameLabel = QtWidgets.QLabel(ConnectTCPDialog)
        self.hostnameLabel.setObjectName("hostnameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.hostnameLabel)
        self.hostname = QtWidgets.QLineEdit(ConnectTCPDialog)
        self.hostname.setMinimumSize(QtCore.QSize(200, 0))
        self.hostname.setObjectName("hostname")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.hostname)
        self.portLabel = QtWidgets.QLabel(ConnectTCPDialog)
        self.portLabel.setObjectName("portLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.portLabel)
        self.port = QtWidgets.QSpinBox(ConnectTCPDialog)
        self.port.setMinimum(1)
        self.port.setMaximum(65535)
        self.port.setProperty("value", 5760)
        self.port.setObjectName("port")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.port)
        self.serialLabel = QtWidgets.QLabel(ConnectTCPDialog)
        self.serialLabel.setObjectName("serialLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.serialLabel)
        self.serial = QtWidgets.QLineEdit(ConnectTCPDialog)
        self.serial.setObjectName("serial")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.serial)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConnectTCPDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(ConnectTCPDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ConnectTCPDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ConnectTCPDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConnectTCPDialog)

    def retranslateUi(self, ConnectTCPDialog):
        ConnectTCPDialog.setWindowTitle(QtWidgets.QApplication.translate("ConnectTCPDialog", "Connect TCP Device", None, -1))
        self.hostnameLabel.setText(QtWidgets.QApplication.translate("ConnectTCPDialog", "Hostname", None, -1))
        self.portLabel.setToolTip(QtWidgets.QApplication.translate("ConnectTCPDialog", "Default: 5760", None, -1))
        self.portLabel.setText(QtWidgets.QApplication.translate("ConnectTCPDialog", "Port", None, -1))
        self.port.setToolTip(QtWidgets.QApplication.translate("ConnectTCPDialog", "Default: 5760", None, -1))
        self.serialLabel.setText(QtWidgets.QApplication.translate("ConnectTCPDialog", "Serial Number (Optional)", None, -1))

