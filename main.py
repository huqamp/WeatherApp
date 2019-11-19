from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import requests
from ui import Ui_MainWindow
from PyQt5.QtGui import QIcon


def join_str(it):
    return ' '.join(map(str, it))


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('pogoda_2.jpg'))
        self.pushButton.clicked.connect(self.dannie)

    def dannie(self):
        api = "16dc0bde73020cf75dbf36bd5a836998"
        ch = 0
        city = self.lineEdit.text()
        if not city.endswith(", RU"):
            city += ", RU"
        # получение данных
        zapros = requests.get("http://api.openweathermap.org/data/2.5/find",
                              params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': api})
        otvet = zapros.json()
        cities = ["{}, {}".format(d['name'], d['sys']['country'])
                  for d in otvet['list']]
        # проверка на наличе данных о городе
        if cities:
            city_id = otvet['list'][0]['id']
            self.lineEdit.setText(city)
            # получение данных о погоде
            zapros = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                  params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': api})
            otvet = zapros.json()
            temp = otvet['main']['temp']
            temp_min = otvet['main']['temp_min']
            temp_max = otvet['main']['temp_max']
            speed = otvet['wind']['speed']
            description = ''
            if otvet['weather']:
                description = otvet['weather'][0]['description']
            self.label_6.setText(str(temp))
            self.label_7.setText(str(temp_min))
            self.label_10.setText(str(temp_max))
            self.label_22.setText(str(speed))
            self.label_23.setText(description)
            # получение данных о ближайшей погоде
            zapros = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                                  params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': api})
            otvet = zapros.json()
            vivod = []
            for i in otvet['list'][1:]:
                if ch % 4 == 0:
                    vivod.append([i['dt_txt'], i['main']['temp'], i['weather'][0]['description']])
            self.label_12.setText(join_str(vivod[0]))
            self.label_13.setText(join_str(vivod[1]))
            self.label_14.setText(join_str(vivod[2]))
            self.label_15.setText(join_str(vivod[3]))
            self.label_16.setText(join_str(vivod[4]))
            self.label_17.setText(join_str(vivod[5]))
            self.label_18.setText(join_str(vivod[6]))
            self.label_19.setText(join_str(vivod[7]))
            self.label_20.setText(join_str(vivod[8]))
            self.label_21.setText(join_str(vivod[9]))
        else:
            self.label_6.setText('Нету данных')
            self.label_7.setText('Нету данных')
            self.label_10.setText('Нету данных')
            self.label_22.setText('Нету данных')
            self.label_23.setText('Нету данных')
            self.label_12.setText('Нету данных')


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
