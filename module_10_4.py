from threading import Thread # из встроеного модуля threading импортируем Thread
from random import randint # из встроеного модуля random импортируем randint
from time import sleep # из встроеного модуля time импортируем sleep
import queue # импорт модуля queue

class Table: # создаем класс Table
    def __init__(self, number): # метод инициализации
        self.number = number  # атрибутами number - номер стола
        self.guest =None # guest - гость (по умолчанию None)

class Guest(Thread): # класс Guest,поток от Thread
    def __init__(self, name):# метод инициализации
        super().__init__() # вызов конструктора родительского класса
        self.name = name # обладает атрибутом name
    def run(self): # используем метод run
        expectation = randint(3, 10)
        sleep(expectation) # где происходит ожидание случайным образом от 3 до 10 секунд

class Cafe(): # создаем класс Cafe
    def __init__(self, tables, queue): # в метод инициализации применим к столам и очереди
        super().__init__() # вызов конструктора родительского класса
        self.tables = tables  # обладает атрибутом стол
        self.queue = queue.Queue()  # обладает атрибутом очереди
    def guest_arrival(self, *guests):  #  метод guest_arrival (прибытие гостей)
        for guest in guests:
            for table in self.tables:  # перебираем гостей и рассаживаем по столикам
                if table.guest is None:
                    guest.start()
                    print (f'{guest.name} сел(-а)за стол номер {table.number}')
                    table.guest = guest
                    break # прерываем цикл guest_arrival
            else: # иначе выводим что находятся в очереди
                print(f'{guest.name}в очереди')
                self.queue.put(guest)

    def discuss_guests(self): # Метод discuss_guests
        while not self.queue.empty() or any(table.guest for table in self.tables):
            for table in self.tables:
                if not table.guest is None and table.guest.is_alive: # метод is_alive проверяет на активность потока
                    table.guest.join()  # проходимся вспомогательным потоком что бы вывести надпись
                    print(f'{table.guest.name} покушал(-а)и ушёл(ушла)')
                    table.guest = None  # стол один из столов освободился (None)
                    print(f'Стол номер {table.number} свободен') # выведем надпись для желающих занять столик))
                elif not self.queue.empty() and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'{table.guest.name} вышел(-ла)из очереди и сел(-а) за стол номер {table.number}')
                    table. guest. start() # запустить поток
 # из условия домашнего задания
tables = [Table(number) for number in range(1, 6)]
guests_names = ['Maria','Oleg','Vakhtang','Sergey','Darya','Arman',
       'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra' ]
guests = [Guest(name) for name in guests_names]
cafe = Cafe(tables, queue)
cafe.guest_arrival(*guests)
cafe.discuss_guests()