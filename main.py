import sys
import os
import time
import cv2
import datetime
import pyautogui
import numpy as np
import platform
import psutil
import wmi
from pynput import mouse
from windows_tools.installed_software import get_installed_software
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import QThread, Signal
from UI.main import Ui_Rec_Window


class Info_Thread(QThread):
    """
    Многопоточный класс реализующий предоставление информации о ПК пользователя

    ...

    Атрибуты
    --------
    directory : str
        Место сохранения файла
    date : str
        Текущие дата и время

    Методы
    ------
    run:
        Создает и заполняет .txt файл, после чего сохраняет в заданную папку

    """
    thread_crashed = Signal(Exception)

    def __init__(self, directory, date):
        """
        Устанавливает все необходимые атрибуты для объекта Info_Thread

        ...

        Параметры
        ---------
        directory : str
            Место сохранения файла
        date : str
            Текущие дата и время
        """
        super().__init__()
        self.date = date
        self.directory = directory

    def run(self):
        """
        Создает и заполняет .txt файл, после чего сохраняет в заданную папку

        ...
        """
        try:
            # Создание кортежа, содержащего шесть атрибутов: system, node, release, version, machine и processor
            uname = platform.uname()
            f = wmi.WMI()
            # Создание и запись в .txt файл характеристики ОС, харастеристики устройства, запущенные процессы, установленное ПО
            with open(f"{self.directory}\\rec_%s%s%s%s%s%s.txt" % (
                    self.date.year, self.date.month, self.date.day, self.date.hour, self.date.minute, self.date.second),
                      "w") as file:
                file.write(
                    "======================================== Характеристики ОС ========================================\n")
                file.write(f"Система: {uname.system}\n")
                file.write(f"Релиз: {uname.release}\n")
                file.write(f"Версия: {uname.version}\n")
                file.write(f"Разрядость: {platform.architecture()[0]}\n")
                file.write(
                    "======================================== Харастеристики устройства =======================================\n")
                file.write(f"Имя устройства: {uname.node}\n")
                file.write(f"Процессор: {uname.processor}\n")
                file.write(f"Ядра: {psutil.cpu_count(logical=False)}\n")
                file.write(f"Логические процессы: {psutil.cpu_count()}\n")
                file.write(f"Минимальная частота процессора: {psutil.cpu_freq().min:.2f}Mhz\n")
                file.write(f"Максимальная частота процессора: {psutil.cpu_freq().max:.2f}Mhz\n")
                file.write(f"Текущая частота процессора: {psutil.cpu_freq().current:.2f}Mhz\n")
                file.write(f"Оперативная память: {round(psutil.virtual_memory().total / 1000000000, 2)} GB\n")
                file.write(
                    f"Используемая оперативная память: {round(psutil.virtual_memory().used / 1000000000, 2)} GB | {psutil.virtual_memory().percent}%\n")
                file.write(
                    f"Доступная оперативная память: {round(psutil.virtual_memory().available / 1000000000, 2)} GB\n")
                file.write(
                    "======================================== Запущенные процессы ========================================\n")
                for process in f.Win32_Process():
                    file.write(f"{process.ProcessId:<10} {process.Name}\n")

                file.write(
                    "======================================== Установленное ПО ========================================\n")
                for software in get_installed_software():
                    file.write(f"{software['name']}, {software['version']}, {software['publisher']}\n")
            window.btn_stop.setDisabled(False)
            window.btn_play.setDisabled(False)
            window.btn_pause.setDisabled(False)
            window.label.setText("")
            file.close()
        except Exception as e:
            self.thread_crashed.emit(e)


class Rec_Thread(QThread):
    """
    Многопоточный класс реализующий запись экрана пользователя

    ...

    Атрибуты
    --------
    date : str
        Текущие дата и время

    Методы
    ------
    run:
        Начинает запись экрана пользователя, отслеживая положение курсора и нажатий ЛКМ
    on_click:
        Отслеживает была ли нажата ЛКМ
    """
    thread_crashed = Signal(Exception)

    def __init__(self, date):
        """
        Устанавливает все необходимые атрибуты для объекта Rec_Thread

        ...

        Параметры
        ---------
        date : str
            Текущие дата и время
        is_clicked : bool
            Нажата ли ЛКМ
        listener :
            Отслеживает нажатия ЛКМ
        """
        super().__init__()
        self.date = date
        self.is_clicked = False
        self.listener = mouse.Listener(on_click=self.on_click)

    def run(self):
        """
        Начинает запись экрана пользователя, отслеживая положение курсора и нажатий ЛКМ

        ...
        """
        try:
            # Запускаем обратный таймер 5 сек перед начальм записи
            mytimer = 5
            while mytimer != 0:
                if not window.sleep:
                    window.label.setText(f"До начала: {mytimer} Секунд")
                    time.sleep(1)
                    mytimer -= 1
            window.info_thread.start()
            xs = [0, 8, 6, 14, 12, 4, 2, 0]
            ys = [0, 2, 4, 12, 14, 6, 8, 0]
            # Задаем максимальную длительнось видео в секундах (record_seconds)
            record_seconds = 5
            # Получаем разрешение экрана
            screen_size = tuple(pyautogui.size())
            # Задаем кодек
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            # Указываем фпс
            fps = 10.0
            # Задаем название файлу
            filename = "rec_%s%s%s%s%s%s.avi" % (
                self.date.year, self.date.month, self.date.day, self.date.hour, self.date.minute, self.date.second)
            # Создаем объкт для записи видео
            self.out = cv2.VideoWriter(f"{window.LineEdit_directory.text()}\\{filename}", fourcc, fps, screen_size)
            # Запускаем объект для отслеживания нажатий ЛКМ
            self.listener.start()
            i = int(record_seconds * fps)
            while i != 0:
                if not window.sleep:
                    window.label.setText(f"Запись идет: {i / 10} Секунд")
                    mouse_x, mouse_y = pyautogui.position()
                    # Создать снимок экрана
                    img = pyautogui.screenshot()
                    # Конвертация изображения в массив numpy
                    frame = np.array(img)
                    # Конвертировать цвеета из BGR в RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    xthis = [1.5 * x + mouse_x for x in xs]
                    ythis = [1.5 * y + mouse_y for y in ys]
                    points = list(zip(xthis, ythis))
                    points = np.array(points, 'int32')
                    cv2.fillPoly(frame, [points], color=[145, 145, 145])
                    # Если ЛКМ нажата, то вокруг курсора появляется красный круг, до момента пока кнопка не будет отжата
                    if self.is_clicked:
                        cv2.circle(frame, (mouse_x, mouse_y), 20, (0, 0, 255), 2)
                    # Записываем фрейм
                    self.out.write(frame)
                    i -= 1
            if window.info_thread.isRunning():
                window.btn_stop.setDisabled(True)
                window.btn_play.setDisabled(True)
                window.btn_pause.setDisabled(True)
                window.label.setText("Сохранение...")
            # По завершению записи останавливаем объект для отслеживания нажатий ЛКМ
            self.listener.stop()
            cv2.destroyAllWindows()
            # Сохраняем видео
            self.out.release()
        except Exception as e:
            self.thread_crashed.emit(e)

    def on_click(self, x, y, button, pressed):
        """
        Отслеживает была ли нажата ЛКМ

        Параметры
        ---------
        x : int
            Координаты по X
        y : int
            Координаты по Y
        button: Button
            Какая кнопка была нажата
        pressed: bool
            Зажата ли кнопка
        """
        # Проверяем, является ла нажатая кнопка ЛКМ
        if str(button) == "Button.left":
            if not self.is_clicked:
                self.is_clicked = True
            else:
                self.is_clicked = False


class MainWindow(QMainWindow, Ui_Rec_Window):
    """
    Класс главного окна приложения

    ...

    Методы
    ------
    closeEvent:
        Событие при закрытии главного окна, отвечающее за остановку работы потоков
    select_directory:
        Открывает окно выбора места сохранения видео и информации о ПО
    rec_pause:
        Ставит запись на паузу
    rec_stop:
         Остановливает запись (прекращает работу класса Rec_Thread)
    rec_start:
        Начинает запись (запускает работу класса Rec_Thread)
    """

    def __init__(self):
        """
        Устанавливает все необходимые атрибуты для объекта MainWindow.

        ...
        """
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.LineEdit_directory.setText(os.getcwd())
        self.btn_directory.clicked.connect(self.select_directory)
        self.btn_stop.clicked.connect(self.rec_stop)
        self.btn_pause.clicked.connect(self.rec_pause)
        self.btn_play.clicked.connect(self.rec_start)
        self.date = datetime.datetime.now()
        self.instanced_thread = Rec_Thread(self.date)
        self.info_thread = Info_Thread(self.LineEdit_directory.text(), self.date)
        self.sleep = False

    def closeEvent(self, event):
        """
        Отслеживает была ли нажата ЛКМ

        Параметры
        ---------
        event :
            Событие
        """
        # Прекращаем работу instanced_thread
        self.instanced_thread.terminate()
        # Останавливаем объект для отслеживания нажатий ЛКМ
        self.instanced_thread.listener.stop()

    def select_directory(self):
        """
        Открывает окно выбора места сохранения видео и информации о ПО

        ...
        """
        # Открываем окно выбора папки
        selected_directory = QFileDialog.getExistingDirectory()
        # Изменяем содержимое LineEdit_directory на путь до выбранной папки
        self.LineEdit_directory.setText(selected_directory)

    def rec_pause(self):
        """
        Ставит запись на паузу

        ...
        """
        if self.instanced_thread.isRunning():
            if not self.sleep:
                self.sleep = True
            else:
                self.sleep = False
        else:
            pass

    def rec_stop(self):
        """
        Остановливает запись (прекращает работу класса Rec_Thread)

        ...
        """
        if self.instanced_thread.isRunning():
            # Прекращаем работу instanced_thread
            self.instanced_thread.terminate()
            # Останавливаем объект для отслеживания нажатий ЛКМ
            self.instanced_thread.listener.stop()
            try:
                self.instanced_thread.out.release()
            except AttributeError:
                pass
            if self.info_thread.isRunning():
                window.label.setText("Сохранение...")
            else:
                window.label.setText("")
        else:
            pass

    def rec_start(self):
        """
        Начинает запись (запускает работу класса Rec_Thread)

        ...
        """
        try:
            # Создаем переменные, содержащие объекты многопоточных классов
            if not self.instanced_thread.isRunning() and not self.info_thread.isRunning():
                # Создаем переменные, содержащие объекты многопоточных классов
                self.info_thread = Info_Thread(self.LineEdit_directory.text(), self.date)
                self.instanced_thread = Rec_Thread(self.date)
                # Проверяем правильно ли прописан путь.
                # Если нет, то выводим сообщение с ощибкой
                if not os.path.isdir(self.LineEdit_directory.text()):
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("Ошибка пути")
                    dlg.setText("Произошла ошибка при сохранении файла")
                    dlg.setStandardButtons(QMessageBox.Ok)
                    dlg.setIcon(QMessageBox.Warning)
                    button = dlg.exec()
                # Если путь прописан правильно, то запускаем работу многопоточных классов
                else:
                    self.instanced_thread.start()
            else:
                pass
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
