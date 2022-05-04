# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/form.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(460, 316)
        Dialog.setWindowTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dialogHeader = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dialogHeader.setFont(font)
        self.dialogHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.dialogHeader.setObjectName("dialogHeader")
        self.verticalLayout.addWidget(self.dialogHeader)
        self.icon = QtWidgets.QLabel(Dialog)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setObjectName("icon")
        self.verticalLayout.addWidget(self.icon)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.wordFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.wordFieldComboBox.setObjectName("wordFieldComboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.wordFieldComboBox)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.definitionFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.definitionFieldComboBox.setObjectName("definitionFieldComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.definitionFieldComboBox)
        self.numberOfDefinitionsCheckBox = QtWidgets.QCheckBox(Dialog)
        self.numberOfDefinitionsCheckBox.setObjectName("numberOfDefinitionsCheckBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.numberOfDefinitionsCheckBox)
        self.numberOfDefinitionsSpinBox = QtWidgets.QSpinBox(Dialog)
        self.numberOfDefinitionsSpinBox.setEnabled(False)
        self.numberOfDefinitionsSpinBox.setObjectName("numberOfDefinitionsSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.numberOfDefinitionsSpinBox)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.exampleFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.exampleFieldComboBox.setObjectName("exampleFieldComboBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.exampleFieldComboBox)
        self.numberOfExamplesCheckBox = QtWidgets.QCheckBox(Dialog)
        self.numberOfExamplesCheckBox.setObjectName("numberOfExamplesCheckBox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.numberOfExamplesCheckBox)
        self.numberOfExamplesSpinBox = QtWidgets.QSpinBox(Dialog)
        self.numberOfExamplesSpinBox.setEnabled(False)
        self.numberOfExamplesSpinBox.setObjectName("numberOfExamplesSpinBox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.numberOfExamplesSpinBox)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.headTailWordFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.headTailWordFieldComboBox.setObjectName("headTailWordFieldComboBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.headTailWordFieldComboBox)
        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setObjectName("addButton")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.addButton)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.wordFieldComboBox, self.definitionFieldComboBox)
        Dialog.setTabOrder(self.definitionFieldComboBox, self.numberOfDefinitionsCheckBox)
        Dialog.setTabOrder(self.numberOfDefinitionsCheckBox, self.numberOfDefinitionsSpinBox)
        Dialog.setTabOrder(self.numberOfDefinitionsSpinBox, self.exampleFieldComboBox)
        Dialog.setTabOrder(self.exampleFieldComboBox, self.numberOfExamplesCheckBox)
        Dialog.setTabOrder(self.numberOfExamplesCheckBox, self.numberOfExamplesSpinBox)
        Dialog.setTabOrder(self.numberOfExamplesSpinBox, self.headTailWordFieldComboBox)
        Dialog.setTabOrder(self.headTailWordFieldComboBox, self.addButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.dialogHeader.setText(_translate("Dialog", "БКРС Downloader"))
        self.icon.setText(_translate("Dialog", "TextLabel"))
        self.label.setText(_translate("Dialog", "Word Field"))
        self.label_2.setText(_translate("Dialog", "Definition Field"))
        self.numberOfDefinitionsCheckBox.setText(_translate("Dialog", "Limit Definitions"))
        self.label_3.setText(_translate("Dialog", "Example Field"))
        self.numberOfExamplesCheckBox.setText(_translate("Dialog", "Limit Examples"))
        self.label_4.setText(_translate("Dialog", "Head/Tail Word Field"))
        self.addButton.setText(_translate("Dialog", "Add"))
