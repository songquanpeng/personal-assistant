# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(711, 353)
        MainWindow.setStyleSheet("font: 11pt \"Microsoft YaHei UI\";")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")
        self.restTab = QtWidgets.QWidget()
        self.restTab.setObjectName("restTab")
        self.gridLayout = QtWidgets.QGridLayout(self.restTab)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.restTab)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.workSpinBox = QtWidgets.QSpinBox(self.restTab)
        self.workSpinBox.setMinimum(1)
        self.workSpinBox.setMaximum(9999)
        self.workSpinBox.setProperty("value", 20)
        self.workSpinBox.setObjectName("workSpinBox")
        self.horizontalLayout.addWidget(self.workSpinBox)
        self.label_2 = QtWidgets.QLabel(self.restTab)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.restSpinBox = QtWidgets.QSpinBox(self.restTab)
        self.restSpinBox.setMinimum(1)
        self.restSpinBox.setMaximum(9999)
        self.restSpinBox.setProperty("value", 60)
        self.restSpinBox.setObjectName("restSpinBox")
        self.horizontalLayout.addWidget(self.restSpinBox)
        spacerItem = QtWidgets.QSpacerItem(188, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.restTab)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.methodComboBox = QtWidgets.QComboBox(self.restTab)
        self.methodComboBox.setObjectName("methodComboBox")
        self.methodComboBox.addItem("")
        self.methodComboBox.addItem("")
        self.methodComboBox.addItem("")
        self.methodComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.methodComboBox)
        spacerItem1 = QtWidgets.QSpacerItem(168, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.restTab)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.restTab)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.workProgressBar = QtWidgets.QProgressBar(self.restTab)
        self.workProgressBar.setProperty("value", 0)
        self.workProgressBar.setObjectName("workProgressBar")
        self.gridLayout.addWidget(self.workProgressBar, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.restTab)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.restProgressBar = QtWidgets.QProgressBar(self.restTab)
        self.restProgressBar.setProperty("value", 0)
        self.restProgressBar.setObjectName("restProgressBar")
        self.gridLayout.addWidget(self.restProgressBar, 6, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(388, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.restStopBtn = QtWidgets.QPushButton(self.restTab)
        self.restStopBtn.setObjectName("restStopBtn")
        self.horizontalLayout_6.addWidget(self.restStopBtn)
        self.restStartBtn = QtWidgets.QPushButton(self.restTab)
        self.restStartBtn.setObjectName("restStartBtn")
        self.horizontalLayout_6.addWidget(self.restStartBtn)
        self.gridLayout.addLayout(self.horizontalLayout_6, 7, 0, 1, 1)
        self.tabWidget.addTab(self.restTab, "")
        self.scheduleTab = QtWidgets.QWidget()
        self.scheduleTab.setObjectName("scheduleTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scheduleTab)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.scheduleTextEdit = QtWidgets.QPlainTextEdit(self.scheduleTab)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.scheduleTextEdit.setFont(font)
        self.scheduleTextEdit.setStyleSheet("font-size: 11pt;\n"
"font-family: \"Consolas\", \"Microsoft YaHei\";")
        self.scheduleTextEdit.setPlainText("")
        self.scheduleTextEdit.setObjectName("scheduleTextEdit")
        self.gridLayout_3.addWidget(self.scheduleTextEdit, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(498, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.scheduleSaveBtn = QtWidgets.QPushButton(self.scheduleTab)
        self.scheduleSaveBtn.setObjectName("scheduleSaveBtn")
        self.horizontalLayout_4.addWidget(self.scheduleSaveBtn)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.tabWidget.addTab(self.scheduleTab, "")
        self.todoTab = QtWidgets.QWidget()
        self.todoTab.setObjectName("todoTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.todoTab)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.todoTextEdit = QtWidgets.QPlainTextEdit(self.todoTab)
        self.todoTextEdit.setStyleSheet("font-size: 11pt;\n"
"font-family: \"Consolas\", \"Microsoft YaHei\";")
        self.todoTextEdit.setObjectName("todoTextEdit")
        self.gridLayout_4.addWidget(self.todoTextEdit, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(428, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.todoSaveBtn = QtWidgets.QPushButton(self.todoTab)
        self.todoSaveBtn.setObjectName("todoSaveBtn")
        self.horizontalLayout_3.addWidget(self.todoSaveBtn)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.tabWidget.addTab(self.todoTab, "")
        self.otherTab = QtWidgets.QWidget()
        self.otherTab.setObjectName("otherTab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.otherTab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.otherTab)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.microblogServerLineEdit = QtWidgets.QLineEdit(self.otherTab)
        self.microblogServerLineEdit.setText("")
        self.microblogServerLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.microblogServerLineEdit.setObjectName("microblogServerLineEdit")
        self.horizontalLayout_5.addWidget(self.microblogServerLineEdit)
        self.gridLayout_5.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.otherTab)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.microblogTokenLineEdit = QtWidgets.QLineEdit(self.otherTab)
        self.microblogTokenLineEdit.setText("")
        self.microblogTokenLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.microblogTokenLineEdit.setObjectName("microblogTokenLineEdit")
        self.horizontalLayout_7.addWidget(self.microblogTokenLineEdit)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.otherTab)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.messageServerLineEdit = QtWidgets.QLineEdit(self.otherTab)
        self.messageServerLineEdit.setText("")
        self.messageServerLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.messageServerLineEdit.setObjectName("messageServerLineEdit")
        self.horizontalLayout_8.addWidget(self.messageServerLineEdit)
        self.gridLayout_5.addLayout(self.horizontalLayout_8, 2, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_9 = QtWidgets.QLabel(self.otherTab)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.messageTokenLineEdit = QtWidgets.QLineEdit(self.otherTab)
        self.messageTokenLineEdit.setText("")
        self.messageTokenLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.messageTokenLineEdit.setObjectName("messageTokenLineEdit")
        self.horizontalLayout_9.addWidget(self.messageTokenLineEdit)
        self.gridLayout_5.addLayout(self.horizontalLayout_9, 3, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.otherTab)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        self.workTextLineEdit = QtWidgets.QLineEdit(self.otherTab)
        self.workTextLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.workTextLineEdit.setObjectName("workTextLineEdit")
        self.horizontalLayout_10.addWidget(self.workTextLineEdit)
        self.gridLayout_5.addLayout(self.horizontalLayout_10, 4, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_11 = QtWidgets.QLabel(self.otherTab)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_11.addWidget(self.label_11)
        self.restTextLineEdit = QtWidgets.QLineEdit(self.otherTab)
        self.restTextLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.restTextLineEdit.setObjectName("restTextLineEdit")
        self.horizontalLayout_11.addWidget(self.restTextLineEdit)
        self.gridLayout_5.addLayout(self.horizontalLayout_11, 5, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 172, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem5, 6, 0, 1, 1)
        self.tabWidget.addTab(self.otherTab, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "个人助理"))
        self.label.setText(_translate("MainWindow", "休息间隔："))
        self.workSpinBox.setSuffix(_translate("MainWindow", " 分钟"))
        self.label_2.setText(_translate("MainWindow", "休息时长："))
        self.restSpinBox.setSuffix(_translate("MainWindow", " 秒"))
        self.label_3.setText(_translate("MainWindow", "提醒方式："))
        self.methodComboBox.setItemText(0, _translate("MainWindow", "消息提醒"))
        self.methodComboBox.setItemText(1, _translate("MainWindow", "弹窗提醒"))
        self.methodComboBox.setItemText(2, _translate("MainWindow", "全屏覆盖"))
        self.methodComboBox.setItemText(3, _translate("MainWindow", "显示桌面"))
        self.label_4.setText(_translate("MainWindow", "工作进度条："))
        self.label_5.setText(_translate("MainWindow", "休息进度条："))
        self.restStopBtn.setText(_translate("MainWindow", "终止"))
        self.restStartBtn.setText(_translate("MainWindow", "开始"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.restTab), _translate("MainWindow", "休息提醒"))
        self.scheduleSaveBtn.setText(_translate("MainWindow", "保存"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scheduleTab), _translate("MainWindow", "定时任务"))
        self.todoTextEdit.setPlainText(_translate("MainWindow", "# 语法：* TODO 内容\n"
""))
        self.todoSaveBtn.setText(_translate("MainWindow", "保存"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.todoTab), _translate("MainWindow", "周期待办"))
        self.label_7.setText(_translate("MainWindow", "microblog 服务地址："))
        self.label_6.setText(_translate("MainWindow", "microblog 访问凭证："))
        self.label_8.setText(_translate("MainWindow", "message pusher 服务地址："))
        self.label_9.setText(_translate("MainWindow", "message pusher 访问凭证："))
        self.label_10.setText(_translate("MainWindow", "提醒开始工作文案："))
        self.workTextLineEdit.setText(_translate("MainWindow", "开始工作！"))
        self.label_11.setText(_translate("MainWindow", "提醒开始休息文案："))
        self.restTextLineEdit.setText(_translate("MainWindow", "开始休息！"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.otherTab), _translate("MainWindow", "其他设置"))
import resource_rc
