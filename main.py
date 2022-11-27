import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QTableWidgetItem

a = None
class Widget(QMainWindow):
    def __init__(self):
        global a
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.run)
        self.new()
        a = self

    def run(self):
        self.secwindow = SecondWindow()
        self.secwindow.show()


    def new(self):
        result = self.cur.execute(f"""SELECT * FROM type""").fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'sort', 'roast', 'type', 'taste', 'price', 'amount'])
        #объем в граммах
        #цена в рублях

        for value, item in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for el, row in enumerate(item):
                self.tableWidget.setItem(value, el, QTableWidgetItem(str(row)))


class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('renew.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.label_8.setText('для удаления введите только id/для добавления все, кроме id')
        self.pushButton.clicked.connect(self.delete)
        self.pushButton_2.clicked.connect(self.add)

    def delete(self):
        self.label_8.setText('')
        id = self.lineEdit.text()
        try:
            self.cur.execute(
                f"""DELETE from type WHERE id = {int(id)}""")
        except Exception:
            self.label_8.setText('неверный ввод')
        self.con.commit()
        self.con.close()
        Widget.new(a)
        self.close()

    def add(self):
        self.label_8.setText('')
        id = self.lineEdit.text()
        sort = self.lineEdit_2.text()
        roast = self.lineEdit_3.text()
        type = self.lineEdit_4.text()
        taste = self.lineEdit_5.text()
        price = self.lineEdit_6.text()
        amount = self.lineEdit_7.text()
        try:
            self.cur.execute(f"""
                                INSERT INTO type(sort, roast, type, taste, price, amount) VALUES('{sort}', '{roast}', '{type}', '{taste}', '{int(price)}', '{int(amount)}')""")
        except Exception:
            self.label_8.setText('Неверно заполнена форма')
            return
        self.con.commit()
        self.con.close()
        Widget.new(a)
        self.close()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())