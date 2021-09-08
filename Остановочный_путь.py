from PyQt5 import QtWidgets, QtGui, QtCore #  модули нужные для интерпритации кода и работы с окном
import sys  
from Driver import Driver as drv
from Road import Road as road

# Настройки окна
app=QtWidgets.QApplication(sys.argv)            # Создание объекта приложения
window=QtWidgets.QWidget()                      # Создание окна                 
window.setWindowTitle("Остановочный путь")      # Заголовок окна
icon=QtGui.QIcon("wheel_icon.jpg")              # Присваивание окну иконки
window.setWindowIcon(icon)
app.setWindowIcon(icon)
window.setFont(QtGui.QFont("Times", 16))        # Назначение шрифта  
window.resize(800,350)                          # Размер окна
 
#____________________________________________________________________________________________________________________________


# Функции калькулятора:

    # вывод результатов в строки
def result():

     #-------Вывод коэффициента сцепления   
    coefficient_label.setText(
    "Коэффициент сцепления с дорогой: %s (%s)" %(road.coefficient,road.name_road) )

    #-------Вывод остановочного пути
    stop_distance_label.setText(
    "Остановочный путь:   %s м" %round(stop_distance,2))

    #-------Вывод времени, нужного для остановки
    stop_time_label.setText(
    "Длительность остановки:   %s сек" %round(stop_time,2) )

    #-------Вывод пройденного пути при реагировании
    reaction_distance_label.setText(
    "Путь реагирования:   %s м" %round(reaction_distance,2) )

    #-------Вывод приблизительного времени реакции
    reaction_time_label.setText(
    "Среднее время реакции:   %s сек (%s/%s)" %(round(drv.reaction_driver + drv.reaction_vehicle,1), drv.name_driver,drv.name_vehicle))

    #-------Вывод тормозного пути
    brake_distance_label.setText(
    "Тормозной путь:   %s м" %round(brake_distance,2) )

    #-------Вывод времени торможения
    brake_time_label.setText(
    "Длительность торможения:   %s сек" %round(brake_time,2) )
   
       
#____________________________________________________________________________________________________________________________

    # Расчет значений
def calculate():
     
    global stop_distance 
    global stop_time 
    global reaction_distance 
    global reaction_time 
    global brake_distance 
    global brake_time 

    Speed = speed_box.value()                                         # Скорость 
    
    reaction_time = drv.reaction_driver + drv.reaction_vehicle        # приблизительная сумма времени реакции водителя и машины

    reaction_distance =  reaction_time * (Speed/3.6)                  # путь реакции

    brake_distance =  Speed*Speed/(road.coefficient * road.g * 3.6 * 3.6 * 2)   # тормозной путь

    brake_time = Speed/(road.coefficient * road.g * 3.6 )                       # время для тормозного пути

    stop_time = reaction_time + brake_time                            # время для остановочного пути 

    stop_distance =  reaction_distance + brake_distance               # Остановочный путь
    

    # Запись в историю расчетов
    print("Скорость %s км/ч" %round(Speed,1))
    print("Коэффициент = %s (%s)" %(round(road.coefficient,1),road.name_road))
    print("Общая реакция %s сек (%s/%s)" %(round(reaction_time,1),drv.name_driver,drv.name_vehicle))
    print("Остановочный путь %s м\n"%round(stop_distance,1))
#____________________________________________________________________________________________________________________________

# Функции для меню:

# Выбор покрытия
def dry():            # сухой асфальт
    road.coefficient = road.dry
    road.name_road = road.name_dry
    result()     # Нужно для обновления параметра на экране
        
def wet():            # мокрый асфальт
    road.coefficient = road.wet
    road.name_road = road.name_wet
    result()
        
def sand():           # сухой песок
    road.coefficient = road.sand
    road.name_road = road.name_sand
    result()

def snow():           # снег
    road.coefficient = road.snow
    road.name_road = road.name_snow
    result()

def ice():            # лед
    road.coefficient = road.ice
    road.name_road = road.name_ice
    result()

# Выбор состояния водителя 
def norm():            # нормальная реакция    
    drv.reaction_driver = drv.norm
    drv.name_driver = drv.name_norm
    result()

    
def tired():            # усталость
    drv.reaction_driver = drv.tired
    drv.name_driver = drv.name_tired
    result()


def drunk():            # опьянение
    drv.reaction_driver = drv.drunk
    drv.name_driver = drv.name_drunk
    result()

    
  
# Выбор тормозной системы

def hydra_1():     # Гидропривод (дисковый)
    drv.name_vehicle = drv.name_hydra_1
    drv.reaction_vehicle = drv.hydra_1
    result()

def hydra_2():    # Гидропривод (барабанный)
    drv.name_vehicle = drv.name_hydra_2
    drv.reaction_vehicle = drv.hydra_2
    result()
        
def pnevmo():    # Пневмопривод
    drv.name_vehicle = drv.name_pnevmo
    drv.reaction_vehicle = drv.pnevmo
    result()


#____________________________________________________________________________________________________________________________

# Окно калькулятора

#-------Ввод скорости 
speed_label = QtWidgets.QLabel("Введите скорость (⩽500) в км/ч :")
speed_box = QtWidgets.QSpinBox()       # строка для ввода скорости
speed_box.clear()
speed_box.setButtonSymbols(2)    # скрывает стрелки у speed_box
speed_box.setMaximum(500)        # Максимальное значение 500 км/ч

#-------Переменные
stop_distance = 0.0          # Остановочный путь
stop_time = 0.0              # время для остановочного пути
reaction_distance = 0.0      # путь реакции
reaction_time = 1.27         # среднее время реакции водителя и машины
brake_distance = 0.0         # тормозной путь
brake_time = 0.0             # время для тормозного пути


#-------Кнопка 
main_btn = QtWidgets.QPushButton("Рассчитать")
main_btn.setShortcut("Enter")  


#-------Меню
Menu = QtWidgets.QMainWindow()
menu_bar =QtWidgets.QMenuBar()
Menu.setMenuBar(menu_bar)
menu_bar.setFont(QtGui.QFont("Times", 12)) 
road_menu = QtWidgets.QMenu("Выбор покрытия дороги")
driver_menu = QtWidgets.QMenu("Выбор состояния водителя")
vehicle_menu = QtWidgets.QMenu("Выбор тормозной системы")
menu_bar.addMenu(road_menu)
menu_bar.addMenu(driver_menu)
menu_bar.addMenu(vehicle_menu)
 

road_menu.setTearOffEnabled(True)
road_menu.addAction("Сухой асфальт",dry)
road_menu.addAction("Мокрый асфальт",wet)
road_menu.addAction("Сухой песок",sand)
road_menu.addAction("Снег",snow)
road_menu.addAction("Лед",ice)


driver_menu.setTearOffEnabled(True)
driver_menu.addAction("Бодрость",norm)
driver_menu.addAction("Усталость",tired)
driver_menu.addAction("Опьянение",drunk)

vehicle_menu.setTearOffEnabled(True)
vehicle_menu.addAction("Гидропривод (дисковый)",hydra_1)
vehicle_menu.addAction("Гидропривод (барабанный)",hydra_2)
vehicle_menu.addAction("Пневмопривод ",pnevmo)


#-------Вывод остановочного пути
stop_distance_label = QtWidgets.QLabel()        #создание пустой строки
stop_distance_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)  # функция копирования текста

#-------Вывод времени, нужного для остановки
stop_time_label= QtWidgets.QLabel()
stop_time_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

#-------Вывод пройденного пути при реагировании
reaction_distance_label = QtWidgets.QLabel()
reaction_distance_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

#-------Вывод приблизительного времени реакции----------------------------
reaction_time_label = QtWidgets.QLabel()
reaction_time_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

#-------Вывод тормозного пути
brake_distance_label = QtWidgets.QLabel()
brake_distance_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

#-------Вывод времени торможения
brake_time_label= QtWidgets.QLabel()
brake_time_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

#-------Вывод коэффициента торможения
coefficient_label= QtWidgets.QLabel()
coefficient_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

#Контейнер GridLayout (Расположение элементов)
grid = QtWidgets.QGridLayout()
grid.addWidget(Menu,0,0,1,2)
grid.addWidget(speed_label,1,0)
grid.addWidget(speed_box,1,1)
grid.addWidget(main_btn,2,0,1,2)
grid.addWidget(coefficient_label,3,0,1,2)
grid.addWidget(stop_distance_label,4,0,1,2)
grid.addWidget(stop_time_label,5,0,1,2)
grid.addWidget(reaction_distance_label,6,0,1,2)
grid.addWidget(reaction_time_label,7,0,1,2)
grid.addWidget(brake_distance_label,8,0,1,2)
grid.addWidget(brake_time_label,9,0,1,2)

#____________________________________________________________________________________________________________________________

# Задание начальных значений
dry() # настройка покрытия

norm()  # настойка автомобиля
hydra_1()

# Оставшиеся действия:
print("История расчетов:\n")
result() # Заполнение пустых строк в окне начальными значениями

#_____________запуск расчета_______________
main_btn.clicked.connect(calculate)

main_btn.clicked.connect(result)
#__________________________________________

window.setLayout(grid)     # Добавление контейнера с элементами в окно     

window.show()              # Отображение окна
sys.exit(app.exec_())      # Запуск обработчика событий

#____________________________________________________________________________________________________________________________

# Код был написан 16.06.2019
