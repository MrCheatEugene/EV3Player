# EV3Player
EV3Player - это простой плеер .wav файлов, написанный на MicroPython. Требуется официальная прошивка PyBricks-MicroPython для Lego EV3
# Нужно
Блок Lego EV3
MicroSD карта на 2+ГБ 
Компьютер

# Как установить

1. Запишите через Etcher образ PyBricks MicroPython для EV3. Его можно скачать с официального сайта Lego: https://education.lego.com/ru-ru/product-resources/mindstorms-ev3/%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B-%D0%B4%D0%BB%D1%8F-%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%BE%D0%B2/python-%D0%B4%D0%BB%D1%8F-ev3
2. Вставьте карту в выключенный блок. 
3. Запустите блок.
4. После запуска программы "Brickman", подключите его к компьютеру. 
5. Запустите на компьютере соединение по SCP к хосту ev3dev. Логин/пароль по умолчанию: robot/maker. В качестве программы для подключения по SCP на Windows, используйте WinSCP.
6. Загрузите в папку "/home/robot" содержимое ZIP-архива этого репозитория.
7. На блоке выберите пункт "File Browser" и нажмите центральную кнопку.
8. Там, если вы распаковали архив в папку, и вы загрузили папку - будет папка с названием архива. Выберите её и нажмите центральную кнопку.
9. Если вы распаковали архив, и загрузили содержимое архива в папку /home/robot - вам ничего выбирать не надо.
10. Выберите в каталоге файл "main.py" и нажмите центральную кнопку. На экране появится знак "▶", после чего появится меню.

Если всё произошло как в инструкции, установка завершена.

# Как использовать

## Выбор трека

Нажмите кнопку "влево" для того чтобы изменить ваш выбор.

## Выбор страницы
Нажмитие кнопку вниз, чтобы перейти на следующую страницу, и кнопку вверх, чтобы перейти на предыдущую страницу.

## Проигрывание трека
После выбора трека, нажмите центральную кнопку, и трек начнёт воспроизведение.
Если программа вылетает, значит, что трек не является верным(об этом можно узнать ниже)

## Остановка трека(0.02+)
При воспроизведении трека, нажмите центральную кнопку, и вы вернётесь в меню.
Если программа вылетает, пожалуйста, создайте новую issue как описано в главе "Вылетает" ниже

## Пропустить трек(вперёд - назад, 0.02 +)
При воспроизведении трека, нажмите кнопку вправо, и вы перейдёте на следующий трек.
При воспроизведении трека, нажмите кнопку влево, и вы перейдёте на следующий трек.
Если программа вылетает, значит, что следующий/предыдущий трек не является верным(об этом можно узнать ниже)

## Загрузка треков
Просто переместите треки в формате .wav в папку, где находится main.py

## Делаем "Верный" трек из "неверного"
Верный трек - любой трек в формате .wav имеющий моно/стерео(рекомендуется моно, так как стерео воспроизвести невозможно) аудио, а также имеющий частоту дискретизации не больше 44.1 кГц.

Для преобразования трека в формат .wav, уменьшения частоты дискретизации, а также преобразования в моно можно использовать Audacity.
Как это сделать вы можете узнать в интернете.

# Вылетает?
Обновите список файлов на компьютере в папке с main.py, и оттуда скачайте файл main.py.err.log, и создайте новую issue, приложив этот файл с описанием ваших действий.
Я/кто то ещё постараюсь/тся решить проблему.

# Поддержите меня!
Реализация подобных проектов даётся мне нелегко, и если вы хотите поддержать меня и мои творения - можете задонатить здесь:
https://donationalerts.com/r/mrcheatt
