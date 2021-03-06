import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtCore import QObject, pyqtSignal

# from View.ConnectionSetting import Ui_Dialog
from View.ReadWriteView import Ui_Dialog
from temp import MyThread


class Communicate(QObject):
    # ---Создаем сигналы---
    displaySignal = QtCore.pyqtSignal()
    btnSignal = QtCore.pyqtSignal()
    rwSignal = QtCore.pyqtSignal()
    startSignal = QtCore.pyqtSignal()
    stopSignal = QtCore.pyqtSignal()

# Новый поток
# class MyThread(QtCore.QThread):
#     mySignal = QtCore.pyqtSignal()
#
#     def __init__(self, parent=None):
#         QtCore.QThread.__init__(self, parent)
#
#     def run(self):
#         pass

class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.signal = Communicate()
        self.raw = self.Raw(self)
        self.css = self.Connection_settings(self)



        # self.myThread = MyThread()

    def on_chahge(self, tag_names):
        _translate = QtCore.QCoreApplication.translate
        for i, (key, val) in enumerate(tag_names.items()):
            self.tableWidget.setRowCount(i + 1)

            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i, 0, item)
            item = self.tableWidget.item(i, 0)
            item.setText(_translate("MainWindow", key))

            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i, 1, item)
            item = self.tableWidget.item(i, 1)
            item.setText(_translate("MainWindow", val))



            # item = QtWidgets.QTableWidgetItem()
            # self.tableWidget.setItem(i, 2, item)
            # item = self.tableWidget.item(i, 2)
            # item.setText(_translate("MainWindow", "Состояние %"))

    def set_table_progress(self, progress_value, tag_name):
        _translate = QtCore.QCoreApplication.translate
        rowCount = self.tableWidget.rowCount()
        x = 1
        # Заполняем словарь тегами из таблицы
        for i in range(0, rowCount):

            item = self.tableWidget.item(i, 0)
            if item.text() == tag_name:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, 2, item)
                item = self.tableWidget.item(i, 2)
                item.setText(_translate("MainWindow", str("{0:.3f}%".format(progress_value))))
                x = x + 1

                if i < x:
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, 2, item)
                    item = self.tableWidget.item(i, 2)
                    item.setText(_translate("MainWindow", "Готово"))
                # elif i == (rowCount - 1):
                #     item = QtWidgets.QTableWidgetItem()
                #     self.tableWidget.setItem(i, 2, item)
                #     item = self.tableWidget.item(i, 2)
                #     item.setText(_translate("MainWindow", "Готово"))





    def test3(self, tag_name, progress_value):
        _translate = QtCore.QCoreApplication.translate
        rowCount = self.tableWidget.rowCount()

        # Заполняем словарь тегами из таблицы
        for i in range(0, rowCount):
            item = self.tableWidget.item(i, 0)
            if item == tag_name:

                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, 2, item)
                item = self.tableWidget.item(i, 2)
                item.setText(_translate("MainWindow", str("{0:.3f}%".format(progress_value))))
                #
                # _translate = QtCore.QCoreApplication.translate
                # print("+set_table_progress " + str(progress_value))

                # item = QtWidgets.QTableWidgetItem()
                # self.tableWidget.setItem(0, 2, item)
                # item = self.tableWidget.item(0, 2)
                # item.setText(_translate("MainWindow", str("{0:.3f}%".format(progress_value))))
                # # print("name", str(tag_name), "=", str(progress_value))

    def Clicked_read_write(self):
        print("YRAAA")

    def Raw_click(self):
        try:
            self.signal.btnSignal.emit()

        except Exception as er:
            print("Вывод :", er)
            #sys.exc_info()[0]

    def Connection_settings_signal(self):
        print("+Connection_settings_signal")
        # self.signal.rwSignal.emit()
        self.myThread.run()


#-------Создаем пункт в меню чтение и запись
    def Raw(self, MainWindow):
        self.actionRead_and_write = QtWidgets.QAction(MainWindow)
        self.actionRead_and_write.setObjectName("actionRead_and_write")
        self.actionRead_and_write.setShortcut('Shift+1')
        self.actionRead_and_write.triggered.connect(self.Raw_click)

    # -------Создаем пункт в меню параметры подключние
    def Connection_settings(self, MainWindow):
        self.actionConnection_settings = QtWidgets.QAction(MainWindow)
        self.actionConnection_settings.setObjectName("actionConnection_settings")
        self.actionConnection_settings.setShortcut('Shift+2')
        self.actionConnection_settings.triggered.connect(self.Connection_settings_signal)

    def start(self):
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget.setItem(0, 0, item)
        self.tableWidget.show()  # Показать таблицу
        self.signal.startSignal.emit()

    def stopSignal(self):
        self.signal.stopSignal.emit()

    def setupUi(self):
        self.setObjectName("MainWindow")
        # self.resize(672, 350)
        self.setFixedSize(672, 350)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(20, 110, 631, 191))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 629, 189))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # ----------------------------Таблица в потоке------------------------------------
        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 631, 192))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())

        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.tableWidget.setBaseSize(QtCore.QSize(0, 0))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        self.tableWidget.setFont(font)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        # self.tableWidget.setSizeAdjustPolicy(
        #     QtWidgets.QAbstractScrollArea.AdjustToContents)
        # self.tableWidget.resizeColumnsToContents()
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()

        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        item.setFont(font)
        item.setBackground(QtGui.QColor(85, 170, 255))
        self.tableWidget.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        item.setFont(font)

        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        item.setFont(font)

        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)


        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)

        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.hide()  # Скрыть таблицу

        # ------------------------------------------------------------------------
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 80, 75, 23))
        self.pushButton.clicked.connect(self.start)


        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)

        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 80, 75, 23))
        self.pushButton_2.clicked.connect(self.stopSignal)

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)

        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")

        self.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 672, 21))
        self.menuBar.setObjectName("menuBar")

        self.menuRead_and_write = QtWidgets.QMenu(self.menuBar)
        self.menuRead_and_write.setObjectName("menuRead_and_write")

        # ------Чтение и запись---
        self.setMenuBar(self.menuBar)

        self.actionStatistical_data = QtWidgets.QAction(self)
        self.actionStatistical_data.setObjectName("actionStatistical_data")


        self.actionCharts = QtWidgets.QAction(self)
        self.actionCharts.setObjectName("actionCharts")

        self.actionFilter = QtWidgets.QAction(self)
        self.actionFilter.setObjectName("actionFilter")

        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setShortcut('Ctrl+O')

        self.menuRead_and_write.addAction(self.actionRead_and_write)
        self.menuRead_and_write.addSeparator()
        self.menuRead_and_write.addAction(self.actionStatistical_data)
        self.menuRead_and_write.addSeparator()
        self.menuRead_and_write.addAction(self.actionConnection_settings)
        self.menuRead_and_write.addSeparator()
        self.menuRead_and_write.addAction(self.actionCharts)
        self.menuRead_and_write.addSeparator()
        self.menuRead_and_write.addAction(self.actionFilter)
        self.menuRead_and_write.addSeparator()
        self.menuRead_and_write.addAction(self.actionExit)
        self.menuBar.addAction(self.menuRead_and_write.menuAction())

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)





    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Главная"))

        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Название"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Описание"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Состояние"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)

        self.tableWidget.setSortingEnabled(__sortingEnabled)



        self.pushButton.setText(_translate("MainWindow", "Пуск"))
        self.pushButton_2.setText(_translate("MainWindow", "Стоп"))
        self.menuRead_and_write.setTitle(_translate("MainWindow", "Меню"))
        self.actionRead_and_write.setText(_translate("MainWindow", "Чтение и запись"))
        self.actionStatistical_data.setText(_translate("MainWindow", "Статистика данных"))
        self.actionConnection_settings.setText(_translate("MainWindow", "Параметры соединения"))
        self.actionCharts.setText(_translate("MainWindow", "Графики"))
        self.actionFilter.setText(_translate("MainWindow", "Фильтры"))
        self.actionExit.setText(_translate("MainWindow", "Выход"))

