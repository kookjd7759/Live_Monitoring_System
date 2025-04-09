import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QDate, QTime, QTimer
from PyQt5.QtGui import QCursor

from ui.UI_main import Ui_MainWindow
from module.database import DB

class MainClass(QMainWindow):
    def update_date_time(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        line = QDate.toString(date, 'yyyy-MM-dd') + '   ' + time.toString(Qt.DefaultLocaleShortDate)
        self.ui.today_date.setText(line)

    def update_info(self):
        date = QDate.toString(self.ui.calendarWidget.selectedDate(), 'yyyy-MM-dd')
        self.database.search_date_one(date)
        self.ui.infomation_textEdit.setText('didn\'t work.')

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint) # delete window Frame
        #self.setAttribute(Qt.WA_TranslucentBackground) # delete Background

        self.init_value()
        self.init_btn()
        self.init_state()

        self.show()
    
    def init_value(self):
        self.current_menu_btn = self.ui.btn_home
        self.database = DB()
    
    def init_state(self):
        self.changePage('home')
        self.ui.selectedDate_lineEdit.setReadOnly(True)
        self.ui.infomation_textEdit.setReadOnly(True)
        self.ui.selectedDate_lineEdit.setText(QDate.toString(self.ui.calendarWidget.selectedDate(), 'yyyy-MM-dd'))
        self.ui.calendarWidget.clicked.connect(lambda: self.ui.selectedDate_lineEdit.setText(QDate.toString(self.ui.calendarWidget.selectedDate(), 'yyyy-MM-dd')))
        self.update_date_time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)
        
    def init_btn(self):
        self.ui.btn_home.clicked.connect(lambda: self.btn_menu_clicked('home'))
        self.ui.btn_map.clicked.connect(lambda: self.btn_menu_clicked('map'))
        self.ui.btn_more.clicked.connect(lambda: self.btn_menu_clicked('more'))



    def changePage(self, key):
        btn = None
        page = None
        if key == 'home':
            btn = self.ui.btn_home
            page = self.ui.page_home
        elif key == 'map':
            btn = self.ui.btn_map
            page = self.ui.page_map
        elif key == 'more':
            btn = self.ui.btn_more
            page = self.ui.page_more

        self.ui.stackwidget.setCurrentWidget(page)
        self.current_menu_btn.setStyleSheet('*{ background-color: #313a46; color: #fff }')
        btn.setStyleSheet('*{ background-color: #1f232a; color: #fff }')
        self.current_menu_btn = btn
        
    def btn_menu_clicked(self, key):
        self.changePage(key)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    window = MainClass() 
    app.exec_()