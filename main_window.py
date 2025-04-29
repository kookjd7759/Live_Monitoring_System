from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt, QDate, QTime, QTimer, QUrl, QThread
from PyQt5.QtGui import QCursor
from PyQt5.QtWebEngineWidgets import QWebEngineView

import folium
import sys
import os

from ui.UI_main import Ui_MainWindow
from module.database import DB

class MyThread(QThread):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)

class MainClass(QMainWindow):
    def update_date_time(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        line = QDate.toString(date, 'yyyy-MM-dd') + '   ' + time.toString(Qt.DefaultLocaleShortDate)
        self.ui.today_date.setText(line)

    def update_realtime_info(self):
        recent_data = self.database.search_recent_one()
        text = ''
        for key in recent_data:
            text += f'{key}, {recent_data[key]}\n'
        print(text)
        self.ui.realTimeInfo_textEdit.setText(text)

    def load_map(self):
        m = folium.Map(location=[37.8690, 127.7382], zoom_start=13)
        folium.Marker(
            [37.8690, 127.7382], popup='(주)솔리메틱스\nhttp://solimatics.co.kr', tooltip='Solimatics'
        ).add_to(m)

        map_file = 'folium_map.html'
        m.save(map_file)

        file_path = os.path.abspath(map_file)
        self.map_view.load(QUrl.fromLocalFile(file_path))

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

        self.map_view = QWebEngineView()
        layout = QVBoxLayout(self.ui.frame_map)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.map_view)
        self.load_map()
    
    def init_state(self):
        self.change_page('home')
        self.ui.selectedDate_lineEdit.setReadOnly(True)
        self.ui.realTimeInfo_textEdit.setReadOnly(True)
        self.ui.infomation_textEdit.setReadOnly(True) 
        self.ui.selectedDate_lineEdit.setText(QDate.toString(self.ui.calendarWidget.selectedDate(), 'yyyy-MM-dd'))
        self.ui.calendarWidget.clicked.connect(self.calendar_clicked)
        self.calendar_clicked()

        self.timer_time = QTimer()
        self.timer_time.timeout.connect(self.update_date_time)
        self.timer_time.start(1000)

        self.timer_realtime_info = QTimer()
        self.timer_realtime_info.timeout.connect(self.update_realtime_info)
        self.timer_realtime_info.start(3000)
        
    def init_btn(self):
        self.ui.btn_home.clicked.connect(lambda: self.change_page('home'))
        self.ui.btn_map.clicked.connect(lambda: self.change_page('map'))
        self.ui.btn_more.clicked.connect(lambda: self.change_page('more'))

    def change_page(self, key):
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
   
    def calendar_update_infomation(self, date):
        if date == QDate.currentDate().toString('yyyy-MM-dd'):
            self.ui.infomation_textEdit.setHtml('<span style="color:black;">[ Today ] ')
            return
        data = self.database.search_date(date)
        if data['worked']:
            start_dt = data['start_time']
            end_dt = data['end_time']
            diff = end_dt - start_dt
            total_seconds = diff.total_seconds()
            duration_h = total_seconds // 3600
            duration_m = (total_seconds % 3600) // 60
            duration_sec = total_seconds % 60

            working_time = total_seconds
            for i in range(0, len(data['time_list(sec)']) - 1):
                diff = data['time_list(sec)'][i + 1] - data['time_list(sec)'][i]
                if diff >= 180:
                    working_time -= diff
            working_h = working_time // 3600
            working_m = (working_time % 3600) // 60
            working_sec = working_time % 60

            text = (
                f'<span style="color:green;">[ Worked on it ]<span style="color:black;"><br><br>'
                f"Start work : {data['start_time']}<br><br>"
                f"End work : {data['end_time']}<br><br>"
                f"Working duration: {int(duration_h):02}h {int(duration_m):02}m {int(duration_sec):02}s<br><br>"
                f"Working time: {int(working_h):02}h {int(working_m):02}m {int(working_sec):02}s<br><br>"
                f"Data counts : {len(data['time_list(sec)']):,}"
            )
            self.ui.infomation_textEdit.setHtml(text)
        else: self.ui.infomation_textEdit.setHtml('<span style="color:red;">[ Didn\'t work on it ]')
    def calendar_clicked(self):
        date = QDate.toString(self.ui.calendarWidget.selectedDate(), 'yyyy-MM-dd')

        ### update selected date lineEdit
        self.ui.selectedDate_lineEdit.setText(date)

        ### update information 
        self.ui.infomation_textEdit.setHtml('<span style="color:gray;">Loading...</span>')
        QTimer.singleShot(10, lambda: self.calendar_update_infomation(date))
     
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