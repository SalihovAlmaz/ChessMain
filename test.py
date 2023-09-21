import  string
class Person:
    S_RUS = 'абвгдеёжзийклмнопрстуфхчцщшьъэюя'
    S_RUS_UPPER = S_RUS.upper()
    __shared_attrs = {
        'name': 'thread1',
        'data': {},
        'id': 1
    }
    def __init__(self,fio,old):
        self.verify_fio(fio)
        self.__old = old
        self.__fio = fio
    @classmethod
    def verify_fio(cls,fio):
        if type(fio) != str:
            raise TypeError("ФИО не строка")
        f = fio.split()
        if len(f) != 3:
            raise TypeError("Неверный формат записи")
        letters = string.ascii_letters + cls.S_RUS + cls.S_RUS_UPPER
        for s in f:
            if len(s) < 0:
                raise TypeError("В ФИО должно быть хотя бы один символ")
            elif len(s.strip(letters)) != 0:
                raise TypeError("В ФИО можно использовать только буквенные символы и дефис")

    @property
    def fio(self):
        return self.__fio
    @fio.setter
    def fio(self, fio):
        self.__fio = fio
    @fio.deleter
    def fio(self):
        del self.__fio
    #old = property(get_old,set_old)    #Удобно не нужно вписовать  геттеры и сеттеры
class Integer:
    @classmethod
    def verify_coord(cls,coord):
        if type(coord) != int:
            raise TypeError("Координата не та")
    def __set_name__(self, owner, name):
        self.name='_' + name
    def __get_name__(self,inctance,owner):
        return inctance.__dict__[self.name]
    def __set__(self,inctance,value):
        self.verify_coord(value)
        print(f'__set__: {self.name} = {value}')
        inctance.__dict__[self.name] = value
class Point:
    x = Integer()
    y = Integer()
    z = Integer()
    def __init__(self):
        self.__counter = 0
        # self.x = x
        # self.y = y
        # self.z = z
    def __call__(self, step=1,*args, **kwargs):  #ЦЕ функтор
        print("__call__")
        self.__counter += step
        return  self.__counter

class Clock:
    __DAY = 86400
    def __init__(self,seconds: int):
        if not isinstance(seconds, int):
            raise TypeError("Секунды должны быть целым числом")
        self.seconds = seconds % self.__DAY

    @classmethod
    def __verify(cls, other):
        if not isinstance(other, (Clock, int)):
            raise TypeError("операнд справа должен быть Clock")
        return other if isinstance(other, int) else other.seconds
    def __eq__(self, other):
        return self.seconds == self.__verify(other)
    def __lt__(self, other):
        return self.seconds < self.__verify(other)
    def __bool__(self):
        return True if self.__DAY  > 2 else False
class Student:
    def __init__(self,name,marks):
        self.name = name
        self.marks = list(marks)
    def __getitem__(self, item):
        return self.marks[item]
    def __setitem__(self, key, value):
        self.marks[key] = value
    def __delitem__(self, key):
        del self.marks[key]

class FRange:
     def __init__(self, start=0.0, stop=0.0, step=1.0):
         self.start = start
         self.stop = stop
         self.step = step
         self.value = self.start - self.step
     def __next__(self):
         if self.value + self.step < self.stop:
             self.value += self.step
             return self.value
         else:
             raise StopIteration
     def __iter__(self):
         self.value = self.start - self.step
         return self
class Geom:
    name = 'Geom'
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def set_coords(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
class Line(Geom):
    def __init__(self,x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
    def set_coords(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        print("Рисование линии")


class Rect(Geom):


    def draw(self):
        print("Рисование прямоугольника")
g = Geom()
l = Line()
l.set_coords(1,1,2,1)
print(Geom.__name__)