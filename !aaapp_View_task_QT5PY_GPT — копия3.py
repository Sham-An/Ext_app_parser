import csv
import os
import pathlib
import ast
import pickle
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QUrl
from urllib.parse import urlparse, parse_qs
# from view_task_form_QT5_GPT import Ui_MainWindow  # изменено
# from view_task_form_QT5_GPT_tmp import Ui_MainWindow  # изменено
from view_task_form_QT5_WIN__3 import Ui_TaskEDIT  # Ui_MainWindow  # изменено
import psycopg2
from config_PySide import params
from urllib.parse import urlparse, parse_qs
from pandas import DataFrame
import Lib.aapp_get_headers as head_get
import Lib.aapp_get_headers as head2

url_str2 = "ru.avito://1/searchSubscription/new/byParams?description=%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB%D1%8B+%D0%B8+%D0%BC%D0%BE%D1%82%D0%BE%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0%2C+%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%2C+%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BD%D0%B0+%D0%BA%D0%B0%D1%80%D1%82%D0%B5%2C+suzuki%2Bgsx-r%2C+%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB%D1%8B%2C+%D0%91%2F%D1%83%2C+%D0%A2%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE+%D1%81+%D1%84%D0%BE%D1%82%D0%BE%2C+%D0%A6%D0%B5%D0%BD%D0%B0+100%C2%A0000%C2%A0%E2%80%94%C2%A0200%C2%A0000%C2%A0%E2%82%BD&filter%5BcategoryId%5D=14&filter%5BlocationId%5D=641780&filter%5Bparams%5D%5B110275%5D=426645&filter%5Bparams%5D%5B30%5D=4969&filter%5BpriceMax%5D=200000&filter%5BpriceMin%5D=100000&filter%5Bquery%5D=suzuki%2Bgsx-r&filter%5BsearchRadius%5D=200&filter%5BwithImagesOnly%5D=1&pushFrequency=3&pushFrequencyOptions%5B0%5D%5Bid%5D=1&pushFrequencyOptions%5B0%5D%5Btitle%5D=%D0%A1%D1%80%D0%B0%D0%B7%D1%83&pushFrequencyOptions%5B1%5D%5Bid%5D=2&pushFrequencyOptions%5B1%5D%5Btitle%5D=%D0%A3%D1%82%D1%80%D0%BE%D0%BC&pushFrequencyOptions%5B2%5D%5Bid%5D=3&pushFrequencyOptions%5B2%5D%5Btitle%5D=%D0%92%D0%B5%D1%87%D0%B5%D1%80%D0%BE%D0%BC&pushFrequencyOptions%5B3%5D%5Bid%5D=0&pushFrequencyOptions%5B3%5D%5Btitle%5D=%D0%9D%D0%B5+%D0%BF%D1%80%D0%B8%D1%81%D1%8B%D0%BB%D0%B0%D1%82%D1%8C&title=%D0%9F%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%BA%D0%B0+%D0%BD%D0%B0+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA"

class Parts_union():
    pass

class MainWindow(QtWidgets.QMainWindow, Ui_TaskEDIT):  # Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Get_Task.clicked.connect(self.get_task)
        ##############################################################
        # # Привязка обработчика событий на смену строки в таблице
        # selection_model = self.tableView.selectionModel()
        # selection_model.currentChanged.connect(self.on_selection_change)
        ###############################################################
        # Настраиваем соединение с базой данных
        self.conn = psycopg2.connect(**params)
        self.cursor = self.conn.cursor()

        # Настраиваем модель таблицы
        self.model = QStandardItemModel(self.View_Task)  # tableView)
        self.View_Task.setModel(self.model)
        # self.tableView.setModel(self.model)
        self.head_list2 = head2.AvitoScraperHead()
        # Привязка обработчика событий на смену строки в таблице
        selection_model = self.View_Task.selectionModel()
        selection_model.currentChanged.connect(self.on_selection_change)
        #self.load_table_from_file("table_data.txt")
        self.get_task()

    def check_task(self):
        # Выполняем запрос к базе данных
        query_all_task = "SELECT * FROM aparser_task"
        self.cursor.execute(query_all_task)
        # Получаем данные и имена столбцов и заполняем модель таблицы
        rows = self.cursor.fetchall()
        head_list = head_get.AvitoScraperHead()
        for row in rows:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! check', row[2])
            url2 = str(row[2])
            head_list.get_url(url2)

    def save_table_to_file(self, file_name):
        table_data = {"column_names": self.get_column_names(), "data": self.get_table_data()}
        with open(file_name, "wb") as file:
            pickle.dump(table_data, file)

    def load_table_from_file(self, file_name):
        with open(file_name, "rb") as file:
            table_data = pickle.load(file)
        column_names = table_data["column_names"]
        table_data = table_data["data"]

        self.model.clear()
        self.model.setColumnCount(len(column_names))
        self.model.setHorizontalHeaderLabels(column_names)
        for row in table_data:
            self.model.appendRow([QStandardItem(data) for data in row])

    def get_column_names(self):
        column_names = []
        for column in range(self.model.columnCount()):
            column_name = self.model.headerData(column, QtCore.Qt.Horizontal)
            column_names.append(column_name)
        return column_names

    def get_table_data(self):
        table_data = []
        for row in range(self.model.rowCount()):
            row_data = []
            for column in range(self.model.columnCount()):
                cell_data = self.model.data(self.model.index(row, column))
                cell_text = str(cell_data) if cell_data is not None else ""
                row_data.append(cell_text)
            table_data.append(row_data)
        return table_data

    def get_task(self):
        # Выполняем запрос к базе данных
        query_all_task = "SELECT * FROM aparser_task"
        self.cursor.execute(query_all_task)

        # Получаем данные и имена столбцов и заполняем модель таблицы
        rows = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        self.model.clear()
        self.model.setColumnCount(len(column_names))
        self.model.setHorizontalHeaderLabels(column_names)
        for row in rows:
            data = [str(col) for col in row]
            self.model.appendRow([QStandardItem(d) for d in data])
        self.View_Task.resizeColumnsToContents()
        # self.View_Task.setColumnWidth(0, 3)
        # self.View_Task.setColumnWidth(1, 50)
        self.View_Task.setColumnWidth(2, 400)
        # self.View_Task.setColumnWidth(3, 0)
        self.View_Task.setColumnHidden(3, True)
        self.View_Task.setColumnHidden(4, True)
        # self.View_Task.setColumnWidth(4, 0)
        # self.View_Task.setColumnWidth(5, 0)
        #self.load_table_from_file("table_data.txt")
        self.save_table_to_file("table_data.txt")

    def on_selection_change(self, current, previous):
        # Получаем URL из текущей строки таблицы
        # url_col = self.model.columnCount() - 1
        column = 2
        if current.row() != previous.row():
            # print('2 url new')

            url = current.sibling(current.row(), column).data()
            print(f'url ===== {url}')
            #head_list2 = head2.AvitoScraperHead()
            path_split, path_split1, parsed_query2, parsed_query3 = self.head_list2.get_url(url)
            #self.head_list2.get_url(url)
            print(f'path_split: {path_split}')
            print(f'path_split1: {path_split1}')
            print(f'parsed_query2: {parsed_query2}')
            print(f'parsed_query3: {parsed_query3}')

            if isinstance(url, QUrl):
                url_str = url.toUrl()
            else:
                url_str = str(url)
            parsed_url = urlparse(url_str)

            print('current.row()', current.row(), current.column())

            self.lineEdit.setText(url)
            self.Path_scheme.setText(parsed_url.scheme)
            self.Path_host.setText(parsed_url.netloc)
            self.Path_parts.setText(parsed_url.path)
            url_parse = self.Path_parts.text()
            path_os = os.path.normpath(url_parse)
            split_path = path_os.split(os.sep)
            View_text = str(f'url = {url}\n \n')
            print("parsed_url ", len(split_path), " @@@@@@", split_path)
            View_text += str(f'split_path = {split_path}\n')
            View_text += str(f'path_split = {path_split}\n')
            View_text += str(f'parsed_query3 "categoryId" = {parsed_query3["categoryId"][0]}\n')
            # head_tail = os.path.split(url_parse)
            # self.Path_local.setText(split_path[1])
            # Заполняем поля парсинга пути из URL
            #     self.Path_local.setText(split_path[1])
            #     self.Path_cat1.setText(split_path[2])
            #     self.Path_cat2.setText(split_path[3])
            #     View_text += str(f'Path_local = {split_path[1]}\n'

            # Создайте список всех виджетов Path_*
            path_widgets = [self.Path_local, self.Path_cat1, self.Path_cat2]

            for i, split_path_part in enumerate(split_path[1:]):
                path_widgets[i].setText(split_path_part)
                View_text += f'Path_{i + 1} = {split_path_part}\n'
                # print('4444444444444444444444444444444444')
            # self.Path_cat1.setText(split_path[2])
            # self.Path_cat2.setText(split_path[3])
            self.list_Query.clear()
            print(parsed_url) #print(parsed_url.query)
            query_dict = parse_qs(parsed_url.query)
            print(f'parsed_url.query = {parsed_url.query}') #print(query_dict)
            #View_text= str(f'url = {url}')
            for param in query_dict:
                self.list_Query.addItem("{}: {}".format(param, query_dict[param][0]))
                self.Task_view_text.setText(View_text)
                #self.Task_view_text.setText("TTTEXTTT") #(parsed_url.fragment)
            #self.Task_view_text.setText(url)  # str(current.row()))#(parsed_url.fragment)



    def closeEvent(self, event):
        # Закрываем соединение с базой данных
        self.cursor.close()
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

#################################################################################
# Вы можете скрыть колонку в QTableView с помощью метода setColumnHidden(). Этот метод принимает индекс столбца и состояние видимости (True для скрытия колонки и False для отображения колонки).CopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopy

# Например, чтобы скрыть вторую колонку, добавьте следующий код после установки модели таблицы:
#
# self.View_Task.setColumnHidden(1, True)
# CopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopy
# Замените 1 на индекс столбца, который нужно скрыть. Если вы хотите сделать колонку видимой снова, то вызовите setColumnHidden() с состоянием видимости False.CopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopy
#
# Также вы можете изменять ширину колонок на ноль, чтобы сделать их невидимыми. Вы можете использовать метод setColumnWidth() и передавать 0 в качестве значения ширины колонки:CopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopy
#
# self.View_Task.setColumnWidth(1, 0)
# CopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopy
# Этот код делает вторую колонку невидимой, так как ее ширина равна нулю. Обратите внимание, что можно использовать любое значение ширины колонки больше нуля, чтобы отобразить ее снова.
#
# User Avatar
# В чем различия этих методов?
# GPT Avatar
# Метод setColumnWidth() устанавливает фиксированную ширину колонок и не позволяет им расширяться или сужаться автоматически в зависимости от содержимого ячеек. Таким образом, если содержимое ячеек не помещается в заданную ширину колонки, то текст может быть обрезан или скрыт.CopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopy
#
# Метод setColumnHidden() делает колонку невидимой, так что она не отображается в таблице.
# Этот метод может быть полезен, если вы хотите временно скрыть какой-то столбец,
# но сделать его видимым снова позже.
#
# В общем случае, выбор метода зависит от вашей конкретной задачи.
# Если вы хотите, чтобы таблица автоматически адаптировалась к содержимому ячеек,
# следует запретить использование метода setColumnWidth()
# и дать таблице регулировать ширину колонок самостоятельно.
# Если вы хотите скрыть какую-то информацию или временно убрать какую-то информацию,
# используйте метод setColumnHidden().
#
# User Avatar
# чтобы таблица автоматически адаптировалась к содержимому ячеек какой метод?
# GPT Avatar
# Чтобы таблица автоматически адаптировалась к содержимому ячеек, можно использовать метод resizeColumnsToContents() объекта QTableView. Этот метод позволяет автоматически настроить ширину столбцов в соответствии с содержимым ячеек.CopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopyCopy
#
# Например, чтобы задать автоадаптивную ширину для всех колонок, можно использовать следующий код:
#
# self.View_Task.resizeColumnsToContents()
#
# Этот код измеряет содержимое каждой ячейки таблицы и настраивает ширину соответствующей колонки в соответствии с этими данными. Обратите внимание, что это может привести к изменению ширины колонок, несмотря на то, что вы могли установить их ширину ранее.
#
# User Avatar
# запретить использование метода setColumnWidth() как? Просто не использовать этот метод?
# GPT Avatar
# Да, если вы не хотите использовать метод setColumnWidth(), то вы можете не вызывать его в вашем коде. Тогда ширина колонок будет автоматически регулироваться в зависимости от содержимого ячеек, если только вы не установили для них фиксированную ширину, например, с помощью метода setFixedSize().CopyCopyCopyCopy
#
# Если вы уже использовали метод setColumnWidth() для задания ширины колонок, то вы можете отменить его действие, вызвав метод QHeaderView.reset() на экземпляре QHeaderView.CopyCopyCopyCopyCopy
#
# Например:
#
# self.View_Task.horizontalHeader().reset()
# CopyCopy
# Этот код сбросит все параметры ширины колонок и включит автоматическую
# адаптацию колонок в зависимости от содержимого ячеек.
#
#
#
