#!/usr/bin/env pybricks-micropython
import _thread
from experimental_c import pthread_raise
from usignal import pthread_kill, SIGUSR2

from pybricks.hubs import (EV3Brick)
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait as blocking_wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

from pybricks.media.ev3dev import Font

## GENERATORS 

def wait_first(*tasks):
    yield from zip(*tasks)
    for t in tasks:
        t.close()

# Create your objects here.
ev3 = EV3Brick()
speaker_lock = _thread.allocate_lock()
screen =ev3.screen
speaker = ev3.speaker
# Write your program here.
#ev3.speaker.beep()
titles=[]
files = []
import os
for file in sorted(os.listdir("./")):
    if file.endswith(".wav"):
        files.append(""+str(file))
        titles.append(str(file))
#print(list(files))# Вывод файлов(для отладки)
page =1# Страница
boxList= []# Список "коробок" в меню(содержит его высоту)
isLocked = False# Играет ли музыка? ( Locked- одно из состояний динамика,занят ли динамик или свободен, поэтому переменная и называется - IsLocked)
def renderPlaying(file):# Рендерим играющую песню 
    maxH =125
    maxW = 170
    #print("Currently playing: "+file)#Отладочная информация
    screen.clear()#Очистка экрана
    font = Font(size=15)# Ставим шрифт
    ev3.screen.set_font(font) #Ставим-ставим шрифт
    screen.draw_box(0, 0, maxW, maxH, fill=False, color=Color.BLACK)# Рисуем контейнер на весь экран
    screen.draw_image(int((maxW-10)/4),int(3), "./vinyl.png")# Рисуем картинку посередине экрана
    screen.draw_text(10,105, str(file), text_color=Color.BLACK, background_color=None) # Пишем название композиции(файла)
def play(file,titles,boxList,page):# Проиграть что-то
    # А вот дальше я не очень понимаю как оно работает,поэтому комментарии будут максимально поверхностными, сорян
    speaker_lock.acquire(False) #???
    def play_in_background_thread():# Проиграть композицию в отдельном потоке
        try:# Попробовать..
            renderPlaying(file) # Рендерим инфу о том, что композиция воспроизводится
            isLocked = True
            ev3.speaker.play_file("./"+str(file))# Воспроизвести файл (файл)
        finally:#Когда композиция закончилась
            speaker_lock.release()# Освобождаем динамик
            isLocked = False
            renderMenu(titles,page,boxList) # Рендерим меню
    thread = _thread.start_new_thread(play_in_background_thread, ()) # Создаём поток с функцией "проиграть в отдельном потоке"
    try:# Я хз что тут происходит, не шарю за генераторы :/
        while speaker_lock.locked():
            yield
    except GeneratorExit:
        pthread_raise(thread, SystemExit())
        pthread_kill(thread, SIGUSR2)
maxH =120#Максимальная высота рендера
boxSize=20# Размер контейнера в меню
def renderMenu(titles,page,boxList):
    screen.clear()
    maxH =120# Максимальная высота рендера
    maxW = 160# Максимальная ширина рендера
    currY=0# Текущая позиция рендера по Y
    boxSize=20# Размер контейнера в меню
    font = Font(size=15)# Создаём шрифт
    offset=int(page*int(maxH/boxSize)-1) # Учитываем страницу
    if(offset > len(titles)):# Если произошла ошибка в расчётах
        offset = int(len(titles)/2) # Пытаемся её исправить
    if(offset<0):# Если число отрицательное
        offset = 0# Возвращаемся к 0
    #print("Offset "+str(offset)) # Отладочная информация
    #print("Page "+str(page))# Отладочная информация
    ev3.screen.set_font(font)# Ставим шрифт
    while (currY < maxH):# Пока не закончили рендерить:
        I=int(currY/boxSize)+offset # I- Внутренний параметр, индекс названия файла 
        if(I+1 > len(titles)): # Если этот индекс больше чем все названия файлов В ЦЕЛОМ
            title= "" # То название равно пустой строке
        else:
            title=titles[I]# Иначе - названию
        pass
        boxList.append(currY)# Добавляем текущую позицию в список с коробками
        screen.draw_text(3,currY, title, text_color=Color.BLACK, background_color=None)# Рендерим текст
        screen.draw_box(0,currY, maxW,(currY+boxSize), r=0, fill=False, color=Color.BLACK)# Рендерим коробку
        currY=currY+boxSize# Текущий Y - Текущий Y+ название коробки
    pass
selected =0# Выбранный элемент
prevselected =0# Старый выбранный элемент(для очистки)
selectedINDEX=0# Index выбранного элемента
renderMenu(titles,0 ,boxList) # Рендерим меню
while (True):# Цикл
    #if(page == 0):
    #    page = 1
    buttonsList=ev3.buttons.pressed()# Список нажатых кнопок
    if(Button.DOWN in buttonsList and page+1 <= int((len(titles)/int(120/20))+1) and page+1 >1): # Если нажата кнопка "вниз", и мы можем переключится на следующую страницу - переключаемся
        page=page+1
        boxList= []
        renderMenu(titles,page-1,boxList) 
    elif(Button.UP in buttonsList and page >0): # Если мы нажали вверх, и можем идти вниз - то идём вниз.
        page=page-1
        boxList= []
        renderMenu(titles,page,boxList)
    elif(Button.CENTER in buttonsList):# Играем музыку
        selectedINDEX=selectedINDEX-1 # Я чёрт возьми не помню зачем это нужно
        #page =0
        if(page >1 and selectedINDEX >=1): # Если и страница и выбранный index больше 1, то
            filesSelectIndex =int((((page*4))+selectedINDEX)-3)# Индекс файла вычисляется так
        elif(page >1 and selectedINDEX <1):# Если страница больше 1, и выбранный index меньше 1 то 
            filesSelectIndex =int((page*6)-1)# Вычисляем так
        elif(page ==1):# Если страница = 1(зачем именно так я не знаю, но оно работает)
            filesSelectIndex=int(page*6-selectedINDEX-1)# Вычисляем вот так
        else: # Если это всё не наш случай, то
            filesSelectIndex=int(selectedINDEX) # Сдаёмся и ставим индекс файла на выбранный вами элемент(если страница - 0, всё будет нормально, если нет - всё не будет так хорошо)
        # DEBUG INFO / ОТЛАДОЧНАЯ ИНФОРМАЦИЯ
        #print(page >0)
        #print(page)
        #print(filesSelectIndex)
        #print(files[filesSelectIndex])
        boxList= []# Список "коробок" в меню(содержит его высоту)
        wait_first([play(files[selectedINDEX],titles,boxList,page)])# Создаём генератор?
        tasks = [play(files[filesSelectIndex],titles,boxList,page)] # Создаём задачу
        for t in tasks: # Исполняем задачи
            next(t)# Исполняем каждую задачу
        blocking_wait(10)# Даём системе подумать
        time.sleep(0.250) # Задержка для кнопок
   # elif(Button.CENTER in buttonsList and isLocked == True): # Это было нужно для одной вещи
   #     print("Playing!")
   #     time.sleep(0.250)
    elif(Button.LEFT in buttonsList): # Кнопка выбора вниз
        time.sleep(0.250) # Задержка для кнопок
        if(selectedINDEX > len(boxList)-1): # Если у нас что-то пошло не так(мы на дне)
            selectedINDEX = 0 # Обнуляем всё
            selected = 0
        pass
        #print(list(boxList)) # Отладка
        screen.draw_text(160, prevselected,"<", Color.WHITE) # Удаляем старый символ-указатель
        selected=boxList[selectedINDEX] # Выбранный элемент по Y
        screen.draw_text(160, selected,"<", Color.BLACK) # Относительно описанного ранее Y рисуем новый символ
        prevselected = selected # Старый элемент = текущий элемент
        selectedINDEX=selectedINDEX+1 # Добавляем 1 к indexу выделенного элемента
        time.sleep(0.250)#Зачем тут вторая задержка?